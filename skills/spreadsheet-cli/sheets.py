#!/usr/bin/env python3
"""Google Sheets CLI helper — uses gcloud auth for access tokens."""

import json
import sys
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import csv
import io

BASE_URL = "https://sheets.googleapis.com/v4/spreadsheets"


def get_access_token():
    result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print("Error: gcloud auth failed. Run: gcloud auth login", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def api_request(url, method="GET", data=None):
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"API error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def extract_spreadsheet_id(url_or_id):
    """Extract spreadsheet ID from a URL or return as-is if already an ID."""
    if "/" in url_or_id:
        # URL format: https://docs.google.com/spreadsheets/d/{ID}/...
        parts = url_or_id.split("/")
        try:
            idx = parts.index("d")
            return parts[idx + 1]
        except (ValueError, IndexError):
            print(f"Error: cannot extract spreadsheet ID from URL: {url_or_id}", file=sys.stderr)
            sys.exit(1)
    return url_or_id


def cmd_info(args):
    """Get spreadsheet metadata (title, sheets, etc.)."""
    sid = extract_spreadsheet_id(args[0])
    data = api_request(f"{BASE_URL}/{sid}?fields=properties.title,sheets.properties")
    print(f"Title: {data['properties']['title']}")
    print(f"Sheets:")
    for s in data.get("sheets", []):
        p = s["properties"]
        print(f"  - {p['title']} (id={p['sheetId']}, rows={p.get('gridProperties',{}).get('rowCount','?')}, cols={p.get('gridProperties',{}).get('columnCount','?')})")


def cmd_read(args):
    """Read a range from a spreadsheet. Usage: read <id_or_url> [range]"""
    sid = extract_spreadsheet_id(args[0])
    range_str = args[1] if len(args) > 1 else "A:ZZ"
    encoded_range = urllib.parse.quote(range_str)
    data = api_request(f"{BASE_URL}/{sid}/values/{encoded_range}")
    rows = data.get("values", [])
    if not rows:
        print("(empty)")
        return
    # Print as aligned table
    col_widths = []
    for row in rows:
        for i, cell in enumerate(row):
            if i >= len(col_widths):
                col_widths.append(0)
            col_widths[i] = max(col_widths[i], len(str(cell)))
    for row in rows:
        line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(line)


def cmd_read_json(args):
    """Read a range and output as JSON (first row = headers)."""
    sid = extract_spreadsheet_id(args[0])
    range_str = args[1] if len(args) > 1 else "A:ZZ"
    encoded_range = urllib.parse.quote(range_str)
    data = api_request(f"{BASE_URL}/{sid}/values/{encoded_range}")
    rows = data.get("values", [])
    if len(rows) < 2:
        print("[]")
        return
    headers = rows[0]
    records = []
    for row in rows[1:]:
        record = {}
        for i, h in enumerate(headers):
            record[h] = row[i] if i < len(row) else ""
        records.append(record)
    print(json.dumps(records, indent=2, ensure_ascii=False))


def cmd_read_csv(args):
    """Read a range and output as CSV."""
    sid = extract_spreadsheet_id(args[0])
    range_str = args[1] if len(args) > 1 else "A:ZZ"
    encoded_range = urllib.parse.quote(range_str)
    data = api_request(f"{BASE_URL}/{sid}/values/{encoded_range}")
    rows = data.get("values", [])
    writer = csv.writer(sys.stdout)
    for row in rows:
        writer.writerow(row)


def cmd_write(args):
    """Write values to a range. Usage: write <id_or_url> <range> <json_values>
    json_values is a JSON array of arrays, e.g. '[["a","b"],["c","d"]]'
    """
    sid = extract_spreadsheet_id(args[0])
    range_str = args[1]
    values = json.loads(args[2])
    encoded_range = urllib.parse.quote(range_str)
    body = {"range": range_str, "majorDimension": "ROWS", "values": values}
    result = api_request(
        f"{BASE_URL}/{sid}/values/{encoded_range}?valueInputOption=USER_ENTERED",
        method="PUT",
        data=body,
    )
    print(f"Updated {result.get('updatedCells', 0)} cells in {result.get('updatedRange', range_str)}")


def cmd_append(args):
    """Append rows to a sheet. Usage: append <id_or_url> <range> <json_values>"""
    sid = extract_spreadsheet_id(args[0])
    range_str = args[1]
    values = json.loads(args[2])
    encoded_range = urllib.parse.quote(range_str)
    body = {"range": range_str, "majorDimension": "ROWS", "values": values}
    result = api_request(
        f"{BASE_URL}/{sid}/values/{encoded_range}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS",
        method="POST",
        data=body,
    )
    updates = result.get("updates", {})
    print(f"Appended {updates.get('updatedRows', 0)} rows to {updates.get('updatedRange', range_str)}")


def cmd_clear(args):
    """Clear a range. Usage: clear <id_or_url> <range>"""
    sid = extract_spreadsheet_id(args[0])
    range_str = args[1]
    encoded_range = urllib.parse.quote(range_str)
    api_request(f"{BASE_URL}/{sid}/values/{encoded_range}:clear", method="POST", data={})
    print(f"Cleared {range_str}")


def cmd_create(args):
    """Create a new spreadsheet. Usage: create <title>"""
    title = args[0] if args else "Untitled"
    body = {"properties": {"title": title}}
    result = api_request(BASE_URL, method="POST", data=body)
    print(f"Created: {result['properties']['title']}")
    print(f"ID: {result['spreadsheetId']}")
    print(f"URL: {result['spreadsheetUrl']}")


def cmd_add_sheet(args):
    """Add a new sheet/tab. Usage: add-sheet <id_or_url> <sheet_title>"""
    sid = extract_spreadsheet_id(args[0])
    title = args[1]
    body = {"requests": [{"addSheet": {"properties": {"title": title}}}]}
    api_request(f"{BASE_URL}/{sid}:batchUpdate", method="POST", data=body)
    print(f"Added sheet '{title}'")


def cmd_search(args):
    """Search for rows matching a value. Usage: search <id_or_url> <search_term> [range]"""
    sid = extract_spreadsheet_id(args[0])
    term = args[1].lower()
    range_str = args[2] if len(args) > 2 else "A:ZZ"
    encoded_range = urllib.parse.quote(range_str)
    data = api_request(f"{BASE_URL}/{sid}/values/{encoded_range}")
    rows = data.get("values", [])
    if not rows:
        print("(empty)")
        return
    header = rows[0] if rows else []
    print(" | ".join(header))
    print("-" * 40)
    for i, row in enumerate(rows[1:], start=2):
        if any(term in str(cell).lower() for cell in row):
            print(f"[row {i}] " + " | ".join(str(c) for c in row))


COMMANDS = {
    "info": cmd_info,
    "read": cmd_read,
    "read-json": cmd_read_json,
    "read-csv": cmd_read_csv,
    "write": cmd_write,
    "append": cmd_append,
    "clear": cmd_clear,
    "create": cmd_create,
    "add-sheet": cmd_add_sheet,
    "search": cmd_search,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: sheets.py <command> [args...]")
        print()
        print("Commands:")
        for name, fn in COMMANDS.items():
            print(f"  {name:12s}  {fn.__doc__.split(chr(10))[0]}")
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}. Use --help for available commands.", file=sys.stderr)
        sys.exit(1)

    COMMANDS[cmd](sys.argv[2:])


if __name__ == "__main__":
    main()
