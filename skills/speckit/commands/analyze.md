# Phase 5 — Plan Analysis (`/speckit.analyze`)

**Goal:** Audit the technical plan against the constitution for completeness and consistency.

1. **Read `constitution.md` and `plan.md`** in parallel.
2. **Check each constitution principle** — does the plan satisfy it? Assign `PASS`, `WARN`, or `FAIL`:
   - **FAIL = hard blocker:** Do not proceed to Phase 6 until resolved. State the required fix explicitly in the Recommendations section.
   - **WARN = documented risk:** Proceed but log the risk in an `## Accepted Risks` section in `analysis.md`.
3. **Check for missing concerns** in priority order (address higher-priority items first):
   1. **Security:** auth, input validation, secrets handling, injection risks.
   2. **Correctness:** error handling, what fails silently, edge cases unaddressed in the plan.
   3. **Performance:** unindexed queries, N+1 patterns, missing caching, large payload transfers.
   4. **DX/Maintainability:** missing abstractions, unclear ownership, untestable components.
4. **Fundamental rework trigger:** If more than 30% of constitution principles receive a `FAIL` status, recommend restarting Phase 4 rather than patching individual issues. State explicitly: "More than 30% of principles fail — recommend revisiting the technical plan (Phase 4) before continuing."
5. **Output:** `analysis.md` validation report.

**Output format:**
```markdown
# Plan Analysis Report

## Constitution Compliance
| Principle | Status | Notes |
|-----------|--------|-------|
| P1: ...   | PASS   | ...   |
| P3: ...   | WARN   | ...   |
| P5: ...   | FAIL   | ...   |

## Missing Concerns
- [SECURITY] ...
- [TESTING] ...

## Recommendations
1. [Action to resolve WARN/FAIL items]
```

Status values: `PASS` | `WARN` | `FAIL`

If running under `commands/auto.md`, return control to the automatic workflow after writing `analysis.md`. The automatic workflow decides whether to repair `plan.md`, continue to tasks, or stop on remaining `FAIL` findings.
