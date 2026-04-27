# Phase 1 — Constitution (`/speckit.constitution`)

**Goal:** Establish governing principles for the project before any feature work begins.

1. **Read existing context in parallel:**
   - Read any available project summary or architecture notes from memory if the current agent supports it.
   - Read `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or equivalent project docs with the current agent's available file-read capability.
   - **No-docs fallback:** If none of these files exist, derive principles from detected framework conventions (e.g., Next.js detected → add SSR performance principle; Express detected → add input validation principle). State the inference explicitly and ask the user to confirm or correct before writing `constitution.md`.
1a. **Load template:** Read `templates/constitution-template.md`. Use its structure (named principle sections, Governance section, Version/Ratified/Last Amended metadata footer) as the output skeleton for `constitution.md`.
2. **Synthesize principles** across these dimensions:
   - **Code Quality:** Style guides, linting rules, testing coverage thresholds.
   - **Testing Standards:** Unit / integration / e2e expectations, frameworks in use.
   - **UX Consistency:** Design system, component patterns, accessibility baseline.
   - **Performance Benchmarks:** Load time targets, API latency budgets, bundle size limits.
   - **Security Posture:** Auth patterns, input validation, data handling rules.
3. **Assign principle IDs:** Number every principle sequentially as `P1`, `P2`, … `Pn` across all sections. These IDs are referenced in Phase 5's compliance table.
4. **User approval gate:** Present the draft `constitution.md` to the user and ask: "Does this capture the project's standards? Confirm or adjust before we proceed." Do not advance to Phase 2 until the user confirms.
5. **Output:** A structured `constitution.md` artifact with named, numbered principles.

**Output format:**
```markdown
# [PROJECT_NAME] Constitution

## [Principle Section Name]
[Named principle description — not just "P1: ..."]

## [Principle Section Name]
[Named principle description]

## [Additional sections as needed]

## Governance
[Governance rules and amendment process]

**Version**: 1.0 | **Ratified**: [DATE] | **Last Amended**: [DATE]
```

**Example:**
> User: "Start spec-kit. I want to build a login feature."
> Agent: Reads README + memory → produces `constitution.md` with named sections (Code Quality, Testing Standards, Security Posture) and Governance footer → asks user to confirm before proceeding to Phase 2.

After the user confirms, state: "Constitution ready. Run `/speckit.specify` to write functional requirements." If running under `commands/auto.md`, return control to the automatic workflow instead of asking the user to invoke the next phase.
