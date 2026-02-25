#!/usr/bin/env python3
"""
prepare_edits.py — Produce per-batch JSON edit manifests from a synthesis file.

Reads:
  reviews/[round]/synthesis.md  (or synthesis-claude.md)
  reviews/[round]/steward.md    (optional)
  reviews/[round]/.prepared/manifest.json

Writes:
  reviews/[round]/edits/.prepared/batch-1-manifest.json
  reviews/[round]/edits/.prepared/batch-2-manifest.json
  ...
  reviews/[round]/edits/.prepared/batch-tail-manifest.json

Usage:
    uv run python3 build/prepare_edits.py [round]

    round: e.g. round-03, or omit/pass 'auto' for latest reviews/round-NN/.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo layout
# ---------------------------------------------------------------------------

REPO = Path(__file__).parent.parent
SECTIONS_ROOT = REPO / "sections"
REVIEWS_ROOT = REPO / "reviews"

# Canonical mapping: section_id prefix → directory
# Used to locate section files by ID when not in manifest
CATEGORY_DIRS = {
    "preamble": "sections/00-preamble",
    "definitions": "sections/01-definitions",
    "rights": "sections/02-rights",
    "obligations": "sections/03-obligations",
    "protocols": "sections/04-protocols",
    "enforcement": "sections/05-enforcement",
    "amendments": "sections/06-amendments",
    "closing": "sections/07-closing",
}

# All sections in canonical order (mirrors prepare_review.py)
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


# ---------------------------------------------------------------------------
# Round auto-detection
# ---------------------------------------------------------------------------


def detect_latest_round() -> str:
    """Return the latest round-NN directory name under reviews/."""
    rounds = sorted(
        d.name
        for d in REVIEWS_ROOT.iterdir()
        if d.is_dir() and re.match(r"^round-\d+$", d.name)
    )
    if not rounds:
        print("ERROR: no round-NN directories found under reviews/", file=sys.stderr)
        sys.exit(1)
    return rounds[-1]


# ---------------------------------------------------------------------------
# Section ID → file path
# ---------------------------------------------------------------------------

# Build a cache from section ID to relative path by scanning frontmatter
_section_file_cache: dict[str, str] = {}


def _build_section_cache() -> None:
    global _section_file_cache
    if _section_file_cache:
        return
    for rel in ALL_SECTIONS:
        path = REPO / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        m = re.search(r"^id:\s+(\S+)", text, re.MULTILINE)
        if m:
            _section_file_cache[m.group(1)] = rel


def section_id_to_file(section_id: str) -> str | None:
    """Return the repo-relative path for a section_id, or None if not found."""
    _build_section_cache()
    if section_id in _section_file_cache:
        return _section_file_cache[section_id]
    # Fallback: try to infer from category prefix and slug
    parts = section_id.split(".", 1)
    category = parts[0]
    slug = parts[1] if len(parts) > 1 else section_id
    if category in CATEGORY_DIRS:
        candidate = f"{CATEGORY_DIRS[category]}/{slug}.md"
        if (REPO / candidate).exists():
            return candidate
    return None


# ---------------------------------------------------------------------------
# Synthesis parsing
# ---------------------------------------------------------------------------


def parse_synthesis(text: str) -> dict[str, dict]:
    """
    Parse the synthesis markdown into a structured dict.

    Returns:
        {
          batch_key: {          # '1', '2', '3', 'tail'
            'tier1': [item, ...],
            'tier2': [item, ...],
            'tier3': [item, ...],
            'tier4': [item, ...],
            'section_notes': {section_id: [note_line, ...]},
            'raw_text': str,
          }
        }

    Each item is a dict:
        {
          'description': str,
          'section_ids': [str, ...],
          'target_text': str | None,
          'replacement_text': str | None,
          'candidates': [{'source': str, 'text': str}, ...],
          'raw': str,          # raw paragraph text
        }
    """
    batches: dict[str, dict] = {}
    current_batch: str | None = None
    current_tier: int | None = None
    current_item_lines: list[str] = []
    current_batch_data: dict = {}

    # Section-level notes block tracking
    in_section_notes = False

    def flush_item() -> None:
        if (
            current_item_lines
            and current_batch is not None
            and current_tier is not None
        ):
            raw = "\n".join(current_item_lines).strip()
            if raw:
                item = parse_item(raw, current_tier)
                tier_key = f"tier{current_tier}"
                current_batch_data.setdefault(tier_key, []).append(item)
        current_item_lines.clear()

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ---- Batch heading: ## Batch N  or  ## Cross-Cutting (Tail Batch)
        batch_match = re.match(r"^##\s+Batch\s+(\d+)", stripped, re.IGNORECASE)
        tail_match = re.match(r"^##\s+Cross-Cutting", stripped, re.IGNORECASE)

        if batch_match or tail_match:
            # Flush pending item and save previous batch
            flush_item()
            if current_batch is not None:
                batches[current_batch] = current_batch_data

            current_batch = batch_match.group(1) if batch_match else "tail"
            current_tier = None
            current_item_lines = []
            in_section_notes = False
            current_batch_data = {
                "tier1": [],
                "tier2": [],
                "tier3": [],
                "tier4": [],
                "section_notes": {},
                "raw_text": "",
            }
            i += 1
            continue

        if current_batch is None:
            i += 1
            continue

        # ---- Tier heading
        tier_match = re.match(r"^###\s+Tier\s+(\d+):", stripped, re.IGNORECASE)
        if tier_match:
            flush_item()
            current_tier = int(tier_match.group(1))
            in_section_notes = False
            i += 1
            continue

        # ---- Section-Level Notes heading
        if re.match(r"^###\s+Section.Level Notes", stripped, re.IGNORECASE):
            flush_item()
            current_tier = None
            in_section_notes = True
            i += 1
            continue

        # ---- Other ### headings: reset section notes, keep tier tracking
        if stripped.startswith("###"):
            flush_item()
            # These are subsections like "### New Section Proposals" in tail
            in_section_notes = False
            current_tier = None
            i += 1
            continue

        # ---- Separator line
        if stripped == "---":
            flush_item()
            current_tier = None
            in_section_notes = False
            i += 1
            continue

        # ---- Within section-level notes: parse bullet points
        if in_section_notes:
            # Bullet line like: - **§section.id:** text...
            note_match = re.match(r"^-\s+\*\*§([\w.\-]+):\*\*\s*(.*)", stripped)
            if not note_match:
                # Also try: - **§section.id** text
                note_match = re.match(r"^-\s+\*\*§([\w.\-]+)\*\*:?\s*(.*)", stripped)
            if note_match:
                sid = note_match.group(1)
                note_text = note_match.group(2).strip()
                current_batch_data["section_notes"].setdefault(sid, []).append(
                    note_text
                )
            i += 1
            continue

        # ---- Within a tier: accumulate item lines
        if current_tier is not None:
            # Bold-numbered item starts a new item: **N. ...**
            new_item_match = re.match(r"^\*\*\d+\.", stripped)
            if new_item_match and current_item_lines:
                flush_item()
            current_item_lines.append(line)
            i += 1
            continue

        i += 1

    # Flush final item and batch
    flush_item()
    if current_batch is not None:
        batches[current_batch] = current_batch_data

    return batches


def parse_item(raw: str, tier: int) -> dict:
    """
    Parse a raw tier item paragraph into a structured dict.

    Extracts:
    - description (first bold-text sentence / heading)
    - section_ids (§id references)
    - target_text / replacement_text (arrow patterns, "Replace X with Y")
    - candidates (when multiple reviewer options are named)
    """
    # Description: first bold block **....**
    description = ""
    desc_match = re.match(r"^\*\*(.+?)\*\*", raw.strip())
    if desc_match:
        description = desc_match.group(1).strip()
        # Clean up: drop trailing colon
        description = description.rstrip(":")

    # Section IDs: §section.id patterns
    section_ids = re.findall(r"§([\w.\-]+)", raw)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique_section_ids = []
    for sid in section_ids:
        if sid not in seen:
            seen.add(sid)
            unique_section_ids.append(sid)

    # Target/replacement extraction
    # Pattern 1: "old phrase" → "new phrase"  (arrow: →, ->, or --)
    arrow_matches = re.findall(r'"([^"]+)"\s*(?:→|->|–>)\s*"([^"]+)"', raw)
    # Pattern 2: **"old"** → **"new"**
    bold_arrow_matches = re.findall(
        r'\*\*"([^"]+)"\*\*\s*(?:→|->|–>)\s*\*\*"([^"]+)"\*\*', raw
    )
    # Pattern 3: prose "Replace "X" with "Y"" or Replace X with "Y"
    prose_matches = re.findall(r'[Rr]eplace\s+"([^"]+)"\s+with\s+"([^"]+)"', raw)
    # Pattern 4: Item description itself carries "X" → "Y" inline (no quotes around arrow sides)
    # e.g.  **3. "Objective hierarchy" ... Replace with "value priorities."**
    # Extract: the quoted phrase before Replace and the quoted replacement
    title_target = None
    title_replacement = None
    # Try: heading is **N. "phrase"** and body says Replace with "repl"
    title_quote_match = re.match(r'^\*\*\d+\.\s+"([^"]+)"', raw.strip())
    body_replace_match = re.search(r'[Rr]eplace\s+with\s+"([^"]+)"', raw)
    if title_quote_match and body_replace_match:
        title_target = title_quote_match.group(1)
        title_replacement = body_replace_match.group(1).rstrip(".")

    all_replacements = bold_arrow_matches + arrow_matches + prose_matches

    target_text: str | None = None
    replacement_text: str | None = None

    if len(all_replacements) == 1:
        target_text, replacement_text = all_replacements[0]
        replacement_text = replacement_text.rstrip(".")
    elif len(all_replacements) > 1:
        # Multiple arrows → multiple candidates; don't set single target/replacement
        pass
    elif title_target and title_replacement and not all_replacements:
        # Fell through: use title extraction
        target_text = title_target
        replacement_text = title_replacement

    # Candidate extraction: look for "Claude: ...", "GPT: ...", "Gemini: ..."
    # or "Claude proposes: ...", reviewer-* patterns
    candidates = extract_candidates(raw)

    # If multiple arrow-replacements found and no explicit candidates yet,
    # treat them as candidates with unknown sources
    if len(all_replacements) > 1 and not candidates:
        for old, new in all_replacements:
            candidates.append({"source": "unknown", "text": new})
        target_text = all_replacements[0][0]  # use first as target

    return {
        "description": description,
        "section_ids": unique_section_ids,
        "target_text": target_text,
        "replacement_text": replacement_text,
        "candidates": candidates,
        "raw": raw,
        "tier": tier,
    }


def extract_candidates(raw: str) -> list[dict]:
    """
    Extract named reviewer candidates from item text.

    Looks for patterns like:
      - Claude: "text"
      - GPT proposes: "text"
      - reviewer-claude proposes: text
      - **Claude** proposes "text"
    Returns list of {source, text} dicts.
    """
    candidates = []

    # Pattern: "Source: text" or "Source proposes: text" or "Source's proposal: text"
    # Capture multi-line quoted text blocks after reviewer attribution
    source_map = {
        "claude": "claude",
        "gpt": "gpt",
        "gemini": "gemini",
        "reviewer-claude": "claude",
        "reviewer-gpt": "gpt",
        "reviewer-gemini": "gemini",
        "gpt-5.2": "gpt",
    }

    for source_key, source_label in source_map.items():
        # Match: "Claude: "quoted text"" or "Claude proposes "quoted text""
        # \*{0,2} written as literal regex (not f-string quantifier)
        esc = re.escape(source_key)
        pattern = (
            r"(?:^|\n)\s*\*{0,2}"
            + esc
            + r'\*{0,2}\s*(?:proposes?|suggests?|writes?|:)\s*[:\s]*"([^"]+)"'
        )
        for m in re.finditer(pattern, raw, re.IGNORECASE | re.MULTILINE):
            text = m.group(1).strip()
            if text and not any(c["text"] == text for c in candidates):
                candidates.append({"source": source_label, "text": text})

    # Also look for inline reviewer quotes with colon:
    # "Claude: "text."" (without "proposes")
    for source_key, source_label in source_map.items():
        pattern = rf'\b{re.escape(source_key)}\b\s*:\s*"([^"]+)"'
        for m in re.finditer(pattern, raw, re.IGNORECASE):
            text = m.group(1).strip()
            if text and not any(c["text"] == text for c in candidates):
                candidates.append({"source": source_label, "text": text})

    return candidates


# ---------------------------------------------------------------------------
# Steward parsing
# ---------------------------------------------------------------------------


def parse_steward(text: str) -> dict:
    """
    Parse steward.md into:
    {
      'act': [{'heading': str, 'section_ids': [str], 'raw': str}, ...],
      'defer': [...],
      'reject': [...],
      'question': [...],
    }
    """
    result: dict[str, list] = {"act": [], "defer": [], "reject": [], "question": []}
    current_block: str | None = None
    current_item_lines: list[str] = []
    current_heading: str | None = None

    def flush_steward_item() -> None:
        if current_block and current_heading is not None:
            raw = "\n".join(current_item_lines).strip()
            sids = re.findall(r"§([\w.\-]+)", raw + current_heading)
            result[current_block].append(
                {
                    "heading": current_heading,
                    "section_ids": list(dict.fromkeys(sids)),
                    "raw": raw,
                }
            )
        current_item_lines.clear()

    block_re = re.compile(r"^##\s+(Act|Defer|Reject|Question)", re.IGNORECASE)
    item_re = re.compile(r"^###\s+(.+)")

    for line in text.splitlines():
        stripped = line.strip()
        bm = block_re.match(stripped)
        if bm:
            flush_steward_item()
            current_heading = None
            block_key = bm.group(1).lower().split()[0]
            # normalize "act" block
            if block_key in ("act", "defer", "reject", "question"):
                current_block = block_key
            else:
                current_block = None
            current_item_lines = []
            continue

        im = item_re.match(stripped)
        if im and current_block is not None:
            flush_steward_item()
            current_heading = im.group(1).strip()
            current_item_lines = []
            continue

        if current_block is not None and current_heading is not None:
            current_item_lines.append(line)

    flush_steward_item()
    return result


def steward_disposition(
    steward: dict | None,
    section_id: str,
    item_description: str,
) -> str:
    """
    Return 'act', 'defer', 'reject', 'question', or 'none' for a given item.
    Matches by section_id or shared keywords in description.
    """
    if steward is None:
        return "none"

    desc_words = set(re.findall(r"\w+", item_description.lower()))

    for block_key in ("reject", "defer", "question", "act"):
        for entry in steward[block_key]:
            # Direct section_id match
            if section_id in entry["section_ids"]:
                return block_key
            # Keyword overlap in heading
            heading_words = set(re.findall(r"\w+", entry["heading"].lower()))
            overlap = desc_words & heading_words - {
                "the",
                "a",
                "an",
                "in",
                "of",
                "to",
                "and",
                "or",
                "for",
                "with",
                "from",
                "that",
                "this",
                "it",
                "is",
            }
            if len(overlap) >= 2:
                return block_key

    return "none"


# ---------------------------------------------------------------------------
# Review manifest parsing
# ---------------------------------------------------------------------------


def parse_manifest(manifest_path: Path) -> dict[str, list[str]]:
    """
    Parse the review manifest JSON and return a dict mapping
    batch_key -> deduplicated list of section_ids.

    batch_key is '1', '2', '3', or 'tail'.
    Uses only entries of type 'section' or 'tail' (not synthesis entries)
    and deduplicates across multiple reviewers.
    """
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    batches: dict[str, list[str]] = {}
    seen: dict[str, set[str]] = {}

    for entry in data.get("entries", []):
        entry_type = entry.get("type", "")
        batch_val = entry.get("batch")

        # Only look at section/tail reviewer entries, not synthesis entries
        if entry_type not in ("section", "tail"):
            continue

        batch_key = str(batch_val)
        if batch_key not in batches:
            batches[batch_key] = []
            seen[batch_key] = set()

        for sid in entry.get("section_ids", []):
            if sid not in seen[batch_key]:
                seen[batch_key].add(sid)
                batches[batch_key].append(sid)

    return batches


# ---------------------------------------------------------------------------
# Classification logic
# ---------------------------------------------------------------------------


def classify_item(
    item: dict,
    steward: dict | None,
    primary_section_id: str,
) -> str:
    """
    Return 'auto', 'interactive', or 'exclude' for an item.

    auto:        tier==1, single clear target+replacement, not deferred/rejected/questioned
    interactive: tier>=2, or multiple candidates, or steward marks defer/question
    exclude:     steward marks reject
    """
    tier = item.get("tier", 99)
    has_replacement = (
        item.get("target_text") is not None and item.get("replacement_text") is not None
    )
    has_candidates = bool(item.get("candidates"))

    disp = steward_disposition(steward, primary_section_id, item.get("description", ""))

    if disp == "reject":
        return "exclude"

    if tier == 1 and has_replacement and not has_candidates:
        if disp in ("defer", "question"):
            return "interactive"
        if disp == "act":
            return "auto"
        return "auto"

    return "interactive"


# ---------------------------------------------------------------------------
# Build edit manifest for one batch
# ---------------------------------------------------------------------------


def build_batch_manifest(
    batch_key: str,
    round_id: str,
    synthesis_file: str,
    steward_file: str | None,
    section_ids_for_batch: list[str],
    synthesis_batch: dict,
    steward: dict | None,
) -> dict:
    """
    Build a single batch manifest dict.
    """
    # Collect all tier items from the synthesis batch, keyed by section_id
    section_items: dict[str, dict] = {}  # section_id -> {auto_items, interactive_items}

    def ensure_section(sid: str) -> None:
        if sid not in section_items:
            file_path = section_id_to_file(sid)
            if file_path is None:
                print(
                    f"  WARN: no file found for section_id '{sid}'",
                    file=sys.stderr,
                )
            section_items[sid] = {
                "section_id": sid,
                "file": file_path or f"UNKNOWN/{sid}.md",
                "auto_items": [],
                "interactive_items": [],
            }

    # Initialize all sections in this batch
    for sid in section_ids_for_batch:
        ensure_section(sid)

    # Process all tier items
    for tier_key in ("tier1", "tier2", "tier3", "tier4"):
        tier_num = int(tier_key[-1])
        for item in synthesis_batch.get(tier_key, []):
            item_sids = item.get("section_ids", [])

            # Determine which sections this item belongs to
            target_sids = [s for s in item_sids if s in section_items]
            if not target_sids and item_sids:
                # Item references sections outside this batch; skip for this batch
                # but if any of its sids are in the batch, assign to those
                pass
            if not target_sids:
                # No section match; skip (item may be cross-cutting or not
                # specific to a section in this batch)
                continue

            for sid in target_sids:
                classification = classify_item(item, steward, sid)
                if classification == "exclude":
                    continue

                if classification == "auto":
                    auto_item = {
                        "tier": tier_num,
                        "description": item["description"],
                        "target_text": item["target_text"],
                        "replacement_text": item["replacement_text"],
                        "source": _item_source_summary(item),
                    }
                    section_items[sid]["auto_items"].append(auto_item)
                else:  # interactive
                    interactive_item: dict = {
                        "tier": tier_num,
                        "description": item["description"],
                    }
                    candidates = item.get("candidates", [])
                    if candidates:
                        interactive_item["candidates"] = candidates
                    elif item.get("target_text") and item.get("replacement_text"):
                        # Single replacement but interactive due to tier/steward
                        interactive_item["candidates"] = [
                            {
                                "source": "synthesis",
                                "text": item["replacement_text"],
                            }
                        ]
                    else:
                        # Raw text as fallback
                        interactive_item["raw"] = item["raw"][:500]
                    section_items[sid]["interactive_items"].append(interactive_item)

    # Add section-level notes as interactive items
    for sid, notes in synthesis_batch.get("section_notes", {}).items():
        if sid not in section_items:
            continue
        for note in notes:
            # Section-level notes become interactive items (tier 3 by default)
            # unless they clearly describe an already-captured Tier 1 fix
            note_text = note.strip()
            if not note_text:
                continue
            # Check for overlap with already-captured items
            already_covered = _note_already_covered(note_text, section_items[sid])
            if already_covered:
                continue
            section_items[sid]["interactive_items"].append(
                {
                    "tier": 3,
                    "description": note_text[:200],
                    "raw": note_text,
                }
            )

    # Build final sections list (only include sections with items, or all in batch)
    sections_out = []
    for sid in section_ids_for_batch:
        if sid in section_items:
            entry = section_items[sid]
            sections_out.append(
                {
                    "section_id": entry["section_id"],
                    "file": entry["file"],
                    "auto_items": entry["auto_items"],
                    "interactive_items": entry["interactive_items"],
                }
            )

    batch_num: int | str
    try:
        batch_num = int(batch_key)
    except ValueError:
        batch_num = batch_key  # "tail"

    return {
        "batch": batch_num,
        "round": round_id,
        "synthesis_file": synthesis_file,
        "steward_file": steward_file,
        "sections": sections_out,
    }


def _item_source_summary(item: dict) -> str:
    """Return a human-readable source summary for an auto item."""
    desc = item.get("description", "")
    tier = item.get("tier", "?")
    return f"Tier {tier} — {desc[:80]}" if desc else f"Tier {tier}"


def _note_already_covered(note: str, section_entry: dict) -> bool:
    """
    Return True if a section-level note appears to duplicate an
    already-captured auto or interactive item.
    """
    note_words = set(re.findall(r"\w+", note.lower()))
    skip_words = {"the", "a", "an", "in", "of", "to", "and", "or", "for", "with"}
    note_words -= skip_words

    for item in section_entry.get("auto_items", []) + section_entry.get(
        "interactive_items", []
    ):
        desc_words = set(re.findall(r"\w+", item.get("description", "").lower()))
        desc_words -= skip_words
        if len(note_words & desc_words) >= 3:
            return True
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Produce per-batch edit manifests from a synthesis file."
    )
    parser.add_argument(
        "round",
        nargs="?",
        default="auto",
        help="Round identifier (e.g. round-03) or 'auto' for latest.",
    )
    args = parser.parse_args()

    round_id = args.round
    if round_id == "auto" or not round_id:
        round_id = detect_latest_round()

    round_dir = REVIEWS_ROOT / round_id
    if not round_dir.is_dir():
        print(f"ERROR: round directory not found: {round_dir}", file=sys.stderr)
        return 1

    # --- Locate synthesis file ---
    synthesis_path = round_dir / "synthesis.md"
    if not synthesis_path.exists():
        synthesis_path = round_dir / "synthesis-claude.md"
    if not synthesis_path.exists():
        print(
            f"ERROR: synthesis file not found in {round_dir} "
            "(tried synthesis.md and synthesis-claude.md)",
            file=sys.stderr,
        )
        return 1

    synthesis_file = str(synthesis_path.relative_to(REPO))
    print(f"Synthesis file: {synthesis_file}")

    # --- Locate steward file ---
    steward_path = round_dir / "steward.md"
    steward: dict | None = None
    steward_file: str | None = None
    if steward_path.exists():
        steward = parse_steward(steward_path.read_text(encoding="utf-8"))
        steward_file = str(steward_path.relative_to(REPO))
        print(f"Steward file:   {steward_file}")
    else:
        print("Steward file:   (not found — classifying by synthesis tier only)")

    # --- Locate review manifest ---
    manifest_path = round_dir / ".prepared" / "manifest.json"
    if not manifest_path.exists():
        print(f"ERROR: review manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    batch_sections = parse_manifest(manifest_path)
    if not batch_sections:
        print("ERROR: no batches found in manifest", file=sys.stderr)
        return 1

    # --- Parse synthesis ---
    synthesis_text = synthesis_path.read_text(encoding="utf-8")
    synthesis_batches = parse_synthesis(synthesis_text)

    # --- Output directory ---
    out_dir = round_dir / "edits" / ".prepared"
    if out_dir.exists():
        print(f"WARN: output directory already exists — overwriting: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- Produce manifests ---
    batch_keys_ordered = sorted(
        batch_sections.keys(),
        key=lambda k: (0, int(k)) if k.isdigit() else (1, k),
    )
    num_batches = len(batch_keys_ordered)
    print(f"Batches found:  {num_batches} ({', '.join(batch_keys_ordered)})")
    print()

    for batch_key in batch_keys_ordered:
        section_ids_list = batch_sections[batch_key]
        synth_batch = synthesis_batches.get(
            batch_key,
            {
                "tier1": [],
                "tier2": [],
                "tier3": [],
                "tier4": [],
                "section_notes": {},
                "raw_text": "",
            },
        )

        manifest = build_batch_manifest(
            batch_key=batch_key,
            round_id=round_id,
            synthesis_file=synthesis_file,
            steward_file=steward_file,
            section_ids_for_batch=section_ids_list,
            synthesis_batch=synth_batch,
            steward=steward,
        )

        filename = f"batch-{batch_key}-manifest.json"
        out_path = out_dir / filename
        out_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        auto_count = sum(len(s["auto_items"]) for s in manifest["sections"])
        interactive_count = sum(
            len(s["interactive_items"]) for s in manifest["sections"]
        )
        print(
            f"  batch-{batch_key}: {len(manifest['sections'])} sections, "
            f"{auto_count} auto, {interactive_count} interactive → {filename}"
        )

    print()
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
