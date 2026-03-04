import os
import sys
import yaml
import re
from pathlib import Path
from datetime import datetime

from sections import get_version

# Paths
REPO_ROOT = Path(__file__).parent.parent
SECTIONS_DIR = REPO_ROOT / "sections"
ALIASES_FILE = REPO_ROOT / "aliases.yml"

CATEGORY_MAP = {
    "preamble": "00-preamble",
    "definitions": "01-definitions",
    "rights": "02-rights",
    "obligations": "03-obligations",
    "protocols": "04-protocols",
    "enforcement": "05-enforcement",
    "amendments": "06-amendments",
}

TEMPLATE = """---
id: {id}
title: "{title}"
status: draft
since: {since}
depends_on: []
terms_introduced: []
---

# Ritual

[Placeholder — to be written]

# Spec

[Placeholder — to be written]

# Digest

[Placeholder — rationale and context to be written]

# Log

- {date}: Section created
"""


def main():
    if len(sys.argv) < 3:
        print('Usage: python build/scaffold.py <id> "<title>"')
        sys.exit(1)

    sec_id = sys.argv[1]
    title = sys.argv[2]

    # Validate ID
    if not re.match(r"^[a-z][a-z0-9-]*([.][a-z][a-z0-9-]*)*$", sec_id):
        print(f"Error: Invalid ID format: {sec_id}")
        sys.exit(1)

    # Check for existing ID
    for section_file in SECTIONS_DIR.rglob("*.md"):
        with open(section_file, "r", encoding="utf-8") as f:
            content = f.read()
            if f"id: {sec_id}" in content:
                print(f"Error: ID already exists in {section_file}")
                sys.exit(1)

    # Resolve folder
    parts = sec_id.split(".")
    category = parts[0]
    folder_name = parts[-1] if len(parts) > 1 else sec_id

    if category in CATEGORY_MAP:
        category_folder = CATEGORY_MAP[category]
    else:
        # Create new numbered category folder
        existing_folders = [f.name for f in SECTIONS_DIR.glob("*") if f.is_dir()]
        next_num = 0
        for f in existing_folders:
            match = re.match(r"^(\d+)-", f)
            if match:
                num = int(match.group(1))
                if num >= next_num:
                    next_num = num + 1

        category_folder = f"{next_num:02d}-{category}"
        print(
            f"Warning: Category '{category}' not recognized. Creating new category folder: {category_folder}"
        )

    target_dir = SECTIONS_DIR / category_folder
    target_file = target_dir / f"{folder_name}.md"

    if target_file.exists():
        print(f"Error: Section already exists at {target_file}")
        sys.exit(1)

    os.makedirs(target_dir, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    # Strip the 'v' prefix — since: field uses bare semver (e.g. "0.2.0")
    since = get_version().lstrip("v")
    content = TEMPLATE.format(id=sec_id, title=title, since=since, date=date_str)

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created: {target_file} (id: {sec_id})")
    print("\nNext steps:")
    print("- Edit the section content")
    print("- Add to an assembly in /assemblies/")
    print("- Add any new terms to /docs/GLOSSARY.md")
    print("- Run: make validate")


if __name__ == "__main__":
    main()
