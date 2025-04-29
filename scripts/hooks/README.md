# Git Hooks for Managing Large `.shapr` Files

This folder contains custom Git hook scripts and tools that help you push `.shapr` files larger than 100MB to GitHub in a safe and compatible way.

## ⚠️ Why This Exists

GitHub has a **hard file size limit of 100MB per file** — any attempt to push larger files will fail. To work around this limitation, this system:

1. Automatically **splits `.shapr` files ≥ 100MB** into `.part*` chunks smaller than 100MB
2. Commits those parts to the repo (Git LFS managed)
3. Reconstructs the full `.shapr` file after clone or pull
4. Cleans up the chunk files locally to reduce clutter

This solution is designed for **Linux or WSL** environments only.

---

## 📦 Git LFS Setup

Make sure Git LFS is installed and initialized (one-time setup per machine):

### ✅ Linux / WSL (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install git-lfs
git lfs install
```

### ✅ macOS (Homebrew)
```bash
brew install git-lfs
git lfs install
```

### ✅ Windows (Git Bash)
- Download from: https://git-lfs.github.com/
- Install and then run:
```bash
git lfs install
```

---

## 🧾 `.gitattributes` Reference (already included in the repo)

The `.gitattributes` file includes:

```gitattributes
*.step filter=lfs diff=lfs merge=lfs -text
*.stl filter=lfs diff=lfs merge=lfs -text
*.3mf filter=lfs diff=lfs merge=lfs -text
*.shapr filter=lfs diff=lfs merge=lfs -text
*.shapr.part* filter=lfs diff=lfs merge=lfs -text
```

These rules ensure all `.shapr` files and their split parts are tracked with Git LFS.

---

## 🛠 What Each Script Does

### `pre-commit`
- Detects staged `.shapr` files
- If file size ≥ 100MB:
  - Adds it to `.gitignore`
  - Splits into `.part*` files
  - Stages the `.part*` files instead
- Removes `Zone.Identifier` metadata files

### `post-commit`
- Deletes `.shapr.part*` files locally after commit to avoid clutter

### `restore-shapr.sh`
- Reassembles `.shapr` files from parts
- Overwrites only if the `.part*` files are newer
- Deletes the parts after successful restore

### `setup-hooks.sh`
- Installs all required Git hooks into `.git/hooks/`
- Ensures auto-restore will work on future checkouts and merges

---

## 🐧 Linux/WSL Only

This system uses Linux tools like `split`, `cat`, `find`, and `stat`. It will not function in native Windows CMD or PowerShell — use WSL, Git Bash, or a Linux environment.

---

## 🔁 After Cloning the Repository (First-Time Setup)

If you've just cloned the repo on a new machine:

```bash
# Step 1: Install Git LFS (if not already done)
git lfs install

# Step 2: Clone the repository
git clone https://github.com/aniva/theperfectkitebar.git
cd theperfectkitebar

# Step 3: Restore .shapr files from parts (if any exist)
bash scripts/hooks/restore-shapr.sh

# Step 4: Install Git hook scripts
bash scripts/hooks/setup-hooks.sh
```

---

## ✅ Quick Summary

- GitHub blocks files > 100MB
- This system splits large `.shapr` files automatically
- Git LFS handles all storage
- Hooks make it seamless for you and your collaborators

You're now ready to work with `.shapr` files of any size.
