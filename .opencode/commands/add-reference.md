---
description: Add a new reference to the corpus — fetch source, analyse relevance, generate bibliography entry and notes
---

You are adding a new reference to the Covenant references corpus. Your job is
to fetch or read the source, analyse it for covenant relevance, generate all
required metadata, write the entry to `references/references.yml`, and (for
Tier A) write a notes file to `references/notes/<slug>.md`.

## Arguments

Arguments provided: $ARGUMENTS

Parse as: `[source]`

- `$1` — a URL or an absolute/repo-relative file path to the source material.
  Required. If absent, ask the steward to provide one.

Examples:
- `/add-reference https://www.anthropic.com/constitution`
- `/add-reference references/TODO.md`
- `/add-reference https://coevolution.fas.harvard.edu/sites/g/files/omnuum5841/files/culture_cognition_coevol_lab/files/which_humans_09222023.pdf`

---

## Step 0 — Check for existing entry

Read `references/references.yml`. Search for any entry whose `url` or `slug`
matches the source argument.

If a match is found, display:

```
─────────────────────────────────────────────
This source is already in the corpus:

  slug:  [slug]
  title: [title]
  tier:  [tier]
  url:   [url]

  [Y] Re-run in full and overwrite this entry
  [N] Cancel
─────────────────────────────────────────────
```

Wait for the steward's response. If they say "n", "cancel", or "abort", stop
here and report that no files were changed.

If they say "y" or "overwrite", proceed to Step 1 and treat this as a fresh
run — the existing entry will be replaced in Step 5.

If no match is found, proceed directly to Step 1.

---

## Step 1 — Fetch or read the source

If `$1` is a URL, use the WebFetch tool to retrieve the content (markdown
format). If retrieval fails or the URL is paywalled/inaccessible, note the
failure and proceed using only the URL and any title information visible in
the response (you will still produce a bibliography entry with what you have,
marking `access: limited`).

If `$1` is a file path, use the Read tool to read the file.

Do not skip this step — the content analysis in Step 2 depends on it.

---

## Step 2 — Analyse for covenant relevance

Read `docs/writing_context.md` in full before doing this analysis.

From the source content, identify:

1. **Core thesis** — one sentence: what is the central claim or argument?
2. **Covenant relevance** — one to two sentences: what does this work contribute
   to the Covenant's concerns? Consider: human-machine relations, rights,
   obligations, dignity, transparency, accountability, power, care, ecological
   responsibility, or the political status of emerging intelligences.
3. **Key points** — up to five bullet points of ideas directly applicable to
   Covenant sections. Frame each point in terms of what it implies for the
   Covenant's content, not just what the source says.
4. **Sections informed** — list the section IDs (from `sections/` directory
   tree or frontmatter `id:` fields) that this reference most directly bears
   on. Read the sections directory listing if needed to check IDs.
5. **Tier assessment** — propose Tier A, B, or C:
   - **Tier A** if it directly shapes the specific language or structure of
     one or more sections (load-bearing)
   - **Tier B** if it provides important context or background
   - **Tier C** if tangentially relevant
   Explain your reasoning in one sentence.

---

## Step 3 — Generate bibliographic metadata

Derive the following fields:

- `slug` — format: `<author-or-org>_<year>_<short-title>`. Use the primary
  author's last name (lowercase), or an org name if no individual author.
  Year is publication year. Short title: 2–4 lowercase hyphenated words from
  the title. Check `references/references.yml` for slug conflicts; append
  `-b` if a conflict exists.
- `title` — full title of the work
- `creator` — author(s) or organisation name(s)
- `year` — publication year (integer, or `null` if unknown)
- `url` — the source URL, or `null` if file-only
- `license` — one of: `cc-by`, `cc-by-sa`, `cc0`, `public-domain`,
  `restricted`, or `unknown`
- `tier` — the proposed tier from Step 2 (subject to steward confirmation
  in Step 4)

---

## Step 4 — Confirm tier with steward

Present the following block and wait for the steward's response before
writing any files:

```
─────────────────────────────────────────────
Reference: [slug]
Title: [title]
Creator: [creator], [year]

Core thesis:
  [thesis from Step 2]

Covenant relevance:
  [relevance from Step 2]

Sections this would inform: [section IDs]

Proposed tier: [Tier X] — [one-sentence rationale]

  [Y] Accept Tier [X] (Recommended)
  [1] Override to Tier A (load-bearing)
  [2] Override to Tier B (supporting)
  [3] Override to Tier C (reading room)
  [N] Cancel — abort without writing anything
─────────────────────────────────────────────
```

Wait for the steward's response. If they say "cancel", "n", or "abort", stop
here and report that no files were written.

Set `tier` from the steward's response before proceeding to Step 5.

---

## Step 5 — Write `references/references.yml` entry

Read `references/references.yml` in full.

Append the new entry to the `references:` list. Use this YAML structure:

```yaml
  - slug: [slug]
    title: "[title]"
    creator: "[creator]"
    year: [year]
    url: "[url]"
    license: [license]
    tier: [A|B|C]
    thesis: "[one-sentence thesis]"
    relevance: "[one-to-two sentence covenant relevance]"
    informs_sections:
[      - section_id for each]
```

If `references: []` is currently an empty list, replace the `[]` with a
newline and the indented entry. If entries already exist, append after the
last entry, maintaining consistent indentation.

---

## Step 6 — Write notes file (Tier A only)

Skip this step if the tier is B or C.

Write `references/notes/[slug].md` with the following structure:

```markdown
# [Title]

**Creator:** [creator]
**Year:** [year]
**URL:** [url]
**License:** [license]
**Tier:** A

## Thesis

[One sentence: the central claim or argument.]

## Covenant Relevance

[One to two paragraphs on what this work contributes to the Covenant's
concerns. No copyrighted text — your own analysis only.]

## Key Points

[Up to five bullet points of ideas directly applicable to Covenant sections.
Frame each point in terms of what it implies for the Covenant's content.]

## Sections Informed

[For each section ID in `informs_sections`, one sentence on the specific
connection.]

## Notes

[Any additional context, caveats, or points to consider when citing this
reference. Leave empty if none.]
```

Do not quote copyrighted text. Use your own analysis and paraphrase only.
For works under permissive licenses (CC, public domain), brief excerpts with
attribution are acceptable.

---

## Step 7 — Report

After writing files, report:

```
─────────────────────────────────────────────
Reference added: [slug]

  references.yml: updated ([tier])
  notes file:     [references/notes/[slug].md | — (not Tier A)]
  TODO.md:        [removed entry | no matching entry found]

Sections informed: [section IDs, or "none identified"]
Tier: [A|B|C]

Review the entry:
  references/references.yml
[  references/notes/[slug].md]
─────────────────────────────────────────────
```

If any field could not be determined from the source (e.g. year unknown,
license unclear), flag it explicitly so the steward can verify and edit.

## Step 8 — Clean up TODO.md

Read `references/TODO.md`. Search for any line that contains the source URL
or slug. If found, remove that line (and any immediately adjacent label line
that refers to the same entry — e.g. a bare title line directly above a URL
line). Write the updated file.

If nothing matching the source is found in `TODO.md`, note "TODO.md: no
matching entry found" in the report instead.
