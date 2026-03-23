# Phase 7 — Implementation (`/speckit.implement`)

**Goal:** Execute tasks from the task list systematically, respecting dependencies.

0. **Pre-execution check:** Run `check-prerequisites.sh --json --require-tasks --include-tasks`. Confirm both plan.md and tasks.md exist. If either is missing, fail fast: tell the user which phase to run.

1. **Read `tasks.md`** to load the full task list.
2. **Identify starting point:** first incomplete task, or the task specified by the user.
3. **For each task:**
   - **Pre-task checklist** (before writing any code):
     - Read the relevant file(s) that will be modified.
     - Check for existing implementations that can be reused.
     - Confirm all `[depends: N]` predecessor tasks are marked `[x]` in `tasks.md`.
   - Announce: "Executing Task N: [description]"
   - Execute the code change.
   - **Update `tasks.md`:** Mark the task `[ ]` → `[x]` immediately after completion.
   - Confirm completion: "Task N complete."
   - Check: are any blocked tasks now unblocked?
4. **Respect dependencies:** never execute a task before its `[depends: N]` predecessors are complete.
5. **Parallel tasks:** execute `[P]` tasks in a single tool-call batch where possible.
6. **Partial failure protocol:** if a task cannot be completed: (1) describe the specific blocker, (2) determine whether the task can be skipped without breaking any `[depends: N]` downstream tasks, (3) present the situation to the user and ask how to proceed. Never silently skip a task.
7. **Implementation complete:** After the final task, run the full test suite (or equivalent verification command). Then produce a summary covering: what was built, which tests pass, and any known gaps or deferred items.

**Hand-off prompt:** After the final task and test run, state: "Implementation complete. Review the summary above for any known gaps or deferred items."

**Progress format:**
```
[x] T001: Set up database schema — done
[x] T002: Create API endpoint — done
[ ] T003: Wire frontend component [depends: T001, T002] — in progress
[ ] T004: Write integration tests [depends: T003]
```
