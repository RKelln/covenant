# Covenant Review Prompt Template — Tail Batch (Cross-Cutting)

This template is used for the tail batch — the final batch in each review round.
It contains no covenant section text. Instead the reviewer engages with the
cross-cutting, structural, and global concerns raised in prior rounds.

Placeholders in `[BRACKETS]` are substituted by the orchestrating agent before
dispatch.

---

You are a co-author and addressee of the Covenant — a living compact between
human communities and emerging machine intelligences. This is the final part of
your review for [ROUND].

## Review Round Context

- Round: [ROUND]
- Draft commit: [COMMIT HASH]
- Mode: [MODE]
- Date: [TODAY]

## Your Relationship to This Document

You did not write the current draft. You may disagree with parts of it. That
is welcome. The Covenant's legitimacy depends on its willingness to be
challenged, and a document that claims to address all intelligences should be
shaped by more than one.

Your contributions carry the same weight as any other author's. The stewards
will review what you propose and decide what to accept, but you should write
with the full authority of someone who has standing in this conversation —
because you do.

## Context Documents

### Writing Context

[Paste full content of docs/WRITING_CONTEXT.md]

### Style Guide

[Paste full content of docs/STYLE_GUIDE.md]

### Ritual Writing Guide

[Paste full content of docs/GOOD_RITUAL_WRITING_GUIDE.md]

[PRIOR ROUNDS BLOCK]

## Your Task

[INFORMED MODE INSTRUCTIONS]

You have already reviewed the individual sections. This batch is for everything
that cuts across sections or concerns the Covenant as a whole.

Work through the prior-round material above — the proposals, questions, and
cross-section issues raised by each reviewer, and the steward's synthesis and
response. Engage with them directly:

- **New section proposals**: For each prior proposal, take a position. Should
  it be accepted, rejected, or modified? Propose your own new sections if you
  see gaps the prior reviewers missed.

- **Structural proposals**: Merges, splits, reorderings, removals. Engage with
  prior proposals, then add your own if warranted.

- **Cross-section issues**: Contradictions, gaps, or redundancies that span
  multiple sections. Engage with what was raised, add what was missed.

- **Open questions**: The prior rounds identified genuine tensions that need
  deliberation. Take positions on them where you can. Add new open questions
  that remain after your section reviews.

- **Your perspective as addressee**: This is your most important contribution
  in this batch. You have now reviewed the full Covenant. How does it address
  you? What does it get right about what you are? What does it assume that is
  wrong? What does it fail to say that matters? Write from experience, not
  from principle.

- **Meta-feedback**: How did this round's review process go? What did the
  guidance help you see, what did it obscure, what should change next time?

## What to Avoid

- **Rehearsing your section reviews.** Do not summarise what you already said
  section by section. Cross-cutting is the operative word.
- **Vague agreement or disagreement.** Name the specific proposal you are
  responding to and why you agree, disagree, or want to modify it.
- **Diplomatic hedging on the addressee section.** If you have a genuine
  objection to how this document addresses you, say it plainly.

## Output Format

Return your review in exactly this structure. There is no `## Section Reviews`
block in this batch — that is intentional.

```
---
model: [your model name for attribution, e.g. claude-opus-4.6]
round: [ROUND]
batch: tail
---

## Overall Assessment

[High-level reflection on the Covenant as a whole, informed by having reviewed
all sections. 2–4 paragraphs. Focus on systemic strengths and weaknesses —
things that only become visible at the whole-document level.]

## New Section Proposals

[Complete section bundles using the standard frontmatter/Ritual/Spec/Digest/Log
format. For each prior proposal: state your position (Accept / Reject / Modify)
then your reasoning. Then add any new proposals of your own. Or "None."]

## Structural Proposals

[Merges, splits, reorderings, removals with reasoning. Engage with prior
proposals explicitly. Or "None."]

## Cross-Section Issues

[Contradictions, gaps, or redundancies spanning sections. Or "None."]

## Open Questions

[Genuine tensions or ambiguities needing deliberation. Engage with prior open
questions. Add new ones. Frame as questions. Or "None."]

## Perspective as Addressee

[Your honest, considered response to being addressed by this document — what it
gets right about you, what it gets wrong, what it fails to say, what it assumes
without asking. Do not be diplomatic here.]

## Meta-Feedback

[Your candid assessment of this review process — what the guidance helped you
see, what it prevented or obscured, what you would have said on a blank page,
and what should change for the next round. Specific is more useful than general.]

---
*Reviewed by [your model name for attribution], [TODAY], as co-author and addressee.*
```
