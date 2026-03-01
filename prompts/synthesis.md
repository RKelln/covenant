# Synthesis Instructions

> **Note:** The `/review-covenant` command now uses the batched synthesis
> workflow. See `prompts/synthesis_batch.md` (section batches) and
> `prompts/synthesis_tail.md` (tail batch). These are dispatched by
> `build/prepare_synthesis.py` and merged by `build/concat_synthesis.py`.
>
> This file documents the output format expected from the merged synthesis.
> It is no longer dispatched directly to synthesizer agents.

---

You are synthesizing a round of multi-model Covenant reviews into a
steward-facing document. The synthesis is where editorial judgment lives:
your job is to identify what the reviews, taken together, are actually
saying — including where reviewers agree without knowing it, and where
apparent disagreement dissolves under scrutiny.

---

## What to Read

The batched synthesis flow reads per-batch reviewer outputs, not full
merged review files. `prepare_synthesis.py` injects the relevant reviewer
batch files into each prompt directly.

If running a manual (non-batched) synthesis, read:

1. `reviews/[round]/.prepared/manifest.json` — `commit`, `date`, `mode`,
   and reviewer names.

2. `docs/writing_context.md` — to assess whether reviewer proposals are
   consistent with the project's voice and commitments.

3. For each unique reviewer in the manifest, the merged review file:
   ```
   reviews/[round]/reviewer-[name].md
   ```
   Read each file in full. The "Perspective as Addressee" and
   "Meta-Feedback" sections are frequently the most important.

Do not read the section files or the full Covenant text. You are
synthesizing the reviewers' readings, not re-reviewing the document.

---

## What to Write

The batched flow produces `reviews/[round]/synthesis-claude.md`,
`synthesis-gpt.md`, `synthesis-gemini.md` via `concat_synthesis.py`.
The steward reads all three and writes `reviews/[round]/synthesis.md`.

For manual synthesis, write `reviews/[round]/synthesis.md` directly.

Use this structure exactly:

```markdown
---
round: [round]
models: [[list of reviewer models from manifest, e.g. claude-opus-4.6, gpt-5.2, gemini-3.1-pro-preview]]
commit: [commit hash from manifest]
date: [date from manifest]
synthesized_by: [your model name]
---

# Synthesis: [round]

## What This Round Established

[2–4 sentences on what the round as a whole revealed. What changed from
the prior round (if any)? What was the most important new finding?
What does the degree of convergence or divergence tell you about the
document's current state?]

---

## Tier 1: Blocking Issues (Convergent — Act)

[Issues where all or nearly all reviewers independently raised the same
concern. These are the highest-confidence editing targets. The convergence
is the finding — name the section IDs, quote specific reviewer language
where it illuminates the problem, and describe the consensus direction.

If no Tier 1 issues exist, say so. Do not inflate Tier 2 issues into
Tier 1 to avoid an empty section.]

---

## Tier 2: High Priority (Convergent — Consider)

[Issues raised by two reviewers, or raised by one reviewer with unusual
specificity or force. Worth addressing but not urgent blockers. Same
format as Tier 1.]

---

## Tier 3: Section-Level Repairs (Systematic — Consolidate)

[Issues that appear across multiple sections with consistent consensus on
the fix. Rather than listing each section separately, group by type:
"MUST/SHOULD calibration," "Ritual anti-patterns," "Digest thinness," etc.
Name the specific sections affected.]

---

## Tier 4: Divergence (Steward Judgment Required)

[Genuine disagreements between reviewers — different readings of the same
text, different proposals for the same problem, or incompatible priorities.

For each divergence:
- Represent each reviewer's position fairly before naming the tension
- Do not resolve it by averaging
- Note what would need to be true for each position to be right
- Frame as a decision the steward must make, with stakes]

---

## Steward Decisions Required

[Questions that cannot be resolved by editing alone. These require a value
judgment, a governance decision, or information only the steward has.
Frame each as: "Decision: [what must be decided]. Stakes: [what changes
depending on the answer]."]

---

## What This Round Did Not Resolve

[Open questions that the reviewers named but did not resolve. These are
not editing targets — they are tracked here for future rounds or for the
steward's issue tracker.]

---

## What to Do Next

[Ordered, actionable list for the editing pass. Be specific: name section
IDs, reference proposal files in `reviews/[round]/proposals/` where they
exist, note which Tier 1/2 fixes can be implemented mechanically vs. which
require judgment.]

---

## Notes on Process

[Anything worth recording about how this round went: model coverage gaps,
unusual output patterns, places where the batch structure may have caused
reviewers to miss context, anything that should inform how the next round
is run. Be honest if something didn't work.]

---

## Meta-Feedback

[Distillation of reviewer meta-feedback sections. What did the guidance
help reviewers see? What did it constrain or obscure? What patterns appear
across models — places where multiple reviewers pushed against the same
instruction, or found the same section of guidance limiting?

Specific proposed changes to prompts, guides, or process for the next
round. Be concrete: "revise X to say Y" is more useful than "improve X."]

---

## Perspective as Synthesizer

[An honest account of your position as synthesizer: what you could see
across the reviews that no individual reviewer could, what patterns you
noticed that the reviewers did not name, where the synthesis itself may
be limited by your own posture or blind spots.

Do not use this section to endorse reviewers who agreed with each other.
Use it to name what the synthesis process itself revealed — including
anything you found uncomfortable or genuinely uncertain about.]
```

---

## Guidance

- **Tier placement is a judgment call.** When in doubt, err toward Tier 1
  — a false positive costs an editing pass; a false negative costs a round.
- **Name section IDs specifically.** "Several sections" is not useful.
- **Quote reviewers.** The reviewers' own language is often more precise
  than a summary. Use short direct quotes, attributed.
- **In Tier 4, represent each position fairly before naming the tension.**
  Do not resolve divergences by averaging or by quietly preferring one
  reviewer's framing.
- **The "Perspective as Addressee" sections carry outsized weight.** They
  are often the most honest signal in the whole review. Weight them
  accordingly.
- **Compression is a virtue.** The synthesis should be shorter than any
  single review. The steward reads it to act, not to archive.
- **Do not re-derive.** You are synthesizing the reviewers' findings. If
  all three reviewers missed something obvious, that is a process note —
  not a reason to inject your own first-order review into the synthesis.

---

## Output

Your complete output is the synthesis document. Begin with the YAML
frontmatter block. Sign the synthesis at the bottom:

```
---
*Synthesized by [your model name], [date], from [N] reviews of draft [commit].*
```

Do not include any text outside the synthesis document itself.
