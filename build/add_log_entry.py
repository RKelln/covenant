#!/usr/bin/env python3
"""
Add a log entry to every section file.

Usage:
    python build/add_log_entry.py "Description of change"
    python build/add_log_entry.py --date 2026-03-10 "Description of change"

Appends a dated log entry as the first item after the `# Log` heading
in each section file under sections/.
"""

import argparse
import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SECTIONS_DIR = REPO_ROOT / "sections"


def add_log_entry(filepath: Path, entry: str) -> bool:
    """Insert a log entry after the # Log heading. Returns True if modified."""
    text = filepath.read_text(encoding="utf-8")

    # Find the # Log heading and insert the new entry as the first bullet
    pattern = r"(# Log\n)\n"
    replacement = rf"\1\n- {entry}\n"

    new_text, count = re.subn(pattern, replacement, text, count=1)
    if count == 0:
        print(f"  WARNING: no '# Log' heading found in {filepath.name}")
        return False

    filepath.write_text(new_text, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Add a log entry to all section files."
    )
    parser.add_argument(
        "message",
        help="Log entry description (without date prefix)",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Date for the entry in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without writing files",
    )
    args = parser.parse_args()

    entry = f"{args.date}: {args.message}"
    section_files = sorted(SECTIONS_DIR.rglob("*.md"))

    if not section_files:
        print("No section files found.")
        return

    print(f"Adding log entry to {len(section_files)} sections:")
    print(f"  - {entry}")
    if args.dry_run:
        print("  (dry run — no files modified)")
    print()

    modified = 0
    for filepath in section_files:
        if args.dry_run:
            print(f"  would update: {filepath.relative_to(REPO_ROOT)}")
            modified += 1
        else:
            if add_log_entry(filepath, entry):
                print(f"  updated: {filepath.relative_to(REPO_ROOT)}")
                modified += 1

    print(
        f"\n{modified}/{len(section_files)} sections {'would be ' if args.dry_run else ''}updated."
    )


if __name__ == "__main__":
    main()
