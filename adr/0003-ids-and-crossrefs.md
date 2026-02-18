# ADR 0003: IDs and Cross-References

## Status

Accepted

## Context

The Covenant is modular. Sections reference each other (dependencies,
definitions, related rights). These references must be stable across
renames and forking.

## Decision

We use dot-delimited permanent section IDs (e.g., `rights.dignity`).

- IDs are mandatory in the YAML frontmatter of every `section.md`.
- References use the syntax `§[section.id]`.
- Naming convention: `[category].[name]` or `[category].[subcategory].[name]`.
- IDs are never changed once ratified. Renames use `aliases.yml`.

## Consequences

- Machine-parsable dependency graphs
- Broken links can be caught by validation tools
- Forking communities can refer to "v0.1.0 rights.dignity" as a baseline
- Documentation remains coherent even if filenames are restructured
