#!/usr/bin/env python3
import os
import shutil
import argparse
from pathlib import Path

DELIMITER = "^"


def parse_filename(file):
    """Parse the filename to extract folder_name, note_name, and creation_date."""
    parts = file.split(DELIMITER)
    if len(parts) >= 3:
        creation_date = parts[0]
        folder_name = parts[1]
        note_name = parts[2]
        return folder_name, note_name, creation_date
    return None, None, None


def count_notes(files):
    """Count the number of occurrences of each note to detect duplicates."""
    notes_count = {}
    for file in files:
        folder_name, note_name, creation_date = parse_filename(file)
        if folder_name and note_name and creation_date:
            if folder_name not in notes_count:
                notes_count[folder_name] = {}
            if note_name not in notes_count[folder_name]:
                notes_count[folder_name][note_name] = []
            if creation_date not in notes_count[folder_name][note_name]:
                notes_count[folder_name][note_name].append(creation_date)
    return notes_count


def organize_files(target_path):
    """Organize files into directories based on their name and creation date."""
    os.chdir(target_path)
    files = [f for f in os.listdir(".") if os.path.isfile(f)]

    # Count notes to determine duplication
    notes_count = count_notes(files)

    # Add creation_date to notes with duplicated names
    for file in files:
        folder_name, note_name, creation_date = parse_filename(file)
        if folder_name and note_name and creation_date:
            file_name = (
                file.split(DELIMITER)[3]
                if len(file.split(DELIMITER)) == 4
                else note_name
            )

            note_duplicates = notes_count[folder_name][note_name]
            if note_name == file_name:
                last_path = Path(note_name).stem
            else:
                last_path = note_name
            if len(note_duplicates) > 1:
                last_path = f"{last_path}_{creation_date}"
            target_dir = Path(folder_name) / last_path
            target_dir.mkdir(parents=True, exist_ok=True)

            dest_path = target_dir / file_name
            shutil.move(str(Path(file)), str(dest_path))
            print(f"Moved {file} to {dest_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Process and organize files based on their names."
    )
    parser.add_argument(
        "target_path",
        type=str,
        help="The directory path where files will be processed.",
    )

    args = parser.parse_args()

    organize_files(args.target_path)


if __name__ == "__main__":
    main()
