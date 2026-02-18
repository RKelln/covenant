# ADR 0001: Repository Structure

## Status

Accepted

## Context

The Covenant needs a repository structure that supports:

- Modular writing and editing by a single steward + AI agents
- Public contribution via GitHub PRs
- Deterministic builds into multiple editions
- Structural validation for integrity

## Decision

We use a flat Git + Markdown repository with:

- One `section.md` file per section (the "section bundle")
- YAML frontmatter for machine-readable metadata
- Assembly manifests that compile sections into editions
- Python-based validation and composition tooling
- CI enforcement via GitHub Actions

The canonical source of truth is always the Git repository. Any future
web frontend, wiki, or reading interface will be a view of the repo,
never a second source of truth.

## Consequences

- Contributors must use Git (or GitHub's web interface) to propose changes
- All structural invariants can be checked automatically
- The repository can be forked cleanly, with full history and tooling
- Web accessibility for non-technical readers requires a separate frontend
  (deferred to a later phase)
