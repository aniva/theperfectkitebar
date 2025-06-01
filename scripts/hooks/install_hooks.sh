#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
GIT_HOOKS_DIR="$(git rev-parse --git-path hooks)"

echo "Installing git hooks..."

# Create symlinks for each hook in scripts/hooks
for hook in "$SCRIPT_DIR"/*; do
    if [[ -f "$hook" && -x "$hook" && "${hook}" != *".sh" ]]; then
        hook_name=$(basename "$hook")
        ln -sf "$hook" "$GIT_HOOKS_DIR/$hook_name"
        echo "Installed $hook_name hook"
    fi
done

echo "Git hooks installation complete!"
