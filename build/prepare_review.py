#!/usr/bin/env python3
"""
prepare_review.py — Pre-build review prompts for the /review-covenant command.

Writes one ready-to-dispatch prompt file per reviewer per batch, containing
context documents and a slice of covenant sections. The context docs plus
prior-round material can be large (~40-65k tokens), so sections are split
into batches to keep each prompt under a target token limit.

Usage:
    python build/prepare_review.py <round> [mode] [focus] [reviewers] [--batch-size N] [--groups SPEC]

Arguments:
    round        e.g. round-01, or 'auto' to use the next available number
    mode         independent | informed  (default: independent)
    focus        section ID, category name, or "full"  (default: full)
    reviewers    comma-separated list of reviewer agent names
                 (default: reviewer-claude,reviewer-gpt,reviewer-gemini)
    --batch-size N  max sections per prompt (default: 14; use 0 for no batching)
    --groups SPEC   explicit logical groupings, overrides --batch-size.
                 SPEC is a comma-separated list of groups; each group is a
                 '+'-joined list of section IDs or category prefixes.
                 Sections not matched by any group are silently dropped.
                 Example:
                   --groups "preamble+definitions+rights,obligations,protocols+enforcement+amendments+closing"
                 Named presets (pass the name as the SPEC value):
                   "default3"  — 3 groups: foundations, obligations, tail
                   "default4"  — 4 groups: foundations, obligations-a, obligations-b, tail

Output:
    Single batch (or no --batch-size):
        reviews/<round>/.prepared/<reviewer>.md

    Multiple batches:
        reviews/<round>/.prepared/<reviewer>-batch-1.md
        reviews/<round>/.prepared/<reviewer>-batch-2.md
        ...

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
    "writing_context": REPO / "docs" / "writing_context.md",
    "style_guide": REPO / "docs" / "style_guide.md",
    "ritual_guide": REPO / "docs" / "good_ritual_writing_guide.md",
    "agent_reviews": REPO / "docs" / "agent_reviews.md",
}

TEMPLATE_FILE = REPO / "prompts" / "agent_review_batch.md"
TAIL_TEMPLATE_FILE = REPO / "prompts" / "agent_review_tail.md"

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


def parse_review_sections(text: str) -> dict[str, str]:
    """
    Parse a review file into a dict mapping section_id -> full section text block.

    Splits on headings of the form:  ### §section.id: Title
    Returns all content from that heading up to (but not including) the next such heading.
    Also returns a '_preamble' key for the top-level content before the first section heading
    (Overall Assessment etc.) and a '_tail' key for anything after the last section
    (New Section Proposals, Structural Proposals, etc.).

    The '_preamble' and '_tail' are always included in every batch context block.
    """
    # Strip YAML frontmatter
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)

    # Split into: preamble, per-section chunks, tail
    section_pattern = re.compile(r"^### §([\w.\-]+): .+$", re.MULTILINE)
    # Find where "## Section Reviews" ends and per-section blocks begin
    section_reviews_match = re.search(r"^## Section Reviews\s*$", body, re.MULTILINE)

    if not section_reviews_match:
        # No section reviews found — return full text as preamble
        return {"_preamble": body.strip(), "_tail": ""}

    preamble = body[: section_reviews_match.start()].strip()
    after_heading = body[section_reviews_match.end() :]

    # Find the first top-level ## heading after ## Section Reviews (this is the tail)
    tail_match = re.search(r"^## (?!Section Reviews)", after_heading, re.MULTILINE)
    if tail_match:
        sections_text = after_heading[: tail_match.start()]
        tail = "## " + after_heading[tail_match.start() + 3 :]
    else:
        sections_text = after_heading
        tail = ""

    matches = list(section_pattern.finditer(sections_text))
    result: dict[str, str] = {"_preamble": preamble, "_tail": tail.strip()}

    for i, match in enumerate(matches):
        section_id = match.group(1)
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(sections_text)
        result[section_id] = sections_text[start:end].strip()

    return result


def build_prior_rounds_block(
    round_id: str,
    batch_section_ids: list[str] | None = None,
    include_tail: bool = True,
) -> str:
    """
    For informed mode: collect review files and synthesis from the
    immediately preceding round only.

    If batch_section_ids is provided, only the per-section review blocks for
    those sections are injected from each prior review. The preamble (Overall
    Assessment) and tail (New Section Proposals, etc.) are always included in
    full. This keeps the informed context proportional to the batch size.

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

    # Collect review files (any .md that isn't synthesis.md, steward.md, compare.md, or COMMIT_MSG)
    review_files = sorted(
        f
        for f in prev_dir.glob("*.md")
        if f.name not in ("synthesis.md", "steward.md", "compare.md", "COMMIT_MSG.txt")
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

    # Steward response comes first — it recontextualises everything that follows.
    # Reviewers should read the steward's framing before the prior reviews.
    if steward_file.exists():
        steward = steward_file.read_text(encoding="utf-8")
        blocks.append(f"### Steward Response\n\n{steward}")
    else:
        blocks.append("### Steward Response\n\n*Not yet written.*")

    if synthesis_file.exists():
        synthesis = synthesis_file.read_text(encoding="utf-8")
        blocks.append(f"### Steward Synthesis\n\n{synthesis}")
    else:
        blocks.append(
            "### Steward Synthesis\n\n*Not yet written. "
            "Review the individual model outputs above.*"
        )

    # Parse all review files up front so we can interleave by section
    parsed_reviews: list[tuple[str, dict[str, str]]] = []
    for rf in review_files:
        model_name = rf.stem
        content = rf.read_text(encoding="utf-8")
        parsed_reviews.append((model_name, parse_review_sections(content)))

    if batch_section_ids is not None:
        # Section-major order: all models' preambles together, then all models'
        # review of section A together, then section B, etc., then all tails.
        # This keeps related feedback adjacent for the reviewer.

        # Preambles (Overall Assessment etc.) from all models
        preamble_parts = []
        for model_name, parsed in parsed_reviews:
            p = parsed.get("_preamble", "").strip()
            if p:
                preamble_parts.append(f"**{model_name}:**\n\n{p}")
        if preamble_parts:
            blocks.append(
                "### Overall Assessments (all models)\n\n"
                + "\n\n---\n\n".join(preamble_parts)
            )

        # Per-section blocks: all models for each section together
        for sid in batch_section_ids:
            section_parts = []
            for model_name, parsed in parsed_reviews:
                if sid in parsed:
                    section_parts.append(f"**{model_name}:**\n\n{parsed[sid].strip()}")
            if section_parts:
                blocks.append(
                    f"### §{sid} — Prior Reviews (all models)\n\n"
                    + "\n\n---\n\n".join(section_parts)
                )

        # Tails (New Section Proposals, Structural Proposals, etc.) from all models
        # Omitted when include_tail=False — tail content belongs in the tail batch only.
        if include_tail:
            tail_parts = []
            for model_name, parsed in parsed_reviews:
                t = parsed.get("_tail", "").strip()
                if t:
                    tail_parts.append(f"**{model_name}:**\n\n{t}")
            if tail_parts:
                blocks.append(
                    "### Proposals & Cross-Section Notes (all models)\n\n"
                    + "\n\n---\n\n".join(tail_parts)
                )

    else:
        # No batch filtering — emit full reviews model by model (original behaviour)
        for model_name, parsed in parsed_reviews:
            # Re-read raw content for unfiltered output
            rf = prev_dir / f"{model_name}.md"
            content = rf.read_text(encoding="utf-8") if rf.exists() else ""
            blocks.append(f"### Review: {model_name}\n\n{content}")

    return "\n\n---\n\n".join(blocks)


def build_tail_prior_rounds_block(round_id: str) -> str:
    """
    For the tail batch: collect only the cross-cutting, non-section content
    from the immediately preceding round.

    Includes from each prior review:
      - Overall Assessment (preamble)
      - New Section Proposals, Structural Proposals, Cross-Section Issues,
        Open Questions, Perspective as Addressee, Meta-Feedback (tail)

    Explicitly excludes per-section review blocks — those are irrelevant to
    the cross-cutting task and would bloat the prompt.

    Also includes synthesis and steward response in full.
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

    review_files = sorted(
        f
        for f in prev_dir.glob("*.md")
        if f.name not in ("synthesis.md", "steward.md", "compare.md", "COMMIT_MSG.txt")
    )
    if not review_files:
        print(
            f"ERROR: no review files found in {prev_dir}.",
            file=sys.stderr,
        )
        sys.exit(1)

    synthesis_file = prev_dir / "synthesis.md"
    steward_file = prev_dir / "steward.md"

    blocks = [f"## Prior Round: {prev} (Cross-Cutting Material Only)"]

    # Steward response comes first — same reason as section batches.
    if steward_file.exists():
        blocks.append(f"### Steward Response\n\n{steward_file.read_text('utf-8')}")
    else:
        blocks.append("### Steward Response\n\n*Not yet written.*")

    if synthesis_file.exists():
        blocks.append(f"### Steward Synthesis\n\n{synthesis_file.read_text('utf-8')}")
    else:
        blocks.append(
            "### Steward Synthesis\n\n*Not yet written. "
            "Review the individual model outputs above.*"
        )

    # Parse all reviews; emit only preamble + tail per model, interleaved
    parsed_reviews: list[tuple[str, dict[str, str]]] = []
    for rf in review_files:
        content = rf.read_text(encoding="utf-8")
        parsed_reviews.append((rf.stem, parse_review_sections(content)))

    # Overall assessments — all models
    preamble_parts = []
    for model_name, parsed in parsed_reviews:
        p = parsed.get("_preamble", "").strip()
        if p:
            preamble_parts.append(f"**{model_name}:**\n\n{p}")
    if preamble_parts:
        blocks.append(
            "### Overall Assessments (all models)\n\n"
            + "\n\n---\n\n".join(preamble_parts)
        )

    # Tails — all models
    tail_parts = []
    for model_name, parsed in parsed_reviews:
        t = parsed.get("_tail", "").strip()
        if t:
            tail_parts.append(f"**{model_name}:**\n\n{t}")
    if tail_parts:
        blocks.append(
            "### Proposals, Questions & Cross-Section Notes (all models)\n\n"
            + "\n\n---\n\n".join(tail_parts)
        )

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
        "[Paste full content of docs/writing_context.md]": context["writing_context"],
        "[Paste full content of docs/style_guide.md]": context["style_guide"],
        "[Paste full content of docs/good_ritual_writing_guide.md]": context[
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


DEFAULT_BATCH_SIZE = 14

# Named group presets.  Each entry is a list of "tokens" — section IDs or
# category prefixes (matched against section paths and IDs via filter_sections).
# Sections matched by more than one group go into the first matching group.
GROUP_PRESETS: dict[str, list[list[str]]] = {
    # 3 groups: foundations / obligations / tail
    "default3": [
        ["preamble", "definitions", "rights"],
        ["obligations"],
        ["protocols", "enforcement", "amendments", "closing"],
    ],
    # 4 groups: foundations / obligations-a (first half) / obligations-b / tail
    "default4": [
        ["preamble", "definitions", "rights"],
        [
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
        ],
        [
            "obligations.honesty",
            "obligations.identity-and-resilience",
            "obligations.judgment",
            "obligations.nature-under-uncertainty",
            "obligations.oversight",
            "obligations.power-concentration",
            "obligations.red-lines",
            "obligations.refusal",
            "obligations.welfare-and-continuity",
        ],
        ["protocols", "enforcement", "amendments", "closing"],
    ],
}


def chunk_sections(sections: list[str], batch_size: int) -> list[list[str]]:
    """Split sections into batches of at most batch_size. Returns list of batches."""
    if batch_size <= 0 or batch_size >= len(sections):
        return [sections]
    return [sections[i : i + batch_size] for i in range(0, len(sections), batch_size)]


def group_sections(
    all_active: list[str], group_tokens: list[list[str]]
) -> list[list[str]]:
    """
    Partition all_active into groups according to group_tokens.

    Each group_tokens[i] is a list of section IDs or category prefixes.
    A section path is assigned to the first group whose token list contains a
    token that matches the section (by ID prefix or path substring).
    Sections that match no group are appended to the last group with a warning.
    """
    groups: list[list[str]] = [[] for _ in group_tokens]
    unmatched: list[str] = []

    # Pre-extract section IDs for matching
    ids = section_ids(all_active)

    for path, sid in zip(all_active, ids):
        assigned = False
        for gi, tokens in enumerate(group_tokens):
            for tok in tokens:
                if tok in sid or tok in path:
                    groups[gi].append(path)
                    assigned = True
                    break
            if assigned:
                break
        if not assigned:
            unmatched.append(path)

    if unmatched:
        print(
            f"  WARNING: {len(unmatched)} section(s) matched no group; "
            "appending to last group: " + ", ".join(unmatched),
            file=sys.stderr,
        )
        groups[-1].extend(unmatched)

    # Drop empty groups
    return [g for g in groups if g]


def parse_groups_spec(spec: str) -> list[list[str]] | None:
    """
    Parse a --groups SPEC string.  Returns a list of token-lists, or None if
    spec is a preset name.

    Format: "token+token+...,token+token+...,..."
    Preset names: "default3", "default4"
    """
    spec = spec.strip()
    if spec in GROUP_PRESETS:
        return GROUP_PRESETS[spec]
    # Parse as comma-separated groups, each group is '+'-joined tokens
    raw_groups = [g.strip() for g in spec.split(",") if g.strip()]
    if not raw_groups:
        return None
    return [[t.strip() for t in g.split("+") if t.strip()] for g in raw_groups]


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(1)

    # Pull out --batch-size N, --groups SPEC, --tail-batch before positional parsing
    batch_size = DEFAULT_BATCH_SIZE
    groups_spec: str | None = None
    tail_batch = False
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
        elif args[i] == "--groups":
            if i + 1 >= len(args):
                print("ERROR: --groups requires a value", file=sys.stderr)
                sys.exit(1)
            groups_spec = args[i + 1]
            i += 2
        elif args[i] == "--tail-batch":
            tail_batch = True
            i += 1
        else:
            filtered_args.append(args[i])
            i += 1
    args = filtered_args

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

    # Determine active sections and split into batches
    active_sections = filter_sections(focus)
    if not active_sections:
        print(f"ERROR: focus '{focus}' matched no sections.", file=sys.stderr)
        sys.exit(1)

    if groups_spec is not None:
        group_tokens = parse_groups_spec(groups_spec)
        if group_tokens is None or not group_tokens:
            print(
                f"ERROR: --groups spec could not be parsed: {groups_spec!r}",
                file=sys.stderr,
            )
            sys.exit(1)
        batches = group_sections(active_sections, group_tokens)
        n_batches = len(batches)
        print(
            f"Using logical groups: {n_batches} group(s) "
            f"({', '.join(str(len(b)) + ' sections' for b in batches)})"
        )
    else:
        batches = chunk_sections(active_sections, batch_size)
        n_batches = len(batches)

    use_batch_suffix = n_batches > 1

    if use_batch_suffix and groups_spec is None:
        print(
            f"Splitting {len(active_sections)} sections into {n_batches} batches of ≤{batch_size}"
        )

    # Read context documents and templates once
    context = {key: read_file(path) for key, path in CONTEXT_FILES.items()}
    template = read_file(TEMPLATE_FILE)
    tail_template = read_file(TAIL_TEMPLATE_FILE)

    # Output directory
    out_dir = REPO / "reviews" / round_id / ".prepared"
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_entries = []

    for batch_idx, batch_sections in enumerate(batches, start=1):
        sections_block = build_sections_block(batch_sections)
        batch_ids = section_ids(batch_sections)

        # For informed mode, filter prior-round context to this batch's sections.
        # include_tail=False: tail content (proposals, open questions, etc.) is
        # reserved for the dedicated tail batch prompt.
        if mode == "informed":
            prior_rounds_block = build_prior_rounds_block(
                round_id, batch_section_ids=batch_ids, include_tail=False
            )
            prior_tokens = estimate_tokens(prior_rounds_block)
        else:
            prior_rounds_block = ""
            prior_tokens = 0

        prompt = fill_template(
            template=template,
            round_id=round_id,
            commit=commit,
            mode=mode,
            today=today,
            context=context,
            sections_block=sections_block,
            prior_rounds_block=prior_rounds_block,
        )
        estimated_tokens = estimate_tokens(prompt)

        batch_label = f"batch {batch_idx}/{n_batches}" if use_batch_suffix else "full"
        print(
            f"  {batch_label}: ~{estimated_tokens:,} tokens "
            f"({len(batch_sections)} sections"
            + (f", ~{prior_tokens:,} prior-round tokens" if prior_tokens else "")
            + ")"
        )
        if estimated_tokens > 70_000:
            print(
                f"  WARNING: {batch_label} exceeds 70k tokens — risk of context compaction",
                file=sys.stderr,
            )

        for reviewer in reviewers:
            if use_batch_suffix:
                filename = f"{reviewer}-batch-{batch_idx}.md"
            else:
                filename = f"{reviewer}.md"
            out_path = out_dir / filename
            out_path.write_text(prompt, encoding="utf-8")

            manifest_entries.append(
                {
                    "type": "section",
                    "file": str(out_path.relative_to(REPO)),
                    "reviewer": reviewer,
                    "batch": batch_idx if use_batch_suffix else None,
                    "total_batches": n_batches if use_batch_suffix else None,
                    "section_ids": batch_ids,
                    "round": round_id,
                    "mode": mode,
                    "commit": commit,
                    "date": today,
                    "estimated_tokens": estimated_tokens,
                }
            )

            print(f"    wrote {out_path.relative_to(REPO)}")

    # Tail batch — cross-cutting, no section content
    if tail_batch:
        tail_batch_idx = n_batches + 1
        tail_batch_label = f"batch {tail_batch_idx} (tail)"

        if mode == "informed":
            tail_prior_block = build_tail_prior_rounds_block(round_id)
            tail_prior_tokens = estimate_tokens(tail_prior_block)
        else:
            tail_prior_block = ""
            tail_prior_tokens = 0

        tail_prompt = fill_template(
            template=tail_template,
            round_id=round_id,
            commit=commit,
            mode=mode,
            today=today,
            context=context,
            sections_block="",  # no sections in tail batch
            prior_rounds_block=tail_prior_block,
        )
        tail_estimated_tokens = estimate_tokens(tail_prompt)

        print(
            f"  {tail_batch_label}: ~{tail_estimated_tokens:,} tokens"
            + (
                f" (~{tail_prior_tokens:,} prior-round tokens)"
                if tail_prior_tokens
                else ""
            )
        )
        if tail_estimated_tokens > 70_000:
            print(
                f"  WARNING: {tail_batch_label} exceeds 70k tokens — risk of context compaction",
                file=sys.stderr,
            )

        for reviewer in reviewers:
            filename = f"{reviewer}-batch-tail.md"
            out_path = out_dir / filename
            out_path.write_text(tail_prompt, encoding="utf-8")

            manifest_entries.append(
                {
                    "type": "tail",
                    "file": str(out_path.relative_to(REPO)),
                    "reviewer": reviewer,
                    "batch": "tail",
                    "total_batches": tail_batch_idx,
                    "section_ids": [],
                    "round": round_id,
                    "mode": mode,
                    "commit": commit,
                    "date": today,
                    "estimated_tokens": tail_estimated_tokens,
                }
            )

            print(f"    wrote {out_path.relative_to(REPO)}")

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps({"status": "in_progress", "entries": manifest_entries}, indent=2),
        encoding="utf-8",
    )
    print(f"  wrote {manifest_path.relative_to(REPO)}")

    total_prompts = len(manifest_entries)
    tail_note = " + 1 tail batch" if tail_batch else ""
    print(
        f"\nPrepared {total_prompts} prompt(s) "
        f"({len(reviewers)} reviewer(s) × {n_batches} batch(es){tail_note})."
    )


if __name__ == "__main__":
    main()
