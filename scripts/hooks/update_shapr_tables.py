#!/usr/bin/env python3
"""
Script to auto-update README.md files by inserting/updating a table of .shapr file download links
from Google Cloud Storage. Replaces content between BEGIN_SHAPR_TABLE and END_SHAPR_TABLE markers.
Handles HTTP access errors by warning and skipping updates.
"""
import sys
import hashlib
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import re
from pathlib import Path

# Ensure Python 3.6+
if sys.version_info < (3, 6):
    print("❌ Python 3.6 or higher is required.")
    sys.exit(1)

# Configuration
GCS_URL = "https://storage.googleapis.com/theperfectkitebar-cad-assets/"
BEGIN_MARKER = r"<!-- BEGIN_SHAPR_TABLE -->"
END_MARKER = r"<!-- END_SHAPR_TABLE -->"


def fetch_gcs_keys():
    try:
        with urllib.request.urlopen(GCS_URL) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        keys = [elem.text for elem in root.findall(".//Contents/Key") if elem.text.endswith('.shapr')]
        return keys

    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"⚠️  Access denied (HTTP {e.code}) when fetching GCS listing. Skipping .shapr table updates.")
            return []
        else:
            print(f"❌ HTTP error {e.code} when fetching GCS listing: {e.reason}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error fetching GCS listing: {e}")
        sys.exit(1)


def compute_md5(url):
    try:
        with urllib.request.urlopen(url) as resp:
            data = resp.read()
        return hashlib.md5(data).hexdigest()
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"⚠️  Access denied (HTTP {e.code}) when fetching {url}. Skipping MD5 calculation.")
            return "N/A"
        else:
            print(f"❌ HTTP error {e.code} when fetching {url}: {e.reason}")
            return "error"
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return "error"


def generate_table(rel_prefix, keys):
    entries = [k for k in keys if k.startswith(rel_prefix)]
    if not entries:
        return ""  # no matching files => no table

    lines = ["| File | MD5 | Download URL |",
             "|------|-----|--------------|"]
    for k in sorted(entries):
        url = GCS_URL + k
        md5 = compute_md5(url)
        name = k[len(rel_prefix):]
        lines.append(f"| `{name}` | `{md5}` | [Download]({url}) |")
    return "\n".join(lines)


def update_file(path, keys):
    text = path.read_text()
    # Only proceed if markers exist
    if BEGIN_MARKER not in text or END_MARKER not in text:
        return

    rel_prefix = str(path.parent).lstrip('./') + '/'
    table_md = generate_table(rel_prefix, keys)
    # If no files or access denied, skip replacement
    if not table_md:
        print(f"ℹ️  No .shapr files found for {path.parent}, skipping update.")
        return

    # Build replacement block
    replacement = (
        f"{BEGIN_MARKER}\n"
        "<!-- This section is auto-generated. Do not edit manually. -->\n"
        f"{table_md}\n"
        f"{END_MARKER}"
    )
    # Replace existing block
    pattern = re.compile(f"{BEGIN_MARKER}.*?{END_MARKER}", flags=re.DOTALL)
    new_text, count = pattern.subn(replacement, text)
    if count:
        path.write_text(new_text)
        print(f"✅ Updated {path}")


def main():
    print("🔍 Updating .shapr tables in README.md files...")
    keys = fetch_gcs_keys()
    if not keys:
        print("⚠️  No .shapr keys to process.")
        return
    for readme in Path('hardware').rglob('README.md'):
        update_file(readme, keys)


if __name__ == '__main__':
    main()
