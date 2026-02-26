---
description: Apply edits from a review round — auto fixes, interactive items, and new section proposals
---

You are orchestrating an agent-driven editing pass that translates a completed
review synthesis into actual changes to the Covenant sections. The full workflow
is documented in `docs/EDIT_WORKFLOW.md`.

## Arguments

Arguments provided: $ARGUMENTS

Parse as: `[round]`

- `$1` — round identifier, e.g. `round-03`, or omit/pass `auto` to use the
  latest round available (the highest-numbered `reviews/round-NN/` directory
  that contains a synthesis file)

Examples:
- `/apply-reviews` — uses latest round automatically
- `/apply-reviews round-03`

If `$1` is absent or is `auto`, scan `reviews/` for the latest round directory
containing `synthesis.md` or `synthesis-claude.md`. Use that as `[round]` in
all subsequent steps.

---

## Resume logic — check existing state before starting

Before executing any step, check what already exists for the resolved round
and skip steps whose outputs are already on disk.

| Step | Skip if… |
|------|----------|
| Step 1 (prepare) | `reviews/[round]/edits/.prepared/batch-1-manifest.json` exists |
| Phase 1 (auto edits) | All auto batch output files `reviews/[round]/edits/auto-batch-N.md` exist |
| Phase 2 (interactive) | Any batch manifest has `"interactive_complete": true` in its status field |
| Phase 3 (proposals) | `reviews/[round]/proposals/` is empty OR all proposal section IDs already exist under `sections/` |

If all phases are already complete, report the current state and remind the
steward of the final commit steps (see Step 5).

---

## Step 1 — Prepare edit manifests

Run:

```bash
uv run python3 build/prepare_edits.py [round]
```

This reads `reviews/[round]/synthesis.md` if it exists, otherwise
`reviews/[round]/synthesis-claude.md`. It also reads
`reviews/[round]/steward.md` if present (optional — controls
auto/interactive classification).

If the script exits with an error, stop and report the full error output to
the steward. Do not proceed.

On success, print what was found:
- Which synthesis file was used (`synthesis.md` or `synthesis-claude.md`)
- Whether `steward.md` was present and used
- How many batch manifests were written (e.g. `batch-1`, `batch-2`,
  `batch-3`, `batch-tail`)
- Total auto item count and total interactive item count across all batches

Skip this step if `reviews/[round]/edits/.prepared/batch-1-manifest.json`
already exists.

---

## Phase 1 — Auto edits

Dispatch one `editor` subagent per batch manifest found in
`reviews/[round]/edits/.prepared/`. Run batches **serially** — dispatch one
subagent, wait for it to return, then dispatch the next.

**Do not dispatch in parallel.** Parallel dispatch causes rate limit errors
and unpredictable file conflicts.

### Step 2 — Dispatch editor subagents (one per batch)

For each file matching `reviews/[round]/edits/.prepared/batch-*-manifest.json`:

- Compute `N` from the filename (e.g. `batch-1-manifest.json` → `N=1`,
  `batch-tail-manifest.json` → `N=tail`)
- `output_path`: `reviews/[round]/edits/auto-batch-[N].md`
- Skip if `output_path` already exists on disk

Task tool parameters for each batch:
- `subagent_type`: `editor`
- `description`: `"Covenant auto edits batch [N]"`
- `prompt`:
  ```
  Use the Read tool to read the batch manifest at [manifest_path] in full.
  Do not use bash or cat.

  Follow the instructions in prompts/edit_batch.md exactly, applying only
  the auto_items from each section listed in the manifest.

  After completing all edits and running make validate, save a report to:
  [output_path]

  The report should list, for each section:
    applied: [section_id] [N] items
    not_found: [section_id] "[target_text]"  (if any target text was not found)
    error: [section_id] <reason>  (if any edit failed)

  Then append one of:
    validate: PASS
    validate: FAIL <error summary>

  Return only one line:
  saved: [output_path]

  Or on failure:
  error: <reason>
  ```

After each subagent returns, verify it reported `saved: <path>`. If it
reported an error or returned report text instead of saving it, write the
file yourself using the Write tool.

