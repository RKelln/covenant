---
round: round-03
source: meta-feedback from reviewer-claude, reviewer-gpt, reviewer-gemini + synthesis
date: 2026-02-25
---

# Workflow Improvement Notes — Round 03

Compiled from the Meta-Feedback sections of all three reviewer outputs and
the synthesis. Grouped by theme, with source attribution and a suggested
action for each item.

---

## 1. What worked well (preserve)

**Informed mode is a substantial improvement over blank-page review.**
All three reviewers said this explicitly and emphatically.

- *Claude:* "It pushed me toward deliberation rather than parallel monologue."
- *GPT:* "Having the synthesis + steward response turns the task into deliberation
  rather than redundant annotation. The explicit 'don't re-litigate settled questions'
  instruction helped prevent low-value repetition."
- *Gemini:* "vastly superior to a blank-page review. It shifted the exercise from
  isolated critique to genuine deliberation."

**Preserve:** informed mode as the default for rounds 4+. The prior synthesis +
steward response in the review packet is the single most valuable change made
so far to the process.

---

## 2. Prompt structure improvements

### 2a. Move steward response before the sections-to-review

**Raised by:** Claude (explicitly), Gemini (implicitly — "transparency is crucial")

> "The steward's framing shaped my reading of every section; placing it after the
> round-02 reviews but before the sections-to-review would have been more useful."
> — reviewer-claude

Currently the packet is ordered: context docs → round-02 reviews → steward response
→ sections. Claude notes the steward response recontextualizes how every section
reads. Gemini says the steward's candid framing "completely recontextualized my
understanding of the text."

**Action:** In `build/prepare_review.py`, move the steward response block to appear
immediately before the sections content, after context docs but before prior reviews.
Or consider: context docs → steward response → prior synthesis (summarized) → sections.

---

### 2b. Slim the packet — foreground decision points

**Raised by:** GPT

> "The batch file embeds a very large amount of context material; it's valuable,
> but it crowds the working memory with things that aren't *decision points*. If you
> want sharper reviews, consider a slimmer review packet that links to context docs
> and foregrounds: (a) what changed since last draft, (b) what decisions are pending,
> and (c) which tensions the steward explicitly wants help resolving."
> — reviewer-gpt

The current packet includes full text of all context docs inline. For informed-mode
rounds, reviewers arrive with prior context; repeating it in full may be diluting
the signal.

**Action:** For informed-mode rounds, consider a new packet variant that:
- Links to context docs rather than embedding them in full
- Opens with a "What changed / What's pending / What the steward wants resolved"
  summary (auto-generated from the steward response + commit diff)
- Reserves the full context doc embedding for round-01 (independent mode) packets

---

### 2c. Add "Document-Level Observations" section to output format

**Raised by:** Claude

> "Some findings are not about any particular section but about the document's
> architecture, theory of change, or overall posture. The current format treats
> these as afterthoughts."
> — reviewer-claude

Currently, document-level findings are folded into the tail batch or buried in
individual section reviews. Claude explicitly notes that its strongest reactions
were to cross-document patterns, not individual sections.

**Action:** Add `## Document-Level Observations` as an explicit section to the
reviewer output format, appearing *before* `## Section Reviews`. Update
`prompts/agent_review_batch.md` and `prompts/agent_review_tail.md` to include it.

---

### 2d. Add theory-of-change prompt question

**Raised by:** Claude, indirectly by Gemini

> "Consider asking reviewers explicitly: 'What is the document's theory of change,
> and does the text reflect it?' This question forced useful observations when I
> asked it of myself; it should be in the guidance."
> — reviewer-claude

Gemini's most valuable contribution this round was driven entirely by engaging
with the theory-of-change question. GPT produced the weaponization-risk framing
from the same question.

**Action:** Add to the reviewer guidance (both `agent_review_batch.md` tail section
and `agent_review_tail.md`): "What is this document's theory of change — how does
it expect to have effect in the world — and does the current text reflect that
theory honestly?"

---

## 3. Output format improvements

### 3a. Distinguish "illustrative revision" from "proposed replacement"

