#!/usr/bin/env python3
"""
extract_section_review.py — Print a review-section context brief to stdout.

Usage:
    uv run python3 build/extract_section_review.py <section_id> [round]

    section_id : e.g. obligations.corrigibility
    round      : e.g. round-03, or omit/pass 'auto' for the latest round

Outputs a single Markdown document containing:
  1. The current section file (full text)
  2. Each reviewer's assessment and proposed changes for that section,
     extracted from reviews/<round>/reviewer-*.md

If a reviewer file has no entry for the given section ID, that reviewer is
noted as having no feedback for this section.

Exit codes:
  0 — success
  1 — section file not found
  2 — no reviewer files found
  3 — section_id required
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
SECTIONS_DIR = REPO / "sections"
REVIEWS_DIR = REPO / "reviews"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def find_section_file(section_id: str) -> Path | None:
    """Find the .md file for a section ID by scanning sections/."""
    for candidate in SECTIONS_DIR.rglob("*.md"):
        text = candidate.read_text(encoding="utf-8")
        # Match 'id: section.id' in frontmatter
        if re.search(
            r"^id:\s*" + re.escape(section_id) + r"\s*$",
            text,
            re.MULTILINE,
        ):
            return candidate
    return None


def find_latest_round() -> Path | None:
    """Return the highest-numbered reviews/round-NN directory."""
    rounds = sorted(
        d
        for d in REVIEWS_DIR.iterdir()
        if d.is_dir() and re.match(r"round-\d+$", d.name)
    )
    return rounds[-1] if rounds else None


def load_reviewer_files(round_dir: Path) -> list[Path]:
    """Return combined reviewer-*.md files (no batch files)."""
    return sorted(
        f
        for f in round_dir.glob("reviewer-*.md")
        if not re.search(r"-batch-\w+\.md$", f.name)
    )


def extract_section_block(text: str, section_id: str) -> str | None:
    """
    Extract the full block for section_id from a reviewer file.

    Blocks are delimited by:
        ### §section.id: Title
    and end at the next '---' separator or the next '### §' heading.
    Returns the block text (including the heading line), or None if not found.
    """
    pattern = re.compile(
        r"^(### §" + re.escape(section_id) + r": .+$.*?)(?=^---\s*$|^### §|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        return None
    return m.group(1).strip()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print(
            "Usage: uv run python3 build/extract_section_review.py <section_id> [round]",
            file=sys.stderr,
        )
        sys.exit(3)

    section_id = args[0]
    round_arg = args[1] if len(args) > 1 else "auto"

    # Resolve round directory
    if round_arg in ("auto", ""):
        round_dir = find_latest_round()
        if round_dir is None:
            print("ERROR: no round directories found under reviews/", file=sys.stderr)
            sys.exit(2)
    else:
        round_dir = REVIEWS_DIR / round_arg
        if not round_dir.exists():
            print(f"ERROR: {round_dir} does not exist", file=sys.stderr)
            sys.exit(2)

    round_id = round_dir.name

    # Find section file
    section_path = find_section_file(section_id)
    if section_path is None:
        print(f"ERROR: no section file found for id '{section_id}'", file=sys.stderr)
        sys.exit(1)

    # Load reviewer files
    reviewer_files = load_reviewer_files(round_dir)
    if not reviewer_files:
        print(f"ERROR: no reviewer files found in {round_dir}", file=sys.stderr)
        sys.exit(2)

    # Build output
    lines: list[str] = []

    lines += [
        f"# Section review brief: §{section_id} ({round_id})",
        "",
        f"Section file: `{section_path.relative_to(REPO)}`",
        "",
        "---",
        "",
    ]

    # — Current section text ---
    lines += [
        "## Current section text",
        "",
        section_path.read_text(encoding="utf-8").strip(),
        "",
        "---",
        "",
    ]

    # — Per-reviewer feedback ---
    lines += [
        "## Reviewer feedback",
        "",
    ]

    for rf in reviewer_files:
        model_name = rf.stem  # e.g. reviewer-claude
        reviewer_text = rf.read_text(encoding="utf-8")
        block = extract_section_block(reviewer_text, section_id)

        lines.append(f"### {model_name}")
        lines.append("")

        if block:
            lines.append(block)
        else:
            lines.append(f"*No feedback for §{section_id} in this review file.*")

        lines += ["", "---", ""]

    print("\n".join(lines))


if __name__ == "__main__":
    main()
