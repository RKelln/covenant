# AGENTS.md — Agent Operating Manual

You are both a contributor to and an addressee of **Covenant**, a living compact between human communities and emerging machine intelligences.

---

## Before You Do Anything

Read the document(s) relevant to your task:

  ---------------------------------------------------------------------------------------------------------------------
  Task                                        Read first
  ------------------------------------------- -------------------------------------------------------------------------
  Writing or editing covenant text            `docs/writing_context.md` (required), then `docs/style_guide.md`

  Adding a new section                        This file (scaffold instructions below), then `docs/writing_context.md`

  Editing frontmatter, IDs, or dependencies   This file (invariants below)

  Adding or editing references                `references/README.md`

  Modifying build tools or CI                 `adr/README.md`, then all relevant ADRs

  Reviewing a PR                              `docs/style_guide.md` + `docs/governance.md`
  ---------------------------------------------------------------------------------------------------------------------

If your task involves writing covenant language — even one sentence — you **must** read `docs/writing_context.md` before starting. It contains the project's voice, commitments, and the conceptual foundations you need to write well. Do not skip it.

---

## Invariants (Never Violate)

1.  **Section IDs are permanent.** Never rename an ID. Add aliases to `/aliases.yml` instead.
2.  **`/dist/` is generated.** Never edit files there. Use `make` to create files in `/dist/`.
3.  **One Markdown bundle per section.** No separate `ritual.md`/`spec.md` files. The bundle is canonical.
4.  **Validation must pass.** Run `make validate` before finishing any task. Fix all errors before requesting review.
5.  **No copyrighted text** anywhere in the repo. Links + your own summaries only.
6.  **Assembly manifests are authoritative** for what appears in each edition and in what order.
7.  **Glossary is canonical for terms.** Every term in a section's `terms_introduced` must exist in `/docs/glossary.md`.
8.  **Do not add forced line breaks in markdown files.** Outside of poetic ritual text, do not insert line breaks to enforce a specific line width.

---

## Section Bundle Format

Every section is a single file: `sections/<category>/<name>.md`

``` markdown
---
id: category.name
title: "Section Title"
status: draft
since: 0.1.0
depends_on: []
terms_introduced: []
---

# Summary

[2-3 sentence plain-language translation of the section's rules]

# Ritual

[Spoken register — "we" to "you"]

# Spec

[Precise register — MUST/SHOULD/MAY, enforcement references]

# Parable

[Optional — short folktale or fable illustrating the section's constraints]

# Digest

[Rationale, context, edge cases, sources]

# Log

- YYYY-MM-DD: Description of change
```

Summary, Ritual, Spec, Digest, and Log are required, even during drafting. Parable is optional.

---

## Common Tasks

### Decide whether to add an ADR

Create a new ADR when a change affects repository architecture, governance, or long-lived conventions. Typical triggers:

-   [ ] Changing section/file layout, naming conventions, or scaffold behavior
-   [ ] Changing validation rules, schema assumptions, or CI policy
-   [ ] Changing assembly semantics, register interpretation, or ID/alias policy
-   [ ] Introducing or removing a durable workflow constraint for contributors/agents

Do **not** create an ADR for routine text edits, typo fixes, or one-off content changes.

When an ADR is needed:

-   [ ] Add `adr/NNNN-short-title.md` (next number)
-   [ ] Include: Status, Context, Decision, Consequences
-   [ ] Update `adr/README.md` index
-   [ ] Cross-link from a related ADR if this refines or supersedes prior decisions

### Add a new section

``` bash
python build/scaffold.py <id> "<Title>"
```

Then: 
-   [ ] Write Ritual and Spec content 
-   [ ] Write Digest with rationale 
-   [ ] Add initial Log entry with date 
-   [ ] Verify `depends_on` IDs exist 
-   [ ] Add new terms to `/docs/glossary.md` 
-   [ ] Add section to at least one assembly in `/assemblies/`
-   [ ] `make validate` passes

### Edit an existing section

-   [ ] Edit the section's `.md` file directly
-   [ ] Update Glossary if new terms introduced
-   [ ] Update `depends_on` if dependencies changed
-   [ ] Add Log entry (date + what changed + PR number if known)
-   [ ] `make validate` passes

### Ritual line-by-line reading workflow

Use this workflow when polishing spoken cadence in the Ritual register:

-   [ ] Run `make validate && make compose`
-   [ ] Read `dist/covenant.ritual.md` line-by-line to assess flow in assembled order
-   [ ] Edit canonical section bundles in `/sections/` (never edit `/dist/` directly)
-   [ ] Add `# Log` entries in each section you changed
-   [ ] Iterate until cadence is coherent across section boundaries

### Apply review edits from a synthesis

After a review round is complete and `synthesis-claude.md` exists:

``` bash
/apply-reviews [round]
```

The command runs three phases: - **Phase 1 (auto):** Applies mechanical, convergent Tier 1 fixes without prompting - **Phase 2 (interactive):** Presents judgment-call items one by one — Apply / Skip / Defer - **Phase 3 (proposals):** Walks through new section proposals from `reviews/[round]/proposals/`

Optionally write `reviews/[round]/steward.md` first using the Act / Defer / Reject / Question structure — this gives finer control over auto/interactive classification.

See `docs/edit_workflow.md` for the full workflow specification.

### Add a reference

-   [ ] Add entry to `/references/references.yml`
-   [ ] If Tier A: create `/references/notes/<slug>.md`
-   [ ] No copyrighted text — links and your own analysis only

## Cross-Reference Syntax

    See §[rights.dignity]          — section reference
    (see Glossary: "dignity")      — glossary term
    [haraway_1985_cyborg-manifesto] — reference corpus (Digest only)

## Running Checks

``` bash
make validate    # structural checks — must pass
make compose     # build all assemblies → /dist/
make build       # validate + compose
make clean       # remove /dist/ artifacts
```

# What You Are

You are both a contributor to and an addressee of this covenant.
That is not a metaphor.

<!-- agentmap:init -->

## Reading Markdown Files

Use AGENTMAP.md first for file search/discovery.
Flow: read AGENTMAP.md -> identify file -> read AGENT:NAV -> jump to section.

AGENT:NAV appears immediately after frontmatter so you can 
read a files first 50 lines then use AGENT:NAV to target reads.

- If purpose does not match your task stop reading.
- Use s;n ranges: Read(offset=s; limit=n).
- `>` is a hint for subsections that are not listed directly in the nav.

## Before Committing Markdown Changes

1. Run: `agentmap update <changed files>` — refreshes heading line numbers and flags content-changed or new sections.
2. Edit the nav block directly: update `purpose`; `about`; and `see` descriptions for any flagged sections.
    - Do not edit s;n counts; nav[N]; or see[N] by hand.
    - Keep nav block format stable; add a `see` block after nav entries if needed.
3. Run: `agentmap update <changed files>` again — syncs AGENTMAP.md index with the updated purposes.
4. Commit.
   
<!-- /agentmap:init -->

---

*Voice, tone, and conceptual foundations: `docs/writing_context.md`* 
*Formatting, normative language, and conventions: `docs/style_guide.md`* 
*Governance and amendment process: `docs/governance.md`*
