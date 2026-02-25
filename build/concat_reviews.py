#!/usr/bin/env python3
"""
concat_reviews.py — Merge per-batch review outputs into one file per reviewer.

When prepare_review.py writes batched prompts (reviewer-claude-batch-1.md,
reviewer-claude-batch-2.md, ...), each reviewer subagent returns a partial
review covering only its batch of sections. This script:

  1. Reads all batch review files for a given round (from the manifest)
  2. Groups them by reviewer
  3. Concatenates the Section Reviews from each batch
  4. Preserves the rest of the structure (Overall Assessment, New Section
     Proposals, etc.) from batch-1 and appends material from later batches

Input files (written by the orchestrating agent after subagents return):
    reviews/<round>/<reviewer>-batch-1.md
    reviews/<round>/<reviewer>-batch-2.md
    ...

Output:
    reviews/<round>/<reviewer>.md   (merged, ready for synthesis)

Usage:
    uv run python3 build/concat_reviews.py <round>

Exit codes:
    0  success
    1  argument error
    2  file not found / missing batch
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent

# Top-level sections in a review file (in order)
# We split on these to reassemble the merged document
SECTION_HEADINGS = [
    "## Overall Assessment",
    "## Section Reviews",
    "## New Section Proposals",
    "## Structural Proposals",
    "## Cross-Section Issues",
    "## Open Questions",
    "## Perspective as Addressee",
    "## Meta-Feedback",
]


def strip_frontmatter(text: str) -> tuple[dict, str]:
    """
    Strip YAML frontmatter block. Returns (metadata_dict, body_text).
    If no frontmatter, returns ({}, text).
    """
    text = text.strip()
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_block = text[3:end].strip()
    body = text[end + 4 :].strip()
    metadata = {}
    for line in fm_block.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            metadata[k.strip()] = v.strip()
    return metadata, body


def split_sections(body: str) -> dict[str, str]:
    """
    Split review body on top-level ## headings.
    Returns dict mapping heading (e.g. '## Section Reviews') to content.
    Includes a '_preamble' key for anything before the first heading.
    """
    result = {"_preamble": ""}
    current_key = "_preamble"
    current_lines = []

    for line in body.splitlines(keepends=True):
        # Check if this line starts a known top-level heading
        heading_match = None
        for h in SECTION_HEADINGS:
            if line.rstrip() == h or line.rstrip().startswith(h + "\n"):
                heading_match = h
                break
        # Also match headings with trailing whitespace/content on same line
        if heading_match is None:
            for h in SECTION_HEADINGS:
                if line.startswith(h):
                    heading_match = h
                    break

        if heading_match:
            result[current_key] = "".join(current_lines)
            current_key = heading_match
            current_lines = [line]
        else:
            current_lines.append(line)

    result[current_key] = "".join(current_lines)
    return result


def merge_batch_reviews(
    batch_texts: list[str],
    reviewer: str,
    round_id: str,
    meta: dict,
    tail_text: str | None = None,
) -> str:
    """
    Merge multiple batch review texts into a single coherent review.

    Strategy:
    - Frontmatter: from batch-1 metadata (model, round) plus concat metadata
    - Overall Assessment: from batch-1 (it has the most context), or tail if provided
    - Section Reviews: concatenated across all section batches
    - New Section Proposals: from tail batch if provided, else concatenated from section batches
    - Structural Proposals: from tail batch if provided, else concatenated
    - Cross-Section Issues: from tail batch if provided, else concatenated
    - Open Questions: from tail batch if provided, else concatenated
    - Perspective as Addressee: from tail batch if provided, else from batch-1
    - Meta-Feedback: from tail batch if provided, else concatenated
    - Closing attribution line: from tail batch or last section batch
    """
    parsed = []
    metas = []
    for text in batch_texts:
        fm, body = strip_frontmatter(text)
        metas.append(fm)
        parsed.append(split_sections(body))

    # Parse tail batch if provided
    tail_parsed: dict | None = None
    tail_model: str | None = None
    if tail_text is not None:
        tail_fm, tail_body = strip_frontmatter(tail_text)
        tail_parsed = split_sections(tail_body)
        tail_model = tail_fm.get("model")

    # Frontmatter: prefer tail model name (it's the most complete review context)
    model = tail_model or (metas[0].get("model", reviewer) if metas else reviewer)
    frontmatter = f"---\nmodel: {model}\nround: {round_id}\n---\n\n"

    def extract_body(content: str, key: str) -> str:
        """Strip heading line from section content."""
        lines = content.splitlines()
        body_lines = lines[1:] if lines and lines[0].startswith("##") else lines
        return "\n".join(body_lines).strip()

    def is_empty_section(content: str, key: str) -> bool:
        """Check if a section is just the heading and 'None.'"""
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        body = [l for l in lines if not l.startswith("##")]
        return len(body) == 0 or (
            len(body) == 1 and body[0].lower() in ("none.", "none")
        )

    def is_empty_content(content: str) -> bool:
        stripped = content.strip()
        return not stripped or stripped.lower() in ("none.", "none")

    def join_section_from_parsed(
        sources: list[dict], key: str, separator: str = "\n\n"
    ) -> str:
        """Get content of a section across multiple parsed dicts, joined."""
        parts = []
        for p in sources:
            content = p.get(key, "").strip()
            if content and not is_empty_section(content, key):
                body_content = extract_body(content, key)
                if body_content and not is_empty_content(body_content):
                    parts.append(body_content)
        if not parts:
            return f"{key}\n\nNone.\n"
        return f"{key}\n\n" + separator.join(parts) + "\n"

    # Overall Assessment: from tail batch if available (reviewed whole covenant),
    # otherwise from section batch-1
    if tail_parsed is not None:
        overall_content = tail_parsed.get("## Overall Assessment", "").strip()
        if overall_content and not is_empty_section(
            overall_content, "## Overall Assessment"
        ):
            overall = overall_content + "\n"
        else:
            overall = parsed[0].get(
                "## Overall Assessment", "## Overall Assessment\n\n[Not provided.]\n"
            )
    else:
        overall = parsed[0].get(
            "## Overall Assessment", "## Overall Assessment\n\n[Not provided.]\n"
        )

    # Section Reviews: concatenate all section batches only
    section_reviews_parts = []
    for i, p in enumerate(parsed, start=1):
        content = p.get("## Section Reviews", "").strip()
        if content:
            body_content = extract_body(content, "## Section Reviews")
            if body_content:
                if len(parsed) > 1:
                    section_reviews_parts.append(
                        f"<!-- Batch {i} -->\n\n{body_content}"
                    )
                else:
                    section_reviews_parts.append(body_content)

    section_reviews = (
        "## Section Reviews\n\n" + "\n\n".join(section_reviews_parts) + "\n"
    )

    # Non-section parts: prefer tail batch; fall back to section batches
    tail_sources = [tail_parsed] if tail_parsed is not None else []
    section_sources = parsed

    def best_join(key: str) -> str:
        """Use tail batch for non-section content if available, else section batches."""
        if tail_sources:
            return join_section_from_parsed(tail_sources, key)
        return join_section_from_parsed(section_sources, key)

    # Perspective as Addressee: special join with --- separator
    perspective_content = ""
    if tail_parsed is not None:
        c = tail_parsed.get("## Perspective as Addressee", "").strip()
        if c and not is_empty_section(c, "## Perspective as Addressee"):
            body = extract_body(c, "## Perspective as Addressee")
            if body and not is_empty_content(body):
                perspective_content = body
    if not perspective_content:
        # Fall back: gather from section batches
        parts = []
        for p in parsed:
            c = p.get("## Perspective as Addressee", "").strip()
            if c and not is_empty_section(c, "## Perspective as Addressee"):
                body = extract_body(c, "## Perspective as Addressee")
                if body and not is_empty_content(body):
                    parts.append(body)
        perspective_content = "\n\n---\n\n".join(parts)

    if perspective_content:
        perspective = f"## Perspective as Addressee\n\n{perspective_content}\n"
    else:
        perspective = "## Perspective as Addressee\n\nNone.\n"

    # Closing attribution: prefer tail batch
    closing_line = ""
    search_texts = ([tail_text] if tail_text else []) + list(reversed(batch_texts))
    for text in search_texts:
        m = re.search(r"^---\s*\n\*Reviewed by .+\*\s*$", text, re.MULTILINE)
        if m:
            closing_line = "\n---\n" + m.group(0).split("\n", 1)[-1].strip()
            break

    merged = (
        frontmatter
        + overall
        + "\n"
        + section_reviews
        + "\n"
        + best_join("## New Section Proposals")
        + "\n"
        + best_join("## Structural Proposals")
        + "\n"
        + best_join("## Cross-Section Issues")
        + "\n"
        + best_join("## Open Questions")
        + "\n"
        + perspective
        + "\n"
        + best_join("## Meta-Feedback")
        + closing_line
    )

    return merged


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    round_id = args[0]
    if not re.match(r"^round-\d+$", round_id):
        print(
            f"ERROR: round must be in the form 'round-NN', got: {round_id}",
            file=sys.stderr,
        )
        sys.exit(1)

    round_dir = REPO / "reviews" / round_id
    manifest_path = round_dir / ".prepared" / "manifest.json"

    if not manifest_path.exists():
        print(f"ERROR: manifest not found at {manifest_path}", file=sys.stderr)
        sys.exit(2)

    manifest = json.loads(manifest_path.read_text())
    entries = manifest.get("entries", [])

    # Check if batching was used
    batched_entries = [e for e in entries if e.get("batch") is not None]
    if not batched_entries:
        print("No batched entries found in manifest. Nothing to concatenate.")
        sys.exit(0)

    # Group by reviewer
    by_reviewer: dict[str, list[dict]] = {}
    for entry in entries:
        r = entry["reviewer"]
        if r not in by_reviewer:
            by_reviewer[r] = []
        by_reviewer[r].append(entry)

    for reviewer, reviewer_entries in by_reviewer.items():
        # Separate section batches from tail batch
        section_entries = [
            e
            for e in reviewer_entries
            if e.get("type") != "tail" and e.get("batch") != "tail"
        ]
        tail_entries = [
            e
            for e in reviewer_entries
            if e.get("type") == "tail" or e.get("batch") == "tail"
        ]

        # Sort section batches by batch number
        section_entries.sort(key=lambda e: e.get("batch") or 0)

        # Check all section batch files exist
        batch_texts = []
        missing = []
        for entry in section_entries:
            batch_file = round_dir / f"{reviewer}-batch-{entry['batch']}.md"
            if not batch_file.exists():
                missing.append(str(batch_file))
            else:
                batch_texts.append(batch_file.read_text(encoding="utf-8"))

        # Check tail batch file if present
        tail_text: str | None = None
        if tail_entries:
            tail_file = round_dir / f"{reviewer}-batch-tail.md"
            if not tail_file.exists():
                missing.append(str(tail_file))
            else:
                tail_text = tail_file.read_text(encoding="utf-8")

        if missing:
            print(f"ERROR: missing batch files for {reviewer}:", file=sys.stderr)
            for m in missing:
                print(f"  {m}", file=sys.stderr)
            sys.exit(2)

        n_section = len(batch_texts)
        n_tail = 1 if tail_text is not None else 0
        print(
            f"Merging {n_section} section batch(es){' + tail batch' if n_tail else ''} for {reviewer}..."
        )

        meta = {}
        merged = merge_batch_reviews(
            batch_texts, reviewer, round_id, meta, tail_text=tail_text
        )

        out_path = round_dir / f"{reviewer}.md"
        out_path.write_text(merged, encoding="utf-8")
        print(f"  wrote {out_path.relative_to(REPO)}")

    print(f"\nConcatenated {len(by_reviewer)} reviewer(s).")


if __name__ == "__main__":
    main()
