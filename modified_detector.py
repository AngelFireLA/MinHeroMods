"""Detect files that differ from the original exported SWF source tree."""

import csv
import hashlib
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_FOLDER = ROOT / "source"
MODIFIED_FOLDER = ROOT / "modified"
CSV_FILE = ROOT / "file_changes.csv"


def compute_hash(path):
    """Return the SHA-256 hash of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_previous_hashes():
    """Load the immutable hashes captured from the original export."""
    if not CSV_FILE.exists():
        return {}
    with CSV_FILE.open(newline="", encoding="utf-8") as source:
        return {
            row["filepath"].replace("\\", "/"): row["hash"]
            for row in csv.DictReader(source)
        }


def save_current_hashes(hash_map):
    """Initialize the original-export baseline."""
    with CSV_FILE.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.writer(destination)
        writer.writerow(["filepath", "hash"])
        for path, file_hash in sorted(hash_map.items()):
            writer.writerow([path, file_hash])


def reset_modified_folder():
    """Ensure stale files from an earlier build cannot be imported."""
    if MODIFIED_FOLDER.exists():
        shutil.rmtree(MODIFIED_FOLDER)
    MODIFIED_FOLDER.mkdir(parents=True)


def scan_current_hashes():
    """Hash every file in the exported source tree using portable paths."""
    hashes = {}
    for root, _, files in os.walk(SOURCE_FOLDER):
        for filename in files:
            source_path = Path(root, filename)
            relative_path = source_path.relative_to(SOURCE_FOLDER).as_posix()
            hashes[relative_path] = compute_hash(source_path)
    return hashes


def main():
    previous_hashes = load_previous_hashes()
    current_hashes = scan_current_hashes()
    reset_modified_folder()

    if not previous_hashes:
        save_current_hashes(current_hashes)
        print(f"Initialized original-source hashes in '{CSV_FILE}'.")
        return []

    changes = []
    for relative_path, current_hash in sorted(current_hashes.items()):
        previous_hash = previous_hashes.get(relative_path)
        if previous_hash == current_hash:
            continue

        status = "new" if previous_hash is None else "modified"
        source_path = SOURCE_FOLDER / Path(relative_path)
        destination_path = MODIFIED_FOLDER / Path(relative_path)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)
        changes.append({"path": relative_path, "status": status})

    if changes:
        new_count = sum(change["status"] == "new" for change in changes)
        modified_count = len(changes) - new_count
        print(
            f"Prepared {len(changes)} changed files in '{MODIFIED_FOLDER}/' "
            f"({new_count} new, {modified_count} modified)."
        )
    else:
        print("No source changes found.")
    return changes


if __name__ == "__main__":
    main()
