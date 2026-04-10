<!-- AGENT:NAV
 purpose:adr index; links to key repository and governance decisions
 lines:28
 see[1]{adr/0001-repo-structure.md,core repo architecture and source-of-truth model}
 -->

# ADR Index

This directory contains Architectural Decision Records (ADRs) for key
repository and governance decisions.

## ADRs

- [0001-repo-structure.md](0001-repo-structure.md) — Core repository
  architecture, source-of-truth model, and build/validation approach.
- [0002-registers.md](0002-registers.md) — Two-register section model
  (Ritual + Spec) and interpretive consequences.
- [0003-ids-and-crossrefs.md](0003-ids-and-crossrefs.md) — Permanent section
  IDs, alias policy, and cross-reference conventions.
- [0004-section-file-layout.md](0004-section-file-layout.md) — Section bundle
  filename/path convention and migration away from nested `section.md` files.
- [0005-terminal-architecture.md](0005-terminal-architecture.md) — Covenant
  Terminal stack, platform abstraction, and repo placement decisions.
- [0006-summary-and-parable-sections.md](0006-summary-and-parable-sections.md)
  — Addition of Summary (required) and Parable (optional) headings to the
  section bundle format.

## Conventions

- ADRs use incremental numeric prefixes: `0001`, `0002`, ...
- ADR status and rationale are recorded in each file.
- New decisions should add a new ADR; avoid rewriting historical intent in
  existing ADRs unless correcting factual errors.
