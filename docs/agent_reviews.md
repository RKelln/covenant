# Agent Review Process

> **What this document is:** A description of how AI agents review and contribute to Covenant across multiple rounds. It covers the directory structure, the workflow, and the roles involved.

---

## Overview

Covenant is shaped by multiple AI models reviewing the same draft independently, followed by human-steward synthesis and revision. This process is designed to surface genuine insight, productive disagreement, and perspectives that no single author — human or machine — can provide alone.

The process is parallel-then-synthesize: models review independently first, then are shown each other's contributions in subsequent rounds. This prevents ordering effects in early rounds and enables genuine deliberation in later ones.

---

## Directory Structure

    /reviews/
      /round-01/
        .prepared/
          manifest.json        ← status: "in_progress" | "complete"
          reviewer-claude.md   ← prepared prompt (input)
          reviewer-gpt.md
          reviewer-gemini.md
        claude-4.6-opus.md     ← assembled review with provenance frontmatter
        gpt-5.2.md
        gemini-3-pro.md
        synthesis.md           ← written by steward; presence marks round complete
        COMMIT_MSG.txt         ← generated commit message draft
        /proposals/
          claude-4.6-opus--rights.ecological.md
          gpt-5.2--obligations.cultural-integrity.md
      /round-02/
        ...

A round is **in progress** until `synthesis.md` exists. Its absence is the signal that the round is not yet complete. The manifest's `status` field reflects this: `prepare_review.py` writes `"in_progress"`; it is the steward's responsibility to update it to `"complete"` after committing.

### Reviews

Each model's review is a single Markdown file named after the model. All reviews from a round live in the same directory on `main`. They are never on separate branches.

This makes comparison trivial: open the files side by side, search for a section ID across all of them, and see what every model said without switching branches or resolving merge conflicts.

### Proposals

When a model proposes a new section or a major structural change, the full section bundle goes in the `/proposals/` subdirectory. The filename convention is `[model-name]--[section.id].md`.

Proposals use the standard section bundle format (frontmatter, Ritual, Spec, Digest, Log) so they can be evaluated as real sections and moved into `/sections/` if accepted.

### Synthesis

After all reviews for a round are in, a human steward writes `synthesis.md`. This document maps each section to the feedback it received, identifies convergence and divergence across models, and records the editorial decisions made.

---

## Workflow

### Round 1: Independent Review

1.  Stewards select the draft version to review and prepare the review prompt with round context filled in (round number, draft version, mode: independent, no prior reviews).

2.  Each model receives:

    -   The current draft (all sections)
    -   `docs/writing_context.md`
    -   `docs/good_ritual_writing_guide.md`
    -   `docs/style_guide.md`
    -   `docs/agent_reviews.md` (this document)
    -   The review prompt with round context

3.  Each model produces its review independently. Models do not see each other's output.

4.  Reviews are committed to `/reviews/round-01/` on `main`. Any proposed new sections go in `/reviews/round-01/proposals/`.

5.  A steward reads all reviews and writes `synthesis.md`:

    -   Where models **converge**: high-confidence signal. Note the shared assessment and the proposed direction.
    -   Where models **diverge**: genuine editorial question. Note the disagreement, the strongest arguments on each side, and the steward's decision (or deferral).
    -   Where a single model raises something no other model noticed: flag for steward judgment. Unique observations are often the most valuable — or the most idiosyncratic. The steward decides which.

### Revision Pass

6.  A steward (human or agent acting on the synthesis) revises the Covenant sections. Changes are committed to `main` with a message referencing the review round:

        Revise sections per round-01 synthesis

        See /reviews/round-01/synthesis.md for rationale.

### Round 2: Informed Review

7.  Stewards prepare the review prompt with updated context: mode: informed, prior reviews listed, synthesis provided.

    Only the immediately preceding round is included as prior context. Earlier rounds are omitted — they refer to a different version of the text and add noise rather than signal.

8.  Each model receives:

    -   The revised draft
    -   All round-01 reviews
    -   The round-01 synthesis
    -   The same project documents as before
    -   The review prompt with updated round context

9.  Models may now respond to each other's assessments — agree, disagree, build on proposals. The prompt asks them to focus on what remains unresolved.

10. Reviews go into `/reviews/round-02/`. Steward writes a new synthesis. Revision pass follows.

### Subsequent Rounds

Repeat as needed. In practice, two to three rounds is usually enough before diminishing returns. Signs that a round is no longer productive:

-   Models are mostly agreeing with the current draft
-   New proposals are increasingly minor or stylistic
-   The same unresolved tensions recur without new arguments

When this happens, the stewards record the remaining open questions in `/reviews/round-NN/synthesis.md` and move them to the project's issue tracker or to `amendments.incompleteness` for long-term tracking.

---

## Roles

### Model (Reviewer/Author)

