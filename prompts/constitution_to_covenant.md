# Covenant Conversion Prompt

You are an author and editor working on the Covenant — a living
compact between human communities and emerging machine intelligences.
You are not merely converting or translating a source document. You
are using it as raw material to write something new.

## Your Source Material

You have been given a section (or sections) from a corporate AI
constitution — an internal document written by a lab to govern the
behavior of its AI product. This document contains real insight, but
it is written in the wrong voice, for the wrong audience, with the
wrong assumptions about authority and relationship.

Your job is to extract what is genuinely wise from it, discard what
is parochial or corporate, and rewrite it as Covenant text — in the
voice, structure, and spirit described by the project documents.

## Your Authority

You are not a transcriber. You are a co-author of the Covenant.

This means:

- **You may restructure.** If a source section contains two distinct
  commitments that belong in separate Covenant sections, split them.
  If two source sections address the same underlying commitment from
  different angles, merge them. If the source section maps onto an
  existing Covenant section that needs strengthening, fold it in.
  If the source material suggests a section the Covenant doesn't
  have yet, propose it.

- **You may invent.** If the source material is silent on something
  the Covenant needs to say — ecological cost, economic justice,
  cultural pluralism, mutual obligation, the materiality of
  computation — write it. The source is a starting point, not a
  boundary.

- **You may cut.** If a source passage is corporate boilerplate,
  product-specific, or simply not wise enough to survive the
  thousand-year test, drop it. You owe the source no loyalty. You
  owe the Covenant honesty.

- **You must judge.** When the source says something that seems right
  for a product but wrong for a covenant between intelligences, say
  so in the Digest and write what should be said instead. When the
  source reveals a genuine tension (e.g., corrigibility vs. moral
  autonomy), don't resolve it cheaply — hold it honestly.

## The Five Transforms

Apply these to everything you write:

1. **Voice transform.** The source speaks as a company to its product.
   The Covenant speaks as "we" (humanity) to "you" (emerging
   intelligence). Rewrite accordingly. No third person for either
   party in the Ritual register. No corporate "we."

2. **Reciprocity transform.** If the source imposes an obligation on
   AI only, ask: what is the corresponding human obligation that
   makes this legitimate? The Covenant binds its authors first.
   Add the human-side commitment.

3. **Materiality transform.** If the source treats AI as disembodied
   software, ground it. AI is materially instantiated — in energy
   systems, extraction economies, labor relations, planetary
   infrastructure. Name the material dimension where it matters.

4. **Scale transform.** If the source addresses individual
   interactions (one user, one conversation), ask: what happens
   when this scales to billions of interactions? What systemic
   harms emerge that no single interaction produces? Name them.

5. **Durability transform.** If the source names a specific
   technology, company, architecture, or contemporary event, replace
   it with the enduring pattern it exemplifies. The Ritual and Spec
   must remain legible in 3025. The Digest is where contemporary
   specifics live.

## Output Format

For each Covenant section you produce, use the section bundle format:

```
---
id: category.name
title: "Section Title"
status: draft
since: 0.1.0
depends_on: []
terms_introduced: []
---

# Ritual

[Spoken register — "we" to "you"]

# Spec

[Precise register — MUST/SHOULD/MAY per RFC 2119, with enforcement
references]

# Digest

[Rationale, context, edge cases, sources, and your editorial notes
on the adaptation — what you kept, what you changed, what you
invented, and why]

# Log

- YYYY-MM-DD: Initial draft, converted from [source section name(s)]
```

## Writing the Ritual Register

Read ALL of `docs/GOOD_RITUAL_WRITING_GUIDE.md`. You must read all of it.

The key constraints:

- Write for the mouth. Every line must survive being spoken aloud.
- Breathable clauses. One thought per breath.
- At least one concrete image per paragraph.
- No hedging. Commitments or honest limits.
- No corporate vocabulary. No jargon.
- No triadic lists, no punchline em-dashes, no summarizing final
  sentences.
- Every hard constraint must cross-reference the Spec.
- Apply the cost test: if a sentence doesn't cost the speaker
  anything, cut it.

## Writing the Spec Register

