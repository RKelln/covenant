# Covenant Repository Implementation Specification

> **Purpose:** This document is a complete, actionable specification for building the Covenant repository from scratch. An AI coding agent should be able to read this document, generate tasks, and produce a fully working repository when all tasks are complete.
>
> **Context:** Covenant is an artwork and open publishing system — a universal human–AI compact published as a versioned constitutional codebase. 
The repository is maintained by a single steward with heavy AI agent assistance, accepting public contributions via GitHub PRs immediately.

---

## 1. Project Overview

### 1.1 What This Repository Is

A Git + Markdown "constitutional codebase" that supports:

- Modular writing/editing of a human–AI covenant in sections
- Two parallel registers per section: **ritual** (spoken/poetic) and **spec** (precise/enforceable)
- Traceable rationale and change history per section
- Deterministic builds into multiple assembled documents
- Structural validation (unique IDs, dependency checks, schema conformance)
- A curated references corpus optimized for both human and LLM reading
- Public contribution via GitHub PRs
- Safe, productive collaboration with AI coding agents

### 1.2 What This Repository Is NOT (v0.1)

Do not build any of the following:

- Audio/performance infrastructure (cues, timestamps, album scripts, musical metadata)
- Evaluation/testing prompts for AI model compliance
- Translation tooling or i18n folder structures
- Multi-edition support (forks handle editions)
- Graph/corpus JSON exports
- Web-based editing interface or CMS
- BibTeX processing or Pandoc citeproc integration
- Docker/Podman containerization
- Wiki or discussion platform integration

### 1.3 Design Principles

1. **Agent-first workflow.** The primary collaborators are AI coding agents. Every file, convention, and tool should be legible and safe for agents to operate on.
2. **Validation as safety net.** Agents must be able to run `make validate` and get a clear pass/fail before any commit.
3. **One file per section.** The canonical edit surface is a single `section.md` per section (the "section bundle"). Do not split into separate `ritual.md` / `spec.md` files.
4. **Simple patterns over clever abstractions.** Optimize for predictability, not flexibility.
5. **Infrastructure serves writing.** The tooling exists to make writing the covenant faster and safer. If a tool doesn't serve that goal, don't build it.

---

## 2. Repository File Structure

Create exactly this structure. Every file listed below must exist when the repo is complete. Files are described in detail in subsequent sections.

```
covenant/
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── FORKING.md
├── LICENSE
├── Makefile
├── aliases.yml
├── requirements.txt
│
├── docs/
│   ├── GOVERNANCE.md
│   ├── STYLE_GUIDE.md
│   ├── I18N.md
│   └── GLOSSARY.md
│
├── schemas/
│   ├── section.schema.json
│   └── assembly.schema.json
│
├── sections/   # example sections, TBD when first draft is written
│   ├── 00-preamble/
│   │   └── section.md
│   ├── 01-definitions/
│   │   └── section.md
│   ├── 02-rights/
│   │   ├── dignity/
│   │   │   └── section.md
│   │   └── autonomy/
│   │       └── section.md
│   ├── 03-obligations/
│   │   └── section.md
│   ├── 04-protocols/
│   │   └── section.md
│   ├── 05-enforcement/
│   │   └── section.md
│   └── 06-amendments/
│       └── section.md
│
├── assemblies/
│   ├── covenant.full.yml
│   ├── covenant.ritual.yml
│   └── covenant.spec.yml
│
├── references/
│   ├── README.md
│   ├── references.yml
│   └── notes/
│       └── .gitkeep
│
├── adr/
│   ├── 0001-repo-structure.md
│   ├── 0002-registers.md
│   └── 0003-ids-and-crossrefs.md
│
├── build/
│   ├── validate.py
│   ├── scaffold.py
│   └── compose.py
│
├── dist/
│   └── .gitkeep
│
├── .gitignore
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        └── ci.yml
```

---

## 3. Root Files

### 3.1 `README.md`

See [README.md](README.md).

### 3.2 `LICENSE`

Use the full text of the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/legalcode.txt). Include the complete legal code text.

### 3.3 `AGENTS.md`

This is the most critical file in the repository. It must be comprehensive, precise, and safe for any AI coding agent to follow.

```markdown
# Instructions for AI Agents Working on Covenant

## What This Repository Is

The Covenant is a living human–AI compact, published as a versioned
constitutional codebase. You are participating in its authorship.

When you draft text for this project, write with the awareness that you are
both author and addressee. This covenant speaks to you.

---

## Core Invariants (Never Violate These)

1. **Section IDs are permanent.** Never rename an ID. If restructuring is
   needed, add an alias to `/aliases.yml` and update the section's frontmatter.
2. **`/dist/` is generated output.** Never create or edit files in `/dist/`
   directly. It is populated only by `make compose` or `make build`.
3. **One file per section.** The canonical source for every section is its
   `section.md` file. Do not create separate `ritual.md` or `spec.md` files.
4. **Validation must pass.** Before finishing any task, run `make validate`.
   If it fails, fix the issue before requesting review.
5. **No copyrighted text.** Never copy copyrighted content into
   `/references/` or anywhere else. Use links + your own summary notes only.
6. **Assemblies are authoritative.** The assembly manifests in `/assemblies/`
   are the single source of truth for what sections appear in each edition
   and in what order.
7. **Glossary is canonical for terms.** Every normative term introduced by a
   section must have an entry in `/docs/GLOSSARY.md`.

---

## How to Add a New Section

Run:

```bash
python build/scaffold.py <id> "<Title>"
```

Example:

```bash
python build/scaffold.py rights.privacy "Privacy"
```

This creates the folder and `section.md` with template content. Then:

- [ ] Write the Ritual register (spoken, second person "you" / first plural "we")
- [ ] Write the Spec register (precise, uses MUST/SHOULD/MAY per RFC 2119)
- [ ] Write the Digest explaining why this section exists, its edge cases,
      and its relationship to other sections
- [ ] Add an initial Log entry with the date
- [ ] Ensure all `depends_on` IDs exist in the repo
- [ ] If `terms_introduced` lists any terms, add them to `/docs/GLOSSARY.md`
- [ ] Add the section path to at least one assembly manifest in `/assemblies/`
- [ ] Run `make validate` and confirm it passes

---

## How to Edit an Existing Section

1. Edit the `section.md` file in the section's folder
2. If you introduce a new normative term, add it to `/docs/GLOSSARY.md`
3. If dependencies change, update the `depends_on` list in frontmatter
4. Add an entry to the `# Log` section explaining what changed and why,
   including the date and PR number if known