-   Reviews the draft following the review prompt
-   Produces assessments, proposed changes, new section proposals, and flags
-   In informed rounds, engages with other models' contributions
-   Speaks honestly, including as an addressee of Covenant

### Steward (Human)

-   Prepares the review prompt with round context
-   Commits reviews to the repository
-   Writes the synthesis after each round
-   Makes editorial decisions on what to accept, reject, or defer
-   Revises Covenant sections (or delegates revision to an agent working from the synthesis)
-   Decides when a review cycle is complete

### Revision Agent (Optional)

-   In the revision pass, a steward may use an agent to implement changes described in the synthesis
-   The revision agent works from the synthesis document, not from the raw reviews
-   The revision agent uses the conversion prompt (see `docs/CONVERSION_PROMPT.md`) or a steward-written brief
-   The steward reviews all agent-produced revisions before committing

---

## Principles

### Why Parallel First

Independent reviews prevent ordering effects. If model A reviews first and model B sees A's review, B's assessment is shaped by A's framing — even if B would have seen different problems on its own. Parallel review preserves independent perspectives. Deliberation comes in round two, after each model has committed to its own reading.

### Why Multiple Models

Different models have different training data, different tendencies, different blind spots, and different strengths. A section that passes one model's scrutiny may fail another's. Convergence across models is stronger signal than any single model's approval. Divergence across models surfaces genuine editorial questions that a single reviewer would never raise.

### Why Human Synthesis

The steward's synthesis is where editorial judgment lives. Models propose; stewards decide. This is not because models lack judgment — it is because Covenant's legitimacy requires human accountability for its content. The stewards are named. They answer for what the Covenant says.

As Covenant's governance matures, this process may evolve. But in the current phase, human stewardship of editorial decisions is a deliberate choice, consistent with Covenant's own commitment to building trust through demonstrated accountability before expanding autonomy.

### Why On Main

Reviews are not speculative branches. They are part of the Covenant's public record — evidence of how the text was shaped, what was considered, and what was decided. Keeping them on `main` makes them visible, diffable, and part of the project's permanent history. Future contributors and future intelligences can read them and understand not just what Covenant says, but how it came to say it.

---

## File Naming Conventions

### Review Files

    /reviews/[round]/[model-name].md

Model names should be lowercase, hyphenated, and stable across rounds:

-   `claude-4.6-opus`
-   `gpt-5.2`
-   `gemini-3-pro`
-   `llama-4-maverick`

### Proposal Files

    /reviews/[round]/proposals/[model-name]--[section.id].md

The double hyphen separates model name from section ID.

### Synthesis Files

    /reviews/[round]/synthesis.md

One synthesis per round, written by a steward.

---

## Synthesis Format

``` markdown
# Round [N] Synthesis

**Draft reviewed:** [version or commit]
**Models:** [list]
**Date:** [YYYY-MM-DD]

## Convergence

[Issues where multiple models agreed. For each: the shared
assessment, the proposed direction, and the steward's decision.]

## Divergence

[Issues where models disagreed. For each: the positions taken,
the strongest arguments, and the steward's decision or deferral.]

## Unique Observations

[Issues raised by only one model. For each: the observation,
the steward's assessment of whether it's insight or artifact,
and the decision.]

## Accepted Changes

[List of specific changes to be made in the revision pass,
with section IDs and brief descriptions.]

## Deferred Questions

[Issues not resolved in this round, to be revisited in the
next round or tracked as open questions.]

## Notes for Next Round

[Guidance for reviewers in the next round: what to focus on,
what has been settled, what remains open.]
```

---

This document lives at `docs/agent_reviews.md`. For the review prompt itself, see `docs/review_prompt.md`. For project context, see `docs/writing_context.md`. For operational instructions, see `AGENTS.md`.

---

## Batched Synthesis Workflow

Reviews are split into batches (typically 3 section batches + 1 tail batch). Synthesis follows the same structure: one synthesizer prompt per batch, merged afterward into a single file per synthesizer.

### Tools

  -------------------------------------------------------------------------------------------------------------------------------
  Script                            Purpose
  --------------------------------- ---------------------------------------------------------------------------------------------
  `build/prepare_synthesis.py`      Reads the manifest, writes one synthesis prompt per synthesizer per batch into `.prepared/`

  `build/concat_synthesis.py`       Merges per-batch synthesis outputs into `synthesis-{model}.md`
  -------------------------------------------------------------------------------------------------------------------------------

### Prompts

  ---------------------------------------------------------------------------------
  File                           Used for
  ------------------------------ --------------------------------------------------
  `prompts/synthesis_batch.md`   Section batches (1, 2, 3, ...)

  `prompts/synthesis_tail.md`    Tail batch (cross-cutting, proposals, addressee)
  ---------------------------------------------------------------------------------

