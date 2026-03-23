#!/usr/bin/env python3
"""
parse_history.py - Extract normalized conversation records from local Claude, Codex,
and Gemini history files.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def resolve_period(period: str) -> tuple[datetime, datetime | None]:
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    normalized = period.lower().strip()
    if normalized == "today":
        return today, None
    if normalized == "yesterday":
        return today - timedelta(days=1), today
    if normalized == "this week":
        return today - timedelta(days=today.weekday()), None
    if normalized == "this month":
        return today.replace(day=1), None
    if normalized == "last 7 days":
        return today - timedelta(days=7), None
    if normalized == "last 30 days":
        return today - timedelta(days=30), None
    raise ValueError(
        f"Unknown period: {period!r}. Valid: today, yesterday, this week, this month, last 7 days, last 30 days"
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Parse local Claude, Codex, and Gemini chat history.")
    parser.add_argument(
        "--agent",
        choices=("auto", "claude", "codex", "gemini", "all"),
        default="auto",
        help="History source to parse (default: auto)",
    )
    parser.add_argument(
        "--claude-projects-dir",
        default=str(Path.home() / ".claude" / "projects"),
        help="Path to Claude projects directory",
    )
    parser.add_argument(
        "--codex-sessions-dir",
        default=str(Path.home() / ".codex" / "sessions"),
        help="Path to Codex sessions directory",
    )
    parser.add_argument(
        "--gemini-tmp-dir",
        default=str(Path.home() / ".gemini" / "tmp"),
        help="Path to Gemini tmp directory",
    )
    parser.add_argument(
        "--gemini-projects-file",
        default=str(Path.home() / ".gemini" / "projects.json"),
        help="Path to Gemini projects.json file",
    )
    parser.add_argument(
        "--period",
        default="today",
        help="Time range keyword: today, yesterday, this week, this month, last 7 days, last 30 days (default: today)",
    )
    parser.add_argument(
        "--since",
        default=None,
        help="Explicit start date override (YYYY-MM-DD); takes precedence over --period",
    )
    parser.add_argument(
        "--until",
        default=None,
        help="Explicit end date (YYYY-MM-DD); takes precedence over period-derived upper bound",
    )
    parser.add_argument(
        "--project-filter",
        default=None,
        help="Substring to filter project names or cwd values",
    )
    return parser.parse_args()


def extract_text(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                text = block.strip()
                if text:
                    parts.append(text)
                continue
            if not isinstance(block, dict):
                continue
            block_type = block.get("type", "")
            if block_type in {"tool_use", "tool_result"}:
                continue
            text = str(block.get("text", "")).strip()
            if text:
                parts.append(text)
        return "\n".join(parts).strip()
    return ""


def parse_timestamp(ts_str: str):
    try:
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def matches_project_filter(project_filter: str | None, *values: str | None) -> bool:
    if not project_filter:
        return True
    needle = project_filter.lower()
    return any(value and needle in value.lower() for value in values)


def normalize_record(agent: str, session_id: str, project: str, cwd: str, timestamp: str, role: str, text: str) -> dict:
    return {
        "agent": agent,
        "session_id": session_id,
        "project": project,
        "cwd": cwd,
        "timestamp": timestamp,
        "role": role,
        "text": text,
    }


def collect_claude_files(projects_dir: Path, project_filter: str | None) -> list[tuple[Path, str]]:
    results = []
    if not projects_dir.exists():
        print(f"Warning: Claude projects dir not found: {projects_dir}", file=sys.stderr)
        return results

    for project_dir in sorted(projects_dir.iterdir()):
        if not project_dir.is_dir():
            continue
        project_name = project_dir.name
        if not matches_project_filter(project_filter, project_name):
            continue
        for jsonl_file in sorted(project_dir.glob("*.jsonl")):
            results.append((jsonl_file, project_name))
    return results


def process_claude_file(
    jsonl_path: Path,
    project_name: str,
    since_dt,
    until_dt=None,
) -> list[tuple[datetime | None, dict]]:
    records = []
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg_type = obj.get("type", "")
                if msg_type not in {"user", "assistant"}:
                    continue

                message = obj.get("message", {})
                if not isinstance(message, dict):
                    continue

                text = extract_text(message.get("content", ""))
                if not text:
                    continue

                timestamp_str = obj.get("timestamp", "")
                ts = parse_timestamp(timestamp_str)
                if since_dt and ts and ts < since_dt:
                    continue
                if until_dt and ts and ts >= until_dt:
                    continue

                session_id = obj.get("sessionId", jsonl_path.stem)
                cwd = obj.get("cwd", "")
                role = message.get("role", msg_type)
                records.append((ts, normalize_record("claude", session_id, project_name, cwd, timestamp_str, role, text)))
    except OSError as exc:
        print(f"Warning: could not read {jsonl_path}: {exc}", file=sys.stderr)

    return records


def iter_codex_files(sessions_dir: Path) -> list[Path]:
    if not sessions_dir.exists():
        print(f"Warning: Codex sessions dir not found: {sessions_dir}", file=sys.stderr)
        return []
    return sorted(sessions_dir.rglob("*.jsonl"))


def process_codex_file(
    jsonl_path: Path,
    since_dt,
    until_dt=None,
    project_filter: str | None = None,
) -> list[tuple[datetime | None, dict]]:
    records = []
    session_id = jsonl_path.stem
    cwd = ""
    project = ""

    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if obj.get("type") == "session_meta":
                    payload = obj.get("payload", {})
                    session_id = payload.get("id", session_id)
                    cwd = payload.get("cwd", cwd)
                    if cwd:
                        project = Path(cwd).name
                    continue

                if obj.get("type") != "event_msg":
                    continue

                payload = obj.get("payload", {})
                payload_type = payload.get("type")
                if payload_type not in {"user_message", "agent_message"}:
                    continue

                text = str(payload.get("message", "")).strip()
                if not text:
                    continue

                timestamp_str = obj.get("timestamp", "")
                ts = parse_timestamp(timestamp_str)
                if since_dt and ts and ts < since_dt:
                    continue
                if until_dt and ts and ts >= until_dt:
                    continue
                if not matches_project_filter(project_filter, project, cwd):
                    continue

                role = "user" if payload_type == "user_message" else "assistant"
                records.append((ts, normalize_record("codex", session_id, project or jsonl_path.parent.name, cwd, timestamp_str, role, text)))
    except OSError as exc:
        print(f"Warning: could not read {jsonl_path}: {exc}", file=sys.stderr)

    return records


def load_gemini_project_map(projects_file: Path) -> dict[str, str]:
    if not projects_file.exists():
        return {}
    try:
        payload = json.loads(projects_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    projects = payload.get("projects", {})
    if not isinstance(projects, dict):
        return {}
    return {alias: path for path, alias in projects.items() if isinstance(path, str) and isinstance(alias, str)}


def iter_gemini_files(tmp_dir: Path) -> list[Path]:
    if not tmp_dir.exists():
        print(f"Warning: Gemini tmp dir not found: {tmp_dir}", file=sys.stderr)
        return []
    return sorted(tmp_dir.glob("*/chats/*.json"))


def process_gemini_file(
    json_path: Path,
    alias_to_path: dict[str, str],
    since_dt,
    until_dt=None,
    project_filter: str | None = None,
) -> list[tuple[datetime | None, dict]]:
    records = []
    project = json_path.parent.parent.name
    cwd = alias_to_path.get(project, "")

    try:
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Warning: could not read {json_path}: {exc}", file=sys.stderr)
        return records

    session_id = payload.get("sessionId", json_path.stem)
    for message in payload.get("messages", []):
        if not isinstance(message, dict):
            continue
        msg_type = message.get("type")
        if msg_type not in {"user", "gemini"}:
            continue

        text = extract_text(message.get("content", ""))
        if not text:
            continue

        timestamp_str = message.get("timestamp", "")
        ts = parse_timestamp(timestamp_str)
        if since_dt and ts and ts < since_dt:
            continue
        if until_dt and ts and ts >= until_dt:
            continue
        if not matches_project_filter(project_filter, project, cwd):
            continue

        role = "user" if msg_type == "user" else "assistant"
        records.append((ts, normalize_record("gemini", session_id, project, cwd, timestamp_str, role, text)))
    return records


def resolve_agents(agent: str, claude_dir: Path, codex_dir: Path, gemini_dir: Path) -> tuple[list[str], list[str]]:
    availability = {
        "claude": claude_dir.exists(),
        "codex": codex_dir.exists(),
        "gemini": gemini_dir.exists(),
    }
    skipped = [name for name, exists in availability.items() if not exists]
    if agent == "all":
        return [name for name, exists in availability.items() if exists], skipped
    if agent == "auto":
        return [name for name, exists in availability.items() if exists], skipped
    if not availability[agent]:
        print(f"Error: requested agent source is unavailable: {agent}", file=sys.stderr)
        sys.exit(1)
    return [agent], skipped


def main():
    args = parse_args()
    claude_projects_dir = Path(args.claude_projects_dir).expanduser()
    codex_sessions_dir = Path(args.codex_sessions_dir).expanduser()
    gemini_tmp_dir = Path(args.gemini_tmp_dir).expanduser()
    gemini_projects_file = Path(args.gemini_projects_file).expanduser()

    if args.since:
        try:
            since_dt = datetime.fromisoformat(args.since).replace(tzinfo=timezone.utc)
            until_dt = None
        except ValueError:
            print(f"Error: --since must be in YYYY-MM-DD format, got: {args.since}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            since_dt, until_dt = resolve_period(args.period)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    if args.until:
        try:
            until_dt = datetime.fromisoformat(args.until).replace(tzinfo=timezone.utc)
        except ValueError:
            print(f"Error: --until must be in YYYY-MM-DD format, got: {args.until}", file=sys.stderr)
            sys.exit(1)

    since_str = since_dt.strftime("%Y-%m-%d") if since_dt else "beginning"
    until_str = until_dt.strftime("%Y-%m-%d") if until_dt else "now"
    print(f"Date range: {since_str} to {until_str}", file=sys.stderr)

    agents, skipped = resolve_agents(args.agent, claude_projects_dir, codex_sessions_dir, gemini_tmp_dir)
    if skipped and args.agent in {"auto", "all"}:
        print(f"Skipped unavailable sources: {', '.join(skipped)}", file=sys.stderr)

    all_records: list[tuple[datetime | None, dict]] = []
    counts: dict[str, int] = {}

    if "claude" in agents:
        claude_files = collect_claude_files(claude_projects_dir, args.project_filter)
        counts["claude_files"] = len(claude_files)
        for jsonl_path, project_name in claude_files:
            all_records.extend(process_claude_file(jsonl_path, project_name, since_dt, until_dt))

    if "codex" in agents:
        codex_files = iter_codex_files(codex_sessions_dir)
        counts["codex_files"] = len(codex_files)
        for jsonl_path in codex_files:
            all_records.extend(process_codex_file(jsonl_path, since_dt, until_dt, args.project_filter))

    if "gemini" in agents:
        alias_to_path = load_gemini_project_map(gemini_projects_file)
        gemini_files = iter_gemini_files(gemini_tmp_dir)
        counts["gemini_files"] = len(gemini_files)
        for json_path in gemini_files:
            all_records.extend(process_gemini_file(json_path, alias_to_path, since_dt, until_dt, args.project_filter))

    if not all_records:
        print("Warning: no history records found matching criteria.", file=sys.stderr)
        print("[]")
        return

    all_records.sort(key=lambda item: (item[0] is None, item[0] or datetime.max.replace(tzinfo=timezone.utc)))
    serialized = [record for _, record in all_records]

    summary = ", ".join(f"{key}={value}" for key, value in counts.items())
    print(f"Scanned agents: {', '.join(agents)}", file=sys.stderr)
    if summary:
        print(f"Source counts: {summary}", file=sys.stderr)
    print(f"Extracted {len(serialized)} message(s).", file=sys.stderr)
    print(json.dumps(serialized, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