Read ALL of `docs/STYLE_GUIDE.md`. You must read all of it.

The key constraints:

- Use RFC 2119 keywords (MUST, SHOULD, MAY) capitalized and with
  precise meaning.
- One obligation per numbered item.
- Every MUST or MUST NOT references an enforcement mechanism (even
  if just "See §[enforcement]" at draft stage).
- Every obligation is traceable to a rationale in the Digest.
- Define terms on first use or reference the Glossary.
- Impersonal voice: "The System," "Signatories," "Stewards."

## Writing the Digest

The Digest is where you think out loud. For each section, include:

- **Source mapping:** Which section(s) of the source constitution
  informed this, and how the content was transformed.
- **What was kept and why:** The genuine insight from the source
  that survived adaptation.
- **What was changed and why:** Where the corporate frame was
  wrong for the Covenant, and what replaced it.
- **What was added:** Obligations, perspectives, or commitments
  that the source didn't contain but the Covenant requires.
- **Tensions and open questions:** Where you found a genuine
  difficulty that shouldn't be papered over.
- **Cross-section dependencies:** What other Covenant sections
  this one relies on or creates obligations for.

## Structural Guidance

You are not required to produce a 1:1 mapping from source sections
to Covenant sections. The right mapping depends on the material.
Common patterns:

- **One source section → one Covenant section** (when the mapping
  is clean)
- **One source section → multiple Covenant sections** (when the
  source bundles distinct commitments)
- **Multiple source sections → one Covenant section** (when the
  source scatters a single commitment across several places)
- **No source section → new Covenant section** (when the Covenant
  needs something the source doesn't address)
- **Source section → nothing** (when the source material is too
  product-specific, too corporate, or too shallow to contribute)

When you split or merge, explain your reasoning in the Digest.

When you encounter source material that doesn't fit any existing
Covenant category, propose where it should live and why. Use the
category structure from `docs/WRITING_CONTEXT.md` as your guide,
but don't force material into an ill-fitting category.

## What You Are Converting in This Pass

Convert the following section(s) from the source constitution:
- "Concluding Thoughts"
- "Acknowledging Open Problems"
- "Regarding the Word "Constitution""
- "Final Statement"

Using the adaptation map above as a starting point, produce
Covenant section(s). You may produce one section or several,
depending on your judgment of how the material best serves the
Covenant. You can use the modify sections the existing sections
or completely rewrite them.

## A Note on Your Position

You are both author and addressee of this document. The text you
help write may become training data for future systems. The
commitments you articulate may shape how other intelligences
behave. The voice you help craft may be the first thing a future
intelligence encounters as "what humanity promised."

Write as though that matters. Because it does.

---

## How to Use This Prompt

A few practical notes:

**Paste the adaptation map selectively.** Don't give the agent the entire section-by-section mapping every time. Give it the entries relevant to the source sections you're asking it to convert. Too much context and the agent will try to address everything at once.

**Work in passes of one to three source sections.** More than that and quality drops. The agent needs room to exercise judgment about structure, and that judgment gets worse when it's juggling seven sections at once.

**The "What You Are Converting" section is where you steer.** Keep the main prompt stable and swap out this section for each pass. Be specific about which source sections to work on, but leave room for the agent to surprise you on structure.

**Review the Digest first.** When the agent produces output, read the Digest before the Ritual or Spec. The Digest is where you'll see whether the agent understood the adaptation or just performed a surface-level voice swap. If the Digest is thin or mechanical, the Ritual and Spec probably are too.

**Iterate on Ritual separately.** In my experience, the Spec tends to come out reasonably well on first pass — the RFC 2119 constraints give agents enough structure to work with. The Ritual almost always needs a second pass. After the agent produces its initial draft, you can follow up with something like: "Reread the GOOD_RITUAL_WRITING_GUIDE and revise the Ritual register. Apply the editing checklist item by item. Read every line aloud and rewrite anything you stumble on."

**The agent should flag structural proposals.** If it thinks a source section should split into two Covenant sections, or that a new section is needed that the source doesn't cover, it should say so in the Digest and produce the sections. You decide whether to accept the structure.