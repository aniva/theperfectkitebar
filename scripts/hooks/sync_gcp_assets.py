#!/usr/bin/env python3
"""
Sync public GCS bucket assets locally with smart updates and backups.

Usage:
    python3 sync_gcp_assets.py --bucket theperfectkitebar-cad-assets --root hardware

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
from pathlib import Path

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

def sync_bucket(bucket, root_dir):
    list_url = f"https://storage.googleapis.com/storage/v1/b/{bucket}/o?alt=json&fields=items(name,updated)"
    data = fetch_json(list_url)
    items = data.get("items", [])
    for item in items:
        name = item["name"]
        updated = datetime.datetime.fromisoformat(item["updated"].replace("Z", "+00:00"))
        local_path = Path(root_dir) / name
        download_url = f"https://storage.googleapis.com/{bucket}/{name}"
        # Skip pseudo-directories
        if name.endswith('/'):
            continue
        local_path.parent.mkdir(parents=True, exist_ok=True)
        if local_path.exists():
            mtime = datetime.datetime.fromtimestamp(local_path.stat().st_mtime, tz=datetime.timezone.utc)
            if mtime >= updated:
                continue
            # backup
            backup_dir = local_path.parent / "backup"
            backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
            backup_file = backup_dir / f"{timestamp}_{local_path.name}"
            shutil.move(str(local_path), str(backup_file))
            print(f"🔄 Backed up {local_path} to {backup_file}")
        print(f"⬇️  Downloading {name}")
        success = download_file(download_url, str(local_path))
        if not success:
            print(f"⚠️  Skipped {name}")
    print("✅ Sync complete.")

def main():
    parser = argparse.ArgumentParser(description="Sync public GCS bucket assets locally.")
    parser.add_argument("--bucket", default="theperfectkitebar-cad-assets",
                        help="Name of the GCS bucket")
    parser.add_argument("--root", default="hardware",
                        help="Local root directory to sync into")
    args = parser.parse_args()
    # update .gitignore
    gitignore = Path(".gitignore")
    ignore_line = f"{args.root}/**/backup/\n"
    if gitignore.exists():
        content = gitignore.read_text()
        if ignore_line not in content:
            gitignore.write_text(content + ignore_line)
    else:
        gitignore.write_text(ignore_line)
    sync_bucket(args.bucket, args.root)

if __name__ == "__main__":
    main()
