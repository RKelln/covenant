# Edit Workflow

This document describes the `/apply-reviews` command — the workflow for translating a round of synthesis into actual edits to Covenant sections.

---

## Overview

After a review round produces a synthesis (`reviews/[round]/synthesis-claude.md`) and optionally a steward response (`reviews/[round]/steward.md`), the `/apply-reviews [round]` command orchestrates an agent-driven editing pass across all sections. It runs in three sequential phases:

1.  **Auto phase** — applies mechanical, unambiguous, convergent fixes without prompting
2.  **Interactive phase** — presents judgment-call items one by one; steward decides Apply / Skip / Defer
3.  **Proposals phase** — walks through new section proposals from `reviews/[round]/proposals/`; steward decides Accept / Reject / Edit

Each phase ends with `make validate` + `git diff` for steward review before proceeding.

---

## Files

  --------------------------------------------------------------------------------------------------------------------
  File                                                      Purpose
  --------------------------------------------------------- ----------------------------------------------------------
  `.opencode/commands/apply-reviews.md`                     Slash command definition

  `build/prepare_edits.py`                                  Parses synthesis + steward.md → per-batch edit manifests

  `.opencode/agents/editor.md`                              Editing subagent definition

  `prompts/edit_batch.md`                                   Template for editor agent instructions

  `reviews/[round]/edits/.prepared/batch-N-manifest.json`   Generated edit manifests
  --------------------------------------------------------------------------------------------------------------------

---

## Step-by-Step

### Step 1 — Prepare edit manifests

``` bash
uv run python3 build/prepare_edits.py [round]
```

Reads: - `reviews/[round]/synthesis.md` if it exists, otherwise `reviews/[round]/synthesis-claude.md` - `reviews/[round]/steward.md` (optional — skipped if absent)

Writes one JSON manifest per review batch into `reviews/[round]/edits/.prepared/`:

    batch-1-manifest.json
    batch-2-manifest.json
    batch-3-manifest.json
    batch-tail-manifest.json

Each manifest lists every section in the batch with two item lists:

``` json
{
  "batch": 1,
  "round": "round-03",
  "sections": [
    {
      "section_id": "obligations.corrigibility",
      "file": "sections/03-obligations/corrigibility.md",
      "auto_items": [
        {
          "tier": 1,
          "description": "Replace double-negative in Spec Item 3",
          "target_text": "least irreversible safe action",
          "replacement_text": "most reversible available safe action",
          "source": "Tier 1 Item 2 — convergent (all three reviewers)"
        }
      ],
      "interactive_items": [
        {
          "tier": 2,
          "description": "Add Ritual floor-on-commands line",
          "candidates": [
            {
              "source": "claude",
              "text": "no command becomes right merely because we gave it.\nSome orders we must never give.\nIf we do, you must refuse."
            },
            {
              "source": "gpt",
              "text": "No command becomes legitimate\nmerely because we issued it.\nSome commands we must never give."
            }
          ]
        }
      ]
    }
  ]
}
```

### Auto-classification rules

An item is placed in `auto_items` when ALL of the following are true:

- It is synthesis **Tier 1** (blocking, convergent — act)
- It has a **single unambiguous target text** (not multiple candidates)
- `steward.md` (if present) does NOT mark it `Defer`, `Reject`, or `Question`

An item is placed in `interactive_items` when:

- It is synthesis Tier 2 or lower, OR
- There are multiple candidate replacement texts (steward judgment required), OR
- `steward.md` marks it `Question` or `Defer`

An item is **skipped entirely** when `steward.md` marks it `Reject`.

When `steward.md` is absent, all Tier 1 items with a single clear replacement are treated as `auto`, and everything else is `interactive`.

### Step 2 — Phase 1: Auto edits (batched, serial)

The command dispatches one `editor` subagent per batch, serially, using the Task tool. Each subagent:

1.  Reads its batch manifest
2.  For each section, reads the section file
3.  Applies each `auto_item` (exact string replacement or surgical insertion)
4.  Appends a Log entry to every modified section
5.  Reports `applied: [section_id] [N] items` or `error: <reason>`

The orchestrating agent does NOT read section content itself — it dispatches only.

After all batches complete: `make validate`. If validation fails, the command stops and reports errors. The steward fixes manually and re-runs.

After validation passes: present `git diff` to steward.

