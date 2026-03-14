#!/usr/bin/env python3
"""
Script to auto-update README.md files by inserting/updating a table of .shapr file download links
from Google Cloud Storage JSON listing. Uses the JSON API to fetch MD5 and Updated timestamp.
Matches local .shapr files under hardware/ to GCS objects without the leading 'hardware/' prefix.
Replaces content between BEGIN_SHAPR_TABLE and END_SHAPR_TABLE markers.
"""
import sys
import json
import base64
import re
from pathlib import Path
from datetime import datetime
import urllib.request, urllib.error

# Ensure Python 3.6+
if sys.version_info < (3, 6):
    print("❌ Python 3.6 or higher is required.")
    sys.exit(1)

# Configuration
GCS_BUCKET = "theperfectkitebar-cad-assets"
GCS_JSON_URL = (
    f"https://storage.googleapis.com/storage/v1/b/{GCS_BUCKET}/o"
    "?alt=json&fields=items(name,md5Hash,updated)"
)
GCS_BASE_URL = f"https://storage.googleapis.com/{GCS_BUCKET}/"
BEGIN_MARKER = r"<!-- BEGIN_SHAPR_TABLE -->"
END_MARKER = r"<!-- END_SHAPR_TABLE -->"


def fetch_metadata():
    """Fetch JSON metadata listing from GCS."""
    try:
        with urllib.request.urlopen(GCS_JSON_URL) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        print(f"⚠️ HTTP error {e.code} fetching JSON metadata: {e.reason}")
        return {}
    except Exception as e:
        print(f"❌ Error fetching JSON metadata: {e}")
        return {}
    try:
        items = json.loads(data).get('items', [])
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        return {}
    meta = {}
    for item in items:
        name = item.get('name')
        if not name or not name.endswith('.shapr'):
            continue
        b64 = item.get('md5Hash', '')
        try:
            md5hex = base64.b64decode(b64).hex()
        except Exception:
            md5hex = 'N/A'
        updated = item.get('updated', '')
        try:
            ts = datetime.fromisoformat(updated.rstrip('Z'))
            updated_str = ts.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            updated_str = updated
        meta[name] = {'md5': md5hex, 'updated': updated_str}
    return meta


def generate_table(dirpath, meta):
    """Generate a Markdown table for all .shapr files under dirpath."""
    local_files = [p for p in Path(dirpath).rglob('*.shapr')]
    if not local_files:
        return ''
    lines = ["| File | MD5 | Last Modified | Download URL |",
             "|------|-----|---------------|--------------|"]
    for p in sorted(local_files):
        # Compute object key by stripping leading 'hardware/' from local path
        rel_full = str(p.relative_to('.')).lstrip('./')
        if rel_full.startswith('hardware/'):
            key = rel_full[len('hardware/'):]  # remove prefix for GCS lookup
        else:
            key = rel_full
        entry = meta.get(key)
        if not entry:
            md5 = 'N/A'
            updated = 'N/A'
        else:
            md5 = entry['md5']
            updated = entry['updated']
        url = GCS_BASE_URL + key
        filename = p.name
        lines.append(f"| `{filename}` | `{md5}` | {updated} | [Download]({url}) |")
    return '\n'.join(lines)


def update_readme(path, meta):
    text = path.read_text()
    if BEGIN_MARKER not in text or END_MARKER not in text:
        return
    table = generate_table(path.parent, meta)
    if not table:
        print(f"ℹ️ No .shapr files under {path.parent}, skipping.")
        return
    replacement = (
        f"{BEGIN_MARKER}\n"
        "<!-- Auto-generated Shapr3D download table. Do not edit manually. -->\n"
        f"{table}\n"
        f"{END_MARKER}"
    )
    new_text, count = re.subn(
        f"{BEGIN_MARKER}.*?{END_MARKER}",
        replacement,
        text,
        flags=re.DOTALL
    )
    if count:
        path.write_text(new_text)
        print(f"✅ Updated {path}")


def main():
    print("🔍 Updating .shapr tables in README.md files...")
    meta = fetch_metadata()
    if not meta:
        print("⚠️ No metadata found; aborting.")
        return
    for readme in Path('hardware').rglob('README.md'):
        update_readme(readme, meta)


if __name__ == '__main__':
    main()
