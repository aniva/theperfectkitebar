#!/usr/bin/env python3
"""Scan all README.md files for broken local links and images."""
import re
import os
from pathlib import Path

ROOT = Path('/home/me/repos/theperfectkitebar')
readmes = list(ROOT.rglob('*.md')) + list(ROOT.rglob('*.html'))
# Exclude .venv and .git
readmes = [r for r in readmes if '.venv' not in str(r) and '.git/' not in str(r)]
readmes.sort()

# Match: ![alt](path), [text](path), <img src="path">, <img src='path'>, href="path", src="path"
md_link_re = re.compile(
    r'(?:'
    r'!\[[^\]]*\]\(([^)\s]+)\)'    # group 1: image ![alt](path)
    r'|'
    r'\[[^\]]*\]\(([^)\s]+)\)'      # group 2: link [text](path)
    r'|'
    r'<img\s[^>]*src=["\']([^"\']+)["\']'  # group 3: <img src="path">
    r'|'
    r'\bhref=["\']([^"\']+)["\']'  # group 4: href="path"
    r'|'
    r'\bsrc=["\']([^"\']+)["\']'   # group 5: src="path"
    r')'
)

broken = []
valid = []

for readme in readmes:
    readme_dir = readme.parent
    text = readme.read_text(errors='replace')
    
    for line_num, line in enumerate(text.splitlines(), 1):
        for m in md_link_re.finditer(line):
            ref = m.group(1) or m.group(2) or m.group(3) or m.group(4) or m.group(5)
            if not ref:
                continue
            # Skip external URLs, anchors, mailto, etc.
            if ref.startswith(('http://', 'https://', '#', 'mailto:', 'data:')):
                continue
            
            # Resolve relative path from the file's directory
            # Strip query params or hash if any (e.g. rope_calculator.html#something)
            clean_ref = ref.split('#')[0].split('?')[0]
            if not clean_ref:
                continue
            target = (readme_dir / clean_ref).resolve()
            rel_readme = str(readme.relative_to(ROOT))
            
            if target.exists():
                valid.append((rel_readme, line_num, ref))
            else:
                broken.append((rel_readme, line_num, ref, str(target)))

print("=" * 80)
print(f"BROKEN LINKS ({len(broken)}):")
print("=" * 80)
for readme_path, line, ref, resolved in broken:
    print(f"  {readme_path}:{line}")
    print(f"    ref:      {ref}")
    print(f"    resolved: {resolved}")
    print()

print("=" * 80)
print(f"VALID LINKS ({len(valid)}):")
print("=" * 80)
for readme_path, line, ref in valid[:30]:
    print(f"  {readme_path}:{line}  ->  {ref}")
if len(valid) > 30:
    print(f"  ... and {len(valid) - 30} more valid links.")