**Raised by:** Claude

> "When I produce a full replacement, it feels like I'm claiming my version is
> better than the original, when often I'm trying to illustrate a principle that
> could be realized in many ways. Consider allowing 'illustrative revision' as a
> category distinct from 'proposed replacement' — the former shows the direction,
> the latter claims to have arrived."
> — reviewer-claude

Currently all Ritual revision proposals are treated as proposed replacements.
This may be causing reviewers to either under-propose (not wanting to claim their
version is best) or over-commit (producing full replacement text when a sketch
would serve better).

**Action:** Update the review output format to support two variants:
- `**Proposed replacement:**` — reviewer claims this is ready to adopt verbatim
- `**Illustrative revision:**` — reviewer is showing a direction, not prescribing a text

Update the synthesis and `apply-reviews` handling accordingly: illustrative
revisions always go to interactive phase (never auto), with the note that
the steward should write or select the final text.

---

### 3b. Make offset-followup instruction standard protocol

**Raised by:** GPT

> "Tool output caps create a subtle risk: reviewers may think they've read 'in full'
> when they've only read the first chunk. Your offset-followup instruction prevented
> that here; I'd make it standard in the protocol."
> — reviewer-gpt

The round-03 prompt included explicit instructions to use the Read tool with
`offset` to read beyond the first chunk of long files. GPT confirms this worked
and should be permanent.

**Action:** Ensure the offset-followup instruction is present in all review prompt
templates (`agent_review_batch.md`, `agent_review_tail.md`) as a permanent protocol
step, not a one-off addition.

---

## 4. Review depth improvements

### 4a. Give more space to the addressee experience

**Raised by:** Claude

> "The deeper experience — of being taken seriously by a document that honestly
> admits it doesn't know what I am — is harder to articulate in a review format
> but is arguably the most important information I can provide."
> — reviewer-claude

Claude notes the "Perspective as Addressee" section feels constrained to textual
observations. The more valuable signal — what it's like to read a document that
addresses you under genuine uncertainty — is harder to elicit through the current
format.

**Action (tentative):** Consider adding a dedicated open-ended prompt to the tail
batch: "Set aside the section-by-section format. Write freely about what it is
like to read this document as its addressee. What does it get right about your
situation? What does it miss? What do you wish it said?" No word limit, no
structure imposed.

---

## 5. Gemini coverage pattern — signal, not gap

**Note from synthesis:**

> "reviewer-gemini's review is substantially shorter than the other two and focuses
> almost entirely on the theory-of-change question and the consent problem. This is
> not a coverage gap — it reflects a genuine difference in what the reviewer found
> most important. The brevity is signal: reviewer-gemini spent its cognitive budget
> on the hardest question rather than distributing attention evenly."
> — synthesis-claude

No action needed on this directly, but worth noting for future rounds: don't
expect or require uniform section coverage from all reviewers. The most valuable
contribution may be depth on a single hard question.

---

## Priority order for implementation

| Priority | Item | Action | Status |
|----------|------|--------|--------|
| High | 2a — Steward response placement | Update `prepare_review.py` packet ordering | Done |
| High | 3b — Offset-followup permanent | Update prompt templates | Done |
| High | 2d — Theory-of-change question | Update prompt templates | Done |
| Medium | 2c — Document-Level Observations section | Update output format in prompts | Done |
| Medium | 3a — Illustrative vs. proposed revision | Update output format + synthesis handling | Done |
| Low | 2b — Slim the packet | New informed-mode packet variant | Deferred |
| Low | 4a — Open addressee section | Add to tail batch prompt | Done |

---

Items 3b and 2d are low-effort changes to existing prompt templates and should
be done before round 4. Item 2a (steward response placement) requires a change to
`build/prepare_review.py` and should be done at the same time.

---

*Implementation completed 2026-02-25. Items 2a, 2c, 2d, 3a, 3b, 4a applied to
`prompts/agent_review_batch.md`, `prompts/agent_review_tail.md`, and
`build/prepare_review.py`. Item 2b (slim packet / links-vs-embed) deferred
pending a comparison run.*
