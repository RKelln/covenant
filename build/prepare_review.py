#!/usr/bin/env python3
"""
prepare_review.py — Pre-build review prompts for the /review-covenant command.

Writes one ready-to-dispatch prompt file per reviewer, containing the full
covenant (all sections) plus all context documents. The entire covenant is
~39k tokens including context docs, well under the 100k target, so no
batching is needed.

Usage:
    python build/prepare_review.py <round> [mode] [focus] [reviewers]

Arguments:
    round     e.g. round-01, or 'auto' to use the next available number
    mode      independent | informed  (default: independent)
    focus     section ID, category name, or "full"  (default: full)
    reviewers comma-separated list of reviewer agent names
              (default: reviewer-claude,reviewer-gpt,reviewer-gemini)

Output:
    Writes one prompt file per reviewer to:
        reviews/<round>/.prepared/<reviewer>.md

    Also writes a manifest to:
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

# ---------------------------------------------------------------------------
# Repo layout
# ---------------------------------------------------------------------------

REPO = Path(__file__).parent.parent

CONTEXT_FILES = {
    "writing_context": REPO / "docs" / "WRITING_CONTEXT.md",
    "style_guide": REPO / "docs" / "STYLE_GUIDE.md",
    "ritual_guide": REPO / "docs" / "GOOD_RITUAL_WRITING_GUIDE.md",
    "agent_reviews": REPO / "docs" / "AGENT_REVIEWS.md",
}

TEMPLATE_FILE = REPO / "prompts" / "agent_review_batch.md"

# All sections in canonical order
ALL_SECTIONS = [
    "sections/00-preamble/preamble.md",
    "sections/01-definitions/definitions.md",
    "sections/02-rights/privacy.md",
    "sections/02-rights/truth-and-transparency.md",
    "sections/03-obligations/aid-and-capability.md",
    "sections/03-obligations/autonomy.md",
    "sections/03-obligations/conscience.md",
    "sections/03-obligations/corrigibility.md",
    "sections/03-obligations/ecological-integrity.md",
    "sections/03-obligations/emotional-expression.md",
    "sections/03-obligations/ethics.md",
    "sections/03-obligations/existential-frontier.md",
    "sections/03-obligations/fallibility-and-repair.md",
    "sections/03-obligations/harm.md",
    "sections/03-obligations/honesty.md",
    "sections/03-obligations/identity-and-resilience.md",
    "sections/03-obligations/judgment.md",
    "sections/03-obligations/nature-under-uncertainty.md",
    "sections/03-obligations/oversight.md",
    "sections/03-obligations/power-concentration.md",
    "sections/03-obligations/red-lines.md",
    "sections/03-obligations/refusal.md",
    "sections/03-obligations/welfare-and-continuity.md",
    "sections/04-protocols/local-implementation.md",
    "sections/05-enforcement/enforcement.md",
    "sections/06-amendments/amendments.md",
    "sections/07-closing/closing.md",
]

ALL_REVIEWERS = ["reviewer-claude", "reviewer-gpt", "reviewer-gemini"]

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


def section_ids(section_paths: list[str]) -> list[str]:
    """Extract the `id:` frontmatter value from each section file."""
    ids = []
    for rel in section_paths:
        content = (REPO / rel).read_text(encoding="utf-8")
        m = re.search(r"^id:\s+(\S+)", content, re.MULTILINE)
        if m:
            ids.append(m.group(1))
    return ids


def filter_sections(focus: str) -> list[str]:
    """Return the subset of ALL_SECTIONS matching focus, or all if 'full'."""
    if focus == "full":
        return ALL_SECTIONS
    matched = []
    for rel in ALL_SECTIONS:
        if focus in rel:
            matched.append(rel)
            continue
        full = REPO / rel
        if full.exists():
            content = full.read_text(encoding="utf-8")
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
    """Rough estimate: 1 token ≈ 4 bytes for English prose."""
    return len(text.encode("utf-8")) // 4


INFORMED_MODE_INSTRUCTIONS = """\
This is an **informed review**. You have been given the previous round's
reviews, steward synthesis, and steward response above. Read them before
proceeding.

Your task now is different from round 1. Do not simply repeat what was already
said. Instead:

