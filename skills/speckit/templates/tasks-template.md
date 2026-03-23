# Tasks: [FEATURE NAME]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Plan**: [link]

<!--
  Task format: - [ ] [T###] [P?] [US#?] Description with exact file path

  [P] = can run in parallel (different files, no dependencies)
  [US#] = which user story this task belongs to (US1, US2, US3...)
  T### = sequential task ID (T001, T002, ...)
-->

## Setup

*Project initialization — run once before anything else.*

- [ ] [T001] Initialize project structure and tooling
- [ ] [T002] Configure environment and dependencies

## Foundational

*Critical infrastructure — MUST be complete before ANY user story can be implemented.*

- [ ] [T003] [P] [US1] Set up data models / schema (`src/models/[entity].ts`)
- [ ] [T004] [P] [US1] Set up core service layer (`src/services/[name].ts`)
- [ ] [T005] Write tests for foundational layer (`tests/unit/[name].test.ts`)

## User Stories — P1

*[User Story 1 title] — independently completable and testable*

- [ ] [T006] [P] [US1] Implement [core behavior] (`src/[path]/[file].ts`)
- [ ] [T007] [P] [US1] Implement [supporting behavior] (`src/[path]/[file].ts`)
- [ ] [T008] [US1] Write unit tests for P1 story (`tests/unit/[file].test.ts`)
- [ ] [T009] [US1] Write integration tests for P1 story (`tests/integration/[file].test.ts`)

## User Stories — P2

*[User Story 2 title] — independently completable and testable*

- [ ] [T010] [P] [US2] Implement [behavior] (`src/[path]/[file].ts`)
- [ ] [T011] [US2] Write tests for P2 story (`tests/unit/[file].test.ts`)

## User Stories — P3

*[User Story 3 title] — independently completable and testable*

- [ ] [T012] [P] [US3] Implement [behavior] (`src/[path]/[file].ts`)
- [ ] [T013] [US3] Write tests for P3 story (`tests/unit/[file].test.ts`)

## Polish

*Cross-cutting improvements — run after all user stories are complete.*

- [ ] [T014] Error handling and edge case hardening
- [ ] [T015] Performance optimization (if benchmarks not met)
- [ ] [T016] Documentation and inline comments

## Dependencies

```
T001 → T003, T004
T003, T004 → T006, T007, T010, T012
T006, T007 → T008, T009
T010 → T011
T012 → T013
T008, T009, T011, T013 → T014
```

## Implementation Strategy

Choose one:
- **MVP-first**: Complete P1 story fully (implement + test), validate, then add P2 and P3.
- **Incremental**: Add stories sequentially with testing between each.
- **Parallel team**: Assign different developers to different user stories simultaneously.

Each story adds value without breaking previous stories.
