#!/usr/bin/env bash
set -euo pipefail

echo "[pre-commit hook] Cleaning up filesystem metadata files..."
# Safely remove lingering metadata files from Windows (Zone.Identifier) and Dropbox.
find . -type f \( -name '*:Zone.Identifier' -o -name '*:com.dropbox.attrs' \) -print0 | xargs -0 --no-run-if-empty rm -f

echo "[pre-commit hook] Updating .shapr download tables..."
if command -v python3 &>/dev/null; then
  # Run the script and capture its output to find which files were modified.
  # The `tee /dev/tty` part ensures the script's output is still visible to the user.
  UPDATED_FILES=$(python3 scripts/hooks/update_shapr_tables.py | tee /dev/tty | grep '✅ Updated' | sed 's/✅ Updated //')

  # If any files were updated, add only those specific files to the index.
  if [ -n "$UPDATED_FILES" ]; then
    echo "[pre-commit hook] Staging updated README files..."
    echo "$UPDATED_FILES" | xargs git add
  fi
else
  echo "⚠️  python3 not found, skipping .shapr table update"
fi

exit 0
