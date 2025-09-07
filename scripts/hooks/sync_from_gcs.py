#!/usr/bin/env python3
"""
Sync public GCS bucket assets locally with smart updates and backups.

Usage:
    python3 sync_from_gcs.py --bucket theperfectkitebar-cad-assets --root hardware

Features:
- Lists all objects via JSON API
- Skips download if local copy is up-to-date
- Backs up overwritten files to a timestamped backup/ folder
- Checks for 401/403 and aborts on access issues
- Automatically updates .gitignore to exclude backup dirs
"""
import os
import sys
import json
import shutil
import argparse
import datetime
from urllib import request, error
import hashlib
import base64
from pathlib import Path

# --- Path Setup ---
# Get the directory of the script to robustly find the project root.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# --- Sanity Check ---
# Verify that the script is running within the correct project directory.
if PROJECT_ROOT.name != 'theperfectkitebar':
    print(f"❌ Error: This script appears to be running from the wrong project.")
    print(f"   Expected project root name: 'theperfectkitebar', but found: '{PROJECT_ROOT.name}'")
    sys.exit(1)

def fetch_json(url):
    try:
        with request.urlopen(url) as response:
            return json.load(response)
    except error.HTTPError as e:
        if e.code in (401, 403):
            print(f"❌ Access denied when listing bucket: HTTP {e.code}")
            sys.exit(1)
        else:
            print(f"❌ Failed to fetch JSON: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error fetching JSON: {e}")
        sys.exit(1)

def download_file(url, local_path):
    try:
        with request.urlopen(url) as response, open(local_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except error.HTTPError as e:
        if e.code in (401, 403):
            print(f"❌ Access denied when downloading {url}: HTTP {e.code}")
            return False
        else:
            print(f"❌ Failed to download {url}: {e}")
            return False
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return False
    return True

def calculate_local_md5(file_path, chunk_size=8192):
    """Calculates the MD5 hash of a local file in a memory-efficient way."""
    md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            # Read in chunks to handle large files without high memory use
            while chunk := f.read(chunk_size):
                md5.update(chunk)
    except IOError as e:
        print(f"  - Could not read {file_path} for MD5 check: {e}")
        return None
    return md5.hexdigest()

def sync_bucket(bucket, root_dir):
    # Fetch only the fields we need: name and MD5 hash.
    list_url = f"https://storage.googleapis.com/storage/v1/b/{bucket}/o?alt=json&fields=items(name,md5Hash)"
    data = fetch_json(list_url)
    items = data.get("items", [])
    print(f"🚚 Syncing from GCS bucket: {bucket}...")
    for item in items:
        name = item["name"]
        remote_md5_b64 = item.get("md5Hash")
        local_path = Path(root_dir) / name
        download_url = f"https://storage.googleapis.com/{bucket}/{name}"

        # Skip pseudo-directories
        if name.endswith('/'):
            continue


        local_path.parent.mkdir(parents=True, exist_ok=True)

        # --- Decision Logic: Should we download? ---
        # Default to downloading unless we can prove the local file is identical.
        should_download = True
        if local_path.exists():
            if not remote_md5_b64:
                print(f"  - ⚠️ No remote MD5 for {name}, re-downloading for safety.")
            else:
                try:
                    remote_md5_hex = base64.b64decode(remote_md5_b64).hex()
                    local_md5_hex = calculate_local_md5(local_path)
                    if local_md5_hex and local_md5_hex == remote_md5_hex:
                        print(f"✅ Up-to-date: {name}")
                        should_download = False
                    else:
                        # This branch handles mismatch or local read error.
                        print(f"🔄 Stale file detected: {name}")
                except Exception as e:
                    print(f"  - ⚠️ MD5 check failed for {name}: {e}. Re-downloading.")

        # --- Action: Download if necessary ---
        if should_download:
            if local_path.exists():
                # Backup existing file before overwriting
                backup_dir = local_path.parent / "backup"
                backup_dir.mkdir(exist_ok=True)
                timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
                backup_file = backup_dir / f"{timestamp}_{local_path.name}"
                shutil.move(str(local_path), str(backup_file))
                print(f"  - Backed up old version to {backup_file}")

            print(f"⬇️  Downloading {name}...")
            success = download_file(download_url, str(local_path))
            if not success:
                print(f"⚠️  Download failed for {name}")

    print("✅ Sync complete.")

def main():
    parser = argparse.ArgumentParser(
        description="Sync public GCS bucket assets locally.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--bucket", default="theperfectkitebar-cad-assets",
                        help="Name of the GCS bucket")
    parser.add_argument("--root", default=str(PROJECT_ROOT / "hardware"),
                        help="Local root directory to sync into")
    args = parser.parse_args()

    # Update .gitignore to ensure backup directories are ignored project-wide.
    gitignore = PROJECT_ROOT / ".gitignore"
    ignore_entry = "**/backup/"
    try:
        if not gitignore.exists():
            gitignore.write_text(f"{ignore_entry}\n")
        else:
            content = gitignore.read_text()
            # Check if the rule is already present, ignoring surrounding whitespace.
            if not any(line.strip() == ignore_entry for line in content.splitlines()):
                with gitignore.open("a") as f:
                    if content and not content.endswith('\n'):
                        f.write('\n')
                    f.write(f"{ignore_entry}\n")
    except IOError as e:
        print(f"⚠️  Could not update .gitignore: {e}")

    sync_bucket(args.bucket, args.root)

if __name__ == "__main__":
    main()
