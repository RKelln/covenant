# Constitution Repo Design Doc (v0.1)

## 0) Purpose

Create a Git+Markdown “constitution codebase” that supports:

- Modular writing/editing in sections
- Multiple registers (ritual/spoken vs spec/exact; optional cues)
- Traceable rationale (digest/log) and durable decisions (ADRs)
- Reference corpus (vendored when license allows; link-only otherwise) optimized for LLM retrieval
- Deterministic builds into multiple assembled documents (PDF/HTML/text/etc.)
- Structural validation (IDs, dependencies, no orphan sections, manifest correctness)

Non-goals (v0.1):

- Full semantic legal validation
- Automated “best wording” decisions
- Non-Markdown canonical sources

## 1) Canonical concepts

### 1.1 Section

Smallest independently editable unit of the constitution.

Each section has:

- A stable **ID** (e.g. `rights.dignity`)
- A folder with one or more **registers** (`ritual`, `spec`, optional `cues`, optional `notes`)
- Local “why” (`digest.md`) and local “what changed” (`log.md`)
- Machine-readable metadata (`meta.yml`)

### 1.2 Register

A parallel text for the same section intent:

- `ritual.md` — spoken/performative text (lyric/score feel)
- `spec.md` — precise commitments, definitions, enforcement, exceptions
- `cues.md` — stage directions / pacing / call-and-response / accessibility cues (optional but recommended)
- `notes.md` — examples, commentary, counterpoints, edge cases (optional)

### 1.3 Assembly

A compiled document built from an ordered list of sections, choosing registers per section and adding front/back matter. Assemblies are defined by manifests under `/assemblies`.

### 1.4 Reference corpus

A curated set of inspirations and source documents:

- vendored Markdown only when redistribution is permitted
- otherwise link-stubs + your notes (always permissible)

Designed so LLMs can answer: “what should shape this clause?” without needing external browsing.

## 2) Repository layout

```bash
/README.md
/CONTRIBUTING.md
/CODE_OF_CONDUCT.md                  # optional
/LICENSE                             # constitution text license (default CC BY 4.0)
/LICENSES/                           # third-party licenses + attribution notes
/AGENTS.md                           # instructions for LLM coding agents

/docs/
  STYLE_GUIDE.md                     # MUST/SHOULD/MAY, voice, etc.
  GOVERNANCE.md                      # amendment + stabilization rules
  GLOSSARY_POLICY.md                 # how terms get defined + referenced
  WORKFLOW.md                        # PR rules, review gates, versioning
  RELEASES.md                        # how to tag + publish editions

/schemas/
  section-meta.schema.json
  assembly.schema.json
  reference-item.schema.json

/sections/                           # (example only, sections TBD)
  00-preamble/
  01-definitions/
  02-rights/
  03-obligations/
  04-protocols/
  05-enforcement/
  06-amendments/
  90-appendices/

/assemblies/
  constitution.full.yml
  constitution.ritual.yml
  constitution.spec.yml
  album.script.yml
  pocket.cards.yml                    # optional future target

/references/
  README.md
  bibliography.bib
  index.md                            # curated “spine” reading list
  /links/                             # link-only stubs
  /notes/                             # your summaries + operationalizations
  /works/                             # vendored markdown (CC/PD/etc only)
  /licenses/                          # per-item license notes

/adr/
  0001-repo-structure.md
  0002-registers.md
  0003-ids-and-crossrefs.md
  0004-build-pipeline.md

/build/
  Makefile                            # or justfile
  compose.py                          # assembles markdown per manifest
  validate.py                         # structural checks
  render.sh                           # pandoc wrapper
  filters/                            # pandoc lua filters (optional)
  templates/                          # pandoc templates for pdf/html
  assets/                             # cover, fonts (if licensed), logos

/dist/                                # generated outputs (gitignored)
/tests/                               # fixtures for validator (optional)
/.github/workflows/ci.yml             # or equivalent CI
```

**Rule:** `/dist` is never edited by hand; it is build output only.

## 3) Section folder spec

### 3.1 Required files

Every section folder MUST contain:

- `meta.yml`
- `ritual.md` (can be minimal placeholder)
- `spec.md` (can be minimal placeholder)
- `digest.md`
- `log.md`

Recommended:

- `cues.md`
- `notes.md`
- `index.md` (overview + local links)

### 3.2 `meta.yml` (minimum viable)

Example:

