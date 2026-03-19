# Codebase Structure & Conventions

## Directory Layout
```
dev-skills/
├── .claude-plugin/
│   ├── marketplace.json   # Skill registry for the marketplace
│   └── plugin.json        # Plugin metadata
├── .claude/
│   └── settings.json      # Reference config
├── skills/
│   ├── case-study/
│   │   └── SKILL.md
│   └── spreadsheet-cli/
│       ├── SKILL.md
│       └── sheets.py
├── CLAUDE.md
├── README.md
└── package.json
```

## Conventions
- Skill names: `kebab-case`
- Each skill lives in `skills/<skill-name>/` with a `SKILL.md` and optional supporting files
- SKILL.md uses YAML frontmatter: `name`, `description`, `triggers`
- Descriptions must be specific to avoid false-positive trigger matching
- Each skill has a single, well-defined responsibility

## Adding a New Skill
1. `mkdir skills/skill-name/`
2. Create `skills/skill-name/SKILL.md` with frontmatter + prompt body
3. Register in `.claude-plugin/marketplace.json`
4. `git push origin main`
