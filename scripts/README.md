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
- pre-commit: Cleans up Windows metadata, syncs files to GCS, and updates .shapr tables.

Make sure you have the necessary dependencies installed (e.g., Python 3) for the hooks to function properly.

## Available Scripts

- `hooks/install_hooks.sh`: Installs the git hooks for the project.
- `hooks/sync_to_gcs.sh`: Syncs selected files to Google Cloud Storage.
- `hooks/update_shapr_tables.py`: Updates .shapr download tables.

For more information on each script, please refer to the comments within the script files.
