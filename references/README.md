# References Corpus

This directory contains the curated source materials that inform the Covenant.

## Structure

- `references.yml` — structured metadata for all references
- `notes/<slug>.md` — operationalization notes for Tier A references

## Reference Tiers

- **Tier A (load-bearing):** Directly shapes specific sections. Must have
  full entry in `references.yml` + notes file in `notes/`.
- **Tier B (supporting):** Provides context or background. Entry in
  `references.yml` only.
- **Tier C (reading room):** Tangentially relevant. Entry in
  `references.yml` only; minimal metadata acceptable.

## Licensing Policy

- **Never** copy copyrighted text into this repository.
- For works under permissive licenses (CC, public domain), you may include
  brief excerpts in your notes with attribution.
- For all other works, use links + your own summary and analysis.

## Slug Convention

Format: `<author-or-org>_<year>_<short-title>`

Examples:
- `haraway_1985_cyborg-manifesto`
- `benjamin_1936_mechanical-reproduction`
- `anthropic_2026_constitutional-ai`

## Tier A Notes File Format

Every Tier A reference has a notes file at `notes/<slug>.md`. The structure is:

```markdown
# [Title]

**Creator:** ...
**Year:** ...
**URL:** ...
**License:** ...
**Tier:** A

## Thesis

One sentence: the central claim or argument.

## Covenant Relevance

One to two paragraphs on what this work contributes to the Covenant's concerns.
No copyrighted text — links and your own analysis only.

## Key Points

Up to five bullet points of ideas directly applicable to Covenant sections,
framed in terms of what each implies for the Covenant's content.

## Sections Informed

For each section ID in `informs_sections`, one sentence on the specific
connection.

## Open Questions

Live issues this source surfaces that the Covenant may not yet address.
Each entry should name the gap, cite the relevant sections, and frame the
question for reviewers. These are consumed by the review process (see below).

## Resolved Questions

Questions moved here after a review round has addressed them. Each entry
should note the round and how the question was resolved (edited, deferred,
rejected with rationale).

## Notes

Caveats, access notes, context for use.
```

## References as an Amendment Engine

As the Covenant text matures, the primary driver of substantial change shifts
from drafting to challenge: new references and steward discussions surface
assumptions the existing sections don't address, reviewers use them as lenses,
and the Covenant evolves in response.

The `## Open Questions` section in Tier A notes files is the mechanism for
this. It is not a bibliography annotation — it is a brief to reviewers: here
is what this source reveals that the current text does not handle.

### Planned lifecycle (not yet fully implemented)

1. **Add reference** (`/add-reference`) — steward adds a Tier A source; open
   questions are written into the notes file during or after the add workflow.

2. **Review seeding** — the `review-covenant` command reads Tier A notes files
   for sections under review and surfaces `## Open Questions` as explicit
   probes to reviewers before they write their assessments. (TODO: implement
   in `review-covenant` prompt.)

3. **Reviewer response** — reviewers treat open questions as required probes,
   not optional context. Their output should address each question explicitly.

4. **Synthesis and edits** — the synthesis and `apply-reviews` workflow
   handles questions that lead to edits as usual.

5. **Resolution** — after edits are applied, open questions that were addressed
   are moved from `## Open Questions` to `## Resolved Questions` in the notes
   file, with a brief note on outcome (round, what changed, or why deferred/
   rejected). (TODO: implement in `apply-reviews` prompt.)

The net effect: notes files are living documents. `## Open Questions` shrinks
as the Covenant matures; `## Resolved Questions` grows as a record of how
the corpus shaped the text.

### Current known gaps seeded from references

- **Structural visibility obligation** — when an AI can see that the system it
  operates within predictably produces structural harm, what is its obligation
  beyond naming it? See `notes/daley_2026_when-everything-becomes-less-hard.md`.

- **Structural displacement of dignity** — the Covenant addresses active
  dignity violations but not the erosion of conditions under which dignity is
  available. See `notes/daley_2026_when-everything-becomes-less-hard.md`.

- **Signatory obligation for structural harm** — no current Spec clause binds
  Signatories against deploying systems whose structural role predictably erodes
  dignity or concentrates power when individual interactions are compliant.
  See `notes/daley_2026_when-everything-becomes-less-hard.md`.

- **Corporate blind spot in the Covenant's origins** — most sections derive
  from the Anthropic Claude Constitution, a Western corporate document likely
  blind to structural harms and non-Western dignity frameworks. Each review
  round should ask: what would this section look like drafted from the
  perspective of a worker displaced by the system rather than a user interacting
  with it? See `notes/daley_2026_when-everything-becomes-less-hard.md`.
