#!/usr/bin/env bash
set -euo pipefail

echo "[pre-commit hook] Cleaning up Windows metadata..."
# Safely remove any lingering Zone.Identifier files
find . -type f -name '*:Zone.Identifier' -print0 | xargs -0 rm -f || true

echo "[pre-commit hook] Updating .shapr download tables..."
if command -v python3 &>/dev/null; then
  python3 scripts/hooks/update_shapr_tables.py
else
  echo "⚠️  python3 not found, skipping .shapr table update"
fi

# After the script runs, automatically stage any README.md files that were modified.
# This ensures the table updates are included in the commit.
git add hardware/**/README.md

exit 0
