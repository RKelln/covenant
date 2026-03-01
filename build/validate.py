import os
import re
import yaml
import json
import sys
from jsonschema import validate as validate_json
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).parent.parent
SECTIONS_DIR = REPO_ROOT / "sections"
ASSEMBLIES_DIR = REPO_ROOT / "assemblies"
SCHEMAS_DIR = REPO_ROOT / "schemas"
GLOSSARY_FILE = REPO_ROOT / "docs" / "glossary.md"
ALIASES_FILE = REPO_ROOT / "aliases.yml"

SECTION_SCHEMA_PATH = SCHEMAS_DIR / "section.schema.json"
ASSEMBLY_SCHEMA_PATH = SCHEMAS_DIR / "assembly.schema.json"

# Exit flags
errors_found = False


def log_error(file, msg):
    global errors_found
    errors_found = True
    print(f"=== ERROR ===\n[{file}] {msg}\n")


def log_warning(file, msg):
    print(f"=== WARNING ===\n[{file}] {msg}\n")


def load_yaml(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Handle frontmatter vs full yaml
            content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    return yaml.safe_load(parts[1]), parts[2]
            return yaml.safe_load(content), content
    except Exception as e:
        log_error(file_path, f"Failed to parse YAML: {e}")
        return None, None


def validate_section(file_path, section_schema, all_ids, all_aliases):
    rel_path = file_path.relative_to(REPO_ROOT)
    data, body = load_yaml(file_path)
    if data is None:
        return

    # Schema
    try:
        validate_json(instance=data, schema=section_schema)
    except Exception as e:
        log_error(rel_path, f"Schema validation failed: {e.message}")

    # Unique ID
    sec_id = data.get("id")
    if sec_id in all_ids:
        log_error(rel_path, f"Duplicate ID: {sec_id}")
    if sec_id in all_aliases:
        log_error(rel_path, f"ID collides with alias: {sec_id}")
    all_ids.add(sec_id)

    # Required headings
    required_headings = ["# Ritual", "# Spec", "# Digest", "# Log"]
    for h in required_headings:
        if h not in body:
            log_error(rel_path, f"Missing required heading: {h}")

    # Track data for later checks
    return data, body


def check_glossary(terms, glossary_content, rel_path):
    if not terms:
        return
    for term in terms:
        # Check for "### term" or "### <term>" or similar
        pattern = rf"^###\s+{re.escape(term)}\b"
        if not re.search(pattern, glossary_content, re.MULTILINE):
            log_warning(
                rel_path, f"Term '{term}' in terms_introduced not found in glossary.md"
            )


def check_cross_refs(body, all_ids, all_aliases, rel_path):
    refs = re.findall(r"§\[([a-z0-9.-]+)\]", body)
    for ref in refs:
        if ref not in all_ids:
            if ref in all_aliases:
                log_warning(rel_path, f"Reference via alias: §[{ref}]")
            else:
                log_error(rel_path, f"Unknown reference: §[{ref}]")


RITUAL_MAX_LINE_CHARS = 70
RITUAL_MAX_LINES = 32


def check_ritual_layout(body, rel_path):
    """Warn if ritual text exceeds line-length or line-count limits."""
    # Extract text between "# Ritual" and the next "# " heading
    match = re.search(r"^# Ritual\s*\n(.*?)(?=^# |\Z)", body, re.MULTILINE | re.DOTALL)
    if not match:
        return
    ritual_text = match.group(1).strip()

    # Only count non-blank lines for both checks
    lines = [ln for ln in ritual_text.splitlines() if ln.strip()]

    long_lines = [
        (i + 1, ln)
        for i, ln in enumerate(lines)
        if len(ln.rstrip()) > RITUAL_MAX_LINE_CHARS
    ]
    for lineno, ln in long_lines:
        log_warning(
            rel_path,
            f"Ritual line {lineno} exceeds {RITUAL_MAX_LINE_CHARS} chars "
            f"({len(ln.rstrip())} chars): {ln.rstrip()[:80]!r}",
        )

    if len(lines) > RITUAL_MAX_LINES:
        log_warning(
            rel_path,
            f"Ritual has {len(lines)} non-blank lines (max {RITUAL_MAX_LINES})",
        )


def check_spec_format(body, rel_path):
    """Verify that Spec list items follow the '1. **Title**' pattern."""
    # Extract text between "# Spec" and the next "# " heading
    match = re.search(r"^# Spec\s*\n(.*?)(?=^# |\Z)", body, re.MULTILINE | re.DOTALL)
    if not match:
        return
    spec_text = match.group(1).strip()

    # regex for numbered list items: digit dot space
    # we want to find if any list item DOES NOT start with **Title**
    items = re.split(r"^\s*\d+\.\s+", spec_text, flags=re.MULTILINE)
    # The first split part is text before the first list item, ignore it
    for item in items[1:]:
        item = item.strip()
        if not item:
            continue
        # Check if the first line starts with ** and ends with **
        first_line = item.splitlines()[0].strip()
        if not (first_line.startswith("**") and first_line.endswith("**")):
            log_error(
                rel_path, f"Spec list item missing bold title: {first_line[:40]}..."
            )

        # Check for newline after the title (the item should have at least two lines if it has text)
        lines = [l for l in item.splitlines() if l.strip()]
        if len(lines) < 2:
            log_warning(
                rel_path, f"Spec list item '{first_line}' appears to have no body text."
            )


def main():
    global errors_found
    all_ids = set()
    all_aliases = {}
    if ALIASES_FILE.exists():
        with open(ALIASES_FILE, "r") as f:
            all_aliases = yaml.safe_load(f) or {}

    # Load schemas
    with open(SECTION_SCHEMA_PATH, "r") as f:
        section_schema = json.load(f)
    with open(ASSEMBLY_SCHEMA_PATH, "r") as f:
        assembly_schema = json.load(f)

    # Load glossary
    glossary_content = ""
    if GLOSSARY_FILE.exists():
        with open(GLOSSARY_FILE, "r") as f:
            glossary_content = f.read()

    # Scan sections
    sections_data = []
    for section_file in SECTIONS_DIR.rglob("*.md"):
        res = validate_section(section_file, section_schema, all_ids, all_aliases)
        if res:
            sections_data.append((section_file.relative_to(REPO_ROOT), res[0], res[1]))

    # Cross-checks
    for rel_path, data, body in sections_data:
        check_glossary(data.get("terms_introduced"), glossary_content, rel_path)
        check_cross_refs(body, all_ids, all_aliases, rel_path)
        check_ritual_layout(body, rel_path)
        check_spec_format(body, rel_path)

        # Check dependencies
        for dep in data.get("depends_on", []):
            if dep not in all_ids and dep not in all_aliases:
                log_error(rel_path, f"Unknown dependency: {dep}")

        # Placeholder check
        if "[Placeholder — to be written]" in body:
            log_warning(rel_path, "Contains placeholder text")

    # Assembly checks
    included_sections = set()
    for assembly_file in ASSEMBLIES_DIR.glob("*.yml"):
        data, _ = load_yaml(assembly_file)
        if not data:
            continue
        rel_path = assembly_file.relative_to(REPO_ROOT)
        try:
            validate_json(instance=data, schema=assembly_schema)
        except Exception as e:
            log_error(rel_path, f"Schema validation failed: {e.message}")

        for sec_path in data.get("sections", []):
            full_path = REPO_ROOT / sec_path
            if not full_path.exists():
                log_error(
                    rel_path, f"Referenced section file does not exist: {sec_path}"
                )
            else:
                included_sections.add(sec_path)

    # Orphan check
    for rel_path, data, body in sections_data:
        if (
            str(rel_path) not in included_sections
            and data.get("status") != "deprecated"
        ):
            log_warning(rel_path, "Section not included in any assembly")

    print(f"=== SUMMARY ===")
    print(f"{len(sections_data)} sections checked")
    if errors_found:
        print("Validation FAILED")
        sys.exit(1)
    else:
        print("Validation PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
