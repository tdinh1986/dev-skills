# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repository stores reusable Claude Code skills for software development workflows. Skills are modular prompt definitions that can be invoked via slash commands (e.g., `/skill-name`) within Claude Code sessions.

## Commands

```bash
# Install this skills package as a Claude Code plugin (from the repo root)
npm install  # no dependencies; just sets up package metadata

# Symlink the skills directory for local development
ln -s $(pwd)/skills ~/.claude/skills/dev-skills

# Verify a skill loads
# Run /reload-plugins inside a Claude Code session after adding a skill
```

## Repository Layout

```
skills/
  case-study/       # Fetches a URL and produces a structured case study
  speckit/          # Spec-Driven Development across 7 sequential phases
  spreadsheet-cli/  # CLI-style interaction with Google Sheets
  til/              # Surfaces learnings from local chat history; identifies skill candidates
CLAUDE.md           # This file
package.json        # Plugin manifest for npm-based distribution
```

## Skill Structure

Each skill lives in its own subdirectory and typically contains:
- `SKILL.md` — the skill definition, including frontmatter (name, description, trigger conditions) and the prompt body
- Supporting files (scripts, templates, examples) as needed

### SKILL.md Frontmatter

Skills use YAML frontmatter to declare metadata:

```yaml
---
name: skill-name
description: One-line description used for trigger matching
triggers:
  - example phrase that activates this skill
---
```

## Adding a New Skill

1. Create a new directory: `mkdir skill-name/`
2. Create `skill-name/SKILL.md` with frontmatter and prompt body
3. Copy or symlink your skill directory into `~/.claude/skills/`
4. Run `/reload-plugins` inside Claude Code to activate
5. Verify it appears in the skill list before writing trigger phrases

## Skill Design Conventions

- Skill names use `kebab-case`
- Descriptions should be specific enough for accurate trigger matching — vague descriptions cause false positives
- Each skill should have a single, well-defined responsibility
- Include concrete trigger phrases that distinguish this skill from others
