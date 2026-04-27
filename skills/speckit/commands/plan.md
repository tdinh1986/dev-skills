# Phase 4 — Technical Planning (`/speckit.plan`)

**Goal:** Define the technical architecture and implementation strategy.

0. **Pre-execution check:** Run `check-prerequisites.sh --json` (or `.ps1 -Json`).
   - Confirm `plan.md` path (FEATURE_DIR). If FEATURE_DIR is missing, tell the user to run `/speckit.specify` first.
   - Load any files listed in `AVAILABLE_DOCS` (research.md, data-model.md, contracts/, quickstart.md) as additional context alongside spec.md.

1. **Read constitution + spec artifacts** (`constitution.md`, `spec.md`) in parallel.
   - **No-spec fallback:** If `spec.md` doesn't exist, work directly from the user's description. Note this assumption explicitly at the top of `plan.md` under a `> Note:` blockquote.
2. **Architecture decisions** — use ADR (Architecture Decision Record) format for each decision:
   - **Decision:** What is being decided.
   - **Options considered:** At least 2 alternatives evaluated.
   - **Choice:** The selected option.
   - **Rationale:** Why this option was chosen. Cite a constitution principle by ID (e.g., `P3`) if applicable.
3. **Data flow:** For any non-trivial data flow (more than 2 hops between components), produce a text-based sequence diagram in the Data Flow section using `-->` notation:
   ```
   Client --> API Gateway: POST /upload
   API Gateway --> Auth Service: validate token
   Auth Service --> API Gateway: 200 OK
   API Gateway --> Storage: write file
   Storage --> API Gateway: file_id
   API Gateway --> Client: { file_id }
   ```
4. **External dependencies:** For any third-party service or library, document:
   - **Integration method:** SDK / REST / webhook
   - **Auth mechanism:** API key / OAuth / service account / none
   - **Fallback behavior:** What happens if the service is unavailable or rate-limited
5. **Load template:** Read `templates/plan-template.md`. Populate the Technical Context fields with known values; mark unknowns `NEEDS CLARIFICATION`. Fill the Constitution Check gates based on `constitution.md` principles. Choose and expand one Project Structure option; remove unused options from the output.
6. **Output:** `plan.md` artifact.
7. **Sync agent context:** Run `update-agent-context.sh existing` (or `.ps1 -AgentType existing`). This parses the new `plan.md` and updates any existing project agent context files such as `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`. If the script exits non-zero, log the error and continue; context sync is advisory, not blocking.

**Hand-off prompt:** After writing `plan.md`, state: "Plan ready. Run `/speckit.tasks` to break this into an ordered task list." If running under `commands/auto.md`, return control to the automatic workflow instead of asking the user to invoke the next phase.

**Output format:**
```markdown
# Implementation Plan: [Feature Name]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

## Summary
[Primary requirement + technical approach]

## Technical Context
**Language/Version**: [value or NEEDS CLARIFICATION]
**Primary Dependencies**: [value or NEEDS CLARIFICATION]
**Storage**: [value or N/A]
**Testing**: [value or NEEDS CLARIFICATION]
**Target Platform**: [value or NEEDS CLARIFICATION]
**Project Type**: [library/cli/web-service/mobile-app/...]
**Performance Goals**: [value or NEEDS CLARIFICATION]
**Constraints**: [value or NEEDS CLARIFICATION]
**Scale/Scope**: [value or NEEDS CLARIFICATION]

## Constitution Check
*GATE: Must pass before proceeding*
[Per-principle gate status from constitution.md]

## Architecture Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| ...      | ...    | ...       |

## Project Structure
\`\`\`text
[Selected structure — single project / web app / mobile+API]
\`\`\`

## Data Flow
[Sequence diagram for non-trivial flows]

## API Contracts
[Endpoint definitions, request/response shapes]

## Open Questions
- [Unresolved technical questions]
```

**Example:**
> User: `/speckit.plan` — "File upload service handling images up to 10MB."
> Agent reads `spec.md`, produces `plan.md` with: storage decision (S3 vs local), file validation approach, API contract for `POST /upload`, virus scanning consideration, Technical Context with all fields populated.
