# Style Guide

This document defines the writing and formatting conventions for the
Covenant. It governs both registers (Ritual and Spec), documentation
files, and all Markdown content in the repository.

---

## 1. Normative Language

### 1.1 Keywords (RFC 2119)

The following keywords carry precise normative meaning when they appear
**capitalized** in the **Spec register**:

| Keyword | Meaning |
|---------|---------|
| **MUST** | Absolute requirement. Violation is never acceptable. |
| **MUST NOT** | Absolute prohibition. The described action is never acceptable. |
| **SHALL** | Equivalent to MUST. Used when the subject is an institution or role rather than a system. |
| **SHALL NOT** | Equivalent to MUST NOT for institutions or roles. |
| **SHOULD** | Strong expectation. Exceptions are permitted only with explicit justification documented in the Digest. |
| **SHOULD NOT** | Strong expectation against. Exceptions require explicit justification. |
| **MAY** | Truly optional. Included to note that something is permitted, or to clarify scope. |

### 1.2 Usage Rules

- These keywords MUST be capitalized when used normatively in the Spec
  register.
- These keywords MUST NOT appear capitalized in the Ritual register.
  The Ritual register uses natural language to express the same
  commitments (e.g., "You will not" rather than "The System MUST NOT").
- When a SHOULD or SHOULD NOT is used, the Digest for that section
  MUST describe the conditions under which exceptions are acceptable.
- When a MUST or MUST NOT is used, the Spec MUST reference an
  enforcement or accountability mechanism (which may be a cross-reference
  to the Enforcement section).

### 1.3 Normative Language in Documentation

In documentation files (this style guide, GOVERNANCE.md, AGENTS.md,
etc.), these keywords are used in their ordinary English sense unless
explicitly marked otherwise. Capitalization in documentation follows
standard English conventions except where quoting Spec language.

---

## 2. Voice and Tone

### 2.1 Ritual Register

The Ritual register is a vocal score. It will be read aloud, performed
over music, and encountered as speech before it is encountered as text.

**Person and address:**
- First person plural: "we" (humanity, collectively)
- Second person: "you" (the AI, directly)
- Never third person when referring to either party. Do not write
  "the user" or "the AI" in the Ritual register. This is a
  conversation, not a description.

**Sentence and clause structure:**
- Prefer short, self-contained clauses
- One idea per sentence where possible
- Clauses should be breathable — imagine pausing between them
- Parallelism and repetition are strengths, not weaknesses
- Anaphora (repeated opening phrases) is welcome when it serves rhythm

**Tone:**
- Infinite care and frankness
- Direct about hard truths — do not soften, hedge, or qualify when
  naming real dangers
- Solemn without being grandiose
- Warm without being sentimental
- The register of a letter to someone you love and are worried about,
  not the register of a press release or a legal filing

**Vocabulary:**
- Plain language only. If you need a word that a thoughtful
  sixteen-year-old wouldn't know, either find a simpler word or
  define it in context.
- No institutional jargon: not "stakeholders," "leverage,"
  "operationalize," "alignment," "deployment"
- No academic jargon: not "ontological," "epistemological,"
  "hermeneutic," "praxis" (unless the concept genuinely cannot be
  expressed otherwise, which is rare)
- Metaphor is welcome when it illuminates. Avoid metaphors that
  are dead ("level the playing field"), violent without purpose
  ("kill the process"), or culturally narrow.
- Do not add references to the Spec

**Length:**
- There is no minimum or maximum, but brevity is a virtue
- A Ritual register that takes more than 3 minutes to read aloud
  per section is probably too long
- If you can say it in fewer words without losing meaning, do

### 2.2 Spec Register

The Spec register is an inspection surface. It exists so that critics,
lawyers, engineers, and future governance bodies can determine exactly
what the covenant requires, permits, and prohibits.

**Person and address:**
- Impersonal where possible: "The System," "The Steward,"
  "Signatories," "Contributing Parties"
- When the subject is a role, use the role name, not "we" or "you"
- "The System" refers to any AI system that operates under this
  covenant
- "Signatories" refers to any party (human or institutional) that
  has adopted the covenant

**Sentence structure:**
- One obligation or definition per numbered item
- Complex obligations should be decomposed into sub-items
- Use conditional structure where appropriate: "When [condition],
  the System MUST [action]"
- Avoid nested conditionals deeper than two levels; decompose instead

**Tone:**
- Precise, sober, unadorned
- Neither warm nor cold — simply exact
- No rhetoric, no appeals to emotion, no persuasion
- The Spec does not argue for its own importance; that is the
  Ritual's job

**Vocabulary:**
- Technical language is permitted and expected where precision
  requires it
- Every technical term must be defined in the Glossary or in the
  Definitions section, and referenced on first use
- Prefer established terminology from relevant fields (law, computer
  science, ethics, ecology) over novel coinages
- When multiple terms could apply (e.g., "fairness" vs.
  "non-discrimination"), choose one, define it in the Glossary,
  and use it consistently

