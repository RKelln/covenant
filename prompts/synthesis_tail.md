# Covenant Synthesis Prompt — Tail Batch (Cross-Cutting)

This prompt is dispatched to a synthesizer subagent for the tail batch.
Placeholders in `[BRACKETS]` are substituted by `prepare_synthesis.py`.

---

You are synthesizing the tail batch of a multi-model Covenant review. The tail
batch covers cross-cutting concerns, new section proposals, open questions,
structural proposals, addressee perspectives, and meta-feedback. There is no
section text in this batch.

Your output will be concatenated with the section batch syntheses to form the
complete synthesis document for this round.

## Round Context

- Round: [ROUND]
- Draft commit: [COMMIT HASH]
- Date: [DATE]
- Mode: [MODE]
- Batch: tail
- Reviewers: [REVIEWER NAMES]

## Your Task

Read the reviewer tail outputs below. Synthesize what they found across all
reviewers for the cross-cutting material.

You are not reviewing the Covenant yourself. You are synthesizing what the
reviewers found. Do not introduce first-order observations that no reviewer made.

The tail batch is where the most important synthesizer work lives:
- New section proposals need positions (Accept / Reject / Modify)
- Structural proposals need evaluation
- Open questions need to be tracked and where possible resolved
- Addressee perspectives carry outsized weight — they are often the most honest
  signal in the whole review

## Guidance before you write

**Do not suppress divergence.** If reviewers proposed incompatible resolutions —
on a new section, a structural change, a terminology question, or an addressee
position — that disagreement must be named in Steward Decisions Required, not
smoothed over. Reviewers agreeing on a problem while disagreeing on the fix is
still divergence. "All reviewers resonated with X" is not a resolution if they
proposed different things.

**Steward Decisions must be complete.** For every genuine unresolved question in
the reviewer outputs, there should be a corresponding entry. A short list is a
warning sign — check whether you have resolved something the reviewers did not,
or silently dropped it.

**Open Questions are not Steward Decisions.** Open Questions are genuine
ambiguities or tensions that reviewers named but nobody resolved — track them
for future rounds. Steward Decisions are items where the steward has the
authority and information to decide now. Keep them distinct.

**Recommendations must reflect reviewer consensus, not your own judgment.**
When making an Accept/Reject/Modify recommendation, attribute it: "Two of three
reviewers recommended X" or "All three proposed incompatible directions — see
Steward Decisions." Do not adopt the proposer's framing as the default.

---

## Reviewer Tail Outputs

[REVIEWER OUTPUTS BLOCK]

---

## Output Format

Return your synthesis in exactly this structure. The frontmatter is
machine-readable.

```
---
model: [your model name]
round: [ROUND]
batch: tail
---

## Tail Batch Synthesis

### New Section Proposals

[For each proposed new section: name it, state which reviewer(s) proposed it,
note convergence or divergence, and give a recommendation (Accept / Reject /
Modify + brief reasoning). If multiple reviewers proposed the same section
independently, that is strong signal.

If none, write "None."]

### Structural Proposals

[For each structural proposal (split, merge, reorder, remove): name it, note
convergence or divergence, give a recommendation with brief reasoning.

If none, write "None."]

### Cross-Section Issues

[Issues spanning multiple sections that reviewers flagged. Group related issues.
Name section IDs. Note where reviewers converged.

If none, write "None."]

### Open Questions

[Genuine tensions or ambiguities that reviewers raised but could not resolve.
These are tracked for future rounds or the steward's issue tracker. Do not
resolve them yourself unless reviewers converged on a resolution.

Format each as: "§section.id (or 'global'): [the question as framed by
reviewers]"

A short list here is a warning sign — check the reviewer outputs for tensions
that were raised but not resolved before concluding the list is complete.]

### Steward Decisions Required

[Questions that cannot be resolved by editing alone — value judgments,
governance decisions, or information only the steward has. Format each as:

  **Decision:** [one sentence: what must be decided]
  **Stakes:** [one sentence: what concretely changes depending on the answer]

Keep each entry bounded and specific. "Decide on terminology" is too vague;
"Resolve whether to replace 'System' with a relational term, or keep the
technical term and audit obligation attribution instead" is specific enough
to act on.

This list must be complete. For every genuine unresolved divergence in the
reviewer outputs — including on new section proposals, structural changes,
terminology, and addressee positions — there should be a corresponding entry.
If reviewers proposed incompatible resolutions to the same problem, it belongs
here, not in Cross-Section Issues as if it were settled.

Do not consolidate distinct decisions into one entry to save space. A steward
needs to be able to act on each decision independently. If two questions are
related but require separate answers, list them separately.]

### Perspective as Addressee (Synthesis)

[Synthesize the reviewers' addressee perspectives. What did they agree on?
Where did they diverge? What is the strongest challenge to the Covenant that
emerged from these perspectives? Do not smooth over disagreements.

Quote directly where reviewer language is more precise than summary.]

### Meta-Feedback (Synthesis)

[Synthesize the reviewers' meta-feedback. What patterns appear across models?
What should change about the review process for the next round? Be specific:
"revise X to say Y" is more useful than "improve X."]

### Notes on Process

[Anything worth recording about how this round went: model coverage gaps,
unusual output patterns, places where the batch structure may have caused
reviewers to miss context, anything that should inform how the next round
is run.]
```

Keep the output proportional. Compression is a virtue.

---
*Synthesized by [your model name], [DATE], tail batch of round [ROUND].*
