# Covenant Synthesis Prompt — Section Batch

This prompt is dispatched to a synthesizer subagent for one batch of sections.
Placeholders in `[BRACKETS]` are substituted by `prepare_synthesis.py`.

---

You are synthesizing one batch of a multi-model Covenant review. Your output
will be concatenated with other batch syntheses to form the complete synthesis
document for this round.

## Round Context

- Round: [ROUND]
- Draft commit: [COMMIT HASH]
- Date: [DATE]
- Mode: [MODE]
- Batch: [BATCH]
- Reviewers: [REVIEWER NAMES]

## Your Task

Read the reviewer outputs below. Synthesize what they found — across all
reviewers — for the sections in this batch.

You are not reviewing the Covenant yourself. You are synthesizing what the
reviewers found. Do not introduce first-order observations that no reviewer
made. If all three reviewers missed something, note it in **Notes on Process**,
not in the findings.

## Tier Calibration Rules (read before writing)

**Tier 1** requires two conditions, both necessary:
1. All or nearly all reviewers raised it independently
2. It is *blocking* — meaning: a steward who skipped this item would ship a
   section with a substantive defect (broken logic, missing obligation, false
   claim, structural incoherence). A phrase that reads badly, a stylistic
   anti-pattern, or a convergent word-choice fix is not blocking. Those go
   to Tier 3.

Use this test for every candidate item: *"If the steward never sees this, does
the published section contain a real defect?"* If yes: Tier 1. If no: Tier 3.

Aim for 3–5 Tier 1 items. Treat 6 as a hard ceiling requiring justification,
and 7+ as a signal you are conflating severity with convergence. Most batches
of 9 sections will have 3–5 genuinely blocking convergences. If you have more,
re-examine each one against the blocking test above before including it.

**Tier 4** is not optional. If reviewers disagreed — even on something that
seems minor — it goes here. Genuine disagreement means: reviewers proposed
incompatible resolutions, or named the same problem but diagnosed different
causes. Do not collapse disagreements into "stylistic differences" or "minor
variation." Do not write "None" unless reviewers showed genuine uniform
agreement on every issue in the batch, which is rare.

**Each item must appear in exactly one tier.** If an issue is in Tier 4
(divergence), it must not also appear in Tier 1 or Tier 2 as if it were
resolved. Pick the tier that reflects the *actual state of reviewer agreement*.

## Section-Level Notes guidance

Each note must be per-section and add value beyond restating the tier entries
above. Ask: "What does the steward need to know about this section that isn't
already captured in Tiers 1–4?" Good notes surface repair direction, flag
Digest or frontmatter issues, or point to cross-section dependencies. A note
that just summarizes the Tier 1 entry for that section is not useful — omit
it rather than restate.

---

## Reviewer Outputs

[REVIEWER OUTPUTS BLOCK]

---

## Output Format

Return your synthesis in exactly this structure. The frontmatter is
machine-readable.

```
---
model: [your model name]
round: [ROUND]
batch: [BATCH]
---

## Batch [BATCH] Synthesis

### What This Batch Established

[1–2 sentences: what did this batch of sections reveal, collectively? What
was the most important convergence or divergence?]

### Tier 1: Blocking Issues (Convergent — Act)

[Issues where all or nearly all reviewers independently raised the same concern,
AND the issue is blocking (not merely a minor or stylistic fix). These are the
highest-confidence editing targets. Name section IDs. Quote specific reviewer
language where it illuminates the problem. Describe the consensus direction.

Minor fixes with three-way convergence belong in Tier 3, not here.
Aim for 3–5 items. More than 6 is almost certainly inflation.

If none, write "None."]

### Tier 2: High Priority (Convergent — Consider)

[Issues raised by two reviewers, or raised by one reviewer with unusual
specificity or force. Same format as Tier 1.

Do not place issues here if they are genuinely contested across reviewers —
those belong in Tier 4. An issue is not "high priority consider" if reviewers
proposed incompatible resolutions; that is divergence.

If none, write "None."]

### Tier 3: Section-Level Repairs (Systematic — Consolidate)

[Issues appearing across multiple sections with consistent consensus on the fix,
including minor convergent fixes that don't rise to Tier 1 severity. Group by
type (e.g. "MUST/SHOULD calibration," "Ritual anti-patterns"). Name the
specific sections affected.

If none, write "None."]

### Tier 4: Divergence (Steward Judgment Required)

[Genuine disagreements between reviewers. For each: represent each reviewer's
position fairly, then name the tension. Do not resolve by averaging. Note what
would need to be true for each position to be right.

This section is rarely empty. If reviewers proposed incompatible resolutions to
the same problem, or named the same problem but diagnosed different causes, it
belongs here — even if all reviewers agreed the problem exists. Agreement on the
problem with disagreement on the fix is still divergence.

If none, write "None."]

### Section-Level Notes

[Brief per-section summary of the most actionable finding that is NOT already
captured in Tiers 1–4. Surface repair direction, Digest/frontmatter issues, or
cross-section dependencies a steward should track. Do not restate tier entries.
Format:
- §section.id: one sentence on the primary issue or proposed fix.
Omit sections where there is nothing to add beyond what the tiers already cover.]
```

Keep the output proportional to the batch. Compression is a virtue.

---
*Synthesized by [your model name], [DATE], batch [BATCH] of round [ROUND].*
