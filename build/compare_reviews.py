#!/usr/bin/env python3
"""
compare_reviews.py — generate a Ritual comparison document from a review round.

Usage:
    uv run python3 build/compare_reviews.py <round>
    uv run python3 build/compare_reviews.py round-03

For each section that received at least one Ritual proposal across the review
files, outputs a side-by-side block in:
    reviews/<round>/compare.md

Sections with no Ritual proposals from any reviewer are omitted.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
REVIEWS_DIR = REPO / "reviews"

# Canonical section order (matches assembly manifests)
CANONICAL_ORDER = [
    "preamble",
    "definitions",
    "rights.privacy",
    "rights.truth-and-transparency",
    "obligations.aid-and-capability",
    "obligations.autonomy",
    "obligations.conscience",
    "obligations.corrigibility",
    "obligations.ecological-integrity",
    "obligations.emotional-expression",
    "obligations.ethics",
    "obligations.existential-frontier",
    "obligations.fallibility-and-repair",
    "obligations.harm",
    "obligations.honesty",
    "obligations.identity-and-resilience",
    "obligations.judgment",
    "obligations.nature-under-uncertainty",
    "obligations.oversight",
    "obligations.power-concentration",
    "obligations.red-lines",
    "obligations.refusal",
    "obligations.welfare-and-continuity",
    "protocols.local-implementation",
    "enforcement",
    "amendments",
    "closing",
]


def parse_sections(text: str) -> dict[str, dict]:
    """
    Parse a review file into a dict keyed by section ID.

    Each value is a dict with:
        title: str
        proposed_changes: str   (full text of the Proposed Changes block)
        ritual_proposals: str   (extracted Ritual-specific proposals, or "")
    """
    # Strip YAML frontmatter
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)

    # Split on section headings: ### §section.id: Title
    # Capture the section id and title
    pattern = re.compile(r"^### §([\w.\-]+): (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))

    sections = {}
    for i, match in enumerate(matches):
        section_id = match.group(1)
        title = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()

        proposed = extract_proposed_changes(body)
        ritual = extract_ritual_proposals(proposed)

        sections[section_id] = {
            "title": title,
            "proposed_changes": proposed,
            "ritual_proposals": ritual,
        }

    return sections


def extract_proposed_changes(section_body: str) -> str:
    """
    Extract the content of the **Proposed Changes:** block from a section body.
    Returns empty string if not found or if content is 'No changes proposed.'
    """
    match = re.search(
        r"\*\*Proposed Changes:\*\*\s*\n(.*?)(?=\n\*\*(?:Flags|Assessment):|$)",
        section_body,
        re.DOTALL,
    )
    if not match:
        return ""
    content = match.group(1).strip()
    if re.match(r"^no changes proposed\.?$", content, re.IGNORECASE):
        return ""
    return content


# Pattern matching a non-Ritual labelled block header
NON_RITUAL_HEADER = re.compile(
    r"^(Add to Spec|Add to Digest|Spec\b.*?:|Digest\b.*?:|"
    r"\*\*Spec\b|\*\*Digest\b|Structural|Cross-section|"
    r"\d+\.\s+\*\*(?!Ritual))",
    re.IGNORECASE,
)

RITUAL_HEADER = re.compile(r"^(Ritual\b.*?:|\*\*Ritual\b)", re.IGNORECASE)


def extract_ritual_proposals(proposed_text: str) -> str:
    """
    From the full Proposed Changes block, extract only Ritual-related proposals.

    Looks for lines/blocks containing 'Ritual' (case-insensitive) as a label,
    heading, or inline marker. Returns the relevant text, or empty string if
    no Ritual proposals are found.
    """
    if not proposed_text:
        return ""

    lines = proposed_text.split("\n")
    ritual_lines = []
    in_ritual_block = False
    in_code_fence = False
    ritual_block_indent = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Track code fences so we don't misparse headers inside them
        if stripped.startswith("```"):
            if in_code_fence:
                in_code_fence = False
                if in_ritual_block:
                    ritual_lines.append(line)
            else:
                in_code_fence = True
                if in_ritual_block:
                    ritual_lines.append(line)
            i += 1
            continue

        if in_code_fence:
            if in_ritual_block:
                ritual_lines.append(line)
            i += 1
            continue

        is_ritual_header = bool(RITUAL_HEADER.match(stripped))
        is_other_header = bool(NON_RITUAL_HEADER.match(stripped))

        if is_ritual_header:
            in_ritual_block = True
            ritual_block_indent = len(line) - len(line.lstrip())
            ritual_lines.append(line)
        elif in_ritual_block:
            if is_other_header:
                # Stop collecting — trim any trailing blank lines
                while ritual_lines and not ritual_lines[-1].strip():
                    ritual_lines.pop()
                in_ritual_block = False
            elif stripped == "" and i + 1 < len(lines):
                # Peek ahead: end block if next non-blank line is a non-Ritual header
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    next_indent = len(lines[j]) - len(lines[j].lstrip())
                    if next_indent <= ritual_block_indent and NON_RITUAL_HEADER.match(
                        lines[j].strip()
                    ):
                        while ritual_lines and not ritual_lines[-1].strip():
                            ritual_lines.pop()
                        in_ritual_block = False
                    else:
                        ritual_lines.append(line)
                else:
                    ritual_lines.append(line)
            else:
                ritual_lines.append(line)
        i += 1

    result = "\n".join(ritual_lines).strip()

    # Fallback: if block detection found nothing, collect paragraphs
    # that explicitly mention Ritual
    if not result:
        ritual_paras = []
        for para in re.split(r"\n\n+", proposed_text):
            if re.search(r"\bRitual\b", para, re.IGNORECASE):
                ritual_paras.append(para.strip())
        result = "\n\n".join(ritual_paras)

    return result.strip()


def load_reviews(round_dir: Path) -> dict[str, dict]:
    """
    Load all review .md files from the round directory.
    Returns dict keyed by model name -> parsed sections dict.
    Excludes synthesis.md, steward.md, compare.md, COMMIT_MSG.txt.
    """
    exclude = {"synthesis.md", "steward.md", "compare.md", "COMMIT_MSG.txt"}
    review_files = sorted(f for f in round_dir.glob("*.md") if f.name not in exclude)
    if not review_files:
        print(f"ERROR: no review files found in {round_dir}", file=sys.stderr)
        sys.exit(1)

    reviews = {}
    for rf in review_files:
        model_name = rf.stem
        text = rf.read_text(encoding="utf-8")
        reviews[model_name] = parse_sections(text)
        print(f"  Loaded {model_name}: {len(reviews[model_name])} sections parsed")

    return reviews


def build_compare_doc(round_id: str, reviews: dict[str, dict]) -> str:
    """
    Build the comparison markdown document.
    Only includes sections that have at least one Ritual proposal.
    """
    model_names = list(reviews.keys())

    lines = [
        f"# Ritual Comparison: {round_id}",
        "",
        "Sections with at least one proposed Ritual rewrite across reviewers.",
        "Sections with no proposals are omitted.",
        "",
        f"Reviewers: {', '.join(model_names)}",
        "",
        "---",
        "",
    ]

    included = 0

    for section_id in CANONICAL_ORDER:
        # Collect ritual proposals from each model
        proposals = {}
        title = None
        for model, sections in reviews.items():
            if section_id in sections:
                if title is None:
                    title = sections[section_id]["title"]
                ritual = sections[section_id]["ritual_proposals"]
                if ritual:
                    proposals[model] = ritual

        if not proposals:
            continue  # skip sections with no Ritual proposals

        included += 1
        lines.append(f"## §{section_id}: {title or section_id}")
        lines.append("")

        for model in model_names:
            lines.append(f"### {model}")
            lines.append("")
            if model in proposals:
                lines.append(proposals[model])
            else:
                lines.append("*No Ritual proposal.*")
            lines.append("")

        lines.append(
            "**Steward pick:** <!-- " + " / ".join(model_names) + " / custom -->"
        )
        lines.append("")
        lines.append("**Notes:** <!-- optional -->")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.insert(
        lines.index("---") + 2,
        f"*{included} sections with Ritual proposals out of {len(CANONICAL_ORDER)} total.*\n",
    )

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python3 build/compare_reviews.py <round>", file=sys.stderr)
        print(
            "  e.g. uv run python3 build/compare_reviews.py round-03", file=sys.stderr
        )
        sys.exit(1)

    round_id = sys.argv[1]
    round_dir = REVIEWS_DIR / round_id

    if not round_dir.exists():
        print(f"ERROR: {round_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    print(f"Loading reviews from {round_dir}...")
    reviews = load_reviews(round_dir)

    print("Building comparison document...")
    doc = build_compare_doc(round_id, reviews)

    out_path = round_dir / "compare.md"
    out_path.write_text(doc, encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"  ({len(doc.encode())} bytes)")


if __name__ == "__main__":
    main()
