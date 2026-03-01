"""
Shared helpers for reading and parsing Covenant section bundles.

Used by compose.py, pdf.py, and website.py to avoid duplication of
the section-parsing and title-map logic.
"""

import re
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
SECTIONS_DIR = REPO_ROOT / "sections"
ASSEMBLIES_DIR = REPO_ROOT / "assemblies"

# ---------------------------------------------------------------------------
# Section parsing
# ---------------------------------------------------------------------------

SECTION_HEADINGS = ["# Ritual", "# Spec", "# Digest", "# Log"]


def extract_body_parts(body: str) -> dict:
    """Split a section body into its register parts (Ritual, Spec, Digest, Log)."""
    positions = []
    for h in SECTION_HEADINGS:
        pos = body.find(h)
        if pos != -1:
            positions.append((pos, h))
    positions.sort()

    parts = {}
    for i, (pos, h) in enumerate(positions):
        start = pos + len(h)
        end = positions[i + 1][0] if i + 1 < len(positions) else len(body)
        parts[h.replace("# ", "")] = body[start:end].strip()
    return parts


def load_section(path: Path):
    """Load a section file, returning (frontmatter_dict, body_parts) or None."""
    content = path.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    data = yaml.safe_load(parts[1])
    body_parts = extract_body_parts(parts[2])
    return data, body_parts


# ---------------------------------------------------------------------------
# Inline markdown
# ---------------------------------------------------------------------------


def inline_md(text: str) -> str:
    """Convert bold, italic, and code markdown to HTML inline elements."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def html_escape(text: str) -> str:
    """Escape &, <, > for safe HTML embedding."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# Title map
# ---------------------------------------------------------------------------

# Module-level title map (populated lazily)
_TITLE_MAP = None


def build_section_title_map() -> dict:
    """Build a mapping from section ID to display title by scanning all sections."""
    title_map = {}
    for md_file in SECTIONS_DIR.rglob("*.md"):
        result = load_section(md_file)
        if result is None:
            continue
        data, _ = result
        sec_id = data.get("id", "")
        title = data.get("title", "")
        if sec_id and title:
            title_map[sec_id] = title
    return title_map


def get_title_map() -> dict:
    """Return the cached section-ID-to-title mapping (built on first call)."""
    global _TITLE_MAP
    if _TITLE_MAP is None:
        _TITLE_MAP = build_section_title_map()
    return _TITLE_MAP


def resolve_title(sec_id: str) -> str:
    """Resolve a section ID to its display title, with titlecase fallback."""
    title_map = get_title_map()
    return title_map.get(sec_id, sec_id.replace(".", " ").replace("-", " ").title())