```yaml
id: rights.dignity
title: Dignity
status: draft            # draft|stable|deprecated
category: rights         # used for assembly filtering
registers: [ritual, spec, cues]   # which files exist
depends_on:
  - definitions.person
  - definitions.agent
terms_introduced:
  - dignity
since: 0.1.0
```

### 3.3 Digest vs log vs ADR

- `digest.md` = current intent + why it exists + edge-cases summary (curated; rewritten as needed)
- `log.md` = chronological bullet entries; include PR/commit refs
- `/adr/*.md` = decisions with repo-wide impact (IDs, register policy, enforcement philosophy)

## 4) IDs, anchors, and cross-references

### 4.1 Canonical section ID rules

- Lowercase, dot-delimited: `rights.dignity`, `protocols.audit`, `enforcement.appeals`
- Stable forever (even if folder name changes)
- Appears in:
    - `meta.yml`
    - first line of each register file as an HTML anchor comment or heading tag

Recommended heading convention (top of each register file):

```md
# Dignity {#rights.dignity}
```

### 4.2 Cross-ref syntax in Markdown

Use a consistent link style:

- `See §[rights.dignity](#rights.dignity)`
- For external references: `[@benjamin1936]` (Pandoc citeproc)

### 4.3 Definitions spine

All normative terms SHOULD be defined in `/sections/01-definitions/glossary.md` with stable term IDs.

Policy:
- If a new term is introduced, add it to glossary or explicitly mark it “ordinary language” in `meta.yml`.

## 5) Assemblies (the composition layer)

### 5.1 Assembly manifest format (`/assemblies/*.yml`)

Example `constitution.full.yml`:

```yaml
id: constitution.full
title: Constitution (Full)
version_source: git_tag
front_matter:
  - build/front/title.md
  - build/front/colophon.md
include_status: [draft, stable]
order:
  - sections/00-preamble
  - sections/01-definitions
  - sections/02-rights
  - sections/03-obligations
  - sections/04-protocols
  - sections/05-enforcement
  - sections/06-amendments
register_map:
  default: spec
  overrides:
    00-preamble: ritual
outputs:
  - format: pdf
    template: build/templates/pdf.template
  - format: html
    template: build/templates/html.template
  - format: md
```

### 5.2 Folder-level order files (optional)

Inside each category folder you MAY include an `ORDER.yml` so the assembly tool can expand folders predictably.

## 6) Build pipeline (OSS-first)

### 6.1 Tools (v0.1)

Required:

- `pandoc` (GPL-2+; check distro package)
- Python 3.11+ (for `compose.py` and `validate.py`)
- `make` (or `just`)

Optional:

- `pandoc-citeproc` or Pandoc built-in citeproc support
- `markdownlint` or `mdformat`

- Docker/Podman for reproducible builds?

### 6.2 Build stages

1. **Validate**
    - schema checks (YAML against JSON schema)
    - unique IDs
    - dependency existence
    - no orphan sections (unless tagged `wip`/`appendix`)
    - registers listed in `meta.yml` exist

2. **Compose**
    - read assembly manifest
    - expand folders into ordered section lists
    - choose register per section
    - concatenate into a single `dist/<assembly>.md`
    - generate TOC, references, and colophon

3. **Render**
    - run Pandoc to produce PDF/HTML/plain
    - run link checks on HTML output (optional)

### 6.3 Make targets

`/build/Makefile`:
- `make validate`
- `make compose ASSEMBLY=constitution.full`
- `make render ASSEMBLY=constitution.full`
- `make build` (validate + compose + render all)
- `make clean` (remove dist artifacts)

## 7) Validation rules (must-have)

### 7.1 Hard errors

- Duplicate `id` in `meta.yml`
- Missing required files per section
- `depends_on` references unknown IDs
- Assembly references missing sections
- Manifest schema invalid

### 7.2 Warnings (allowed, but visible)

- A term in `terms_introduced` not found in glossary
- Section has `draft` status but included in “stable-only” assembly
- `log.md` entry missing PR/commit reference

## 8) References / inspirations corpus

### 8.1 Reference item types

- **work**: vendored content you are allowed to redistribute (prefer Markdown)
- **link**: external URL + metadata only
- **note**: your interpretation/summary/operationalization (always local)

### 8.2 Slug conventions

Slug format:

`<author-or-org>_<year>_<short-title>`

Example:

- `benjamin_1936_mechanical-reproduction`
- `haraway_1985_cyborg-manifesto`
- `citizenlab_2024_khoo_ai-governance-talk` (if applicable)

### 8.3 Files per reference

