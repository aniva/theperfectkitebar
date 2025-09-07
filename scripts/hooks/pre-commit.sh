#!/usr/bin/env bash
set -euo pipefail

echo "[pre-commit hook] Cleaning up filesystem metadata files..."
# Safely remove lingering metadata files from Windows (Zone.Identifier) and Dropbox.
find . -type f \( -name '*:Zone.Identifier' -o -name '*:com.dropbox.attrs' \) -print0 | xargs -0 --no-run-if-empty rm -f

echo "[pre-commit hook] Updating .shapr download tables..."
if command -v python3 &>/dev/null; then
  python3 scripts/hooks/update_shapr_tables.py
else
  echo "⚠️  python3 not found, skipping .shapr table update"
fi

# After the script runs, automatically stage any README.md files that were modified.
# This ensures the table updates are included in the commit.
git add -u hardware/**/README.md

exit 0
