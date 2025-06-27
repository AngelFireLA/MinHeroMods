# file_changes.py

import os
import hashlib
import csv
import shutil

# ─── Configuration ────────────────────────────────────────────────────────────
SOURCE_FOLDER   = "source"
MODIFIED_FOLDER = "modified"
CSV_FILE        = "file_changes.csv"

# ─── Helpers ───────────────────────────────────────────────────────────────────
def compute_hash(path):
    """Return SHA256 of the file at path."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_previous_hashes():
    """Read CSV_FILE if it exists, return dict filepath → hash."""
    if not os.path.exists(CSV_FILE):
        return {}
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["filepath"]: row["hash"] for row in reader}

def save_current_hashes(hmap):
    """Write out the current filepath→hash map to CSV_FILE."""
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filepath", "hash"])
        for path, h in sorted(hmap.items()):
            writer.writerow([path, h])

def clear_modified_folder():
    """Wipe and re-create the MODIFIED_FOLDER."""
    if os.path.exists(MODIFIED_FOLDER):
        shutil.rmtree(MODIFIED_FOLDER)
    os.makedirs(MODIFIED_FOLDER)

# ─── Main Logic ────────────────────────────────────────────────────────────────
def main():
    prev_hashes = load_previous_hashes()
    curr_hashes = {}
    modified = []

    # Walk the source tree, compute hashes
    for root, dirs, files in os.walk(SOURCE_FOLDER):
        for fn in files:
            src = os.path.join(root, fn)
            rel = os.path.relpath(src, SOURCE_FOLDER)
            h = compute_hash(src)
            curr_hashes[rel] = h
            # if new file or hash changed → mark it
            if prev_hashes.get(rel) != h:
                modified.append(rel)

    if modified:
        clear_modified_folder()
        for rel in modified:
            src = os.path.join(SOURCE_FOLDER, rel)
            dst = os.path.join(MODIFIED_FOLDER, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        print(f"Copied {len(modified)} modified files → '{MODIFIED_FOLDER}/'")
    else:
        print("No modified files found, nothing copied.")

    if prev_hashes == {}:
        # Overwrite CSV with current hashes
        save_current_hashes(curr_hashes)

if __name__ == "__main__":
    main()
