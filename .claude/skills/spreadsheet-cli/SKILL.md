---
name: spreadsheet-cli
description: >
  Interact with Google Spreadsheets from the command line. Use this skill when the user wants to
  read, write, search, create, or manage Google Sheets data. Triggers on phrases like
  "read the spreadsheet", "update the sheet", "pull data from Google Sheets",
  "add rows to the spreadsheet", "export sheet to CSV/JSON", "create a new spreadsheet",
  "search the spreadsheet for...", or when the user provides a Google Sheets URL and wants
  to interact with its data programmatically.
---

## Description

Interact with Google Spreadsheets directly from the terminal using the Google Sheets API, authenticated via `gcloud`. Supports reading, writing, searching, creating, and managing sheet data through a Python CLI helper.

## Instructions

### Prerequisites

- `gcloud` CLI installed and authenticated (`gcloud auth login`)
- Google Sheets API enabled in the user's GCP project
- Authenticated account has access to the target spreadsheet

If authentication fails, guide the user through:
```bash
gcloud auth login
gcloud services enable sheets.googleapis.com
```

### Helper Script

The CLI helper is located at `<skill_dir>/sheets.py` where `<skill_dir>` is the directory containing this `SKILL.md`.

Run it with: `python3 <skill_dir>/sheets.py <command> [args...]`

### Available Commands

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

### Workflow

1. **Identify the spreadsheet** — extract the ID from a Google Sheets URL or use a raw ID.
2. **Run `info` first** — check available sheets, dimensions, and accessibility before any other operation. This scopes subsequent reads to the actual data range instead of defaulting to `A:ZZ`.
3. **Read before writing** — always read the current state before modifying data.
4. **Preview changes** — before executing `write`, `append`, or `clear`, show the user exactly what will change (target range, values, rows affected). Wait for confirmation.
5. **Execute and verify** — after a write or append, re-read the affected range to confirm the change was applied correctly.
6. **Report results** — summarize what was done: cells updated, rows appended, or range cleared.

### Performance

- Use specific ranges (e.g., `Sheet1!A1:D50`) instead of `A:ZZ` whenever possible. Use `info` output to determine actual data boundaries.
- For large datasets, read in targeted ranges rather than fetching everything.
- When multiple independent reads are needed (e.g., `info` + `read` on different sheets), execute them in parallel if the agent supports it.

### Input Validation

Before executing commands, validate inputs:
- **Spreadsheet ID/URL**: Confirm the string looks like a valid Google Sheets URL or a 44-character alphanumeric ID. Reject obviously malformed inputs.
- **Range**: Confirm A1 notation format (e.g., `Sheet1!A1:C10`). Reject strings that don't match expected patterns.
- **JSON values**: For `write`/`append`, validate that the JSON parses as an array of arrays before passing to the script. Report parse errors to the user with the specific issue.
- **Required arguments**: Check that all required arguments for a command are present before running. If missing, prompt the user rather than passing incomplete arguments.

### Error Handling

| Error | Cause | Remediation |
|-------|-------|-------------|
| 403 Forbidden | Account lacks access to the spreadsheet | User needs to share the spreadsheet or check permissions |
| 404 Not Found | Wrong spreadsheet ID or spreadsheet deleted | Verify the URL/ID with the user |
| gcloud auth failed | Token expired or not authenticated | Run `gcloud auth login` |
| API not enabled | Sheets API not activated in GCP project | Run `gcloud services enable sheets.googleapis.com` |
| Invalid range | Range format doesn't match A1 notation | Show the correct format and ask user to re-specify |
| Malformed JSON | JSON input doesn't parse or isn't array-of-arrays | Show the expected format with an example |
| Network timeout | Connectivity issue or API unresponsive | Retry once, then report the issue to the user |
| Missing arguments | Required command arguments not provided | Show the command's usage and prompt for missing values |

If a command fails, report the full error message and suggest the most likely fix. Do not silently retry without informing the user.

### Security and Data Privacy

- Do not log, store, or display more spreadsheet data than the user requested.
- If a sheet appears to contain sensitive data (emails, phone numbers, credentials, financial data), warn the user before displaying it in full.
- Only access spreadsheets the user has explicitly identified. Do not enumerate or browse other spreadsheets in the account.
- Confirm destructive operations (`clear`, overwriting existing data) with the user before executing.

### Guidelines

- Always show the user what data looks like before making changes.
- When the user provides a URL, extract the spreadsheet ID automatically.
- Prefer `append` over `write` when adding new data to avoid overwriting.
- Use `read-json` when the data needs further processing or analysis.
- Use neutral, factual descriptions of data content. Do not interpret or editorialize.

## Examples

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