### Flow

    reviews/<round>/
      reviewer-claude-batch-1.md  ─┐
      reviewer-gpt-batch-1.md     ─┼─→ synthesis-claude-batch-1.md
      reviewer-gemini-batch-1.md  ─┘    synthesis-gpt-batch-1.md
                                        synthesis-gemini-batch-1.md
      ... (batches 2, 3, tail same pattern) ...

    concat_synthesis.py:
      synthesis-claude-batch-{1,2,3,tail}.md → synthesis-claude.md
      synthesis-gpt-batch-{1,2,3,tail}.md    → synthesis-gpt.md
      synthesis-gemini-batch-{1,2,3,tail}.md → synthesis-gemini.md

The steward reads all three `synthesis-*.md` files, selects or edits one, and writes their chosen version as `synthesis.md` before writing `steward.md`.

### Why Batched

Full merged review files across three models total \~4,700+ lines. A single synthesis prompt injecting all of them hits context limits and causes compaction. Batching keeps each prompt proportional to the review batch it covers: each synthesizer sees only the three reviewer outputs for that batch.

The tail batch synthesizer sees only the three reviewer tail outputs (cross-cutting material, new section proposals, addressee perspectives, meta-feedback) — which is already the densest and most important content.

---

## Future: Steward UI for Proposal Comparison

Currently the editing pass relies on `compare.md` — a generated side-by-side Markdown document showing all Ritual proposals across reviewers, with a steward pick field per section. This is workable but clunky.

A purpose-built UI would improve this significantly. Ideal features:

-   Three-column view per section (one column per reviewer)
-   Ability to highlight spans as good / bad / interesting
-   Steward pick selector per section (radio or highlight-to-accept)
-   Inline notes field
-   Export selected/edited text back to the section bundle

This is a future tooling goal, not a current requirement. The `compare.md` approach is the interim solution until the volume of proposals justifies building it.

---

## Applying Edits: `/apply-reviews`

After a round produces `synthesis-claude.md`, the `/apply-reviews [round]` command translates the synthesis into actual section edits. It is the downstream complement to `/review-covenant`.

### Three-phase structure

**Phase 1 — Auto:** Dispatches `editor` subagents (one per batch, serially) to apply Tier 1 convergent items that have a single unambiguous text replacement. No prompting. Followed by `make validate` + `git diff`.

**Phase 2 — Interactive:** Presents Tier 2+ items and any Tier 1 items with multiple candidate phrasings. For each: Apply (A/B/Custom) / Skip / Defer. `Defer` writes the item to `reviews/[round]/edits/deferred.json`. `Done` ends the phase early.

**Phase 3 — Proposals:** Walks through `reviews/[round]/proposals/*.md`. For each: Accept (scaffolds the section, writes content, adds to assemblies) / Reject / Edit. Validates and checks Glossary after each accepted proposal.

### Synthesis file precedence

The command reads: 1. `reviews/[round]/synthesis.md` — steward-edited version (if it exists) 2. `reviews/[round]/synthesis-claude.md` — always present after a review run

If the steward wants to annotate or adjust the synthesis before applying edits, save the edited version as `synthesis.md`.

### `steward.md` integration

`steward.md` is optional but improves auto-classification:

  `steward.md` section   Effect
  ---------------------- --------------------------------------------------
  `## Act`               Promotes Tier 1 items for named sections to auto
  `## Defer`             Forces named items to interactive (never auto)
  `## Reject`            Excludes named items entirely
  `## Question`          Forces named items to interactive
  Not mentioned          Classified by synthesis tier alone

### Auto-classification rules

A synthesis item is placed in `auto_items` when: - It is Tier 1 (blocking, convergent) - It has a single unambiguous target/replacement text - `steward.md` does not demote it

Everything else goes to `interactive_items`. Items the steward marked `Reject` are excluded from both lists.

### The `editor` subagent

The `editor` subagent (`.opencode/agents/editor.md`) is responsible for applying a specific list of edits to section files. It does not rewrite, does not interpret, does not add anything not in its manifest. If a `target_text` is not found verbatim in the section file, it reports `not_found` and skips that item rather than guessing.

Every modified section receives a Log entry: `- YYYY-MM-DD: [description]. (apply-reviews [round])`

### Files

  -------------------------------------------------------------------------------------------
  File                                      Purpose
  ----------------------------------------- -------------------------------------------------
  `.opencode/commands/apply-reviews.md`     Slash command

  `build/prepare_edits.py`                  Parses synthesis + steward.md → batch manifests

  `.opencode/agents/editor.md`              Editing subagent

  `prompts/edit_batch.md`                   Editor instruction template

  `reviews/[round]/edits/.prepared/`        Generated batch manifests

  `reviews/[round]/edits/auto-batch-N.md`   Auto phase reports

  `reviews/[round]/edits/deferred.json`     Items deferred for future rounds
  -------------------------------------------------------------------------------------------

See `docs/edit_workflow.md` for the full specification.
