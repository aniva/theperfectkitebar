# Developer Automation & Git Hooks

This directory contains utility scripts and Git hooks that automate local CAD file management, keep documentation in sync with cloud storage, and clean up workspace metadata.

## The Big Picture: Why are hooks needed?

Since Git is not designed to track large binary CAD files (like high-res `.stl` models or parametric `.shapr` source files), we host these files on a Google Cloud Storage (GCS) bucket (`theperfectkitebar-cad-assets`).

To make collaboration smooth, we use Git hooks to:
1. **Sync Assets**: Fetch latest CAD files from GCS to your local `hardware/` directory.
2. **Synchronize Docs**: Keep download links, file hashes (MD5), and modification dates in README files automatically in sync with the files stored on GCS.
3. **Clean Metadata**: Strip hidden OS and cloud sync files (e.g. Windows `:Zone.Identifier` or Dropbox attributes) from the repository before commits.

---

## Installation

To set up the automated hooks on your local machine, run:

```bash
./scripts/hooks/install_hooks.sh
```

This script creates symbolic links in your local `.git/hooks/` directory to point to the active scripts in `scripts/hooks/`.

---

## Script Reference

### Hooks
* **`install_hooks.sh`**: Installs symlinks from `.git/hooks/` to the project's scripts.
* **`pre-commit.sh`** (runs automatically before each commit):
  * Cleans up OS/Dropbox metadata files (`:Zone.Identifier`, `:com.dropbox.attrs`) to prevent Git pollution.
  * Runs `update_shapr_tables.py` to auto-generate markdown download tables in component READMEs.
  * Automatically stages any modified READMEs.

### Python Utilities
* **`update_shapr_tables.py`**:
  * Scans local directories for `.shapr` source files.
  * Fetches file metadata (MD5 hashes, last-modified dates) from the GCS JSON API.
  * Dynamically updates markdown tables inside READMEs between `<!-- BEGIN_SHAPR_TABLE -->` and `<!-- END_SHAPR_TABLE -->` tags.
* **`sync_from_gcs.py`**:
  * Syncs public GCS assets locally into your `hardware/` directory.
  * Compares local MD5 hashes with GCS metadata to perform smart, delta-only updates.
  * Backs up overwritten files into timestamped local `backup/` folders so you never lose local edits.
