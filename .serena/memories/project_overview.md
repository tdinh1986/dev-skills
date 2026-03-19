# dev-skills Project Overview

## Purpose
A personal Claude Code skills marketplace. Stores reusable Claude Code skills (modular prompt definitions) that can be invoked via slash commands (e.g., `/skill-name`) within Claude Code sessions.

## Tech Stack
- No build system or runtime dependencies
- Skills are Markdown files (SKILL.md) with YAML frontmatter
- One skill (spreadsheet-cli) includes a Python helper script (sheets.py)
- Published as a Claude Code plugin marketplace via `.claude-plugin/`

## Distribution
- GitHub repo: git@github.com:tdinh1986/dev-skills.git
- Users install via: `/plugin install skill-name@dev-skills`
- Marketplace registry: `.claude-plugin/marketplace.json`
- Plugin metadata: `.claude-plugin/plugin.json`

## Available Skills
- `spreadsheet-cli` — Google Sheets interaction via terminal
- `case-study` — Fetches a URL and produces a structured markdown case study