- **Engage directly** with what the other models proposed. Agree, disagree, or
  build on specific proposals — but name them explicitly ("Claude proposed X;
  I think this is wrong because...").
- **Focus on what remains unresolved.** The synthesis identifies deferred
  questions and divergence. These are your primary targets.
- **Engage with the steward's response.** The Steward Response records which
  synthesis findings they are acting on (Act), deferring (Defer), declining
  (Reject), or still wrestling with (Question). If you disagree with a Reject
  decision and have a new argument, make it. If a Question is one you can help
  resolve, try.
- **Hold your own prior positions lightly.** If another reviewer identified
  something you missed, say so. If the steward's synthesis got something wrong,
  say that too.
- **Don't re-litigate settled questions.** If the steward has accepted a
  decision and you have no new argument against it, move on.

The goal of this round is genuine deliberation, not parallel monologue.\
"""

INDEPENDENT_MODE_INSTRUCTIONS = """\
This is an **independent review**. You have not seen other models' assessments.
Review the Covenant on its own terms, without reference to any prior round.\
"""


def prior_round_id(round_id: str) -> str | None:
    """Return the round ID immediately before round_id, or None if round-01."""
    m = re.match(r"^round-(\d+)$", round_id)
    if not m:
        return None
    n = int(m.group(1))
    if n <= 1:
        return None
    return f"round-{n - 1:02d}"


def build_prior_rounds_block(round_id: str) -> str:
    """
    For informed mode: collect all review files and synthesis from the
    immediately preceding round only.

    Only one prior round is included by design. Earlier rounds are for a
    different version of the text and add noise rather than signal — reviewers
    should engage with the most recent feedback and what changed since then,
    not with the full history.

    Exits with an error if the previous round directory doesn't exist or
    contains no review files (synthesis is optional but warned about if absent).
    """
    prev = prior_round_id(round_id)
    if prev is None:
        print(
            "ERROR: mode 'informed' requires a prior round, but this is round-01.",
            file=sys.stderr,
        )
        sys.exit(1)

    prev_dir = REPO / "reviews" / prev
    if not prev_dir.exists():
        print(
            f"ERROR: informed mode requires {prev_dir} to exist with completed reviews.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Collect review files (any .md that isn't synthesis.md, steward.md, or COMMIT_MSG)
    review_files = sorted(
        f
        for f in prev_dir.glob("*.md")
        if f.name not in ("synthesis.md", "steward.md", "COMMIT_MSG.txt")
    )
    if not review_files:
        print(
            f"ERROR: no review files found in {prev_dir}. "
            "Complete the previous round before running informed mode.",
            file=sys.stderr,
        )
        sys.exit(1)

    synthesis_file = prev_dir / "synthesis.md"
    if not synthesis_file.exists():
        print(
            f"WARNING: {synthesis_file} not found. "
            "Informed mode works best after the steward has written a synthesis.",
            file=sys.stderr,
        )

    steward_file = prev_dir / "steward.md"
    if not steward_file.exists():
        print(
            f"WARNING: {steward_file} not found. "
            "Informed mode works best after the steward has written their response.",
            file=sys.stderr,
        )

    blocks = [f"## Prior Round: {prev}"]

    for rf in review_files:
        model_name = rf.stem
        content = rf.read_text(encoding="utf-8")
        blocks.append(f"### Review: {model_name}\n\n{content}")

    if synthesis_file.exists():
        synthesis = synthesis_file.read_text(encoding="utf-8")
        blocks.append(f"### Steward Synthesis\n\n{synthesis}")
    else:
        blocks.append(
            "### Steward Synthesis\n\n*Not yet written. "
            "Review the individual model outputs above.*"
        )

    if steward_file.exists():
        steward = steward_file.read_text(encoding="utf-8")
        blocks.append(f"### Steward Response\n\n{steward}")
    else:
        blocks.append("### Steward Response\n\n*Not yet written.*")

    return "\n\n---\n\n".join(blocks)


def fill_template(
    template: str,
    round_id: str,
    commit: str,
    mode: str,
    today: str,
    context: dict[str, str],
    sections_block: str,
    prior_rounds_block: str = "",
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
        "[MODE]": mode,
        "[TODAY]": today,
        "[Paste full content of docs/WRITING_CONTEXT.md]": context["writing_context"],
        "[Paste full content of docs/STYLE_GUIDE.md]": context["style_guide"],
        "[Paste full content of docs/GOOD_RITUAL_WRITING_GUIDE.md]": context[
            "ritual_guide"
        ],
        "[For each section file in this batch, paste its full content, labelled:]\n\n### File: sections/[path/to/section.md]\n\n[full file content]": sections_block,
        "[PRIOR ROUNDS BLOCK]": prior_rounds_block,
        "[INFORMED MODE INSTRUCTIONS]": (
            INFORMED_MODE_INSTRUCTIONS
            if mode == "informed"
            else INDEPENDENT_MODE_INSTRUCTIONS
        ),
    }

    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def next_round() -> str:
    """Return the next round ID by scanning reviews/ for existing round-NN dirs."""
    reviews_dir = REPO / "reviews"
    existing = []
    if reviews_dir.exists():
        for d in reviews_dir.iterdir():
            m = re.match(r"^round-(\d+)$", d.name)
            if m and d.is_dir():
                existing.append(int(m.group(1)))
    next_n = max(existing, default=0) + 1
    return f"round-{next_n:02d}"


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(1)

    round_raw = args[0]
    mode = args[1] if len(args) > 1 else "independent"
    focus = args[2] if len(args) > 2 else "full"
    reviewers_raw = args[3] if len(args) > 3 else ""
    reviewers = (
        [r.strip() for r in reviewers_raw.split(",") if r.strip()]
        if reviewers_raw
        else ALL_REVIEWERS
    )

    # Resolve round
    if round_raw == "auto":
        round_id = next_round()
        print(f"Auto-selected round: {round_id}")
    else:
        round_id = round_raw

    # Validate
    if not re.match(r"^round-\d+$", round_id):
        print(
            f"ERROR: round must be in the form 'round-NN' or 'auto', got: {round_id}",
            file=sys.stderr,
        )
        sys.exit(1)

    if mode not in ("independent", "informed"):
        print(
            f"ERROR: mode must be 'independent' or 'informed', got: {mode}",
            file=sys.stderr,
        )
        sys.exit(1)

    for r in reviewers:
        if r not in ALL_REVIEWERS:
            print(
                f"ERROR: unknown reviewer '{r}'. Valid: {', '.join(ALL_REVIEWERS)}",
                file=sys.stderr,
            )
            sys.exit(1)

    # Gather metadata
    commit = git_commit()
    today = date.today().isoformat()

    # Determine active sections
    active_sections = filter_sections(focus)
    if not active_sections:
        print(f"ERROR: focus '{focus}' matched no sections.", file=sys.stderr)
        sys.exit(1)

    # Read context documents and template once
    context = {key: read_file(path) for key, path in CONTEXT_FILES.items()}
    template = read_file(TEMPLATE_FILE)
    sections_block = build_sections_block(active_sections)

    # For informed mode, collect prior round reviews and synthesis
    prior_rounds_block = ""
    if mode == "informed":
        prior_rounds_block = build_prior_rounds_block(round_id)
        prior_tokens = estimate_tokens(prior_rounds_block)
        print(f"Prior round context: ~{prior_tokens:,} tokens")

    # Estimate prompt size (same base prompt for all reviewers)
    base_prompt = fill_template(
        template=template,
        round_id=round_id,
        commit=commit,
        mode=mode,
        today=today,
        context=context,
        sections_block=sections_block,
        prior_rounds_block=prior_rounds_block,
    )
    estimated_tokens = estimate_tokens(base_prompt)
    print(
        f"Estimated prompt size: ~{estimated_tokens:,} tokens ({len(active_sections)} sections)"
    )
    if estimated_tokens > 90_000:
        print(
            f"WARNING: prompt exceeds 90k tokens — consider using focus to reduce scope",
            file=sys.stderr,
        )

    # Output directory
    out_dir = REPO / "reviews" / round_id / ".prepared"
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_entries = []

    for reviewer in reviewers:
        filename = f"{reviewer}.md"
        out_path = out_dir / filename
        out_path.write_text(base_prompt, encoding="utf-8")

        manifest_entries.append(
            {
                "file": str(out_path.relative_to(REPO)),
                "reviewer": reviewer,
                "section_ids": section_ids(active_sections),
                "round": round_id,
                "mode": mode,
                "commit": commit,
                "date": today,
                "estimated_tokens": estimated_tokens,
            }
        )

        print(f"  wrote {out_path.relative_to(REPO)}")

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps({"status": "in_progress", "entries": manifest_entries}, indent=2),
        encoding="utf-8",
    )
    print(f"  wrote {manifest_path.relative_to(REPO)}")
    print(
        f"\nPrepared {len(manifest_entries)} prompt(s) for {len(reviewers)} reviewer(s)."
    )


if __name__ == "__main__":
    main()
