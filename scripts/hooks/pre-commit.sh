#!/usr/bin/env bash
set -euo pipefail

echo "[pre-commit hook] Cleaning up filesystem metadata files..."
# Safely remove lingering metadata files from Windows (Zone.Identifier) and Dropbox.
find . -type f \( -name '*:Zone.Identifier' -o -name '*:com.dropbox.attrs' \) -print0 | xargs -0 --no-run-if-empty rm -f

echo "[pre-commit hook] Updating .shapr download tables..."
if command -v python3 &>/dev/null; then
  # Capture output without requiring a terminal; no updates is a normal result.
  OUTPUT=$(python3 scripts/hooks/update_shapr_tables.py)
  printf '%s\n' "$OUTPUT"
  while IFS= read -r line; do
    if [[ "$line" == "✅ Updated "* ]]; then
      git add -- "${line#✅ Updated }"
    fi
  done <<< "$OUTPUT"
else
  echo "⚠️  python3 not found, skipping .shapr table update"
fi

exit 0
