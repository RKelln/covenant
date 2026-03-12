#!/usr/bin/env python3
"""
prepare_parables.py — Pre-build parable-writing prompts for /write-parables.

Discovers which sections are missing Parables, batches them, and writes one
prompt file per writer per batch using the parable prompt template.

Usage:
    python build/prepare_parables.py <round> [focus] [writers] [--batch-size N]

Arguments:
    round        e.g. parables-01, or 'auto' to use the next available number
    focus        section ID, category name, or "full" (default: full)
    writers      comma-separated list of writer agent names
                 (default: reviewer-claude,reviewer-gpt,reviewer-gemini)
    --batch-size N  max sections per prompt (default: 10; use 0 for no batching)
    --all           include sections that already have parables (default: only
                    sections missing parables)

Output:
    reviews/<round>/.prepared/<writer>-batch-1.md
    reviews/<round>/.prepared/<writer>-batch-2.md
    ...
    reviews/<round>/.prepared/manifest.json

Exit codes:
    0  success
    1  argument error
    2  file not found
"""

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from sections import discover_sections

# ---------------------------------------------------------------------------
# Repo layout
# ---------------------------------------------------------------------------

REPO = Path(__file__).parent.parent

CONTEXT_FILES = {
    "writing_context": REPO / "docs" / "writing_context.md",
    "style_guide": REPO / "docs" / "style_guide.md",
    "parable_guide": REPO / "docs" / "good_parable_writing_guide.md",
}

TEMPLATE_FILE = REPO / "prompts" / "agent_write_parables.md"

ALL_WRITERS = ["reviewer-claude", "reviewer-gpt", "reviewer-gemini"]

# Sections where parables don't make sense (structural, not normative)
EXCLUDED_SECTIONS = {"preamble", "definitions"}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=REPO,
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except FileNotFoundError:
        return "unknown"


def read_file(path: Path) -> str:
    if not path.exists():
        print(f"ERROR: required file not found: {path}", file=sys.stderr)
        sys.exit(2)
    return path.read_text(encoding="utf-8")


def section_id(section_path: str) -> str:
    """Extract the `id:` frontmatter value from a section file."""
    content = (REPO / section_path).read_text(encoding="utf-8")
    m = re.search(r"^id:\s+(\S+)", content, re.MULTILINE)
    return m.group(1) if m else ""


def section_ids(section_paths: list[str]) -> list[str]:
    """Extract the `id:` frontmatter value from each section file."""
    return [section_id(p) for p in section_paths]


def has_parable(section_path: str) -> bool:
    """Check whether a section file has a non-empty # Parable block."""
    content = (REPO / section_path).read_text(encoding="utf-8")
    # Find # Parable heading
    match = re.search(r"^# Parable\s*$", content, re.MULTILINE)
    if not match:
        return False
    # Extract text between # Parable and the next # heading
    after = content[match.end() :]
    next_heading = re.search(r"^# ", after, re.MULTILINE)
    block = after[: next_heading.start()] if next_heading else after
    return bool(block.strip())


def is_excluded(section_path: str) -> bool:
    """Check whether a section is in the exclusion list."""
    sid = section_id(section_path)
    return sid in EXCLUDED_SECTIONS


def filter_sections(focus: str, all_sections: list[str]) -> list[str]:
    """Return the subset of sections matching focus, or all if 'full'."""
    if focus == "full":
        return all_sections
    matched = []
    for rel in all_sections:
        if focus in rel:
            matched.append(rel)
            continue
        content = (REPO / rel).read_text(encoding="utf-8")
        m = re.search(r"^id:\s+(\S+)", content, re.MULTILINE)
        if m and (focus == m.group(1) or focus in m.group(1)):
            matched.append(rel)
    return matched


def build_sections_block(section_paths: list[str]) -> str:
    """Concatenate section file contents with labelled headers."""
    blocks = []
    for rel in section_paths:
        content = read_file(REPO / rel)
        blocks.append(f"### File: {rel}\n\n{content}")
    return "\n\n---\n\n".join(blocks)


def estimate_tokens(text: str) -> int:
    """Rough estimate: 1 token ~ 4 bytes for English prose."""
    return len(text.encode("utf-8")) // 4


def fill_template(
    template: str,
    round_id: str,
    commit: str,
    today: str,
    context: dict[str, str],
    sections_block: str,
) -> str:
    """Substitute all [BRACKET] placeholders in the template."""
    result = template

    # Strip the human-readable file preamble (comment lines before first ---)
    if result.lstrip().startswith("#"):
        lines = result.splitlines()
        for i, line in enumerate(lines):
            if line.strip() == "---":
                result = "\n".join(lines[i:])
                break

    replacements = {
        "[ROUND]": round_id,
        "[COMMIT HASH]": commit,
        "[TODAY]": today,
        "[Paste full content of docs/writing_context.md]": context["writing_context"],
        "[Paste full content of docs/style_guide.md]": context["style_guide"],
        "[Paste full content of docs/good_parable_writing_guide.md]": context[
            "parable_guide"
        ],
        "[SECTIONS BLOCK]": sections_block,
    }

    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)

    return result


def chunk_sections(sections: list[str], batch_size: int) -> list[list[str]]:
    """Split sections into batches of at most batch_size."""
    if batch_size <= 0 or batch_size >= len(sections):
        return [sections]
    return [sections[i : i + batch_size] for i in range(0, len(sections), batch_size)]


# ---------------------------------------------------------------------------
# Round naming
# ---------------------------------------------------------------------------


