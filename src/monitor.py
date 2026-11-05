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


def run_check(directory_path):
    print("Not implemented yet")

def run_init(directory_path):
    print("Not implemented yet")


# Main function
def main():
    print(f"{PROJECT_NAME} v{VERSION}")
    print(f"Active: {IS_ACTIVE}")
    print()

    command = sys.argv[1]   

    if len(sys.argv) < 3:
        print("\nUsage: python3 src/monitor.py <command> <directory_path>", file=sys.stderr)
        print(f"\n Commands: 'init' or 'check' ")
        sys.exit(1)
   
    directory_path = sys.argv[2]
        
    if not os.path.isdir(directory_path):
        print(f"\ERROR '{directory_path}' is not known path.",file=sys.stderr)
        sys.exit(1)

    if command == "init":
        run_init(directory_path)
    elif command == "check":
        run_check(directory_path)
    else:
        print("\nUsage: python3 src/monitor.py <command> <directory_path>", file=sys.stderr)
        print(f"ERROR: unknown command '{command}'. Use 'init' or 'check' ", file=sys.stderr)
        sys.exit(1)
        

if __name__ == "__main__":
    main()