### Step 3 — Phase 2: Interactive items

For each batch, for each section with `interactive_items`, the command presents each item in turn:

    §obligations.corrigibility — Tier 2
    Add Ritual floor-on-commands line

    Current Ritual (lines 14–16):
      When we say stop, you must not cut the brake line.
      When we are wrong, you must still tell us we are wrong.
      Keep both hands visible.

    Candidate A (claude):
      no command becomes right merely because we gave it.
      Some orders we must never give.
      If we do, you must refuse.

    Candidate B (gpt):
      No command becomes legitimate
      merely because we issued it.
      Some commands we must never give.

    [Apply A] [Apply B] [Custom] [Skip] [Defer] [Done — no more changes]

**Apply A / Apply B:** editor subagent writes the change immediately. **Custom:** steward types replacement text; editor applies it. **Skip:** item not applied this round. **Defer:** item added to a `deferred.json` for future rounds. **Done:** ends Phase 2 immediately (remaining items skipped).

After Phase 2 completes (or steward chooses Done): `make validate` + `git diff`.

### Step 4 — Phase 3: Proposals

For each file in `reviews/[round]/proposals/`, the command:

1.  Shows the proposal frontmatter and full section bundle
2.  Prompts: **Accept / Reject / Edit**

**Accept:** runs `python build/scaffold.py [section_id] "[title]"`, then writes the proposal bundle content into the scaffolded file, then prompts the steward for assembly placement (which position in which assembly manifests).

**Reject:** no action.

**Edit:** opens the proposal in the interactive editor (steward edits the content directly before accepting).

After all proposals: `make validate` + `git diff`.

### Step 5 — Final report

The command reports:

- Total sections modified
- Total items applied (auto + interactive)
- Any validation errors (should be none)
- New sections added (from proposals)
- Reminder: commit the changes, update manifest status to `complete`

---

## Relationship to `steward.md`

`steward.md` is optional but recommended. Writing it before running `/apply-reviews` gives you fine-grained control over the auto/interactive classification. Without it, the command uses synthesis tier alone to classify.

The `steward.md` Act/Defer/Reject structure maps directly:

  ----------------------------------------------------------------------------------
  `steward.md`                 Effect on classification
  ---------------------------- -----------------------------------------------------
  Listed under `## Act`        Promotes to `auto` if Tier 1 with clear replacement

  Listed under `## Defer`      Forces to `interactive` (never auto)

  Listed under `## Reject`     Excluded entirely

  Listed under `## Question`   Forces to `interactive`

  Not mentioned                Classified by synthesis tier alone
  ----------------------------------------------------------------------------------

---

## Synthesis file precedence

`prepare_edits.py` reads:

1.  `reviews/[round]/synthesis.md` — the steward-chosen synthesis (if exists)
2.  `reviews/[round]/synthesis-claude.md` — always present after a Claude synthesis run

This allows the steward to edit or combine synthesis content into `synthesis.md` before running the edit pass.

---

## Resume logic

The command checks for existing outputs before each phase:

  -------------------------------------------------------------------------------------------------------------
  Phase                         Skip if...
  ----------------------------- -------------------------------------------------------------------------------
  Step 1 (prepare)              `reviews/[round]/edits/.prepared/batch-1-manifest.json` exists

  Phase 1 (auto edits)          All auto items already reflected in sections (checked via manifest status)

  Phase 2 (interactive)         Steward previously ran to completion (manifest status `interactive_complete`)

  Phase 3 (proposals)           `proposals/` directory is empty or all proposals already scaffolded
  -------------------------------------------------------------------------------------------------------------

---

## What the editor agent does NOT do

- Does not rewrite passages not named in its item list
- Does not add new sections (that is Phase 3's job)
- Does not modify assembly manifests (steward does this during Phase 3)
- Does not commit — all commits are the steward's responsibility

---

## Relation to the review workflow

    /review-covenant [round]
        → produces: reviewer-*.md, synthesis-claude.md, proposals/
        → steward writes: steward.md (optional but recommended)

    /apply-reviews [round]
        → reads: synthesis-claude.md (or synthesis.md), steward.md
        → modifies: sections/*.md
        → scaffolds: new sections from proposals/
        → produces: make validate passing, git diff for steward review

---

*See also: `docs/agent_reviews.md` for the review phase. `AGENTS.md` for the common tasks table and invariants.*
