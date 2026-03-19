---
name: skill-market
description: Browse and install skills from the personal dev-skills repository into ~/.claude/skills/. Use when the user wants to list available skills, install a skill, uninstall a skill, or check which skills are already installed.
argument-hint: [list|install <skill-name>|uninstall <skill-name>|status]
allowed-tools: [Bash, Read, Glob]
---

# Skill Market

Manage skills from the personal dev-skills repository (`/Users/kenzen/Documents/Work/dev-skills`).

## Constants

```
SKILLS_REPO=/Users/kenzen/Documents/Work/dev-skills/skills
INSTALL_DIR=~/.claude/skills
```

## Commands

### No argument or `list`
Show all available skills in the repo with their install status:
1. Run `ls "$SKILLS_REPO"` to get available skills
2. For each skill, check if `~/.claude/skills/<skill-name>` exists
3. Show a table: skill name | installed (✓ or —) | description (from first line of SKILL.md `description:` field)

Example output:
```
Available skills in dev-skills repo:

  case-study          ✓ installed    Fetches a URL and produces a case study summary
  spreadsheet-cli     — not installed  CLI tool for managing Google Sheets
```

### `install <skill-name>`
Install a skill by copying it to `~/.claude/skills/`:
1. Verify `$SKILLS_REPO/<skill-name>` exists — if not, show available skills and stop
2. Check if already installed — if so, ask if user wants to reinstall/update
3. Run: `cp -r "$SKILLS_REPO/<skill-name>" ~/.claude/skills/`
4. Confirm success: "Installed <skill-name>. Available as /<skill-name> in Claude Code sessions."

### `uninstall <skill-name>`
Remove a skill from `~/.claude/skills/`:
1. Verify `~/.claude/skills/<skill-name>` exists — if not, say it's not installed
2. Run: `rm -rf ~/.claude/skills/<skill-name>`
3. Confirm: "Uninstalled <skill-name>."

### `status`
Show a summary: how many skills are in the repo vs. how many are installed.

## Behavior Notes

- If the user provides a skill name without a subcommand (e.g., `/skill-market case-study`), treat it as `install <skill-name>`
- Always show the skill's description when listing so the user knows what each skill does
- If `$SKILLS_REPO` doesn't exist (repo not found), say: "dev-skills repo not found at /Users/kenzen/Documents/Work/dev-skills. Please verify the path."
- Skills are installed as copies (not symlinks) so they survive repo moves
