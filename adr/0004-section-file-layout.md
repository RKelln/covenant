# ADR 0004: Section File Layout and Naming

## Status

Accepted

## Date

2026-02-20

## Context

The previous repository layout used many files named `section.md` in nested
folders (for example, `sections/03-obligations/harm/section.md`).

This created frequent ambiguity in human and agent collaboration:

- Change reports often read as "edited section.md" without clear identity.
- File references in reviews and chat were harder to scan quickly.
- Tooling and manifests depended on a special filename rather than a general
  section-bundle convention.

The project still requires one Markdown bundle per section containing Ritual,
Spec, Digest, and Log in a single file.

## Decision

Adopt category-level named section bundles:

- Top-level sections use `sections/<category>/<name>.md`
  (for example, `sections/00-preamble/preamble.md`).
- Category children also use `sections/<category>/<name>.md`
  (for example, `sections/03-obligations/harm.md`).
- The canonical rule is one section bundle `.md` file per section,
  not one specially named `section.md` file.

Tooling and manifests must treat section bundles as general Markdown files:

- Validator scans section bundle files by `*.md` under `sections/`.
- Scaffolder creates `sections/<category>/<id-tail>.md`.
- Assemblies list explicit `.md` paths for section bundles.

## Consequences

- File references become unambiguous in PRs, chat, and review workflows.
- Agents and humans can reference changes by meaningful filenames.
- Existing docs and schemas must avoid assuming the filename `section.md`.
- Historical and archive paths may continue to use legacy layout unless
  explicitly migrated.
