# Phase 3 — Clarification (`/speckit.clarify`)

**Goal:** Surface edge cases and missing flows before technical planning begins.

This phase can be run standalone after Phase 2 or before Phase 4.

Ask structured questions across these dimensions (max 5 total):
- **Functional gaps:** "What happens when [edge case]?"
- **Non-functional requirements:** "Is there a latency target for [operation]?"
- **Integrations:** "Does this interact with [external system]?"
- **Rollback/failure:** "How should the system behave if [step] fails?"
- **Scale:** "What is the expected volume / concurrent user count?"

After the user responds:
1. **Answer consumption:** Explicitly update `spec.md` with the clarified answers. Add a `## Clarifications` section at the bottom of `spec.md` listing each question and its answer.
2. **Loop-back rule:** If any answer changes a *functional* requirement (not just a constraint or non-functional detail), return to Phase 2 and revise that requirement and its BDD scenario before continuing to Phase 4.
3. **Completion signal:** Phase 3 is complete when all questions are answered and `spec.md` reflects the clarifications. State: "Clarification complete. Proceeding to `/speckit.plan`." If running under `commands/auto.md`, return control to the automatic workflow instead of asking the user to invoke the next phase.
