import hashlib
import sys
import os

# File Integrity Monitor

PROJECT_NAME = "File Integrity Monitor"
VERSION = "1.0"
IS_ACTIVE = True


CHUNK_SIZE = 65536  # 64KB

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

# Main function
def main():
    print(f"{PROJECT_NAME} v{VERSION}")
    print(f"Active: {IS_ACTIVE}")
    print()

    if len(sys.argv) < 2:
        print("\nUsage: python3 src/monitor.py <directory_path>", file=sys.stderr)
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print(f"\nError '{directory_path}' is not valid.", file=sys.stderr)
        sys.exit(1)

    hashes = scan_directory(directory_path)
    for file_path, sha256_hash in hashes.items():
        print(f"\nHash of '{file_path}': {sha256_hash}")

if __name__ == "__main__":
    main()
