# Suggested Commands

## Git (primary workflow — no build step)
- `git status` — check working tree
- `git add skills/<name>/SKILL.md` — stage new/modified skill
- `git commit -m "..."` — commit changes
- `git push origin main` — publish to marketplace

## No linting, formatting, or test commands
This repo has no test suite, linter, or formatter configured. Skills are Markdown files; correctness is verified by reading them.

## Verifying a skill locally
Skills in `.claude/skills/` are auto-discovered by Claude Code. After editing, reload Claude Code to pick up changes.