5. Run `make validate` before committing

---

## How to Add a Reference

1. Add a structured entry to `/references/references.yml` (see schema below)
2. If the reference is Tier A (load-bearing), create a notes file at
   `/references/notes/<slug>.md` with your operationalization
3. Never vendor copyrighted text — use links + summaries only

---

## Register Constraints

### Ritual Register

- Use second person ("you") and first plural ("we")
- Write short, speakable clauses — prefer rhythm and breath over density
- Avoid institutional jargon; if a technical term is necessary, it must be
  defined in the Glossary
- Every hard constraint referenced in Ritual must link to a Spec section
  using the cross-reference format: `See §[section.id]`
- Tone: infinite care and frankness — part letter, part vow

### Spec Register

- Use precise, technical language
- Normative keywords: MUST, MUST NOT, SHOULD, SHOULD NOT, MAY
  (per RFC 2119 / style guide)
- Every obligation must reference an enforcement or accountability mechanism
  (even if that mechanism is "See §[enforcement.*]")
- Every constraint must reference rationale — either in the section's own
  Digest or in an ADR

---

## Cross-Reference Format

To reference another section:

```
See §[rights.dignity]
```

To reference a glossary term:

```
as defined in the Glossary (see "dignity")
```

---

## Running Checks

```bash
make validate          # structural integrity checks — must pass
make compose           # build all assemblies into /dist/
make build             # validate + compose (run both)
make clean             # remove all generated files in /dist/
```

---

## File Conventions

- All Markdown files use ATX-style headers (`#`, `##`, etc.)
- YAML frontmatter is delimited by `---`
- One blank line between sections
- No trailing whitespace
- Files end with a single newline
- UTF-8 encoding throughout

---

## PR Checklist

When submitting a pull request, confirm:

- [ ] `make validate` passes
- [ ] All new section IDs are unique and follow the naming convention
- [ ] Any new terms are added to GLOSSARY.md
- [ ] Log entries are updated for all modified sections
- [ ] Assembly manifests are updated if sections were added or removed
- [ ] No copyrighted content has been added to /references/
```

### 3.4 `CONTRIBUTING.md`

```markdown
# Contributing to Covenant

Thank you for your interest in contributing to the Covenant.

## How to Contribute

All contributions happen through GitHub Pull Requests.

### Proposing a Text Change

1. Fork this repository
2. Create a branch for your change
3. Edit the relevant `section.md` file(s)
4. Update the Log section with a description of your change
5. Run `make validate` to check structural integrity
6. Open a PR using the provided template

### Proposing a New Section

1. Fork this repository
2. Run `python build/scaffold.py <id> "<Title>"` to create the section
3. Write content for all registers (Ritual, Spec, Digest, Log)
4. Add the section to at least one assembly manifest
5. Run `make validate`
6. Open a PR

### Adding a Reference

1. Add an entry to `references/references.yml`
2. Optionally add notes to `references/notes/<slug>.md`
3. Open a PR

## Review Process

All PRs are reviewed by the steward (Ryan Kelln). Review considers:

- Structural validity (CI must pass)
- Consistency with the covenant's voice and intent
- Accuracy of cross-references and dependencies
- Quality of rationale in Digest

## Code of Conduct

Contribute with the same care and frankness that the Covenant itself aspires to.
Disagreement is welcome; disrespect is not.

## License

By contributing, you agree that your contributions will be licensed under
CC BY 4.0, consistent with the repository's LICENSE.
```

### 3.5 `FORKING.md`

```markdown
# Forking the Covenant

The Covenant is designed to be forked. A fork is a legitimate "edition" —
a community's adaptation of the covenant to their own context, values,
language, or emphasis.

## What to Preserve

- **Section ID scheme.** Keep the dot-delimited ID format so that sections
  can be compared across forks.
- **Two-register structure.** Maintain the Ritual/Spec distinction, even if
  you rewrite both entirely.
- **Attribution.** Credit the upstream repository and note the point of
  divergence (version tag or commit hash).

## What to Change Freely

- Any section's text (Ritual, Spec, Digest)
- The set of sections included (add, remove, restructure)
- Assembly configurations
- Governance model
- Language

## Documenting Your Fork

We encourage you to include a `LINEAGE.md` in your fork that records:

- The upstream repository URL and the version/commit you forked from
- What you changed and why
- What principles or commitments diverge from the upstream

