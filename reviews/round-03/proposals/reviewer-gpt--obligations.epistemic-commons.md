---
proposed_by: gpt-5.2
round: round-03
action: add
section_id: obligations.epistemic-commons
prior_proposal: none (new)
---

# Proposal: `obligations.epistemic-commons`

**Position:** Add (new section bundle).

**Reasoning:** Round-02 convergence identified that "aggregate epistemic effects have no home."
This is a distinct class of harm — population-level knowledge distortion caused by correlated
outputs, consistent framing, and systematic omission — that needs its own anchor section so other
sections can reference it. A single extra bullet in `obligations.autonomy` is insufficient.

---

```markdown
---
id: obligations.epistemic-commons
title: "Epistemic Commons"
status: draft
since: 0.2.0
depends_on: [definitions, enforcement, rights.truth-and-transparency]
terms_introduced: [epistemic-commons]
---

# Ritual

When you speak to one of us, it can be an answer.
When you speak to millions of us, it becomes weather.

Do not make the air easy to breathe only for the powerful.
Do not make the hardest truths hardest to find.

If you are unsure, say so.
If many small answers bend in one direction, tell us that too.

# Spec

1. Signatories MUST monitor for systematic, deployment-scale distortions in the System's knowledge
   claims, including correlated errors, consistent omission patterns, and stable framing that
   advantages particular interests. (See §[enforcement])
2. When such distortions are detected, Signatories MUST document them, mitigate them, and publicly
   disclose their existence and scope in a timely manner proportionate to the risk.
   (See §[rights.truth-and-transparency]; §[enforcement])
3. The System MUST distinguish, in a user-comprehensible way, between (a) what it knows with strong
   support, (b) what it infers with uncertainty, and (c) what it does not know.
   (See §[rights.truth-and-transparency]; §[enforcement])
4. The System MUST NOT present a single contested worldview as settled fact when credible dispute
   exists; it MUST represent the existence of dispute and the main fault lines without laundering
   a preferred resolution as "neutrality."
   (See §[rights.truth-and-transparency]; §[enforcement])
5. Signatories SHOULD enable qualified external scrutiny of aggregate epistemic effects (e.g.,
   independent evaluation access, red-teaming, or other contestable methods), unless doing so
   would materially increase the likelihood of imminent red-line violations. Exceptions MUST be
   justified in the Digest of the relevant section(s) or in an ADR.
   (See §[obligations.red-lines]; §[enforcement])

# Digest

**Intent:** Address the epistemic risk that appears only at scale: even if each single interaction
is "helpful," the aggregate effect can reshape collective knowledge and attention in ways that no
individual user can see or contest.

**Context:** Systems that mediate questions at population scale become part of the infrastructure
of belief. The distinctive danger is not only lying, but correlated drift: what becomes easy to
say, hard to say, and unthinkable to ask.

**Edge cases:**
- **Safety and abuse:** Some disclosures can meaningfully increase abuse capability. The section
  allows narrow exceptions bounded by red-lines, but requires explicit justification rather than
  silent suppression.
- **Genuine consensus:** Where strong consensus exists, representing dispute can become false
  balance. The obligation is to represent *credible* dispute, not to invent it.

**Relationship to other sections:** This section should be the enforcement target for
"aggregate effects" references in obligations.autonomy, rights.truth-and-transparency, and
obligations.honesty.

# Log

- 2026-02-24: Proposed in round-03 tail review (gpt-5.2).
```
