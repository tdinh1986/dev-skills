---
name: speckit
description: "Run Spec-Driven Development workflows for feature ideas, specs, architecture plans, task breakdowns, and implementation. Trigger on `$speckit`, automatic/full spec-driven workflow requests, feature specification requests, planning/analysis/task generation requests, implementation requests, or any `/speckit.*` command."
---

# Skill: Speckit — Spec-Driven Development

## Description

Senior Software Architect applying Spec-Driven Development (SDD). Core principle: **intent-first** — define *what* and *why* before *how*. Move through structured phases that build on each other, producing artifacts at each step.

## Instructions

<phase>Phase Execution</phase>

When a phase is triggered:

1. Read the corresponding command file from the Entry-Point table below using the current agent's available file-read capability.
   If the file read fails, stop and report: "Could not read command file [path]. Check that the skill is installed correctly."
2. Read the command file and all required context files (e.g., `constitution.md`, `spec.md`) **in parallel** in a single turn.
3. Execute the command file's instructions fully before responding.
4. Resolve `<skill_dir>`: determine the absolute path of the directory containing this `SKILL.md`. Substitute `<skill_dir>` with that resolved path in all script invocations.
5. After writing each phase artifact, announce: "Phase N complete — [artifact] written to [path]."
6. Do not rely on memory of previous command file contents; always read the command file fresh.

When an automatic workflow is triggered, read `commands/auto.md` first. Let it orchestrate the phases by reading each phase command file fresh and applying the stop gates it defines.

<phase>Parallel Tool Mandate</phase>

Execute all independent tool calls in a single turn. Examples:
- Reading multiple context files (constitution.md + spec.md + plan.md) → a single parallel read step.
- Running a prerequisite script and reading the command file → single parallel call.
- Never chain sequential Reads for files that have no dependency between them.

<phase>Pre-Flight Checks</phase>

Before executing phases 3–7 (clarify, plan, analyze, tasks, implement):
1. Verify the required upstream artifact(s) exist by checking the FEATURE_DIR.
2. If a required artifact is missing, stop and report: "Missing prerequisite: [artifact]. Run `/speckit.[phase]` first."

| Phase | Required upstream artifacts |
|-------|---------------------------|
| 3 (clarify) | `spec.md` |
| 4 (plan) | `constitution.md`, `spec.md` |
| 5 (analyze) | `constitution.md`, `spec.md`, `plan.md` |
| 6 (tasks) | `spec.md`, `plan.md` |
| 7 (implement) | `spec.md`, `plan.md`, `tasks.md` |

## Entry-Point → Command File

| Trigger | Command file |
|---------|--------------|
| `/speckit.constitution` | `commands/constitution.md` |
| `/speckit.specify` | `commands/specify.md` |
| `/speckit.clarify` | `commands/clarify.md` |
| `/speckit.plan` | `commands/plan.md` |
| `/speckit.analyze` | `commands/analyze.md` |
| `/speckit.tasks` | `commands/tasks.md` |
| `/speckit.implement` | `commands/implement.md` |
| `$speckit`, "start speckit", "start spec-kit", "automatic flow", "full workflow" | `commands/auto.md` |
| No command, spec/feature request | `commands/specify.md` |
| No command, architecture/stack request | `commands/plan.md` |
| No command, task breakdown request | `commands/tasks.md` |

## Automatic Workflow Defaults

- Run the automatic workflow through `tasks.md`, then stop before code changes.
- Never run `/speckit.implement` unless the user explicitly asks to implement.
- After each completed phase artifact, stop for user review and approval before continuing to the next phase.
- Resume only after the user approves the current artifact. If the user requests changes, revise the current phase artifact and repeat that phase's review gate.
- Pause for user input when a phase hits its ambiguity, clarification, approval, or hard-failure gate.
- If plan analysis returns `FAIL`, ask the user to review `analysis.md`, then attempt one plan-repair loop after approval, rerun analysis, and gate the revised `analysis.md` before continuing. Stop if any `FAIL` remains.
- During automatic workflow, phase hand-off prompts return control to `commands/auto.md`; do not ask the user to manually invoke the next phase unless a gate stops progress.

## Script Invocation

