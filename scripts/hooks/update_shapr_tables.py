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
import hashlib
import re
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import urllib.request, urllib.error

# Ensure Python 3.7+
if sys.version_info < (3, 7):
    print("❌ Python 3.7 or higher is required.")
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
        with urllib.request.urlopen(GCS_JSON_URL, timeout=15) as resp:
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


def calculate_local_md5(file_path, chunk_size=8192):
    """Calculate the MD5 hex digest of a local file."""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return md5.hexdigest()


def sync_shapr_to_gcs(meta):
    """Upload any new or modified local .shapr files under hardware/ to GCS."""
    local_files = [
        p for p in sorted(Path('hardware').rglob('*.shapr'))
        if 'backup' not in p.parts
    ]
    to_upload = []
    for p in local_files:
        rel_full = str(p.relative_to('.')).lstrip('./')
        key = rel_full[len('hardware/'):] if rel_full.startswith('hardware/') else rel_full
        local_md5 = calculate_local_md5(p)
        remote = meta.get(key)
        if not remote or remote.get('md5') != local_md5:
            to_upload.append((p, key))

    if not to_upload:
        return False

    if not shutil.which('gsutil'):
        print("⚠️ gsutil not found; cannot upload new/modified .shapr files to GCS.")
        return False

    uploaded_any = False
    for local_path, key in to_upload:
        dest = f"gs://{GCS_BUCKET}/{key}"
        print(f"⬆️ Uploading {local_path} -> {dest}...")
        res = subprocess.run(['gsutil', 'cp', str(local_path), dest])
        if res.returncode == 0:
            uploaded_any = True
        else:
            print(f"❌ Failed to upload {local_path} to {dest}")
    return uploaded_any


def generate_table(dirpath, meta):
    """Generate a Markdown table for all .shapr files under dirpath."""
    local_files = [
        p for p in Path(dirpath).rglob('*.shapr')
        if 'backup' not in p.parts
    ]
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
    if count and new_text != text:
        path.write_text(new_text)
        print(f"✅ Updated {path}")


def main():
    print("🔍 Updating .shapr tables in README.md files...")
    meta = fetch_metadata()
    if not meta:
        print("⚠️ No metadata found; aborting.")
        return
    if sync_shapr_to_gcs(meta):
        meta = fetch_metadata()
    for readme in Path('hardware').rglob('README.md'):
        update_readme(readme, meta)


if __name__ == '__main__':
    main()
