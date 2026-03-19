---
name: spreadsheet-cli
description: >
  Interact with Google Spreadsheets from the command line. Use this skill when the user wants to
  read, write, search, create, or manage Google Sheets data. Triggers on phrases like
  "read the spreadsheet", "update the sheet", "pull data from Google Sheets",
  "add rows to the spreadsheet", "export sheet to CSV/JSON", "create a new spreadsheet",
  "search the spreadsheet for...", "look up this value in the gsheet", "analyze the data in
  this sheet", "generate a report from the spreadsheet", or when the user provides a Google
  Sheets URL and wants to interact with its data programmatically. Also use when the user
  shares a docs.google.com/spreadsheets link and asks anything about its contents — even
  simple lookups like "what's in column B?" or "find all rows where status is done".
---

# Spreadsheet CLI

Interact with Google Spreadsheets directly from the terminal using the Google Sheets API, authenticated via `gcloud`.

## Prerequisites

- `gcloud` CLI installed and authenticated (`gcloud auth login`)
- The Google Sheets API must be enabled in the user's GCP project
- The authenticated account must have access to the target spreadsheet

If authentication fails, guide the user through:
```bash
gcloud auth login
gcloud services enable sheets.googleapis.com
```

## Helper Script

The CLI helper is located at `sheets.py` in this skill's directory (sibling to this SKILL.md file). Resolve the full path from the skill's location.

Run it with: `python3 <skill-dir>/sheets.py <command> [args...]`

## Available Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `info` | `sheets.py info <url_or_id>` | Show spreadsheet title, sheet names, dimensions |
| `read` | `sheets.py read <url_or_id> [range]` | Read data as aligned table |
| `read-json` | `sheets.py read-json <url_or_id> [range]` | Read data as JSON (first row = headers) |
| `read-csv` | `sheets.py read-csv <url_or_id> [range]` | Read data as CSV |
| `write` | `sheets.py write <url_or_id> <range> '<json>'` | Write values to a range |
| `append` | `sheets.py append <url_or_id> <range> '<json>'` | Append rows after existing data |
| `clear` | `sheets.py clear <url_or_id> <range>` | Clear a range |
| `create` | `sheets.py create <title>` | Create a new spreadsheet |
| `add-sheet` | `sheets.py add-sheet <url_or_id> <title>` | Add a new sheet/tab |
| `search` | `sheets.py search <url_or_id> <term> [range]` | Search rows matching a term |

### Range Format

Ranges follow A1 notation: `Sheet1!A1:C10`, `A:ZZ` (all data), `Sheet2!B2:D` (open-ended).
If omitted, defaults to all data (`A:ZZ`).

### Value Format for Write/Append

Pass values as a JSON array of arrays:
```bash
sheets.py write <url> "A1:B2" '[["Name","Score"],["Alice",95]]'
sheets.py append <url> "Sheet1!A:B" '[["Bob",87],["Carol",92]]'
```

## Workflow

1. **Identify the spreadsheet** — extract the ID from a Google Sheets URL or use a raw ID
2. **Check metadata first** — run `info` to see available sheets and dimensions
3. **Read before writing** — always read the current state before modifying data
4. **Use appropriate output format** — table for display, JSON for processing, CSV for export
5. **Confirm destructive operations** — ask the user before `clear` or overwriting data

## Common Patterns

### Read and display a sheet
```bash
python3 sheets.py info "https://docs.google.com/spreadsheets/d/abc123/edit"
python3 sheets.py read "https://docs.google.com/spreadsheets/d/abc123/edit"
```

### Export to JSON file
```bash
python3 sheets.py read-json "abc123" "Sheet1!A1:E100" > data.json
```

### Export to CSV file
```bash
python3 sheets.py read-csv "abc123" > data.csv
```

### Add new rows
```bash
python3 sheets.py append "abc123" "Sheet1!A:D" '[["2024-01-15","Task","Done","Notes"]]'
```

### Search for specific data
```bash
python3 sheets.py search "abc123" "error" "Logs!A:F"
```

### Analyze data from a sheet
```bash
# Export to JSON, then process with Python or jq
python3 sheets.py read-json "abc123" "Sales!A1:F500" > sales.json
# Or pipe CSV to other tools
python3 sheets.py read-csv "abc123" "Sheet1!A:D" | head -20
```

### Large Sheets

The script reads the full requested range in one API call. For very large sheets (10k+ rows):
- Read specific ranges instead of the whole sheet (`A1:Z1000` instead of `A:ZZ`)
- Use `search` to find relevant rows rather than reading everything
- Export to CSV/JSON and process locally for heavy analysis

## Error Handling

- **403 Forbidden**: The authenticated account lacks access to the spreadsheet. The user needs to share it or check permissions.
- **404 Not Found**: The spreadsheet ID is wrong or the spreadsheet was deleted.
- **gcloud auth failed**: Run `gcloud auth login` to re-authenticate.
- **API not enabled**: Run `gcloud services enable sheets.googleapis.com`.

## Guidelines

- Always show the user what data looks like before making changes
- For large sheets, read specific ranges rather than the entire sheet
- When the user provides a URL, extract the spreadsheet ID automatically
- Prefer `append` over `write` when adding new data to avoid overwriting
- Use `read-json` when the data needs further processing or analysis
