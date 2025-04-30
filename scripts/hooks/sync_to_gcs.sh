#!/bin/bash

# Configuration
LOCAL_DIR="$HOME/repos/theperfectkitebar/hardware"
BUCKET="gs://theperfectkitebar-cad-assets"
EXTENSIONS=("shapr" "stl" "step")

# Find all relevant files and sync them individually
find "$LOCAL_DIR" -type f \( $(printf -- '-name "*.%s" -o ' "${EXTENSIONS[@]}" | sed 's/ -o $//') \) | while read -r file; do
  # Get the relative path from LOCAL_DIR
  rel_path="${file#$LOCAL_DIR/}"
  gcs_path="$BUCKET/$rel_path"

  # Check if the object exists in GCS
  if ! gcloud storage objects describe "$gcs_path" > /dev/null 2>&1; then
    echo "Uploading new: $rel_path"
    gsutil cp "$file" "$gcs_path"
  else
    # Compare MD5 hashes if available
    local_md5=$(md5sum "$file" | awk '{print $1}')
    remote_md5=$(gsutil stat "$gcs_path" 2>/dev/null | awk -F': ' '/Hash \(md5\)/ {print $2}')
    if [[ "$local_md5" != "$remote_md5" ]]; then
      echo "Updating changed: $rel_path"
      gsutil cp "$file" "$gcs_path"
    else
      echo "Unchanged: $rel_path"
    fi
  fi
done

# Now remove remote files that no longer exist locally
remote_files=$(gsutil ls -r "$BUCKET/**" | grep -E "\.(${EXTENSIONS[*]// /|})$")

for remote_file in $remote_files; do
  # Reconstruct the corresponding local file path
  file_rel_path="${remote_file#"$BUCKET/"}"
  local_file="$LOCAL_DIR/$file_rel_path"
  if [[ ! -f "$local_file" ]]; then
    echo "Deleting orphaned remote file: $remote_file"
    gsutil rm "$remote_file"
  fi
done
