#!/bin/bash

for partfile in $(find . -type f -name "*.shapr.part000"); do
  base="${partfile%.part000}"

  # If full .shapr already exists, check freshness
  if [ -f "$base" ]; then
    if [ "$base" -nt "$partfile" ]; then
      echo "$base is newer than parts — skipping"
      continue
    fi
  fi

  echo "Rebuilding $base from parts..."
  cat "$base".part* > "$base"
done

# Clean up parts
find . -type f -name "*.shapr.part*" -delete
echo "Cleaned up .shapr.part* after restore"
