# Automatic Workflow (`$speckit`, "start speckit", "full workflow")

**Goal:** Run the Spec-Driven Development workflow automatically through task generation while requiring user review after every completed phase artifact and avoiding code changes.

## Default Stop Point

Run through Phase 6 (`tasks.md`) and stop. Do **not** run Phase 7 implementation unless the user explicitly invokes `/speckit.implement` or asks to implement after reviewing the tasks.

## Review Gate Protocol

After each completed phase artifact:
- Announce the completed phase, artifact name, and artifact path.
- Ask the user to review the artifact and reply with approval before continuing.
- Do not start the next phase until the user approves the current artifact.
- If the user requests changes, revise the current phase artifact, then repeat the same review gate.
- If the phase stopped for ambiguity, clarification, or a material planning question, collect the answer first, update the relevant artifact, then run that phase's review gate.

Use this gate wording:
```text
Phase N complete — [artifact] written to [path].
Please review [path]. Reply with approval to continue to Phase N+1, or provide changes for this phase.
```

## Automatic Flow

0. **Resolve context:**
   - Resolve `<skill_dir>` to the directory containing `SKILL.md`.
   - Determine the project root from the current working directory.
   - Detect platform once: macOS/Linux uses `scripts/bash/`; Windows uses `scripts/powershell/`.

1. **Constitution:**
   - If project `constitution.md` exists, read it in parallel with the relevant project docs and treat it as the Phase 1 artifact.
   - If `constitution.md` is missing, read `commands/constitution.md` fresh and execute Phase 1 to create it.
   - Run the Phase 1 review gate for `constitution.md`. Do not continue to Phase 2 until the user approves.

2. **Specification:**
   - Read `commands/specify.md` fresh.
   - Execute Phase 2 to create or update `spec.md`.
   - If the ambiguity gate triggers, ask the targeted questions and stop until the user answers, then update `spec.md`.
   - Run the Phase 2 review gate for `spec.md`. Do not continue to the clarification decision until the user approves.

3. **Clarification decision:**
   - Inspect `spec.md` for `[NEEDS CLARIFICATION: ...]`, undefined actors, undefined success states, subjective qualifiers, or missing failure/edge-case behavior.
   - If any are present, read `commands/clarify.md` fresh, execute Phase 3, collect required answers, and update `spec.md`.
   - Run the Phase 3 review gate for the updated `spec.md`. Do not continue to Phase 4 until the user approves.
   - If none are present, state that Phase 3 was skipped because no clarification artifact was produced, then continue to Phase 4 without a review gate.

4. **Technical plan:**
   - Read `commands/plan.md` fresh.
   - Execute Phase 4 to create or update `plan.md`.
   - If Phase 4 reports `NEEDS CLARIFICATION` for a decision that materially changes implementation, ask and stop until the user answers, then update `plan.md`.
   - Run the Phase 4 review gate for `plan.md`. Do not continue to Phase 5 until the user approves.

5. **Plan analysis and repair loop:**
   - Read `commands/analyze.md` fresh.
   - Execute Phase 5 to create or update `analysis.md`.
   - Run the Phase 5 review gate for `analysis.md`. Do not repair the plan or continue to Phase 6 until the user approves.
   - If all findings are `PASS` or `WARN`, continue to Phase 6 after approval.
   - If any finding is `FAIL`, read `commands/plan.md` fresh after approval, revise `plan.md` once to address the blockers, run the Phase 4 review gate for the repaired `plan.md`, rerun Phase 5 after approval, then run the Phase 5 review gate for the revised `analysis.md`.
   - If any `FAIL` remains after the single repair loop, stop after the Phase 5 review gate and report the remaining blockers.

6. **Task breakdown:**
   - Read `commands/tasks.md` fresh.
   - Execute Phase 6 to create or update `tasks.md`.
   - Run the Phase 6 review gate for `tasks.md`.
   - After approval, stop and report that the automatic workflow is complete through tasks.

## Handoff Rules

- During this automatic workflow, ignore single-phase handoff prompts such as "Run `/speckit.plan` next"; continue to the next automatic phase instead.
- Stop after every completed phase artifact for user review and approval.
- Stop for explicit blocking gates: ambiguity questions, clarification questions, material planning questions, unrepaired analysis `FAIL`, script failure, or write failure.
- If a script fails non-zero, report the exit code and stderr and stop.
- If an artifact write fails, retry once. If the retry fails, stop and report the path and error.

## Final Output

Summarize:
- Phases completed and artifacts written.
- Gates encountered and their resolution.
- Whether implementation was intentionally skipped.
- Next explicit command: `/speckit.implement`.