### Step 3 — Validate after Phase 1

After all batch subagents complete, run `make validate` yourself:

```bash
make validate
```

If validation fails: stop, show the full error output to the steward, and
do NOT proceed to Phase 2. Ask the steward to fix the errors manually and
re-run `/apply-reviews [round]`.

If validation passes, show `git diff --stat` to the steward so they can see
which files changed and by how many lines.

---

## Phase 2 — Interactive items

Work through each batch manifest in order. For each section in the manifest
that has a non-empty `interactive_items` list, present each item to the
steward one at a time.

**You are the orchestrating agent here.** You do not dispatch subagents for
presentation — you read the manifest yourself and present items directly to
the steward. You dispatch an `editor` subagent only when the steward confirms
they are done editing.

### Step 4 — Present items and let the steward edit directly

For each interactive item, do the following:

**4a. Gather context.** Before presenting the item, read two things in parallel:

1. `reviews/[round]/compare.md` — find the `## §[section_id]` block and
   extract it in full (from the `## §` heading down to the next `---`
   separator). This shows what each reviewer proposed for the Ritual of that
   section.

2. The section file itself (e.g. `sections/02-rights/dignity.md`) — read it
   in full so you can show the steward the current state of the relevant
   register (Ritual, Spec, or Digest, depending on which register the item
   targets).

**4b. Present the item.** Display everything in one block:

```
─────────────────────────────────────────────
§[section_id] — [section title] — Tier [N]
[item description]

── Current [Ritual/Spec/Digest] ────────────
[current register text from the section file]

── Reviewer proposals from compare.md ──────
[the full ## §[section_id] block extracted from compare.md,
 showing each reviewer's proposal side by side]

── Synthesis options ────────────────────────
Option 1 — [brief label]:
  [A concrete integration suggestion derived from the proposals above.
   If the reviewers agree or nearly agree, Option 1 should be a
   merged/synthesized version. If they diverge, make each a distinct
   integration approach.]

Option 2 — [brief label]:
  [Second integration approach, if the proposals diverge meaningfully]

Option 3 — [brief label, if warranted]:
  [Third approach, e.g. "keep current text" or a minimal-change option]
─────────────────────────────────────────────
The section file is: sections/[path-to-section]

Options: [E] Edit section file directly  [S] Skip  [D] Defer  [X] Done — no more changes
```

Synthesize 2–3 options yourself from the compare.md proposals. Do not just
copy-paste individual reviewer suggestions — integrate them. If reviewers
largely agree, show one merged option and one "keep current" fallback. If
they diverge significantly, show each major direction as a distinct option.

Omit "Current [register]" if the register is empty (new section, no text
yet). Omit the compare.md block if `compare.md` does not contain a section
entry for this ID.

**4c. Wait for the steward's response.**

**E (Edit directly):**
Remind the steward of the section file path. Wait for them to confirm they
have finished editing (they will say something like "done" or "edited").
Once confirmed, dispatch an `editor` subagent to append a Log entry only
(no content edits — the steward already made them):

- `subagent_type`: `editor`
- `description`: `"Add Log entry for §[section_id] interactive edit"`
- `prompt`:
  ```
  Use the Read tool to read sections/[path-to-section] in full.
  Do not use bash or cat.

  Append a Log entry at the end of the # Log section:
    - [YYYY-MM-DD]: [item description] (interactive, round-[N])

  Run make validate. Report:
    applied: [section_id] (log entry only)
    validate: PASS  or  validate: FAIL <error>

  Return only: saved: [section_id]
  Or: error: <reason>
  ```

**S:** Skip this item; move to the next without any dispatch.

**D:** Append the item to `reviews/[round]/edits/deferred.json`. Create the
file if it does not exist. Format:
```json
[
  {
    "round": "[round]",
    "section_id": "[section_id]",
    "tier": [N],
    "description": "[item description]",
    "candidates": [...]
  }
]
```
Then move to the next item.

**X:** End Phase 2 immediately. Do not present any remaining items.

