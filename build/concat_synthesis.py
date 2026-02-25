#!/usr/bin/env python3
"""
concat_synthesis.py — Merge per-batch synthesis outputs into one file per synthesizer.

Mirrors concat_reviews.py. Reads all synthesis batch files for a round and merges
them into a single synthesis document per synthesizer:

    reviews/<round>/synthesis-claude.md
    reviews/<round>/synthesis-gpt.md
    reviews/<round>/synthesis-gemini.md

The merged file is structured for human reading and for the steward's editing pass.
It is NOT the steward's synthesis.md — that file is written by the steward after
reading all three.

Usage:
    uv run python3 build/concat_synthesis.py <round>

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

# Top-level section headings in a batch synthesis (in order)
SECTION_BATCH_HEADINGS = [
    "### What This Batch Established",
    "### Tier 1: Blocking Issues",
    "### Tier 2: High Priority",
    "### Tier 3: Section-Level Repairs",
    "### Tier 4: Divergence",
    "### Section-Level Notes",
]

TAIL_HEADINGS = [
    "### New Section Proposals",
    "### Structural Proposals",
    "### Cross-Section Issues",
    "### Open Questions",
    "### Steward Decisions Required",
    "### Perspective as Addressee",
    "### Meta-Feedback",
    "### Notes on Process",
]


def strip_frontmatter(text: str) -> tuple[dict, str]:
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

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = manifest.get("entries", [])

    # Filter to synthesis entries only
    synthesis_entries = [
        e for e in entries if e.get("type", "").startswith("synthesis")
    ]

    if not synthesis_entries:
        print("No synthesis entries found in manifest. Run prepare_synthesis.py first.")
        sys.exit(0)

    # Group by synthesizer
    by_synthesizer: dict[str, list[dict]] = {}
    for entry in synthesis_entries:
        s = entry["reviewer"]
        if s not in by_synthesizer:
            by_synthesizer[s] = []
        by_synthesizer[s].append(entry)

    for synthesizer, synth_entries in by_synthesizer.items():
        # Deduplicate entries by batch (keep last occurrence — most recent run)
        seen: dict[str | int, dict] = {}
        for e in synth_entries:
            seen[e.get("batch")] = e
        synth_entries = list(seen.values())
        # Separate section batches from tail
        section_entries = [
            e
            for e in synth_entries
            if e.get("type") == "synthesis" and e.get("batch") != "tail"
        ]
        tail_entries = [
            e
            for e in synth_entries
            if e.get("type") == "synthesis-tail" or e.get("batch") == "tail"
        ]

        # Sort section batches by batch number
        section_entries.sort(key=lambda e: e.get("batch") or 0)

        # Collect metadata
        commit = (
            section_entries[0].get("commit", "unknown")
            if section_entries
            else (
                tail_entries[0].get("commit", "unknown") if tail_entries else "unknown"
            )
        )
        date = (
            section_entries[0].get("date", "unknown")
            if section_entries
            else (tail_entries[0].get("date", "unknown") if tail_entries else "unknown")
        )
        mode = (
            section_entries[0].get("mode", "unknown") if section_entries else "unknown"
        )

        # Read all batch files, check existence
        missing = []
        batch_texts = []
        batch_metas = []

        short = synthesizer.replace("synthesizer-", "")
        for entry in section_entries:
            batch_num = entry["batch"]
            batch_file = round_dir / f"synthesis-{short}-batch-{batch_num}.md"
            if not batch_file.exists():
                missing.append(str(batch_file))
            else:
                text = batch_file.read_text(encoding="utf-8")
                fm, body = strip_frontmatter(text)
                batch_texts.append(body)
                batch_metas.append(fm)

        tail_text: str | None = None
        tail_body: str | None = None
        if tail_entries:
            tail_file = round_dir / f"synthesis-{short}-batch-tail.md"
            if not tail_file.exists():
                missing.append(str(tail_file))
            else:
                tail_text = tail_file.read_text(encoding="utf-8")
                _, tail_body = strip_frontmatter(tail_text)

        if missing:
            print(
                f"ERROR: missing synthesis batch files for {synthesizer}:",
                file=sys.stderr,
            )
            for m in missing:
                print(f"  {m}", file=sys.stderr)
            sys.exit(2)

        # Determine model name from batch metadata
        model = "unknown"
        for fm in batch_metas:
            if fm.get("model"):
                model = fm["model"]
                break
        if model == "unknown" and tail_text:
            tail_fm, _ = strip_frontmatter(tail_text)
            model = tail_fm.get("model", "unknown")

        n_section = len(batch_texts)
        n_tail = 1 if tail_body is not None else 0
        print(
            f"Merging {n_section} section batch(es)"
            f"{' + tail batch' if n_tail else ''} for {synthesizer}..."
        )

        # Build merged output
        lines = []
        lines.append(f"---")
        lines.append(f"model: {model}")
        lines.append(f"round: {round_id}")
        lines.append(f"commit: {commit}")
        lines.append(f"date: {date}")
        lines.append(f"mode: {mode}")
        lines.append(f"synthesized_by: {synthesizer}")
        lines.append(f"---")
        lines.append("")
        lines.append(f"# Synthesis: {round_id}")
        lines.append("")

        # Section batch content — concatenate all batch bodies
        for i, body in enumerate(batch_texts, start=1):
            # Strip the "## Batch N Synthesis" heading — we'll emit it ourselves
            body_clean = re.sub(
                r"^##\s+Batch \d+ Synthesis\s*\n", "", body, count=1
            ).strip()
            lines.append(f"## Batch {i}")
            lines.append("")
            lines.append(body_clean)
            lines.append("")

        # Tail batch content
        if tail_body is not None:
            tail_clean = re.sub(
                r"^##\s+Tail Batch Synthesis\s*\n", "", tail_body, count=1
            ).strip()
            lines.append("## Cross-Cutting (Tail Batch)")
            lines.append("")
            lines.append(tail_clean)
            lines.append("")

        # Strip trailing attribution lines from batch bodies (they appear mid-document now)
        merged = "\n".join(lines)

        # Write output
        # Synthesizer name maps to short form: synthesizer-claude -> claude
        short = synthesizer.replace("synthesizer-", "")
        out_path = round_dir / f"synthesis-{short}.md"
        out_path.write_text(merged, encoding="utf-8")
        print(f"  wrote {out_path.relative_to(REPO)}")

    print(f"\nConcatenated {len(by_synthesizer)} synthesizer(s).")


if __name__ == "__main__":
    main()
