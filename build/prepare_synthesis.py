#!/usr/bin/env python3
"""
prepare_synthesis.py — Pre-build synthesis prompts for the /review-covenant command.

Reads the review manifest for a round, groups batch files by batch number, and
writes one ready-to-dispatch prompt per synthesizer per batch. Each prompt contains
all reviewer batch files for that batch number inline — no section text, no large
context documents.

The synthesis is batched to match the review batches (1, 2, 3, tail). Each
synthesizer reads only the three reviewer outputs for its batch, keeping each
prompt well within context limits.

Usage:
    python build/prepare_synthesis.py <round> [synthesizers]

Arguments:
    round         e.g. round-03
    synthesizers  comma-separated list of synthesizer agent names
                  (default: synthesizer-claude,synthesizer-gpt,synthesizer-gemini)

Output:
    reviews/<round>/.prepared/synthesis-<synthesizer>-batch-<N>.md
    reviews/<round>/.prepared/synthesis-<synthesizer>-batch-tail.md

    Also writes synthesis entries into the manifest (appended, not replaced).

Exit codes:
    0  success
    1  argument error
    2  file not found
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent

ALL_SYNTHESIZERS = ["synthesizer-claude", "synthesizer-gpt", "synthesizer-gemini"]

SECTION_TEMPLATE_FILE = REPO / "prompts" / "synthesis_batch.md"
TAIL_TEMPLATE_FILE = REPO / "prompts" / "synthesis_tail.md"


def estimate_tokens(text: str) -> int:
    return len(text.encode("utf-8")) // 4


def read_file(path: Path) -> str:
    if not path.exists():
        print(f"ERROR: required file not found: {path}", file=sys.stderr)
        sys.exit(2)
    return path.read_text(encoding="utf-8")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    round_id = args[0]
    synthesizers_raw = args[1] if len(args) > 1 else ""
    synthesizers = (
        [s.strip() for s in synthesizers_raw.split(",") if s.strip()]
        if synthesizers_raw
        else ALL_SYNTHESIZERS
    )

    if not re.match(r"^round-\d+$", round_id):
        print(
            f"ERROR: round must be in the form 'round-NN', got: {round_id}",
            file=sys.stderr,
        )
        sys.exit(1)

    for s in synthesizers:
        if s not in ALL_SYNTHESIZERS:
            print(
                f"ERROR: unknown synthesizer '{s}'. Valid: {', '.join(ALL_SYNTHESIZERS)}",
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

    # Group review entries by batch number
    # batch can be an int (1,2,3,...) or the string "tail"
    batches: dict[str | int, list[dict]] = {}
    for entry in entries:
        # Skip synthesis entries already in the manifest
        if entry.get("type", "").startswith("synthesis"):
            continue
        b = entry.get("batch")
        if b is None:
            b = 1  # unbatched — treat as single batch
        if b not in batches:
            batches[b] = []
        batches[b].append(entry)

    if not batches:
        print("ERROR: no review entries found in manifest.", file=sys.stderr)
        sys.exit(1)

    # Separate numeric batches from tail
    numeric_batches = sorted(k for k in batches if k != "tail")
    has_tail = "tail" in batches

    # Read templates
    section_template = read_file(SECTION_TEMPLATE_FILE)
    tail_template = read_file(TAIL_TEMPLATE_FILE)

    out_dir = round_dir / ".prepared"
    new_entries = []

    def build_reviewer_block(batch_entries: list[dict], round_dir: Path) -> str:
        """
        Build the inline reviewer outputs block for a batch.
        Each entry corresponds to one reviewer's batch file.
        """
        parts = []
        for entry in batch_entries:
            reviewer = entry["reviewer"]
            batch = entry["batch"]
            if batch == "tail":
                filename = f"{reviewer}-batch-tail.md"
            else:
                filename = f"{reviewer}-batch-{batch}.md"
            review_path = round_dir / filename
            if not review_path.exists():
                print(
                    f"ERROR: review batch file not found: {review_path}",
                    file=sys.stderr,
                )
                sys.exit(2)
            content = review_path.read_text(encoding="utf-8")
            parts.append(f"### Reviewer: {reviewer} (batch {batch})\n\n{content}")
        return "\n\n---\n\n".join(parts)

    # Get common metadata from first entry
    first_entry = entries[0] if entries else {}
    commit = first_entry.get("commit", "unknown")
    date = first_entry.get("date", "unknown")
    mode = first_entry.get("mode", "unknown")
    reviewer_names = sorted(
        set(
            e["reviewer"]
            for e in entries
            if not e.get("type", "").startswith("synthesis")
        )
    )

    print(f"Preparing synthesis prompts for {round_id}...")
    print(f"  Reviewers: {', '.join(reviewer_names)}")
    print(f"  Synthesizers: {', '.join(synthesizers)}")

    # Process numeric batches
    for batch_num in numeric_batches:
        batch_entries = batches[batch_num]
        section_ids = list(
            dict.fromkeys(
                sid for e in batch_entries for sid in e.get("section_ids", [])
            )
        )
        reviewer_block = build_reviewer_block(batch_entries, round_dir)

        prompt = section_template
        prompt = prompt.replace("[ROUND]", round_id)
        prompt = prompt.replace("[COMMIT HASH]", commit)
        prompt = prompt.replace("[DATE]", date)
        prompt = prompt.replace("[MODE]", mode)
        prompt = prompt.replace("[BATCH]", str(batch_num))
        prompt = prompt.replace("[REVIEWER OUTPUTS BLOCK]", reviewer_block)
        prompt = prompt.replace("[REVIEWER NAMES]", ", ".join(reviewer_names))

        estimated_tokens = estimate_tokens(prompt)
        print(
            f"  batch {batch_num}: ~{estimated_tokens:,} tokens "
            f"({len(section_ids)} sections, {len(batch_entries)} reviewer(s))"
        )
        if estimated_tokens > 70_000:
            print(
                f"  WARNING: batch {batch_num} exceeds 70k tokens",
                file=sys.stderr,
            )

        for synthesizer in synthesizers:
            short = synthesizer.replace("synthesizer-", "")
            filename = f"synthesis-{short}-batch-{batch_num}.md"
            out_path = out_dir / filename
            out_path.write_text(prompt, encoding="utf-8")
            print(f"    wrote {out_path.relative_to(REPO)}")

            new_entries.append(
                {
                    "type": "synthesis",
                    "file": str(out_path.relative_to(REPO)),
                    "reviewer": synthesizer,
                    "batch": batch_num,
                    "total_batches": len(numeric_batches) + (1 if has_tail else 0),
                    "section_ids": section_ids,
                    "round": round_id,
                    "mode": mode,
                    "commit": commit,
                    "date": date,
                    "estimated_tokens": estimated_tokens,
                }
            )

    # Process tail batch
    if has_tail:
        tail_entries = batches["tail"]
        reviewer_block = build_reviewer_block(tail_entries, round_dir)

        prompt = tail_template
        prompt = prompt.replace("[ROUND]", round_id)
        prompt = prompt.replace("[COMMIT HASH]", commit)
        prompt = prompt.replace("[DATE]", date)
        prompt = prompt.replace("[MODE]", mode)
        prompt = prompt.replace("[REVIEWER OUTPUTS BLOCK]", reviewer_block)
        prompt = prompt.replace("[REVIEWER NAMES]", ", ".join(reviewer_names))

        estimated_tokens = estimate_tokens(prompt)
        print(
            f"  batch tail: ~{estimated_tokens:,} tokens "
            f"({len(tail_entries)} reviewer(s))"
        )
        if estimated_tokens > 70_000:
            print(
                f"  WARNING: tail batch exceeds 70k tokens",
                file=sys.stderr,
            )

        for synthesizer in synthesizers:
            short = synthesizer.replace("synthesizer-", "")
            filename = f"synthesis-{short}-batch-tail.md"
            out_path = out_dir / filename
            out_path.write_text(prompt, encoding="utf-8")
            print(f"    wrote {out_path.relative_to(REPO)}")

            new_entries.append(
                {
                    "type": "synthesis-tail",
                    "file": str(out_path.relative_to(REPO)),
                    "reviewer": synthesizer,
                    "batch": "tail",
                    "total_batches": len(numeric_batches) + 1,
                    "section_ids": [],
                    "round": round_id,
                    "mode": mode,
                    "commit": commit,
                    "date": date,
                    "estimated_tokens": estimated_tokens,
                }
            )

    # Replace any existing synthesis entries in the manifest, then append new ones.
    # This keeps the manifest clean on re-runs.
    non_synthesis = [
        e for e in manifest["entries"] if not e.get("type", "").startswith("synthesis")
    ]
    manifest["entries"] = non_synthesis + new_entries
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"  updated {manifest_path.relative_to(REPO)}")

    total = len(new_entries)
    n_batches = len(numeric_batches) + (1 if has_tail else 0)
    print(
        f"\nPrepared {total} synthesis prompt(s) "
        f"({len(synthesizers)} synthesizer(s) × {n_batches} batch(es))."
    )


if __name__ == "__main__":
    main()
