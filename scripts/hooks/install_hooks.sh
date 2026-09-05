#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."
GIT_HOOKS_DIR="$(git rev-parse --git-path hooks)"
mkdir -p "$GIT_HOOKS_DIR"

# Absolute targets also work when Git stores hooks outside this checkout.
for hook_script in "$SCRIPT_DIR"/*.sh; do
    hook_name=$(basename "$hook_script" .sh)
    [[ "$hook_name" == "install_hooks" ]] && continue
    destination="$GIT_HOOKS_DIR/$hook_name"
    if [[ -e "$destination" && ! -L "$destination" ]]; then
        echo "Refusing to replace existing hook: $destination" >&2
        exit 1
    fi
    chmod +x "$hook_script"
    ln -sfn "$hook_script" "$destination"
    echo "Installed $hook_name hook"
done