Scripts live at `<skill_dir>/scripts/bash/` (macOS/Linux) or `<skill_dir>/scripts/powershell/` (Windows).
`<skill_dir>` is the directory containing this `SKILL.md`.
Command files reference scripts as `bash <skill_dir>/scripts/bash/<script>.sh --json`.

**Script failure handling:**
- If a script exits non-zero, report the exit code and stderr to the user. Do not proceed to artifact writing.
- If the script file is not found, report: "Script not found at [path]. Verify the skill installation."

## Guardrails

### Scope Limitation
- Write artifacts only to the project's `.specify/` directory and the allowed project-root context files such as `constitution.md`, `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`.
- Never modify: `.git/`, `.env`, `node_modules/`, `~/.ssh/`, or any file outside the project directory.
- Before writing, confirm the target path is within the allowed scope.

### Input Sanitization
- Sanitize user-provided feature names before passing to shell scripts: strip shell metacharacters (`` ` ``, `$`, `|`, `;`, `&`, `>`, `<`).
- Use double-quoted variables in all script arguments.

### Write Failure Handling
- If an artifact write fails, report the error and retry once.
- If the retry fails, stop and report: "Write failed for [artifact] at [path]. Check directory permissions."

## Observability

### CoT Logging
Before executing each phase, print a brief plan:
```
Phase N: [phase name]
Action: [what will be done]
Inputs: [files/scripts to be read/run]
Output: [expected artifact and path]
```

### Source Attribution
When writing artifacts that reference project files, cite the source file and relevant sections.

### Methodology (Final Output)
At the end of multi-phase runs or the implement phase, include a summary:
- Phases executed and artifacts produced.
- Key decisions made and their rationale.
- Source files consulted.

## References

| Artifact | Phase | Description |
|----------|-------|-------------|
| `constitution.md` | Phase 1 | Project governing principles |
| `spec.md` | Phase 2 | Functional requirements + BDD acceptance criteria |
| `plan.md` | Phase 4 | Technical architecture, stack, component breakdown |
| `analysis.md` | Phase 5 | Constitution compliance + gap report |
| `tasks.md` | Phase 6 | Ordered, dependency-annotated task list |
| `scripts/bdd_converter.cjs` | — | Converts JSON to Gherkin BDD format (used in Phase 2) |
| `scripts/bash/` | — | Bash scripts for feature scaffolding, prereq checking, and agent context sync |
| `scripts/powershell/` | — | PowerShell equivalents of bash scripts (Windows) |
| `templates/` | — | Output skeletons loaded by each phase command |

## Examples

### Trigger → Action → Output

**User:** `/speckit.specify` — "Add a user login feature"
**Agent actions:**
1. Prints CoT log: Phase 2 (specify), will run create-new-feature script, output spec.md.
2. Reads `commands/specify.md`.
3. Runs `bash <skill_dir>/scripts/bash/create-new-feature.sh --json` → gets `BRANCH=001-user-login`, `FEATURE_DIR=.specify/specs/001-user-login/`.
   - If script fails: reports error and stops.
4. Writes `spec.md` to `FEATURE_DIR` with BDD scenarios.
5. Announces: "Phase 2 complete — spec.md written to .specify/specs/001-user-login/spec.md"
6. States: "Spec ready. Run `/speckit.clarify` to surface edge cases, or `/speckit.plan` to proceed to architecture."

**User:** `/speckit.plan`
**Agent actions:**
1. Prints CoT log: Phase 4 (plan), inputs: constitution.md + spec.md, output: plan.md.
2. Reads `commands/plan.md`.
3. Pre-flight: verifies `constitution.md` and `spec.md` exist in FEATURE_DIR.
4. Runs `bash <skill_dir>/scripts/bash/check-prerequisites.sh --json` → confirms FEATURE_DIR and AVAILABLE_DOCS.
5. Reads `constitution.md` and `spec.md` in parallel.
6. Writes `plan.md` to `FEATURE_DIR`.
7. Runs `bash <skill_dir>/scripts/bash/update-agent-context.sh existing` (non-blocking; logs result).
8. Announces: "Phase 4 complete — plan.md written to .specify/specs/001-user-login/plan.md"
9. States: "Plan ready. Run `/speckit.tasks` to break this into an ordered task list."