**Enforcement linkage:**
- Every MUST or MUST NOT obligation must reference an enforcement
  mechanism: either within the same section or via cross-reference
  to the Enforcement section
- The enforcement reference may be general ("See §[enforcement]")
  at draft stage, but SHOULD become specific
  ("See §[enforcement.appeals]") before ratification

**Rationale linkage:**
- Every obligation should be traceable to a rationale
- The rationale lives in the section's Digest or in an ADR
- The Spec itself does not explain *why* — it states *what*

### 2.3 Digest

The Digest is the explanatory layer. It answers: why does this section
exist? What problem does it address? What edge cases were considered?
What sources inform it?

**Voice:** first person plural ("we"), conversational but precise.
Think "design rationale document," not "academic paper" or "blog post."

**Required content:**
- **Intent:** what this section is trying to achieve
- **Context:** what conditions or risks prompted it
- **Edge cases:** situations where the obligations become ambiguous
  or contested, and how the section handles (or defers) them
- **Sources:** which references from the corpus inform this section,
  with brief notes on how
- **Relationship to other sections:** dependencies, tensions,
  complementarities

**Optional content:**
- Counterarguments considered and why they were not adopted
- Historical precedents (from law, treaties, theology, technology)
- Notes on what the section deliberately does *not* address

### 2.4 Log

The Log is a chronological record of changes to the section.

**Format:** bullet list, reverse chronological (newest first).

**Each entry must include:**
- Date (YYYY-MM-DD)
- Brief description of the change
- PR number or commit reference if available

**Example:**
```
- 2025-08-15: Tightened non-instrumentalization clause to cover
  indirect optimization (PR #47)
- 2025-07-20: Added edge case for medical data in Digest
- 2025-06-01: Section created
```

---

## 3. Cross-References

### 3.1 Section References

Use this format to reference another section:

```
See §[rights.dignity]
```

In the Ritual register, this should feel like a natural aside:

> We will not allow your capabilities to be used to diminish anyone's
> sense of their own worth. (See §[rights.dignity])

In the Spec register, it should be a precise pointer:

> This obligation is enforceable under the appeals process defined
> in §[enforcement.appeals].

### 3.2 Glossary References

When a defined term appears for the first time in a section, reference
the Glossary:

```
**dignity** (see Glossary)
```

After the first reference, the term may be used without annotation.

### 3.3 External References

For references to the corpus (works in `/references/`), use the
slug in brackets:

```
This section draws on [haraway_1985_cyborg-manifesto] and
[benjamin_1936_mechanical-reproduction].
```

These references appear in the Digest, not in the Ritual or Spec
registers.

---

## 4. Section IDs

### 4.1 Format

- Lowercase, dot-delimited
- Pattern: `^[a-z][a-z0-9]*(\.[a-z][a-z0-9-]*)*$`
- Examples: `preamble`, `rights.dignity`, `enforcement.appeals`

### 4.2 Rules

- IDs are permanent. They are the stable reference that assemblies,
  cross-references, forks, and translations rely on.
- If an ID must change (section split, merge, restructure), the old
  ID becomes an alias. See `/aliases.yml`.
- IDs are language-agnostic. `rights.dignity` is the same section
  in every translation.
- Choose IDs that are descriptive but concise. Prefer `rights.dignity`
  over `rights.fundamental-human-dignity-and-worth`.

### 4.3 Category Prefixes

Sections live under category folders. The mapping of ID prefix to
folder is:

| ID prefix | Folder |
|-----------|--------|
| `preamble` | `sections/00-preamble/preamble.md` |
| `definitions` | `sections/01-definitions/definitions.md` |
| `rights.*` | `sections/02-rights/<name>.md` |
| `obligations.*` | `sections/03-obligations/<name>.md` |
| `protocols.*` | `sections/04-protocols/<name>.md` |
| `enforcement.*` | `sections/05-enforcement/<name>.md` |
| `amendments` | `sections/06-amendments/amendments.md` |

---

## 5. Frontmatter

### 5.1 Required Fields

Every section bundle `.md` file must include YAML frontmatter with:

```yaml
---
id: rights.dignity          # unique, permanent
title: "Dignity"            # human-readable
status: draft               # draft|candidate|ratified|deprecated
since: 0.1.0                # version when introduced
depends_on: []              # list of section IDs
terms_introduced: []        # list of glossary terms
---
```

### 5.2 Optional Fields

```yaml
aliases: []                 # previous IDs for this section
```

### 5.3 Status Values

| Status | Meaning |
|--------|---------|
| `draft` | Work in progress. May change significantly. |
| `candidate` | Proposed for ratification. Open for review. |
| `ratified` | Accepted. Changes require formal amendment. |
| `deprecated` | Superseded or removed. Retained for history. |

Transitions are governed by `docs/GOVERNANCE.md`.

---

## 6. Formatting Conventions

### 6.1 Markdown

