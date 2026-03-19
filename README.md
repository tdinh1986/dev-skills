# dev-skills

Reusable Claude Code skills for software development workflows. Skills are modular prompt definitions invoked via slash commands (e.g., `/skill-name`) within Claude Code sessions.

## Installation

### 1. Register the marketplace

Add the following to your `~/.claude/plugins/known_marketplaces.json`:

```json
{
  "dev-skills": {
    "source": {
      "source": "npm",
      "package": "dev-skills"
    },
    "installLocation": "~/.claude/plugins/marketplaces/dev-skills"
  }
}
```

### 2. Install a skill via `/plugin`

```
/plugin install <skill-name>@dev-skills
```

For example:
```
/plugin install case-study@dev-skills
/plugin install spreadsheet-cli@dev-skills
```

### 3. Enable globally (optional)

To auto-enable all skills from this marketplace, add to your `~/.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "dev-skills@dev-skills": true
  }
}
```

---

## Available Skills

### spreadsheet-cli

Interact with Google Spreadsheets directly from the terminal using the Google Sheets API.

- **Commands:** `info`, `read`, `read-json`, `read-csv`, `write`, `append`, `clear`, `create`, `add-sheet`, `search`
- **Auth:** `gcloud` CLI (`gcloud auth login --enable-gdrive-access`)
- **Usage:** `/spreadsheet-cli` — then describe what you want (e.g., "read the spreadsheet", "create a new sheet", "append rows")

### case-study

Fetches content from a web URL and produces a standardized case study summary in markdown.

- **Input:** Any web article URL
- **Output:** Structured markdown with overview, challenge, solution, comparison table, results, and suggested actions
- **Usage:** `/case-study` — then provide a URL

---

## Project Structure

```
dev-skills/
├── .claude-plugin/
│   └── plugin.json            # Plugin metadata
├── .claude/
│   └── settings.json          # Reference config for marketplace + enabledPlugins
├── skills/
│   ├── case-study/
│   │   └── SKILL.md
│   └── spreadsheet-cli/
│       ├── SKILL.md
│       └── sheets.py
├── package.json
├── CLAUDE.md
└── README.md
```

## Adding a New Skill

1. Create a directory under `skills/`: `mkdir skills/skill-name/`
2. Add `skills/skill-name/SKILL.md` with YAML frontmatter (`name`, `description`) and prompt body
3. Publish a new version to npm: `npm publish`
4. Users install with: `/plugin install skill-name@dev-skills`
