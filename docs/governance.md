# Governance

## Stewardship

Covenant is currently stewarded by **Ryan Kelln**. The steward has final authority over merges to the `main` branch. This model applies until the project matures enough to warrant a broader governance structure.

## Amendment Process

### Proposing Changes

Anyone may propose changes via GitHub Pull Request. All PRs must:

1.  Pass CI validation (`make validate`)
2.  Include rationale for the change (in the PR description and in the section's Digest/Log)
3.  Be reviewed by the steward

### Status Transitions

Sections progress through these statuses:

- **`draft`** — work in progress, may change significantly
- **`candidate`** — proposed for ratification, open for public comment
- **`ratified`** — accepted into the stable covenant; changes require a formal amendment PR with explicit rationale
- **`deprecated`** — superseded or removed; retained for historical record

Transitions: - `draft` → `candidate`: requires complete Ritual, Spec, and Digest; all dependencies must be `candidate` or `ratified` - `candidate` → `ratified`: requires steward approval after a review period - `ratified` → `deprecated`: requires a replacement section or explicit rationale for removal - Any status → `draft`: allowed at steward discretion (e.g., for major rewrites)

### Register Hierarchy

When the Ritual and Spec registers of a section diverge in meaning:

- The **Spec register** is authoritative for obligation and enforcement.
- The **Ritual register** is authoritative for intent and orientation.
- Where they conflict, Spec governs what is *required*; Ritual governs what is *aspired to*.
- Reconciling divergence is a standing obligation of the steward.

## Versioning

Releases follow semantic versioning:

- **MINOR** (e.g., v0.2.0): adds sections, introduces major terms, or changes normative commitments
- **PATCH** (e.g., v0.1.1): clarifies wording, fixes build/formatting, updates references

A release is tagged when all assemblies build cleanly and the steward considers the state coherent enough to be cited.

## Forks

Forks are welcome and encouraged. See [FORKING.md](../FORKING.md).
