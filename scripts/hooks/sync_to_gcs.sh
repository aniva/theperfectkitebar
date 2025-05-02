#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
LOCAL_DIR="$HOME/repos/theperfectkitebar/hardware"
BUCKET="gs://theperfectkitebar-cad-assets"
EXTENSIONS=("shapr") # "stl" "step")  # include all CAD extensions

# --- build extension test array for find ---
EXT_ARGS=()
for ext in "${EXTENSIONS[@]}"; do
  EXT_ARGS+=( -iname "*.${ext}" -o )
done
# drop the trailing '-o'
unset 'EXT_ARGS[${#EXT_ARGS[@]}-1]'

# --- Environment Validation ---
echo "🔍 Validating GCP environment…"
ACTIVE_ACCOUNT=$(gcloud auth list --format="value(account)" --filter="status:ACTIVE")
if [[ -z "$ACTIVE_ACCOUNT" ]]; then
  echo "❌ No active GCP account. Run: gcloud auth login"
  exit 1
fi

PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [[ -z "$PROJECT_ID" ]]; then
  echo "❌ No GCP project set. Run: gcloud config set project YOUR_PROJECT_ID"
  exit 1
fi

echo "✅ Using project: $PROJECT_ID"
echo "✅ Bucket: $BUCKET"
echo

# --- Upload New or Changed Files ---
echo "⬆️  Uploading new or changed files…"
while IFS= read -r -d '' file; do
  rel_path="${file#$LOCAL_DIR/}"
  gcs_path="$BUCKET/$rel_path"

  echo "🔍 Checking remote: $rel_path"
  if ! gsutil ls "$gcs_path" &>/dev/null; then
    echo "📤 New file → $rel_path"
    gsutil cp "$file" "$gcs_path"
    continue
  fi

  # Compute local MD5 in base64 (keep '=' padding)
  local_md5_base64=$(md5sum "$file" \
    | awk '{print $1}' \
    | xxd -r -p \
    | openssl base64 \
    | tr -d '\n')
  echo "   local_md5 (base64): $local_md5_base64"

  # Fetch remote MD5, then strip *all* whitespace before comparing
  remote_md5=$(gsutil stat "$gcs_path" \
    | awk -F': ' '/Hash \(md5\)/ {print $2}' \
    | tr -d '[:space:]')
  echo "   remote_md5:         $remote_md5"

  if [[ "$local_md5_base64" != "$remote_md5" ]]; then
    echo "📤 Changed → $rel_path"
    gsutil cp "$file" "$gcs_path"
  else
    echo "✅ Unchanged → $rel_path"
  fi
done < <(find "$LOCAL_DIR" -type f \( "${EXT_ARGS[@]}" \) -print0)

# --- Delete Orphaned Remote Files ---
echo
echo "🗑️  Checking for orphaned remote files…"
gsutil ls -r "${BUCKET}/**" \
  | grep -Ei "\.($(IFS=\|; echo "${EXTENSIONS[*]}"))$" \
  | tr '\n' '\0' \
| while IFS= read -r -d '' remote_file; do
    rel_path="${remote_file#"$BUCKET/"}"
    if [[ ! -f "$LOCAL_DIR/$rel_path" ]]; then
      echo "   Deleting → $rel_path"
      gsutil rm "$remote_file"
    else
      echo "   Keeping  → $rel_path"
    fi
done

echo "✅ Sync complete."

# if needed remove all remote files
# gsutil ls -r gs://theperfectkitebar-cad-assets/** | grep -E '\.(stl|step|shapr)$' | xargs -I {} gsutil rm "{}"

