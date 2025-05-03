#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
# Determine repo root dynamically
REPO_ROOT="$(git rev-parse --show-toplevel)"
LOCAL_DIR="$REPO_ROOT/hardware"
BUCKET="gs://theperfectkitebar-cad-assets"
# Only sync these extensions
EXTENSIONS="shapr"  # you can add: shapr|stl|step

# --- Prerequisites ---
if ! command -v gsutil &> /dev/null; then
  echo "❌ gsutil not found. Please install the Google Cloud SDK."
  exit 1
fi

# --- Clean Windows metadata ---
echo "[pre-commit] Cleaning Windows ADS metadata…"
find "$LOCAL_DIR" -type f -name '*:Zone.Identifier' -print0 \
  | xargs -0 rm -f || true

# --- Sync changed CAD files ---
echo "[pre-commit] Syncing CAD assets to GCS bucket…"
# -m = parallel; -r = recursive; -d = delete orphaned remote files
gsutil -m rsync -r -d -x ".*\.(?!$EXTENSIONS$)" "$LOCAL_DIR" "$BUCKET"

# --- End hook ---
exit 0
