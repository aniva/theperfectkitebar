#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
GIT_HOOKS_DIR="$(git rev-parse --git-path hooks)"

echo "Installing git hooks..."

# Find all executable .sh files, excluding this installer script itself.
for hook_script in "$SCRIPT_DIR"/*.sh; do
    hook_name=$(basename "$hook_script" .sh)
    # Skip the installer script itself and ensure the file is executable
    if [[ "$hook_name" != "install_hooks" && -x "$hook_script" ]]; then
        ln -sf "../../scripts/hooks/$hook_name.sh" "$GIT_HOOKS_DIR/$hook_name"
        echo "✅ Installed $hook_name hook"
    fi
done

echo "Git hooks installation complete!"