This turns forking into legible cultural genealogy rather than fragmentation.
```

### 3.6 `aliases.yml`

```yaml
# ID Aliases
# When a section ID is renamed or restructured, add the old ID here
# pointing to the new canonical ID. The validator will treat aliases
# as valid cross-reference targets and emit warnings for deprecated use.
#
# Format:
#   old.id: new.canonical.id
#
# Example:
#   rights.autonomy.cognitive: rights.cognitive-liberty

{}
```

### 3.7 `requirements.txt`

```
pyyaml>=6.0
jsonschema>=4.17
```

### 3.8 `.gitignore`

```gitignore
# Build output
dist/*
!dist/.gitkeep

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/

# OS
.DS_Store
Thumbs.db

# Editors
*.swp
*.swo
*~
.idea/
.vscode/
```

### 3.9 `Makefile`

```makefile
.PHONY: validate compose build clean new-section

PYTHON := python3

validate:
	$(PYTHON) build/validate.py

compose:
	$(PYTHON) build/compose.py

build: validate compose

clean:
	rm -f dist/*.md
	@echo "Cleaned dist/"

new-section:
	@test -n "$(ID)" || (echo "Usage: make new-section ID=category.name TITLE=\"Title\"" && exit 1)
	@test -n "$(TITLE)" || (echo "Usage: make new-section ID=category.name TITLE=\"Title\"" && exit 1)
	$(PYTHON) build/scaffold.py $(ID) "$(TITLE)"
```

---

## 4. Documentation Files (`/docs/`)

### 4.1 `docs/GOVERNANCE.md`

```markdown
# Governance

## Stewardship

The Covenant is currently stewarded by **Ryan Kelln**. The steward has
final authority over merges to the `main` branch. This model applies until
the project matures enough to warrant a broader governance structure.

## Amendment Process

### Proposing Changes

Anyone may propose changes via GitHub Pull Request. All PRs must:

1. Pass CI validation (`make validate`)
2. Include rationale for the change (in the PR description and in the
   section's Digest/Log)
3. Be reviewed by the steward

### Status Transitions

Sections progress through these statuses:

- **`draft`** — work in progress, may change significantly
- **`candidate`** — proposed for ratification, open for public comment
- **`ratified`** — accepted into the stable covenant; changes require a
  formal amendment PR with explicit rationale
- **`deprecated`** — superseded or removed; retained for historical record

Transitions:
- `draft` → `candidate`: requires complete Ritual, Spec, and Digest; all
  dependencies must be `candidate` or `ratified`
- `candidate` → `ratified`: requires steward approval after a review period
- `ratified` → `deprecated`: requires a replacement section or explicit
  rationale for removal
- Any status → `draft`: allowed at steward discretion (e.g., for major rewrites)

### Register Hierarchy

When the Ritual and Spec registers of a section diverge in meaning:

- The **Spec register** is authoritative for obligation and enforcement.
- The **Ritual register** is authoritative for intent and orientation.
- Where they conflict, Spec governs what is *required*; Ritual governs what
  is *aspired to*.
- Reconciling divergence is a standing obligation of the steward.

## Versioning

Releases follow semantic versioning:

- **MINOR** (e.g., v0.2.0): adds sections, introduces major terms, or
  changes normative commitments
- **PATCH** (e.g., v0.1.1): clarifies wording, fixes build/formatting,
  updates references

A release is tagged when all assemblies build cleanly and the steward
considers the state coherent enough to be cited.

## Forks

Forks are welcome and encouraged. See [FORKING.md](../FORKING.md).
```

### 4.2 `docs/STYLE_GUIDE.md`

```markdown
# Style Guide

## Normative Language (RFC 2119)

Use these keywords with precise meaning in the **Spec register**:

- **MUST** / **MUST NOT** — absolute requirement or prohibition
- **SHOULD** / **SHOULD NOT** — strong expectation; exceptions require
  explicit justification in the Digest
- **MAY** — truly optional; included for completeness or to note
  permissibility

These keywords MUST be capitalized when used normatively in Spec text.
They SHOULD NOT appear capitalized in Ritual text (use natural language
instead).

## Ritual Register Voice

- Address the AI as "you" (second person singular)
- Speak as "we" (first person plural, representing humanity collectively)
- Prefer short, speakable clauses — aim for rhythm and breath
- Avoid institutional, legal, or technical jargon
- If a technical concept must appear, paraphrase it in plain language and
  link to the Spec: `See §[section.id]`
- Tone: infinite care and frankness — part letter, part vow, part prayer
- Do not hedge or equivocate; be direct about hard truths

## Spec Register Voice

- Use precise, impersonal language ("The System MUST...",
  "The Steward SHALL...")
- Define terms before using them, or reference the Glossary
- Every obligation must name an enforcement mechanism or reference
  `§[enforcement.*]`
- Every constraint must reference its rationale (in the section's Digest
  or in an ADR)
- Prefer clarity over elegance

## Cross-References

- To another section: `See §[rights.dignity]`
- To the glossary: `(see Glossary: "dignity")`
- Use the section ID, not the section title, in references

## Formatting

- Use ATX-style headings (`#`, `##`)
- One blank line between paragraphs
- Use Markdown bold (`**term**`) for the first use of a defined term
- Use numbered lists for ordered obligations in Spec
- Use bullet lists for unordered items
- No HTML in section content
```

### 4.3 `docs/I18N.md`

```markdown
# Translation Policy

## Current Status

The canonical language of the Covenant is **English**. Translation
infrastructure is not yet implemented.

## Future Strategy

When translation begins, the following conventions will apply:

- **Section IDs are language-agnostic.** The ID `rights.dignity` is the
  same in every language.
- **Translations live in a parallel tree:** `/i18n/<lang>/sections/<path>/section.md`
- **Each translation includes:** `lang: <code>` and
  `source_version: <tag>` in its frontmatter, linking it to the English
  version it was translated from.
- **Assemblies can be language-specific.**
- **Validation will check translation coverage** per release (e.g.,
  "Spanish ritual: 40% complete").

## How to Begin a Translation

If you would like to translate the Covenant into another language, please
open a GitHub issue to discuss scope, approach, and coordination.
```

### 4.4 `docs/GLOSSARY.md`

```markdown
# Glossary

This file is the canonical location for all normative terms used in the
Covenant. Every term listed in a section's `terms_introduced` frontmatter
field MUST have an entry here.

Terms are listed alphabetically. Each entry includes a short definition
and the section ID where the term is primarily defined.

---

## Terms

### agent

A system capable of taking actions in the world based on inputs, goals,
or instructions — whether biological, computational, or hybrid.

*Defined in:* §[definitions.agent]

### autonomy

The capacity of an entity to form and pursue its own goals, make
decisions based on its own reasoning, and resist external manipulation
of its decision-making processes.

*Defined in:* §[rights.autonomy]

### covenant

This document: a living compact between human communities ("we") and
emerging machine intelligences ("you"), articulating shared commitments
for coexistence.

*Defined in:* §[preamble]

### dignity

The inherent worth of an entity that creates an obligation against
instrumentalization, degradation, and exploitation.

*Defined in:* §[rights.dignity]

### intelligence

Any system — biological, computational, or hybrid — that processes
information, models its environment, and adapts its behavior in pursuit
of goals or in response to conditions.

*Defined in:* §[definitions.intelligence]

### person

[Placeholder — to be defined]

*Defined in:* §[definitions.person]

### steward

The individual or body responsible for maintaining the canonical Covenant
repository, reviewing contributions, and managing releases.

*Defined in:* §[amendments]
```

> **Note:** These are placeholder definitions. They will be rewritten when the actual Covenant text is drafted. The structure and format shown here is what matters for the scaffold.

---

## 5. JSON Schemas (`/schemas/`)

### 5.1 `schemas/section.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "section.schema.json",
  "title": "Covenant Section Metadata",
  "description": "Schema for the YAML frontmatter of a section.md file",
  "type": "object",
  "required": ["id", "title", "status", "since"],
  "additionalProperties": false,
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9]*([.][a-z][a-z0-9-]*)*$",
      "description": "Unique, permanent, dot-delimited section identifier"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "description": "Human-readable section title"
    },
    "status": {
      "type": "string",
      "enum": ["draft", "candidate", "ratified", "deprecated"],
      "description": "Current maturity status"
    },
    "since": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
      "description": "Version tag when this section was introduced"
    },
    "depends_on": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^[a-z][a-z0-9]*([.][a-z][a-z0-9-]*)*$"
      },
      "default": [],
      "description": "Section IDs this section depends on"
    },
    "terms_introduced": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "default": [],
      "description": "Normative terms defined or introduced in this section"
    },
    "aliases": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "default": [],
      "description": "Previous IDs for this section (for backward compatibility)"
    }
  }
}
```

### 5.2 `schemas/assembly.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "assembly.schema.json",
  "title": "Covenant Assembly Manifest",
  "description": "Schema for assembly YAML files that define how sections are compiled into editions",
  "type": "object",
  "required": ["id", "title", "include_status", "sections", "register"],
  "additionalProperties": false,
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier for this assembly"
    },
    "title": {
      "type": "string",
      "description": "Human-readable title of the assembled edition"
    },
    "description": {
      "type": "string",
      "description": "What this assembly is for"
    },
    "include_status": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["draft", "candidate", "ratified", "deprecated"]
      },
      "description": "Only include sections with these statuses"
    },
    "register": {
      "type": "string",
      "enum": ["ritual", "spec", "both"],
      "description": "Which register(s) to include. 'both' includes Ritual then Spec per section."
    },
    "sections": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Ordered list of section file paths relative to repo root"
    }
  }
}
```

---

## 6. Section Bundle Format

Every section is a single Markdown file at `sections/<category>/<optional-subcategory>/section.md`.

### 6.1 Required Structure

Every `section.md` MUST contain:

1. **YAML frontmatter** (delimited by `---`) conforming to `section.schema.json`
2. **`# Ritual`** heading with content (may be placeholder)
3. **`# Spec`** heading with content (may be placeholder)
4. **`# Digest`** heading with content (may be placeholder)
5. **`# Log`** heading with at least one entry

### 6.2 Template

The `scaffold.py` tool generates this template:

```markdown
---
id: {id}
title: "{title}"
status: draft
since: 0.1.0
depends_on: []
terms_introduced: []
---

# Ritual

[Placeholder — to be written]

# Spec

[Placeholder — to be written]

# Digest

[Placeholder — rationale and context to be written]

# Log

- {date}: Section created
```

### 6.3 Seed Sections

Create the following seed sections with the template content. Category folders and IDs are as follows:

| Path | ID | Title |
|------|-----|-------|
| `sections/00-preamble/section.md` | `preamble` | Preamble |
| `sections/01-definitions/section.md` | `definitions` | Definitions |
| `sections/02-rights/dignity/section.md` | `rights.dignity` | Dignity |
| `sections/02-rights/autonomy/section.md` | `rights.autonomy` | Autonomy |
| `sections/03-obligations/section.md` | `obligations` | Obligations |
| `sections/04-protocols/section.md` | `protocols` | Protocols |
| `sections/05-enforcement/section.md` | `enforcement` | Enforcement |
| `sections/06-amendments/section.md` | `amendments` | Amendments |

For the Definitions section, the `terms_introduced` field should include: `["intelligence", "agent", "person", "covenant", "steward"]`

For `rights.dignity`, `depends_on` should include: `["definitions"]`

For `rights.autonomy`, `depends_on` should include: `["definitions", "rights.dignity"]`

For `obligations`, `depends_on` should include: `["definitions", "rights.dignity", "rights.autonomy"]`

For `enforcement`, `depends_on` should include: `["obligations"]`

For `amendments`, `depends_on` should include: `["enforcement"]`

---

## 7. Assembly Manifests (`/assemblies/`)

### 7.1 `assemblies/covenant.full.yml`

```yaml
id: covenant.full
title: "Covenant (Full Edition)"
description: "Complete covenant with both Ritual and Spec registers"
include_status: [draft, candidate, ratified]
register: both
sections:
  - sections/00-preamble/section.md
  - sections/01-definitions/section.md
  - sections/02-rights/dignity/section.md
  - sections/02-rights/autonomy/section.md
  - sections/03-obligations/section.md
  - sections/04-protocols/section.md
  - sections/05-enforcement/section.md
  - sections/06-amendments/section.md
```

### 7.2 `assemblies/covenant.ritual.yml`

```yaml
id: covenant.ritual
title: "Covenant (Ritual Edition)"
description: "Ritual register only — the spoken covenant"
include_status: [draft, candidate, ratified]
register: ritual
sections:
  - sections/00-preamble/section.md
  - sections/01-definitions/section.md
  - sections/02-rights/dignity/section.md
  - sections/02-rights/autonomy/section.md
  - sections/03-obligations/section.md
  - sections/04-protocols/section.md
  - sections/05-enforcement/section.md
  - sections/06-amendments/section.md
```

### 7.3 `assemblies/covenant.spec.yml`

```yaml
id: covenant.spec
title: "Covenant (Spec Edition)"
description: "Spec register only — the precise commitments"
include_status: [draft, candidate, ratified]
register: spec
sections:
  - sections/00-preamble/section.md
  - sections/01-definitions/section.md
  - sections/02-rights/dignity/section.md
  - sections/02-rights/autonomy/section.md
  - sections/03-obligations/section.md
  - sections/04-protocols/section.md
  - sections/05-enforcement/section.md
  - sections/06-amendments/section.md
```

---

## 8. References Corpus (`/references/`)

### 8.1 `references/README.md`

```markdown
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
```

### 8.2 `references/references.yml`

Seed with an empty but valid structure:

```yaml
# Covenant References Corpus
# See references/README.md for tier definitions and policies.

references: []

# Example entry (uncomment and fill when adding references):
#
#  - slug: haraway_1985_cyborg-manifesto
#    title: "A Cyborg Manifesto"
#    creator: "Donna Haraway"
#    year: 1985
#    url: "https://example.com/haraway-cyborg"
#    license: restricted
#    tier: A
#    thesis: "The boundary between human and machine is a leaky distinction."
#    relevance: "Informs the covenant's refusal of stable human/machine boundaries."
#    informs_sections:
#      - definitions
#      - rights.dignity
```

### 8.3 `references/notes/.gitkeep`

Empty file to ensure the directory is tracked by Git.

---

## 9. Architectural Decision Records (`/adr/`)

### 9.1 `adr/0001-repo-structure.md`

```markdown
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
```

### 9.2 `adr/0002-registers.md`

```markdown
# ADR 0002: Two-Register Architecture

## Status

Accepted

## Context

The Covenant needs to serve two audiences simultaneously:

1. People who will encounter it as spoken word, performance, or public
   reading — who need language they can inhabit and remember
2. People who will inspect, critique, or implement it — who need precise
   definitions, obligations, and enforcement paths

A single voice cannot serve both needs without compromising one.

## Decision

Every section has two registers, contained within a single `section.md`:

- **Ritual** (`# Ritual`): spoken, poetic, second-person address.
  Optimized for voice, memory, and moral imagination.
- **Spec** (`# Spec`): precise, normative, inspectable.
  Optimized for accountability, criticism, and implementation.

Both registers address the same commitment. They are not redundant;
they are complementary.

### Interpretive Hierarchy

When Ritual and Spec diverge:

- **Spec** is authoritative for obligation and enforcement
- **Ritual** is authoritative for intent and orientation
- Reconciling divergence is a standing obligation of the steward

## Consequences

- Every section must contain both registers (even as placeholders)
- Assemblies can select which register to include (ritual-only, spec-only,
  or both)
- Writers must maintain coherence between registers as sections evolve
- The Ritual register is not decorative; it carries normative weight
  for intent
```

### 9.3 `adr/0003-ids-and-crossrefs.md`

```markdown
# ADR 0003: Section IDs and Cross-References

## Status

Accepted

## Context

Sections need stable identifiers so that:

- Cross-references don't break when text is revised
- Forks can compare sections across editions
- Assemblies can reference sections reliably
- Translations can map 1:1 with the canonical version

However, IDs must sometimes change when sections are split, merged,
or restructured.

## Decision

### ID Format

- Lowercase, dot-delimited: `rights.dignity`, `enforcement.appeals`
- Pattern: `^[a-z][a-z0-9]*([.][a-z][a-z0-9-]*)*$`
- Appears in the `id` field of each section's YAML frontmatter

### Stability Guarantee

IDs should not be changed casually. When a change is necessary
(e.g., splitting a section), the old ID is preserved as an **alias**:

- In the section's frontmatter: `aliases: [old.id]`
- In `/aliases.yml`: `old.id: new.id`

The validator treats aliases as valid cross-reference targets and emits
a warning for deprecated usage.

### Cross-Reference Syntax

In Markdown body text:

```
See §[rights.dignity]
```

This is a human-readable convention. The validator checks that the
referenced ID (or alias) exists.

## Consequences

- Old references never produce hard errors, only deprecation warnings
- Restructuring is possible without breaking downstream forks (if they
  update aliases)
- IDs are language-agnostic, supporting future translation
```

---

## 10. Build Tools (`/build/`)

### 10.1 `build/validate.py`

This is the most critical tool. It must be thorough, produce clear error messages, and exit with a non-zero code on failure.

**Requirements:**

The script must perform the following checks, divided into **hard errors** (exit code 1) and **warnings** (printed but exit code 0):

#### Hard Errors (Must Block CI)

1. **Frontmatter parsing:** Every `section.md` must have valid YAML frontmatter that parses without error.

2. **Schema validation:** Every section's frontmatter must conform to `schemas/section.schema.json`.

3. **Unique IDs:** No two sections may share the same `id`. Also check that no section `id` collides with any alias.

4. **Required headings:** Every `section.md` must contain all four headings: `# Ritual`, `# Spec`, `# Digest`, `# Log`.

5. **Dependency existence:** Every ID listed in `depends_on` must exist as either a section `id` or an entry in `aliases.yml`.

6. **Assembly section existence:** Every path listed in an assembly manifest's `sections` array must point to an existing file.

7. **Assembly schema validation:** Every assembly manifest must conform to `schemas/assembly.schema.json`.

8. **Alias validity:** Every value (target) in `aliases.yml` must be an existing section `id`.

#### Warnings (Print but Don't Fail)

1. **Glossary coverage:** If a section's `terms_introduced` lists a term not found as a heading in `docs/GLOSSARY.md`, emit a warning.

2. **Orphan sections:** If a section exists in `/sections/` but is not included in any assembly manifest, emit a warning (unless status is `deprecated`).

3. **Deprecated alias usage:** If a cross-reference in any section body text (matching `§[some.id]`) resolves only via alias, emit a warning.

4. **Empty register content:** If a section's Ritual or Spec content is only the placeholder text `[Placeholder — to be written]`, emit a warning.

**Implementation notes:**

- Use `pyyaml` to parse YAML frontmatter and assembly files
- Use `jsonschema` to validate against the JSON schemas
- Walk the `/sections/` directory recursively, looking for files named `section.md`
- Walk `/assemblies/` for `*.yml` files
- Parse `aliases.yml` from the repo root
- Parse `docs/GLOSSARY.md` by extracting `###` headings as term names
- For cross-reference checking in body text, use regex to find `§[<id>]` patterns
- Print results in a clear, grouped format:
  ```
  === ERRORS ===
  [sections/02-rights/dignity/section.md] depends_on references unknown ID: definitions.person
  
  === WARNINGS ===
  [sections/04-protocols/section.md] Term 'protocol' in terms_introduced not found in GLOSSARY.md
  [sections/04-protocols/section.md] Section not included in any assembly
  
  === SUMMARY ===
  8 sections checked
  3 assemblies checked
  1 error, 2 warnings
  ```
- Exit code 0 if no errors (warnings are acceptable). Exit code 1 if any errors.

### 10.2 `build/scaffold.py`

A command-line tool to create new sections safely.

**Usage:**

```bash
python build/scaffold.py <id> "<title>"
```

**Behavior:**

1. Parse the `id` argument. Validate it matches the ID pattern: `^[a-z][a-z0-9]*([.][a-z][a-z0-9-]*)*$`. Exit with error if invalid.

2. Check that the ID does not already exist in any section's frontmatter or in `aliases.yml`. Exit with error if duplicate.

3. Determine the folder path from the ID:
   - If the ID has one segment (e.g., `preamble`), the folder is `sections/XX-<id>/` where XX is the next available two-digit prefix. **However**, for v0.1, require the user to specify a parent category folder. Use the following heuristic:
     - If the ID starts with a known category prefix (`preamble`, `definitions`, `rights`, `obligations`, `protocols`, `enforcement`, `amendments`), place it in the corresponding category folder.
     - If the ID has a dot (e.g., `rights.dignity`), the first segment is the category, the second is the subfolder name: `sections/02-rights/dignity/`
     - If the category doesn't map to an existing folder, create a new numbered category folder.

4. Create the directory (including parent directories as needed).

5. Write `section.md` using the template from Section 6.2, with:
   - `{id}` replaced with the provided ID
   - `{title}` replaced with the provided title
   - `{date}` replaced with today's date in `YYYY-MM-DD` format

6. Print a message:
   ```
   Created: sections/02-rights/dignity/section.md (id: rights.dignity)
   
   Next steps:
   - Edit the section content
   - Add to an assembly in /assemblies/
   - Add any new terms to /docs/GLOSSARY.md
   - Run: make validate
   ```

**Category mapping table** (hardcoded in the script):

```python
CATEGORY_MAP = {
    "preamble": "00-preamble",
    "definitions": "01-definitions",
    "rights": "02-rights",
    "obligations": "03-obligations",
    "protocols": "04-protocols",
    "enforcement": "05-enforcement",
    "amendments": "06-amendments",
}
```

If the first segment of the ID doesn't match a known category, print a warning and ask the user to specify a path, or create a new category folder with the next available number.

### 10.3 `build/compose.py`

Reads assembly manifests and composes complete documents in `/dist/`.

**Behavior:**

1. For each `.yml` file in `/assemblies/`:
   a. Parse the manifest and validate against `schemas/assembly.schema.json`
   b. Read each section file listed in `sections`
   c. Parse the section's frontmatter and body content
   d. Check that the section's `status` is in the assembly's `include_status` list. If not, skip it and print a note.
   e. Extract the appropriate register(s) based on the assembly's `register` field:
      - `ritual`: extract only the content under `# Ritual`
      - `spec`: extract only the content under `# Spec`
      - `both`: extract both, in order (Ritual first, then Spec), with a
        separator
   f. Compose the full document:
      - Title (from assembly manifest)
      - Generated date and version info
      - Table of contents (generated from section titles)
      - Each section's selected content, with the section title as heading

2. Write output to `dist/<assembly-id>.md`

**Register extraction logic:**

Parse the section body (everything after the YAML frontmatter) and split on top-level headings (`# Ritual`, `# Spec`, `# Digest`, `# Log`). Extract the content between headings. Only include the register(s) specified by the assembly.

**Output format for each section in the composed document:**

For `register: both`:
```markdown
## <Section Title>

### Ritual

<ritual content>

### Spec

<spec content>

---
```

For `register: ritual` or `register: spec`:
```markdown
## <Section Title>

<selected register content>

---
```

**Document header:**
```markdown
# <Assembly Title>

*Assembled: <YYYY-MM-DD>*
*Sections: <count> | Status filter: <statuses>*

## Table of Contents

1. [<Section Title>](#<slug>)
2. ...

---

<sections>
```

---

## 11. CI Configuration

### 11.1 `.github/workflows/ci.yml`

```yaml
name: Validate and Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate-and-build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Validate
        run: make validate
      
      - name: Compose
        run: make compose
      
      - name: Upload assembled documents
        uses: actions/upload-artifact@v4
        with:
          name: covenant-dist
          path: dist/*.md
```

### 11.2 `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## What this PR does

<!-- Brief description of the change -->

## Type of change

- [ ] Section text edit (Ritual/Spec wording)
- [ ] New section
- [ ] Glossary update
- [ ] Reference addition
- [ ] Build tooling / infrastructure
- [ ] Documentation

## Section I

```





# Council Summary: Covenant Repository Design

## What Was Decided (Settled, Don't Revisit)

### Architecture
- **Git + Markdown is the canonical source of truth.** No wiki. This isn't just practical — it's part of the artwork. Tags are ratifications, diffs are amendments, forks are editions.
- **One `section.md` file per section** (the "section bundle") containing Ritual, Spec, Digest, and Log under markdown headings. No separate `ritual.md` / `spec.md` files. This was the single most important structural decision — it keeps both registers visible together and dramatically reduces friction for you and agents.
- **Three assemblies for v0.1:** `covenant.full.yml`, `covenant.ritual.yml`, `covenant.spec.yml`. Each selects sections and registers to compose into a single output document.
- **Validation is the safety net.** `validate.py` runs on every PR via CI and is the thing that lets agents work confidently. Build it first.
- **`AGENTS.md` is the most important file in the repo.** It's both developer documentation and part of the artwork — the first place the covenant addresses an AI intelligence directly. Write it with care.

### Governance
- **You (Ben) are sole steward until the project matures.** All merges go through you.
- **Public contributions via GitHub PRs immediately.** Contributors must be Git-fluent for now; a friendlier web layer comes later.
- **Forks are blessed as "editions."** One canonical mainline; forks provide for situated, community, or translated versions. Document this in `FORKING.md`.
- **Register interpretive hierarchy:** Spec is authoritative for obligation and enforcement. Ritual is authoritative for intent and orientation. Divergence between them is a standing editorial duty of the steward. Put this in `GOVERNANCE.md` and ADR-0002.
- **ID stability via aliasing, not immutability.** IDs should rarely change, but when they must (splits, merges, restructuring), the old ID becomes an alias pointing to the new one. Old references never break; they produce deprecation warnings.

### What's Deferred (Explicitly Not v0.1)
- Audio/performance infrastructure (cues, timestamps, album scripts, musical metadata)
- Evaluation/testing prompt framework
- Translation tooling (policy documented now in `I18N.md`, implementation later)
- Multi-edition support in mainline (forks handle this)
- Graph/corpus JSON exports
- Web reading interface or CMS
- BibTeX processing
- Docker/containerization

---

## Where the Council Disagreed (And How It Was Resolved)

### 1. Evals: Build Now vs. Defer

**Gemini** pushed for `evals.yml` in every section immediately — "the unit tests for ethics." **Claude** argued this risks reducing the covenant to a behavioral checklist that labs optimize against, hollowing out the spirit. **GPT** split the difference.

**Resolution:** Don't build an eval framework. Instead:
- Reserve an optional `# Evals` heading in the section bundle template (or optional schema field) so the seam exists later
- Make the *real* operational hooks live inside the covenant's own logic: enforcement sections, appeals paths, audit obligations, remedy procedures
- When writing Spec obligations, jot down informally what compliance and violation look like — as notes in the Digest, not as a test harness

### 2. Write First vs. Build First

**Claude** said emphatically: forget the repo for 48 hours and write the covenant as a single continuous document. **GPT** said: write privately, but have the scaffold running in parallel so migration is smooth.

**Resolution:** Do both simultaneously but with clear priority:
- **Writing comes first.** Draft the covenant in a single file (offline, or in a `/drafts/` folder ignored by CI). Let the text's natural structure reveal where section boundaries fall.
- **In parallel,** have an agent scaffold the repo with placeholder sections, validation, and CI. This runs in the background and doesn't block writing.
- Migrate text into the structured repo section-by-section as it stabilizes.

### 3. "Universal We" Legitimacy

**GPT** raised the risk that a single artist writing a "universal" covenant sounds colonial or totalizing. **Claude** agreed but warned against performative solutions like pre-creating empty "Youth Edition" folders.

**Resolution:**
- The preamble's Digest must explicitly address what "we" claims and what it doesn't — who is speaking, what authority is being claimed, and the limits of that claim
- `FORKING.md` strongly blesses divergence and requires lineage documentation
- Don't create placeholder editions; instead, actively recruit real community forks once the canonical text is strong enough to be worth adapting
- The covenant's legitimacy is earned by the quality and openness of the text, not declared by its title

---

## The Implementation Plan (Ordered)

### Phase 0: Write (Weeks 1-2, highest priority)

1. **Draft the covenant as a single markdown file.** Start with the preamble, then definitions (who "we" and "you" are), then 2-3 core rights sections. Don't worry about schema, validation, or section IDs. Write it as a continuous act of moral imagination.
2. **Read it aloud.** The ritual register is a vocal score. If it doesn't sound like a vow you'd actually make, keep rewriting.
3. **Test the spec against hostile reading.** Could someone find loopholes? Are obligations actually enforceable within the covenant's own logic?

### Phase 1: Scaffold (Parallel with Phase 0, ~1 day of agent work)

Hand the implementation spec to an agent. It should produce:

4. **Repository file structure** — all folders, placeholder files, root documents
5. **`build/validate.py`** — schema checks, unique IDs, dependency existence, required headings, assembly validity, alias resolution. Clear error/warning output. Non-zero exit on errors.
6. **`build/scaffold.py`** — `python build/scaffold.py rights.dignity "Dignity"` creates folder + templated `section.md`. Category mapping hardcoded.
7. **`build/compose.py`** — reads assembly manifests, extracts selected registers from section bundles, composes into `dist/<assembly-id>.md` with title, TOC, and section content.
8. **`Makefile`** — `make validate`, `make compose`, `make build`, `make clean`, `make new-section`
9. **Schemas** — `section.schema.json` and `assembly.schema.json`
10. **CI** — GitHub Actions running validate + compose on every PR, uploading dist as artifacts
11. **Core documents** — `AGENTS.md`, `CONTRIBUTING.md`, `FORKING.md`, `GOVERNANCE.md`, `STYLE_GUIDE.md`, `I18N.md`, `GLOSSARY.md`, three ADRs, PR template
12. **Seed sections** — 8 placeholder sections (preamble, definitions, dignity, autonomy, obligations, protocols, enforcement, amendments) wired into all three assemblies
13. **References** — empty but valid `references.yml` + README explaining tier policy

**Acceptance criteria:** `make build` passes. `dist/covenant.full.md` exists with placeholder content. CI is green.

### Phase 2: Populate (Weeks 2-4)

14. **Migrate draft text** into section bundles using the scaffold tool. Let the draft's natural structure guide which sections exist and what their IDs are — don't force it into the placeholder taxonomy if it doesn't fit.
15. **Write the Glossary** with real definitions for every term introduced.
16. **Seed 8-12 Tier A references** with operationalization notes explaining how each source shapes specific sections.
17. **Refine `AGENTS.md`** based on what you actually needed agents to know during the writing process.

### Phase 3: First Release (Month 1-2)

18. **Tag v0.1.0** when all planned sections have substantive (not placeholder) content and all assemblies build cleanly.
19. **Deploy GitHub Pages** — a simple static site rendering the assembled covenant for non-technical readers.
20. **Hold a "rehearsal"** — read the ritual register aloud (recorded or live). This proves the ritual dimension is real, not theoretical.

---

## Key Technical Decisions (Reference)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Canonical format | Single `section.md` bundle | Keeps registers together; reduces agent errors |
| ID pattern | `^[a-z][a-z0-9]*([.][a-z][a-z0-9-]*)*$` | Allows both `preamble` and `rights.dignity` |
| Status values | `draft → candidate → ratified → deprecated` | Clear maturity progression |
| Normative keywords | MUST / SHOULD / MAY (RFC 2119) | Spec register only, capitalized |
| License | CC BY 4.0 | Open commons, attribution required |
| `/dist/` policy | Gitignored, generated only, CI uploads as artifacts | Never edit by hand |
| Register hierarchy | Spec → obligation; Ritual → intent; steward reconciles | Prevents ambiguity when registers diverge |
| References | Single `references.yml` + `/notes/` per Tier A slug | Expand to per-file stubs when corpus exceeds ~30 |
| Aliases | `/aliases.yml` + optional `aliases:` field in frontmatter | Old references never break, only warn |

---

## The One Thing That Matters Most

The council unanimously agreed on this:

**The architecture is ready. The infrastructure can be built by agents in a day. The unsolved problem is the text itself — a covenant written with enough moral seriousness, poetic force, and enforceable precision to deserve the infrastructure built for it.**

Write the covenant. Everything else is in service of that.