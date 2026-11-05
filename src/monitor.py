import hashlib
import sys

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

# Main function
def main():
    print(f"{PROJECT_NAME} v{VERSION}")
    print(f"Active: {IS_ACTIVE}")
    print()

    if len(sys.argv) < 2:
        print("\nUsage: python3 src/monitor.py <file_path>", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        hash_value = calculate_sha256(file_path)
        print(f"\nSHA-256 Hash of '{file_path}': {hash_value}")
    except FileNotFoundError:
        print(f"\nError: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
