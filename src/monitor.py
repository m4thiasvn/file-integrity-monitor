import hashlib
import sys
import os
import json

# File Integrity Monitor

PROJECT_NAME = "File Integrity Monitor"
VERSION = "1.0"
IS_ACTIVE = True


CHUNK_SIZE = 65536  # 64KB
BASELINE_FILE = "baseline.json"

# Calculate the SHA-256 hash of a file.
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 65K
        for byte_block in iter(lambda: f.read(CHUNK_SIZE), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Scan a directory and return a dictionary of file paths and their corresponding SHA-256 hashes.
def scan_directory(directory_path):
    hashes = {}
    for root, dirs, files in os.walk(directory_path):
        for name in files:
            full_path = os.path.join(root, name)
            hashes[full_path] = calculate_sha256(full_path)
    return hashes

# Save the hashes in a json file
def save_baseline(hashes):
    with open(BASELINE_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

# Load and reads the BASELINE_FILE
def load_baseline(baseline_path):    
    with open(baseline_path, "r") as f:
        return json.load(f)  

# Runs the scan_directory and the save_baseline by the command init
def run_init(directory_path):
    hashes = scan_directory(directory_path)
    save_baseline(hashes)
    print(f"\nFiles saved ",len(hashes))

# Runs the scan_directory and load_baseline by the command check
def run_check(directory_path):
    try:
        baseline_hashes = load_baseline(BASELINE_FILE)
    except FileNotFoundError:
        print(f"ERROR: '{BASELINE_FILE}' not found. Run 'init' first.", file=sys.stderr) 
        sys.exit(1)

    current_hashes = scan_directory(directory_path)

    baseline_files = set (baseline_hashes.keys())
    current_files = set (current_hashes.keys())
    new_files = current_files - baseline_files
    deleted_files = baseline_files - current_files
    modified_files = {
        path for path in baseline_files & current_files
        if baseline_hashes[path] != current_hashes[path]
    }

    if not new_files and not deleted_files and not modified_files:
        print("No changes detected")
    else:
        if new_files:
            print("\nNew files:")
            for path in sorted(new_files):
                print(f"  {path}")
        
        if deleted_files:
            print("\nDeleted files:")
            for path in sorted(deleted_files):
                print(f"  {path}")
        if modified_files:
            print("\nModified files:")
            for path in sorted(modified_files):
                print(f"  {path}")

    if new_files or deleted_files or modified_files:
        sys.exit(1)
        
    
# Main function
def main():
    print(f"{PROJECT_NAME} v{VERSION}")
    print(f"Active: {IS_ACTIVE}\n")

    if len(sys.argv) < 3:
        print("\nUsage: python3 src/monitor.py <command> <directory_path>", file=sys.stderr)
        print("\nCommands: 'init' or 'check' ")
        sys.exit(1)

    command = sys.argv[1]   
    directory_path = sys.argv[2]
        
    if not os.path.isdir(directory_path):
       print(f"ERROR: '{directory_path}' is not a known path.", file=sys.stderr)
       sys.exit(1)

    if command == "init":
        run_init(directory_path)
    elif command == "check":
        run_check(directory_path)
    else:
        print(f"ERROR: unknown command '{command}'. Use 'init' or 'check' ", file=sys.stderr)
        sys.exit(1)
        

if __name__ == "__main__":
    main()