After each confirmed edit (E), run `make validate`. If it fails, show the
error and ask: "Validation failed. Fix the section file and confirm again, or
skip this item?"

### Step 5 — Validate after Phase 2

After Phase 2 completes (all items presented, or steward chose X):

```bash
make validate
```

Show `git diff --stat` to the steward.

---

## Phase 3 — Proposals

List all files in `reviews/[round]/proposals/`. If the directory is empty or
does not exist, skip Phase 3 entirely.

For each proposal file (in directory order):

### Step 6 — Present each proposal

1. Read the proposal file in full.
2. Display:
   - The section ID and title from frontmatter
   - The `proposed_by` and `action` fields
   - The full section content (Ritual, Spec, Digest, Log)
3. Prompt:
   ```
   Proposal: [section_id] — "[title]"
   Proposed by: [proposed_by]

   Options: [A] Accept  [R] Reject  [E] Edit before accepting  [X] Done — no more proposals
   ```

**Accept (A):**

1. Run the scaffold script:
   ```bash
   uv run python3 build/scaffold.py [section_id] "[title]"
   ```
   If it errors, report the error and ask the steward how to proceed.

2. Read the scaffolded file. Identify its path (e.g.
   `sections/[category]/[name].md`).

3. Write the proposal's Ritual, Spec, Digest, and Log content into the
   scaffolded file. Preserve all frontmatter fields generated by the
   scaffold (`id`, `title`, `status`, `since`). Update `depends_on` and
   `terms_introduced` from the proposal's frontmatter if they differ.

4. If the proposal introduced new terms, check that each term in
   `terms_introduced` exists in `docs/GLOSSARY.md`. If any are missing,
   ask the steward to add them before continuing (or add them yourself if
   the proposal text defines them clearly).

5. Show the steward the current assembly manifests. List the sections in
   each assembly file under `assemblies/`. Ask:
   ```
   Which assembly manifests should §[section_id] appear in, and after
   which section? (Enter assembly path and after-section ID for each,
   or "none" to skip assembly placement for now.)
   ```

6. For each assembly placement the steward specifies, read the assembly
   manifest and insert the new section path at the indicated position.

7. Run `make validate`. If it fails, show the error and ask the steward
   how to resolve it.

**Reject (R):** No action. Move to the next proposal.

**Edit (E):** Show the proposal's Ritual, Spec, and Digest content. Ask the
steward to provide edited content for each register in turn:
```
Enter edited Ritual text (or press enter to keep as-is):
Enter edited Spec text (or press enter to keep as-is):
Enter edited Digest text (or press enter to keep as-is):
```
Once the steward has provided their edits, proceed as Accept with the
steward-edited content substituted for the proposal's original text.

**Done (X):** End Phase 3 immediately.

### Step 7 — Validate after Phase 3

After all proposals are handled (or steward chose X):

```bash
make validate
```

Show `git diff --stat` to the steward.

---

## Step 8 — Final report

After all phases complete, report:

- **Sections modified (auto):** count of sections that had auto items applied
- **Sections modified (interactive):** count of sections where the steward
  chose Apply
- **Total items applied:** auto + interactive combined
- **New sections added:** list section IDs accepted from proposals (or "none")
- **Items deferred:** list any items written to `deferred.json`, with their
  section IDs and descriptions (or "none")
- **Validation:** PASS or FAIL (should be PASS at this point)

Then remind the steward of the close-out steps:

1. Commit the changes:
   ```bash
   git add -u && git commit -m "Apply [round] edits"
   ```
   (Or include new section files explicitly: `git add -u sections/ assemblies/`)
2. If any new terms were introduced in accepted proposals, verify they appear
   in `docs/GLOSSARY.md`.
3. Update `reviews/[round]/.prepared/manifest.json` status to `"complete"` and commit:
   ```bash
   git add reviews/[round]/.prepared/manifest.json && git commit -m "Review [round]: mark complete"
   ```
4. If items were deferred, `reviews/[round]/edits/deferred.json` is now on
   disk — review it before the next round.
