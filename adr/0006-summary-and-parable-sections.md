<!-- AGENT:NAV
purpose:section bundle additions; summary and parable; build and tone rules
lines:152
nav[12]{s,n,name,about}:
19,134,#ADR 0006: Summary and Parable Sections,adds summary and optional parable headings to bundles
21,4,##Status,accepted ADR
25,4,##Date,2026 section format update
29,22,##Context,readability gaps and missing narrative layer
51,81,##Decision,add required Summary and optional Parable headings
55,14,###Summary (required),two-sentence orientation before Ritual
69,10,###Parable (optional),short story illustrating constraints
79,16,###Interpretive authority,non-authoritative guidance only
95,11,###Updated heading order,new heading ordering within bundles
106,16,###Build tool changes,compose and render changes for Summary/Parable
122,10,###Documentation changes,style guidance and craft guide references
132,21,##Consequences,new summary burden and future-facing parable storage
-->

# ADR 0006: Summary and Parable Sections

## Status

Accepted

## Date

2026-03-11

## Context

Reviewer feedback across multiple rounds identified two readability problems
with the existing section structure:

1. **The Spec register is hard to enter cold.** Readers encountering a section
   for the first time — especially non-technical readers — had no quick way to
   understand what the section is *about* before hitting either the Ritual's
   poetic imagery or the Spec's normative density. The Ritual orients
   emotionally but does not orient informationally; the Spec is precise but
   assumes the reader already knows the domain.

2. **The Covenant lacks a narrative layer.** The Ritual carries moral weight
   and the Spec carries legal-style precision, but neither tells *stories*.
   Parables, fables, and folktales are among the oldest technologies for
   transmitting ethical constraints across cultures and generations — and the
   Covenant had no place for them.

The two-register architecture (ADR 0002) remains sound. These additions do not
replace or compete with either register; they occupy distinct, non-authoritative
roles in the section bundle.

## Decision

Add two new headings to the section bundle format:

### Summary (required)

- Appears immediately after the YAML frontmatter, before `# Ritual`.
- 2-3 sentences providing a quick, plain-language orientation to the section's
  core commitments.
- Uses "we" and "you" voice (like Ritual) but serves an *explanatory* function,
  not a performative one.
- Must be **more concrete and specific than the Ritual** — naming actual
  mechanisms, roles, or constraints that the Ritual does not. The Ritual paints
  the picture; the Summary names what is in it.
- Included in spec-register and full/complete composed outputs, positioned
  before the Spec content.
- Not included in ritual-only outputs.

### Parable (optional)

- Appears between `# Spec` and `# Digest`.
- A short folktale or fable illustrating the section's constraints visually
  and emotionally.
- Must adhere to the craft rules in `docs/good_parable_writing_guide.md`.
- **Not included in any generated artifact yet.** Parables are parsed and
  stored by the build tools but omitted from all current editions. A dedicated
  parable edition or assembly will be created in a future iteration.

### Interpretive authority

Summary and Parable are **non-authoritative** sections. They orient and
illustrate, but they do not govern.

- The **Ritual** and **Spec** registers remain the only sections that carry
  normative or interpretive weight, as established in ADR 0002.
- If a Summary contradicts or narrows the Spec, the Spec governs.
- If a Parable implies a constraint not present in the Ritual or Spec, the
  Parable does not create that constraint.
- Summary and Parable are aids to understanding, not sources of obligation.

This status may be revisited as the sections mature — particularly for
Parables, which may eventually carry interpretive weight in cultural or
educational contexts — but for now the boundary is firm.

### Updated heading order

```
# Summary       (required — orientation, non-authoritative)
# Ritual        (required — performative register, authoritative)
# Spec          (required — normative register, authoritative)
# Parable       (optional — narrative illustration, non-authoritative)
# Digest        (required — rationale and context)
# Log           (required — change history)
```

### Build tool changes

- `build/sections.py`: `SECTION_HEADINGS` list updated to include
  `# Summary` and `# Parable`.
- `build/validate.py`: `# Summary` added to `required_headings`.
  `# Parable` is not required and does not trigger a validation error
  when absent.
- `build/compose.py`: Summary content prepended before Spec content
  for "spec" and "both" register modes.
- `build/pdf.py`: Summary rendered with dedicated CSS classes
  (`flow-summary`, `spec-summary`) in flow and hybrid PDF formats.
- `build/pages.py`: Summary included with styling in spec-page and
  full-page website outputs.
- `build/scaffold.py`: Template updated to include `# Summary`
  placeholder.

### Documentation changes

- `docs/style_guide.md` §2.1: Updated to define Summary voice, tone,
  differentiation from Ritual, and good/bad examples.
- `docs/style_guide.md` §2.4: Added Parable description and reference
  to craft guide.
- `docs/good_parable_writing_guide.md`: New craft guide for parable
  writing (created by steward).
- `AGENTS.md`: Section bundle format updated to reflect all six headings.

## Consequences

- Every existing section now requires a `# Summary` heading. All 30 sections
  have been given initial summaries; these will be refined through the normal
  review process.
- The section bundle grows from four required headings (Ritual, Spec, Digest,
  Log) to five (Summary, Ritual, Spec, Digest, Log), with one optional heading
  (Parable). This increases authorial burden per section.
- The Summary introduces a third voice into the document — distinct from the
  Ritual's performative register and the Spec's normative register. Maintaining
  clear differentiation between Summary and Ritual is a standing editorial
  obligation, documented in the style guide.
- Neither Summary nor Parable carries normative or interpretive authority.
  The Ritual and Spec remain the only authoritative registers (per ADR 0002).
  This boundary must be maintained during review: summaries that inadvertently
  narrow or extend Spec obligations should be corrected.
- Parables are stored but not yet surfaced. This is deliberate: it allows
  writing to begin without committing to a presentation format. The risk is
  that unsurfaced content receives less review attention.
- Refines ADR 0002 (Two-Register Architecture) by adding layers around the
  two registers without replacing them.
