#!/bin/bash

HOOKS_DIR=".git/hooks"
SOURCE_DIR="$(dirname "$0")"

for hook in pre-commit post-commit; do
  src="$SOURCE_DIR/$hook"
  dest="$HOOKS_DIR/$hook"

  if [ -f "$src" ]; then
    # Backup old non-symlink hooks
    [ -f "$dest" ] && [ ! -L "$dest" ] && mv "$dest" "$dest.bak"
    ln -sf "../../$src" "$dest"
    echo "✅ Linked $hook → $dest"
  fi
done

# Auto-restore hooks for large .shapr files
for hook in post-checkout post-merge; do
  dest="$HOOKS_DIR/$hook"
  echo -e "#!/bin/bash\nbash scripts/hooks/restore-shapr.sh" > "$dest"
  chmod +x "$dest"
  echo "✅ Created auto-restore hook: $dest"
done
