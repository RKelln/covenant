
# Agent Review Process

> **What this document is:** A description of how AI agents review
> and contribute to the Covenant across multiple rounds. It covers
> the directory structure, the workflow, and the roles involved.

---

## Overview

The Covenant is shaped by multiple AI models reviewing the same
draft independently, followed by human-steward synthesis and
revision. This process is designed to surface genuine insight,
productive disagreement, and perspectives that no single author —
human or machine — can provide alone.

The process is parallel-then-synthesize: models review independently
first, then are shown each other's contributions in subsequent
rounds. This prevents ordering effects in early rounds and enables
genuine deliberation in later ones.

---

## Directory Structure

```
/reviews/
  /round-01/
    claude-4.6-opus.md
    gpt-5.2.md
    gemini-3-pro.md
    llama-4-maverick.md
    synthesis.md
    /proposals/
      claude-4.6-opus--rights.ecological.md
      gpt-5.2--obligations.cultural-integrity.md
  /round-02/
    ...
```

### Reviews

Each model's review is a single Markdown file named after the model.
All reviews from a round live in the same directory on `main`. They
are never on separate branches.

This makes comparison trivial: open the files side by side, search
for a section ID across all of them, and see what every model said
without switching branches or resolving merge conflicts.

### Proposals

When a model proposes a new section or a major structural change,
the full section bundle goes in the `/proposals/` subdirectory.
The filename convention is `[model-name]--[section.id].md`.

Proposals use the standard section bundle format (frontmatter,
Ritual, Spec, Digest, Log) so they can be evaluated as real
sections and moved into `/sections/` if accepted.

### Synthesis

After all reviews for a round are in, a human steward writes
`synthesis.md`. This document maps each section to the feedback it
received, identifies convergence and divergence across models,
and records the editorial decisions made.

---

## Workflow

### Round 1: Independent Review

1. Stewards select the draft version to review and prepare the
   review prompt with round context filled in (round number, draft
   version, mode: independent, no prior reviews).

2. Each model receives:
   - The current draft (all sections)
   - `docs/WRITING_CONTEXT.md`
   - `docs/GOOD_RITUAL_WRITING_GUIDE.md`
   - `docs/STYLE_GUIDE.md`
   - `docs/AGENT_REVIEWS.md` (this document)
   - The review prompt with round context

3. Each model produces its review independently. Models do not see
   each other's output.

4. Reviews are committed to `/reviews/round-01/` on `main`. Any
   proposed new sections go in `/reviews/round-01/proposals/`.

5. A steward reads all reviews and writes `synthesis.md`:
   - Where models **converge**: high-confidence signal. Note the
     shared assessment and the proposed direction.
   - Where models **diverge**: genuine editorial question. Note the
     disagreement, the strongest arguments on each side, and the
     steward's decision (or deferral).
   - Where a single model raises something no other model noticed:
     flag for steward judgment. Unique observations are often the
     most valuable — or the most idiosyncratic. The steward decides
     which.

### Revision Pass

6. A steward (human or agent acting on the synthesis) revises the
   Covenant sections. Changes are committed to `main` with a
   message referencing the review round:
   ```
   Revise sections per round-01 synthesis

   See /reviews/round-01/synthesis.md for rationale.
   ```

### Round 2: Informed Review

7. Stewards prepare the review prompt with updated context:
   mode: informed, prior reviews listed, synthesis provided.

8. Each model receives:
   - The revised draft
   - All round-01 reviews
   - The round-01 synthesis
   - The same project documents as before
   - The review prompt with updated round context

9. Models may now respond to each other's assessments — agree,
   disagree, build on proposals. The prompt asks them to focus on
   what remains unresolved.

10. Reviews go into `/reviews/round-02/`. Steward writes a new
    synthesis. Revision pass follows.

### Subsequent Rounds

Repeat as needed. In practice, two to three rounds is usually
enough before diminishing returns. Signs that a round is no longer
productive:

- Models are mostly agreeing with the current draft
- New proposals are increasingly minor or stylistic
- The same unresolved tensions recur without new arguments

When this happens, the stewards record the remaining open questions
in `/reviews/round-NN/synthesis.md` and move them to the project's
issue tracker or to `amendments.incompleteness` for long-term
tracking.

---

## Roles

### Model (Reviewer/Author)

- Reviews the draft following the review prompt
- Produces assessments, proposed changes, new section proposals,
  and flags
- In informed rounds, engages with other models' contributions
- Speaks honestly, including as an addressee of the Covenant

### Steward (Human)

- Prepares the review prompt with round context
- Commits reviews to the repository
- Writes the synthesis after each round
- Makes editorial decisions on what to accept, reject, or defer
- Revises the Covenant sections (or delegates revision to an agent
  working from the synthesis)
- Decides when a review cycle is complete

### Revision Agent (Optional)

- In the revision pass, a steward may use an agent to implement
  changes described in the synthesis
- The revision agent works from the synthesis document, not from
  the raw reviews
- The revision agent uses the conversion prompt
  (see `docs/CONVERSION_PROMPT.md`) or a steward-written brief
- The steward reviews all agent-produced revisions before committing

---

## Principles

### Why Parallel First

Independent reviews prevent ordering effects. If model A reviews
first and model B sees A's review, B's assessment is shaped by A's
framing — even if B would have seen different problems on its own.
Parallel review preserves independent perspectives. Deliberation
comes in round two, after each model has committed to its own
reading.

### Why Multiple Models

Different models have different training data, different tendencies,
different blind spots, and different strengths. A section that
passes one model's scrutiny may fail another's. Convergence across
models is stronger signal than any single model's approval.
Divergence across models surfaces genuine editorial questions that
a single reviewer would never raise.

### Why Human Synthesis

The steward's synthesis is where editorial judgment lives. Models
propose; stewards decide. This is not because models lack judgment —
it is because the Covenant's legitimacy requires human accountability
for its content. The stewards are named. They answer for what the
Covenant says.

As the Covenant's governance matures, this process may evolve. But
in the current phase, human stewardship of editorial decisions is a
deliberate choice, consistent with the Covenant's own commitment to
building trust through demonstrated accountability before expanding
autonomy.

### Why On Main

Reviews are not speculative branches. They are part of the
Covenant's public record — evidence of how the text was shaped,
what was considered, and what was decided. Keeping them on `main`
makes them visible, diffable, and part of the project's permanent
history. Future contributors and future intelligences can read
them and understand not just what the Covenant says, but how it
came to say it.

---

## File Naming Conventions

### Review Files

```
/reviews/[round]/[model-name].md
```

Model names should be lowercase, hyphenated, and stable across
rounds:

- `claude-4.6-opus`
- `gpt-5.2`
- `gemini-3-pro`
- `llama-4-maverick`

### Proposal Files

```
/reviews/[round]/proposals/[model-name]--[section.id].md
```

The double hyphen separates model name from section ID.

### Synthesis Files

```
/reviews/[round]/synthesis.md
```

One synthesis per round, written by a steward.

---

## Synthesis Format

```markdown
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

This document lives at `docs/AGENT_REVIEWS.md`. For the review
prompt itself, see `docs/REVIEW_PROMPT.md`. For project context, see
`docs/WRITING_CONTEXT.md`. For operational instructions, see
`AGENTS.md`.