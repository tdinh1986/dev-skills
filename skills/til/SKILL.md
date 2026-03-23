---
name: til
description: Analyze local Claude, Codex, and Gemini chat history to surface learnings and identify repeated tasks as skill candidates.
---

## Description

Analyze local agent chat history to surface what you learned and identify repeated tasks that should become skills. Defaults to today's sessions. Supports Claude, Codex, and Gemini through a shared workflow with source-specific adapters.

## Instructions

<phase name="pre-flight">

**1. Determine period and agent scope.**
Extract the period keyword from the user's request. Valid keywords:

| Keyword | Meaning |
|---|---|
| `today` (default) | From midnight of current day |
| `yesterday` | Previous calendar day only |
| `this week` | Monday of current week to now |
| `this month` | 1st of current month to now |
| `last 7 days` | Rolling 7-day window |
| `last 30 days` | Rolling 30-day window |

If no keyword is provided, use `today`. If the user provides an unrecognized keyword, stop and list the valid options above.

Resolve the agent scope:
- `auto` if the user does not name an agent
- `claude`, `codex`, `gemini`, or `all` if the user is explicit

**2. Verify environment.**
Run these checks. Stop on first failure with the stated message:

- `python3 --version` → if not found: "Python 3 is required but not found. Install it and retry."
- Resolve `<skill_dir>` as the directory containing this `SKILL.md`.
- Default history sources:
  - Claude: `~/.claude/projects`
  - Codex: `~/.codex/sessions`
  - Gemini: `~/.gemini/tmp`
- If an explicitly requested agent has no readable default source, stop and say which source is missing.
- If the scope is `auto` or `all`, continue with readable sources and report any skipped source.

</phase>

<phase name="parse">

**3. Print a short scan log** before running the script:

```
Agents:         <resolved agent scope>
Period:         <keyword>
Date range:     <resolved from/to>
Project filter: <value or "all projects">
Script:         <skill_dir>/scripts/parse_history.py
```

**4. Run the parse script:**

```bash
python3 <skill_dir>/scripts/parse_history.py \
  --agent <resolved agent scope> \
  --period <keyword>
```

Optional flags:
- `--project-filter <substring>` — restrict to specific project directories
- `--since <YYYY-MM-DD>` — explicit date override
- `--until <YYYY-MM-DD>` — explicit end date
- `--claude-projects-dir <path>`
- `--codex-sessions-dir <path>`
- `--gemini-tmp-dir <path>`

> **Security note:** Chat history may contain sensitive material. Use `--project-filter` and tight date ranges to scope access to the minimum needed. Do not share raw history outside the local workflow.

The script outputs a JSON array of normalized records to stdout and a summary to stderr. Capture stdout for analysis. Each record includes `agent`, `session_id`, `project`, `cwd`, `timestamp`, `role`, and `text`.

**5. Guard: empty results.**
If the JSON array is empty (`[]`), stop and report:
> "No sessions found for the requested scope and period. Try `--period last 7 days`, broaden the agent scope, or check the configured history roots."

</phase>

<phase name="analyze">

**6. Analyze sessions.**
Group messages by agent, session, and project. Analyze across all sessions for:

**Learning points** — Look for:
- First appearances of tools, libraries, commands, or techniques
- Architectural decisions and patterns adopted
- Workflow discoveries (slash commands, plan mode, hooks, agent-specific habits, etc.)
- Debugging strategies and non-obvious fixes

**Repeated task patterns** — Look for semantic categories appearing 3+ times:
- Group by intent, not exact wording ("Fix failing test" = "debug test error" = "tests are broken")
- Count session occurrences (not message occurrences) to avoid inflation
- Focus on tasks that follow a predictable workflow — best skill candidates

</phase>

<phase name="report">

**7. Verify report structure** before rendering: confirm the draft has a TIL section and a Repeated Tasks section. If either is missing, synthesize from the analysis before continuing.

**8. Render the TIL report.** Set title by period:

| Period | Title |
|---|---|
| `today` | `# TIL — Today I Learned` |
| `yesterday` | `# TIL — Yesterday` |
| `this week` | `# TIL — This Week` |
| `this month` | `# TIL — This Month` |
| `last 7 days` | `# TIL — Last 7 Days` |
| `last 30 days` | `# TIL — Last 30 Days` |

```markdown
# TIL — Today I Learned
_Generated: <date> | Period: today | Sessions: N_

## TIL
### [Theme: e.g., Python tooling]
- Learned to use `uv` for dependency management instead of pip
- Discovered that pytest fixtures can be scoped per session

### [Theme: e.g., agent workflow]
- /init generates agent guidance from codebase analysis
- Plan mode forces read-only exploration before edits

## Repeated Tasks → Skill Candidates
### 1. <Task name> (appeared N times) [⚠️ _Existing skill `<skill-name>` may cover this_]
**Pattern:** <description of what the user repeatedly asks the agent to do>
**Suggested skill name:** `<kebab-case-name>`
**Description:** <one sentence — what triggers this skill>
**Key instructions:**
1. <what the skill should tell Claude to do first>
2. <second step>
3. <third step>

## How This Report Was Generated
- Date: <today's date>
- Period: <keyword> (<resolved date range>)
- Agents scanned: <list>
- Projects scanned: N
- Messages analyzed: N
- Project filter: <value or "none">
```

Keep TIL items concise: 3–8 bullets per theme, max 4 themes. Prioritize novel/actionable learnings over routine activity.

For skill suggestions, aim for 2–5 high-quality candidates. Each must be concrete enough to implement — vague suggestions are not useful.

</phase>

<phase name="cross-reference">

**9. Scan existing skills** to avoid redundant suggestions:

Resolve `<skills_root>` as the parent directory of `<skill_dir>` and scan that directory for existing skills.

For each repeated task pattern:
- If an existing skill significantly overlaps, mark it: `⚠️ _Existing skill \`<name>\` covers this_` and suggest what to add/change in that SKILL.md instead of creating a new one.
- If no overlap, propose a new skill as normal.

</phase>

<phase name="act">

**10. Offer to act.** After presenting the report, ask:

> "Which of these would you like to act on?"
> - To create a new skill: use the current agent's available skill-creation workflow or create the skill files directly.
> - To update an existing skill: edit the relevant `SKILL.md` and any named support files.
> - To skip a suggestion: say which ones to ignore.

Wait for the user's response, then execute their chosen actions.

</phase>

## Examples

| User says | Period used |
|---|---|
| "what did I learn today" | `today` |
| "TIL" | `today` |
| "daily review" | `today` |
| "TIL this week" | `this week` |
| "what have I been doing in Codex last 30 days" | `last 30 days` + `codex` |
| "summarize Gemini sessions for the management project" | `today` + `gemini` + `--project-filter management` |