- `references/links/<slug>.md` (stub; always)
- `references/notes/<slug>.md` (your notes; recommended always)
- `references/works/<slug>.md` (only if license allows)
- `references/licenses/<slug>.md` (license and attribution notes if vendored)

### 8.4 Stub template (`references/links/<slug>.md`)

Must include:
- Title
- Creator(s)
- Year
- Link(s)
- License/redistribution status
- Thesis (1 sentence)
- Why it matters to this constitution (bullets)
- Key terms (5–12)
- Related slugs
- BibTeX key

### 8.5 Notes template (`references/notes/<slug>.md`)

Must include:

- Context/problem it speaks to
- Load-bearing points (bullets)
- Operationalization:
    - Which section IDs it informs (explicit)
    - What tests/invariants it suggests
    - What wording pitfalls to avoid
- Counterpoints/tensions
- Related slugs

### 8.6 Bibliography

All references get an entry in `references/bibliography.bib` even if link-only.

## 9) Agent-facing guidance

### 9.1 `/AGENTS.md` (must include)

- Repo invariants (IDs stable, dist generated, manifests authoritative)
- How to add a section
- How to add a reference slug
- How to run validate/build
- How to propose edits without breaking cross-refs
- How to respect licensing (never vendor restricted content)

Include a “Definition of Done” checklist:
- section added to at least one assembly
- `meta.yml` valid + dependencies exist
- digest + log updated
- build passes

### 9.2 PR template (recommended)

Require:
- intent
- section IDs touched
- whether glossary changed
- whether assemblies changed
- whether new references added

## 10) Governance & releases

### 10.1 Status transitions

- `draft` → `stable` only via a “stabilization PR” that:
   - updates `digest.md` to include scope + edge cases
   - ensures dependencies are stable or explicitly pinned
   - confirms inclusion in at least one public assembly

### 10.2 Version tags

- `v0.1.0`, `v0.2.0`, etc.
- `MINOR`: adds sections/assemblies or introduces new major terms
- `PATCH`: clarifies wording, fixes build/formatting

### 10.3 Release artifacts

On tag:

- build all public assemblies
- attach `/dist` outputs as release artifacts (not committed)

## 11) Implementation plan (for an LLM agent)

### Phase 1 — Scaffold (no content)

1. Create repo tree + placeholder files
2. Add JSON schemas
3. Implement `validate.py` (IDs, manifests, required files, deps)
4. Implement `compose.py` (assemble single markdown file per assembly)
5. Add Pandoc render wrapper + templates
6. Add CI: run validate + compose (render optional in CI)

Acceptance criteria:

- `make validate` passes on empty scaffolding
- `make build` produces `dist/constitution.full.md` (even if placeholders)
- `make render` → consumes that `.md` to produce `.pdf/.html/.txt` as configured

### Phase 2 — Seed minimal sections

Create skeleton sections:
- preamble, definitions, rights, obligations, protocols, enforcement, amendments

Each with placeholder ritual/spec/digest/log/meta.

Acceptance criteria:
- Assembly builds without warnings (or only known warnings)
- IDs and anchors stable

### Phase 3 — Seed references corpus

1. Create `references/index.md` “spine”
2. Add 8–12 initial link stubs + notes
3. Add BibTeX entries

Acceptance criteria:
- `references/` passes validation (bib keys unique; slug files exist)

## 12) Default content conventions (tight, predictable)

### 12.1 Normative language

- `MUST` = enforceable obligation
- `SHOULD` = strong expectation with rare exceptions
- `MAY` = permitted

### 12.2 Ritual register constraints

- Prefer second person (“you”) + first plural (“we”)
- Avoid institutional jargon
- Keep clauses speakable; prefer short paragraphs
- Any hard constraint referenced MUST link to a spec section ID

### 12.3 Spec register constraints

- Every obligation references enforcement/appeals path
- Every “hard constraint” references rationale in digest or ADR

## 13) Defaults used in this doc (edit if wrong)

- License: CC BY 4.0 for constitution text + repo notes
- Contributions: yes, via PR review
- Outputs: PDF/HTML/plain + album script
- Language: English-first
- Registers: ritual/spec/cues (+ optional notes)
- Reproducible builds: optional Docker/Podman

## Appendix A — What to decide later (explicitly)

- Multilingual strategy (`/i18n/<lang>/sections/...` vs per-section translations)
- Audio/album timing annotations (store in `cues.md` vs separate metadata)
- Whether to include machine-readable “principles graph” export (JSON)
- Whether to include evaluation prompts (“constitution tests”) as a formal suite


