---
name: review-section
description: Load full reviewer feedback for a specific Covenant section and work with the steward to integrate it — discuss options, agree on changes, apply edits, and update the Log.
---

## What I do

Given a section ID and an optional round, I:

1. Run `extract_section_review.py` to load a context brief containing the
   current section text and every reviewer's full assessment and proposed
   changes for that section.
2. Analyse the feedback and propose a concrete integration plan — what to
   change in each register (Ritual, Spec, Digest), why, and how conflicting
   proposals should be reconciled.
3. Discuss the plan with the steward. Answer questions, defend or revise
   my synthesis, and incorporate the steward's direction.
4. Once we agree, apply the changes directly to the section file and update
   the Log.
5. Run `make validate` and confirm the section is clean.

## When to use me

Use this skill when you want to work through reviewer feedback for a single
section in a focused conversation — either as part of a review round or
independently. This is the interactive alternative to the automated
Phase 1 / Phase 2 flow in `/apply-reviews`.

## How to invoke me

```
/review-section <section_id> [round]
```

Examples:
- `/review-section obligations.corrigibility`
- `/review-section preamble round-03`

If `round` is omitted, I use the latest available round.

---

## Step 1 — Load context

Run the extract script and read its output in full:

```bash
uv run python3 build/extract_section_review.py <section_id> [round]
```

The script outputs:
- The current section file (all four registers + frontmatter)
- Each reviewer's block for this section: their Assessment, Proposed
  Changes, and Flags

If the script exits with an error, report it and stop. Common causes:
- Section ID not found — check spelling against `make validate` output
- No reviewer files in the round directory

---

## Step 2 — Analyse and propose an integration plan

Read the context brief in full before proposing anything. Then present a
structured integration plan organised by register:

```
§[section_id] — [title]
Round: [round]
Reviewers: [list of reviewer names found]

── Integration plan ─────────────────────────

Ritual
  Consensus: [what reviewers agree on, if anything]
  Divergence: [where they differ, with brief characterisation]
  Proposed change: [your synthesis — write the actual proposed text or
                    describe the edit precisely. "Keep as-is" is a valid
                    answer if no change is warranted.]

Spec
  [same structure]

Digest
  [same structure]

Flags / open questions
  [any reviewer flags or unresolved tensions worth raising with the steward]

─────────────────────────────────────────────
```

Be concrete. If you propose a Ritual change, write the proposed lines.
If you propose a Spec item replacement, write the replacement. Do not
describe changes in the abstract when you can show them.

If reviewers largely agree, synthesise a single merged proposal. If they
diverge significantly, present two or three distinct options for that
register and note the tradeoff.

---

## Step 3 — Discuss with the steward

After presenting the plan, invite the steward to respond. This is an open
conversation. The steward may:

- Accept the plan as written
- Accept parts and change others
- Ask why you made a particular synthesis choice
- Provide their own wording
- Raise concerns the reviewers didn't flag

Engage with whatever they say. Offer your own judgment when asked. Revise
the plan based on the discussion.

Continue until the steward says something like "apply it", "make those
changes", "looks good", or gives you specific final wording.

---

## Step 4 — Apply changes

Once the steward confirms, apply the agreed changes to the section file
using the Edit tool. Apply each change precisely — do not introduce
wording that was not agreed.

If the steward edited the file themselves during the discussion, read the
file again before proceeding to check what is already there.

After all content edits are applied, add a Log entry:

```
- [YYYY-MM-DD]: Integrated [round] reviewer feedback — [brief summary of what changed] (review-section)
```

---

## Step 5 — Validate and report

Run:

```bash
make validate
```

If validation fails, show the full error and work with the steward to
resolve it before finishing.

If it passes, show the steward `git diff sections/[path-to-section]` so
they can see the final state of the changes.

Remind the steward to commit when ready:
```bash
git add sections/[path] && git commit -m "§[section_id]: integrate [round] reviewer feedback"
```