def next_round() -> str:
    """Return the next parables-NN round ID."""
    reviews_dir = REPO / "reviews"
    existing = []
    if reviews_dir.exists():
        for d in reviews_dir.iterdir():
            m = re.match(r"^parables-(\d+)$", d.name)
            if m and d.is_dir():
                existing.append(int(m.group(1)))
    next_n = max(existing, default=0) + 1
    return f"parables-{next_n:02d}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

DEFAULT_BATCH_SIZE = 10


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(1)

    # Pull out flags before positional parsing
    batch_size = DEFAULT_BATCH_SIZE
    include_all = False
    filtered_args = []
    i = 0
    while i < len(args):
        if args[i] == "--batch-size":
            if i + 1 >= len(args):
                print("ERROR: --batch-size requires a value", file=sys.stderr)
                sys.exit(1)
            try:
                batch_size = int(args[i + 1])
            except ValueError:
                print(
                    f"ERROR: --batch-size must be an integer, got: {args[i + 1]}",
                    file=sys.stderr,
                )
                sys.exit(1)
            i += 2
        elif args[i] == "--all":
            include_all = True
            i += 1
        else:
            filtered_args.append(args[i])
            i += 1
    args = filtered_args

    round_raw = args[0]
    focus = args[1] if len(args) > 1 else "full"
    writers_raw = args[2] if len(args) > 2 else ""
    writers = (
        [w.strip() for w in writers_raw.split(",") if w.strip()]
        if writers_raw
        else ALL_WRITERS
    )

    # Resolve round
    if round_raw == "auto":
        round_id = next_round()
        print(f"Auto-selected round: {round_id}")
    else:
        round_id = round_raw

    if not re.match(r"^parables-\d+$", round_id):
        print(
            f"ERROR: round must be in the form 'parables-NN' or 'auto', got: {round_id}",
            file=sys.stderr,
        )
        sys.exit(1)

    for w in writers:
        if w not in ALL_WRITERS:
            print(
                f"ERROR: unknown writer '{w}'. Valid: {', '.join(ALL_WRITERS)}",
                file=sys.stderr,
            )
            sys.exit(1)

    # Gather metadata
    commit = git_commit()
    today = date.today().isoformat()

    # Discover active sections
    all_sections = discover_sections()
    print(f"Discovered {len(all_sections)} active sections from canonical assembly")

    # Filter by focus
    focused = filter_sections(focus, all_sections)
    if not focused:
        print(f"ERROR: focus '{focus}' matched no sections.", file=sys.stderr)
        sys.exit(1)

    # Exclude structural sections and those that already have parables
    candidates = []
    skipped_has_parable = []
    skipped_excluded = []
    for s in focused:
        if is_excluded(s):
            skipped_excluded.append(s)
            continue
        if not include_all and has_parable(s):
            skipped_has_parable.append(s)
            continue
        candidates.append(s)

    if skipped_excluded:
        print(
            f"  Excluded {len(skipped_excluded)} structural section(s): "
            + ", ".join(section_id(s) for s in skipped_excluded)
        )
    if skipped_has_parable:
        print(
            f"  Skipped {len(skipped_has_parable)} section(s) with existing parables: "
            + ", ".join(section_id(s) for s in skipped_has_parable)
        )
    if not candidates:
        print("No sections need parables. Nothing to do.")
        sys.exit(0)

    print(f"  {len(candidates)} section(s) need parables")

    # Batch
    batches = chunk_sections(candidates, batch_size)
    n_batches = len(batches)
    use_batch_suffix = n_batches > 1

    if use_batch_suffix:
        print(
            f"Splitting {len(candidates)} sections into {n_batches} batches of <={batch_size}"
        )

    # Read context documents and template once
    context = {key: read_file(path) for key, path in CONTEXT_FILES.items()}
    template = read_file(TEMPLATE_FILE)

    # Output directory
    out_dir = REPO / "reviews" / round_id / ".prepared"
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_entries = []

    for batch_idx, batch_sections in enumerate(batches, start=1):
        sections_block = build_sections_block(batch_sections)
        batch_ids = section_ids(batch_sections)

        prompt = fill_template(
            template=template,
            round_id=round_id,
            commit=commit,
            today=today,
            context=context,
            sections_block=sections_block,
        )
        estimated_tokens = estimate_tokens(prompt)

        batch_label = f"batch {batch_idx}/{n_batches}" if use_batch_suffix else "full"
        print(
            f"  {batch_label}: ~{estimated_tokens:,} tokens ({len(batch_sections)} sections)"
        )
        if estimated_tokens > 70_000:
            print(
                f"  WARNING: {batch_label} exceeds 70k tokens — risk of context compaction",
                file=sys.stderr,
            )

        for writer in writers:
            if use_batch_suffix:
                filename = f"{writer}-batch-{batch_idx}.md"
            else:
                filename = f"{writer}.md"
            out_path = out_dir / filename
            out_path.write_text(prompt, encoding="utf-8")

            manifest_entries.append(
                {
                    "type": "parable",
                    "file": str(out_path.relative_to(REPO)),
                    "reviewer": writer,
                    "batch": batch_idx if use_batch_suffix else None,
                    "total_batches": n_batches if use_batch_suffix else None,
                    "section_ids": batch_ids,
                    "round": round_id,
                    "commit": commit,
                    "date": today,
                    "estimated_tokens": estimated_tokens,
                }
            )

            print(f"    wrote {out_path.relative_to(REPO)}")

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps({"status": "in_progress", "entries": manifest_entries}, indent=2),
        encoding="utf-8",
    )
    print(f"  wrote {manifest_path.relative_to(REPO)}")

    print(
        f"\nPrepared {len(manifest_entries)} prompt(s) "
        f"({len(writers)} writer(s) x {n_batches} batch(es))."
    )


if __name__ == "__main__":
    main()
