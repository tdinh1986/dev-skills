# Phase 2 — Specification (`/speckit.specify`)

**Goal:** Transform a user request into functional requirements with BDD acceptance criteria.

0. **Create feature structure:** Detect platform (macOS/Linux → bash; Windows → pwsh).
   - bash: `bash <skill_dir>/scripts/bash/create-new-feature.sh --json`
   - pwsh: `pwsh <skill_dir>/scripts/powershell/create-new-feature.ps1 -Json`
   - Parse the returned JSON for `BRANCH` and `FEATURE_DIR`. All output artifacts (spec.md, plan.md, tasks.md) go into `FEATURE_DIR`.
   - **Fallback:** If the script fails or is unavailable, ask the user for a feature name, derive a `NNN-kebab-name` slug, and create the directory manually.

1. **Parallel context retrieval:**
   - Read project memory and relevant source files simultaneously.
2. **Write functional requirements** (no tech prescriptions — describe behavior, not implementation):
   - Use "The system shall..." or "As a [user], I can..." format.
   - Cover happy path, error cases, and edge cases.
   - **Requirement quality rules:** Each requirement must be:
     - **Atomic** — describes exactly one behavior. If "and" connects two behaviors, split into two requirements.
     - **Testable** — has a clear binary pass/fail outcome.
     - **Implementation-free** — no technology references ("use React", "call the API"). Describe *what* the system does, not *how*.
3. **Ambiguity gate:** If the request is ambiguous, STOP and ask max 3 targeted questions:
   - **Functional:** What is the expected happy path?
   - **Non-Functional:** Are there performance or security constraints?
   - **Constraints:** Any platform, browser, or device limitations?
   - **Ambiguity decision tree:** A requirement is ambiguous if it has an undefined actor (who triggers it?), an undefined success state (what does "done" look like?), or a subjective qualifier ("fast", "easy", "modern", "clean"). Any of these → trigger the gate. If none apply, proceed without asking.
4. **Load template:** Read `templates/spec-template.md`. Use FR-001 codes for functional requirements, P1/P2/P3 priority tiers for user stories, SC-001 codes for success criteria. Mark any unclear requirements `[NEEDS CLARIFICATION: ...]` (max 3 such markers per spec).
5. **Generate BDD scenarios** for each requirement:
   - Draft a JSON object using this exact shape:
     ```json
     {
       "feature": "User Login",
       "scenarios": [
         {
           "title": "Successful login with valid credentials",
           "given": ["the user is on the login page"],
           "when": ["the user enters a valid email and password", "the user clicks Sign In"],
           "then": ["the user is redirected to the dashboard", "a session token is set"]
         },
         {
           "title": "Login fails with wrong password",
           "given": ["the user is on the login page"],
           "when": ["the user enters a valid email and an incorrect password"],
           "then": ["an error message is displayed", "no session token is set"]
         }
       ]
     }
     ```
   - **Pre-flight:** Verify `scripts/bdd_converter.cjs` exists via `Glob`.
   - **Run conversion:** `node <skill_dir>/scripts/bdd_converter.cjs '<json_string>'`
     - `<skill_dir>` is the directory containing `SKILL.md`.
     - Ensure `<json_string>` is properly escaped with no shell control characters.
   - **Fallback:** If script is missing or fails, format Gherkin manually.
   - **Multiple Feature blocks:** If the request spans multiple independent behavior areas (e.g., login + registration), produce one Feature block per area, each with its own JSON object and `bdd_converter.cjs` call.
6. **Output:** `spec.md` artifact with Feature/Scenario blocks + Definition of Done checklist.
7. **Hand-off prompt:** After writing `spec.md`, state: "Spec ready. Run `/speckit.clarify` to surface edge cases, or `/speckit.plan` to proceed to architecture." If running under `commands/auto.md`, return control to the automatic workflow instead of asking the user to invoke the next phase.

**Output format:**
```markdown
# Feature Specification: [Feature Name]

**Feature Branch**: `[###-feature-name]`
**Created**: [DATE]
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - [Title] (Priority: P1)
[Plain-language description]
**Why this priority**: [Rationale]
**Independent Test**: [How to test standalone]
**Acceptance Scenarios**:
1. **Given** ..., **When** ..., **Then** ...

### User Story 2 - [Title] (Priority: P2)
...

## Requirements

### Functional Requirements
- **FR-001**: System MUST [capability]
- **FR-002**: System MUST [capability]
- **FR-003**: System MUST [NEEDS CLARIFICATION: unclear aspect]

## Success Criteria

### Measurable Outcomes
- **SC-001**: [Measurable metric]
- **SC-002**: [Measurable metric]
```

**Example:**
> User: `/speckit.specify` — "Make the dashboard faster."
> Agent triggers ambiguity gate: "1. Are we targeting TTFB/LCP or interaction latency? 2. Current baseline and target? 3. All dashboards or a specific view?"
