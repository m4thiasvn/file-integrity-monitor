# File Integrity Monitor

A small command-line tool that records SHA-256 hashes for files in a directory and checks later whether files have changed.

## Requirements

- Python 3
- No third-party packages

## Usage

Run commands from the project directory:

```bash
python3 src/monitor.py <command> <directory_path>
```

### Create a baseline

The `init` command scans the directory and saves its file hashes to `baseline.json` in the current working directory.

```bash
python3 src/monitor.py init test-files
```

Run `init` when you want to establish or replace the trusted reference state.

### Check for changes

The `check` command compares the current directory contents with the saved baseline. It reports new, deleted, and modified files. It does not update the baseline.

```bash
python3 src/monitor.py check test-files
```

`check` exits with status `0` when no changes are found and status `1` when changes are found or an error occurs.

## Ignored files

The scanner skips files named `.DS_Store` and `baseline.json` wherever they appear in the scanned directory.

If a file cannot be read because of a permission error, the scanner prints a warning and continues with the remaining files.

## How it works

Files are read in 64 KB blocks, and SHA-256 hashes are stored as a JSON mapping of file paths to hashes. The baseline is a reference for comparison; keep it unchanged between checks if you want to detect changes against the original state.
