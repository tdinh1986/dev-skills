# Phase 6 — Task Breakdown (`/speckit.tasks`)

**Goal:** Convert the plan into an ordered, dependency-aware task list.

0. **Pre-execution check:** Run `check-prerequisites.sh --json`. Confirm plan.md exists in FEATURE_DIR. Load AVAILABLE_DOCS for additional context. If plan.md is missing, tell the user to run `/speckit.plan` first.

1. **Read `plan.md`** (and `spec.md` for user story grouping).
2. **Group tasks by user story or component.**
3. **Order tasks** so dependencies are explicit — no task should reference work not yet defined.
   - **Infrastructure first:** Always place env/config/schema/migration tasks before feature implementation tasks, regardless of story grouping. These are prerequisites even if not explicitly called out in user stories.
4. **Mark parallelism:** tasks that can be executed concurrently get `[P]`; dependent tasks get `[depends: N]`.
   - **Cross-story dependencies:** If a task in Story 2 depends on a task in Story 1, use the global task number in `[depends: N]`, not the story-local number.
5. **Granularity rule:** One task = one file, one function, one migration, or one test suite. Never bundle multiple distinct changes into one task (e.g., "implement the whole API" is too coarse — break it into individual endpoint tasks).
6. **Test pairing:** Every implementation task that adds behavior must be immediately followed by an explicit test task, unless the task itself is "write tests".
7. **Size guidance:** Aim for 5–15 tasks per feature. If the total exceeds 20 tasks, suggest splitting into milestones and prompt the user before proceeding.
8. **Load template:** Read `templates/tasks-template.md`. Use format `- [ ] [T###] [P?] [US#?] Description with exact file path`. Organize output into phases: Setup → Foundational → User Stories (P1, P2, P3) → Polish. `[P]` marks parallel-safe tasks; `[US#]` links tasks to their user story.
9. **Output:** `tasks.md` artifact.

**Output format:**
```markdown
# Tasks: [Feature Name]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Plan**: [link]

## Setup
- [ ] [T001] Initialize project structure and tooling

## Foundational
*MUST be complete before any user story*
- [ ] [T002] [P] [US1] Set up data models (`src/models/[entity].ts`)
- [ ] [T003] [P] [US1] Set up core service layer (`src/services/[name].ts`)

## User Stories — P1
*[Story title]*
- [ ] [T004] [P] [US1] Implement [behavior] (`src/[path]/[file].ts`)
- [ ] [T005] [US1] Write tests (`tests/unit/[file].test.ts`)

## User Stories — P2
*[Story title]*
- [ ] [T006] [P] [US2] Implement [behavior] (`src/[path]/[file].ts`)
- [ ] [T007] [US2] Write tests (`tests/unit/[file].test.ts`)

## User Stories — P3
*[Story title]*
- [ ] [T008] [P] [US3] Implement [behavior] (`src/[path]/[file].ts`)
- [ ] [T009] [US3] Write tests (`tests/unit/[file].test.ts`)

## Polish
- [ ] [T010] Error handling and edge case hardening
- [ ] [T011] Documentation
```

Each task entry should be actionable at the level of a single code change (file, function, migration, test, etc.).

**Hand-off prompt:** After writing `tasks.md`, state: "Tasks ready. Run `/speckit.implement` to begin execution." If running under `commands/auto.md`, report automatic workflow completion through tasks and do not proceed to implementation.

**Example:**
> User: `/speckit.tasks` — Agent reads `plan.md`, identifies 3 user stories (Upload, Preview, Delete), produces `tasks.md` with 12 tasks: T001–T003 marked `[P]` (schema + S3 config + API scaffolding), T004 marked `[depends: 1, 2, 3]`.
