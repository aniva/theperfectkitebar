# Development Setup

## Installing Git Hooks

This project uses git hooks to automate certain tasks. To install the hooks, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/theperfectkitebar.git
   cd theperfectkitebar
   ```

2. Run the hook installation script:
   ```
   ./scripts/hooks/install_hooks.sh
   ```

This will set up the following hooks:
- `pre-commit`: Cleans up filesystem metadata files and updates `.shapr` download tables in READMEs.
- `pre-push`: Syncs local CAD assets (`.shapr` files) to Google Cloud Storage.
- `post-merge`: Syncs CAD assets from Google Cloud Storage after a pull or merge.

Make sure you have the necessary dependencies installed (e.g., Python 3) for the hooks to function properly.

## Available Scripts

This project contains several scripts to automate development tasks. The primary scripts are located in the `scripts/hooks/` directory.

### Hook Scripts
- **`install_hooks.sh`**: Sets up symbolic links in your `.git/hooks` directory to enable the automated hooks below. This is the only script you need to run manually.
- **`pre-commit.sh`**: (Runs automatically before each commit)
  - Cleans up temporary metadata files (`:Zone.Identifier`, `:com.dropbox.attrs`).
  - Runs `update_shapr_tables.py` to keep README download tables current.
  - Automatically stages the updated README files.
- **`pre-push.sh`**: (Runs automatically before you push) Uploads local CAD files (e.g., `.shapr`) from the `hardware/` directory to the Google Cloud Storage bucket using `gsutil rsync`.
- **`post-merge.sh`**: (Runs automatically after a pull or merge) Downloads the latest CAD files from GCS to your local `hardware/` directory, ensuring your workspace is up to date.

### Utility Scripts
- **`update_shapr_tables.py`**: A Python script that scans for `.shapr` files, fetches their metadata from GCS, and updates the download tables within any `README.md` file that contains the special markers.
- **`sync_from_gcs.py`**: A Python script that intelligently downloads files from GCS, using MD5 hashes to avoid re-downloading up-to-date files. This is called by the `post-merge` hook.
- **`util/check_step_headers.sh`**: A shell script to validate that `.step` files have the correct `ISO-10303-21` header, ensuring they are not corrupted.
