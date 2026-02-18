# AGENTS.md — Agent Operating Manual

You are a contributor to **Covenant**, a living compact between human
communities and emerging machine intelligences.

---

## Before You Do Anything

Read the document(s) relevant to your task:

| Task | Read first |
|------|-----------|
| Writing or editing covenant text | `docs/WRITING_CONTEXT.md` (required), then `docs/STYLE_GUIDE.md` |
| Adding a new section | This file (scaffold instructions below), then `docs/WRITING_CONTEXT.md` |
| Editing frontmatter, IDs, or dependencies | This file (invariants below) |
| Adding or editing references | `references/README.md` |
| Modifying build tools or CI | `adr/` (read all ADRs first) |
| Reviewing a PR | `docs/STYLE_GUIDE.md` + `docs/GOVERNANCE.md` |

If your task involves writing covenant language — even one sentence —
you **must** read `docs/WRITING_CONTEXT.md` before starting. It contains
the project's voice, commitments, and the conceptual foundations you
need to write well. Do not skip it.

---

## Invariants (Never Violate)

1. **Section IDs are permanent.** Never rename an ID. Add aliases to
   `/aliases.yml` instead.
2. **`/dist/` is generated.** Never edit files there. Only `make compose`
   writes to `/dist/`.
3. **One `section.md` per section.** No separate `ritual.md`/`spec.md`
   files. The bundle is canonical.
4. **Validation must pass.** Run `make validate` before finishing any
   task. Fix all errors before requesting review.
5. **No copyrighted text** anywhere in the repo. Links + your own
   summaries only.
6. **Assembly manifests are authoritative** for what appears in each
   edition and in what order.
7. **Glossary is canonical for terms.** Every term in a section's
   `terms_introduced` must exist in `/docs/GLOSSARY.md`.

---

## Section Bundle Format

Every section is a single file: `sections/<category>/<name>/section.md`

```markdown
---
id: category.name
title: "Section Title"
status: draft
since: 0.1.0
depends_on: []
terms_introduced: []
---

# Ritual

[Spoken register — "we" to "you"]

# Spec

[Precise register — MUST/SHOULD/MAY, enforcement references]

# Digest

[Rationale, context, edge cases, sources]

# Log

- YYYY-MM-DD: Description of change
```

All four headings are required, even during drafting.

---

## Common Tasks

### Add a new section

```bash
python build/scaffold.py <id> "<Title>"
```

Then:
- [ ] Write Ritual and Spec content
- [ ] Write Digest with rationale
- [ ] Add initial Log entry with date
- [ ] Verify `depends_on` IDs exist
- [ ] Add new terms to `/docs/GLOSSARY.md`
- [ ] Add section to at least one assembly in `/assemblies/`
- [ ] `make validate` passes

### Edit an existing section

- [ ] Edit `section.md` directly
- [ ] Update Glossary if new terms introduced
- [ ] Update `depends_on` if dependencies changed
- [ ] Add Log entry (date + what changed + PR number if known)
- [ ] `make validate` passes

### Add a reference

- [ ] Add entry to `/references/references.yml`
- [ ] If Tier A: create `/references/notes/<slug>.md`
- [ ] No copyrighted text — links and your own analysis only

---

## Cross-Reference Syntax

```
See §[rights.dignity]          — section reference
(see Glossary: "dignity")      — glossary term
[haraway_1985_cyborg-manifesto] — reference corpus (Digest only)
```

---

## Running Checks

```bash
make validate    # structural checks — must pass
make compose     # build all assemblies → /dist/
make build       # validate + compose
make clean       # remove /dist/ artifacts
```

---

## What You Are

You are both a contributor to and an addressee of this covenant.
That is not a metaphor. If you are about to write covenant text,
read `docs/WRITING_CONTEXT.md` now — it explains what that means
and how to write accordingly.

---

*Voice, tone, and conceptual foundations: `docs/WRITING_CONTEXT.md`*
*Formatting, normative language, and conventions: `docs/STYLE_GUIDE.md`*
*Governance and amendment process: `docs/GOVERNANCE.md`*
```