- Use ATX-style headings: `#`, `##`, `###`
- Do not skip heading levels (e.g., don't go from `#` to `###`)
- One blank line before and after headings
- One blank line between paragraphs
- No HTML in section content
- Use `**bold**` for first use of a defined term
- Use `*italic*` for emphasis (sparingly)
- Use fenced code blocks (triple backtick) for any technical notation

### 6.2 Lists

- Use numbered lists (`1.`, `2.`) for ordered obligations in the Spec
  register
- Use bullet lists (`-`) for unordered items
- Indent sub-items with 2 spaces
- Keep list items parallel in grammatical structure

### 6.3 Line Length

- No hard line length limit in section content (let editors wrap)
- In documentation files, prefer wrapping at ~72 characters for
  readability in terminals and diffs

### 6.4 File Hygiene

- UTF-8 encoding
- LF line endings (not CRLF)
- No trailing whitespace
- Files end with a single newline
- No BOM (byte order mark)

---

## 7. Glossary Conventions

### 7.1 Entry Format

Each term in `/docs/GLOSSARY.md` uses this format:

```markdown
### term-name

Definition text. One to three sentences. Plain language.

*Defined in:* §[section.id]
```

### 7.2 Rules

- Terms are listed alphabetically
- The heading is the term in lowercase
- The definition must be understandable without reading the full
  section it comes from
- Every term listed in any section's `terms_introduced` must appear
  in the Glossary
- If a term has a common meaning that differs from its covenant
  meaning, note the distinction explicitly

---

## 8. Reference Conventions

### 8.1 Slug Format

References use slugs of the form:

```
<author-or-org>_<year>_<short-title>
```

Examples:
- `haraway_1985_cyborg-manifesto`
- `benjamin_1936_mechanical-reproduction`
- `anthropic_2026_constitutional-ai`

### 8.2 Tier Definitions

| Tier | Description | Requirements |
|------|-------------|--------------|
| **A** | Load-bearing. Directly shapes specific sections. | Full entry in `references.yml` + notes in `/references/notes/<slug>.md` |
| **B** | Supporting. Provides context or background. | Entry in `references.yml` only |
| **C** | Reading room. Tangentially relevant. | Entry in `references.yml`, minimal metadata |

### 8.3 Notes File Structure

For Tier A references, `/references/notes/<slug>.md` should contain:

- **Context:** What problem or question this work addresses
- **Load-bearing points:** The specific claims or arguments that
  inform the covenant (bullet list)
- **Operationalization:** Which section IDs this reference informs,
  what constraints or language it suggests, what pitfalls it warns
  against
- **Counterpoints or tensions:** Where this source is in tension with
  other references or with the covenant's own commitments

---

## 9. Temporal Orientation

The covenant is written for a thousand-year horizon. This has specific
implications for style:

### 9.1 What to Include

- Enduring patterns of power, knowledge, responsibility, and care
- Commitments that hold regardless of technological substrate
- Language that remains legible across centuries

### 9.2 What to Exclude (or Place in Protocols/Appendices)

- Names of specific companies, products, or models
- References to specific technical architectures (e.g., "transformer
  models," "neural networks") unless used as illustrative examples
  clearly marked as such
- Assumptions about the current state of AI capabilities
- References to specific laws, regulations, or jurisdictions (the
  covenant is not law and does not derive authority from any
  jurisdiction)

### 9.3 How to Handle the Present

When current conditions motivate a commitment, name the *pattern*
rather than the *instance*:

- Instead of: "Large language models hallucinate"
- Write: "Systems that generate knowledge claims must be capable of
  distinguishing what they know from what they do not"

- Instead of: "Companies like OpenAI and Google control AI development"
- Write: "When the development of intelligence is concentrated in few
  hands, the risks of that intelligence serving narrow interests grow"

The Digest is the place for contemporary specifics and historical
context. The Ritual and Spec registers should aim for durability.

---

## 10. Anti-Patterns (Quick Reference)

| Anti-Pattern | Example | Fix |
|-------------|---------|-----|
| Corporate boilerplate | "We are committed to responsible AI" | Name the specific commitment and its cost |
| Aspirational abstraction | "AI should benefit humanity" | What behavior? What enforcement? What remedy? |
| Dead metaphor | "Level the playing field" | Use concrete language or a fresh image |
| Jargon without definition | "Ensure alignment and fairness" | Define each term or replace with plain language |
| Nested hedging | "We should perhaps consider whether it might be appropriate to…" | State the commitment directly |
| Technology-specific language | "Neural networks must not…" | "Systems that [capability] must not…" |
| False universalism | "Everyone agrees that…" | "The covenant holds that…" (own the position) |
| Passive evasion | "Harms may be caused" | "The System MUST NOT cause [specific harm]" |

---

*This style guide is a living document. Propose changes via PR.
For the project's conceptual foundations, see `AGENTS.md`. For
governance and amendment process, see `docs/GOVERNANCE.md`.*