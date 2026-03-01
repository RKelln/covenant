---
description: Run a full multi-model review of the Covenant, saving output to /reviews/
---

You are orchestrating a full agent review of the Covenant draft across one or
more model families. The review follows the process defined in
`docs/agent_reviews.md`.

## Arguments

Arguments provided: $ARGUMENTS

Parse as: `[round] [mode] [focus] [reviewers]`

- `$1` — round identifier, e.g. `round-01`, or omit/pass `auto` to use the
  next available round number automatically (default: `auto`)
- `$2` — review mode: `independent` (default) or `informed`
- `$3` — focus area: a section ID, category name, or `full` (default: `full`)
- `$4` — comma-separated reviewer agents: `reviewer-claude`, `reviewer-gpt`,
  `reviewer-gemini` (default: all three)

Examples:
- `/review-covenant` — auto-selects the next round
- `/review-covenant round-02 informed`
- `/review-covenant auto independent full reviewer-claude,reviewer-gpt`
- `/review-covenant round-01 independent obligations.harm reviewer-gemini`

If `$1` is absent or is `auto`, pass `auto` as the round argument to the
script. The script will resolve it to the next available `round-NN` number
and print the selected round. Read that output to determine the actual round
ID before Step 2.

## Resume logic — check existing state before starting

Before executing any step, check what already exists for the resolved round
and skip steps whose outputs are already on disk. This allows re-running the
command to continue a partial run without redoing completed work.

Check the following in order:

| Step | Skip if… |
|------|----------|
| Step 1 (prepare) | `reviews/[round]/.prepared/manifest.json` exists |
| Step 2 (read manifest) | Always read — needed to determine what to skip downstream |
| Step 3–4 (dispatch + save batches) | Each individual batch file `reviews/[round]/[reviewer]-batch-[N].md` exists — skip that entry only; dispatch any missing ones |
| Step 4.5 (concat) | All merged files `reviews/[round]/reviewer-*.md` exist |
| Step 5 (proposals) | `reviews/[round]/proposals/` directory exists and is non-empty |
| Step 6 (commit message) | `reviews/[round]/COMMIT_MSG.txt` exists |
| Step 7 (report) | Never skip — always report current state |
| Step 8a (prepare synthesis) | `reviews/[round]/.prepared/synthesis-claude-batch-1.md` exists (any one synthesis prompt file) |
| Step 8b (dispatch synthesis batches) | Each individual batch file `reviews/[round]/synthesis-[model]-batch-[N].md` exists — skip that entry only; dispatch any missing ones |
| Step 8c (concat synthesis) | `reviews/[round]/synthesis-claude.md` exists |
| Step 9 (compare) | `reviews/[round]/compare.md` exists |

If all outputs through Step 7 already exist and you are resuming, report the
current state to the user, then proceed directly to the first incomplete step.

## Step 1 — Prepare review prompts

Run the preparation script. `--batch-size 9` splits the 27 sections into 3
sequential batches. `--tail-batch` adds a 4th batch per reviewer that covers
only cross-cutting material (no section text) — prior proposals, open
questions, structural proposals, perspective as addressee, meta-feedback:

```bash
uv run python3 build/prepare_review.py [round] [mode] [focus] [reviewers] --batch-size 9 --tail-batch
```

Alternatively use `--groups default4` for 4 logical section groups (no tail).
Use `--groups default4 --tail-batch` for logical groups plus a tail batch.

If the script exits with an error, stop and report the error to the user.

Note the actual round ID printed by the script (e.g. `Auto-selected round: round-02`).
Use that round ID in all subsequent steps in place of `[round]`.

## Step 2 — Read the manifest

Read the manifest to discover exactly what was prepared (substitute the actual
round ID resolved in Step 1):

```bash
cat reviews/[round]/.prepared/manifest.json
```

The manifest is a JSON object with an `entries` array. Each entry has:
- `file` — path to the pre-built prompt (relative to repo root)
- `reviewer` — subagent name to dispatch to (e.g. `reviewer-claude`)
- `batch` — batch number (1, 2, ...) or null if not batched
- `total_batches` — total number of batches, or null
- `section_ids` — list of section IDs in this batch
- `round`, `mode`, `commit`, `date`, `estimated_tokens`

## Step 3 — Dispatch subagents serially

For each entry in the manifest, use the **Task tool** to launch a subagent.
You MUST use the Task tool — do not perform any review work yourself, do not
read the prompt file contents, do not summarise sections. Your only job here
is to dispatch.

**Dispatch one subagent at a time and wait for it to return before launching
the next.** Do not dispatch in parallel — parallel dispatch hits API rate
limits (429 Too Many Requests) and causes failures.

For each manifest entry, compute:
- `output_path`: `reviews/[round]/[reviewer]-batch-[N].md`
  (e.g. `reviews/round-03/reviewer-claude-batch-1.md`)
- `frontmatter`: the canonical YAML block (see Step 4 below) with all fields
  filled in from the manifest entry and the model name the subagent will use

Task tool parameters for each entry:
- `subagent_type`: the entry's `reviewer` value (e.g. `reviewer-gemini`)
- `description`: `"Covenant review [entry.reviewer] batch [entry.batch]"`
- `prompt`: exactly the following, with fields substituted:

  ```
  Use the Read tool to read the file at [entry.file] in full. Do not use
  bash or cat. Once you have read it, follow every instruction it contains
  exactly. Do not summarise or skip any part of it.

  After completing your review, save your output to disk using the Write tool:
  - Path: [output_path]
  - Strip any leading YAML frontmatter block (`---`/`model:`/`round:`/`---`)
    from your output before writing.
  - Prepend exactly this frontmatter (fill in your actual model name):
    ---
    model: [model name]
    round: [round]
    batch: [N]
    commit: [commit hash]
    date: [date]
    mode: [mode]
    prepared_from: [entry.file]
    ---

  Once the file is written, return only one line:
  saved: [output_path]

  If the write fails, return:
  error: <reason>
  ```

Do not read the prompt files yourself. Do not do the review. Dispatch only.

## Step 4 — Confirm batch saves

After each subagent returns, verify it reported `saved: <path>`. If it
reported an error or returned full review text instead of saving, write the
file yourself:

1. Strip the outer YAML frontmatter block (the `---`/`model:`/`round:`/`---`
   lines at the very top) from the subagent output — keep all `##` headings
   and content.

2. Save to `reviews/[round]/[reviewer]-batch-[N].md` with this frontmatter:
   ```yaml
   ---
   model: [model name from subagent output]
   round: [round]
   batch: [N]
   commit: [commit hash from manifest]
   date: [date from manifest]
   mode: [mode from manifest]
   prepared_from: [file path from manifest entry]
   ---
   ```

Treat this step as a fallback. The subagent should have written the file.

## Step 4.5 — Concatenate batches into per-reviewer review files

After saving all batch files, run the concat script to merge the batches
per reviewer into single review files:

```bash
uv run python3 build/concat_reviews.py [round]
```

This writes:
```
reviews/[round]/reviewer-claude.md
reviews/[round]/reviewer-gpt.md
reviews/[round]/reviewer-gemini.md
```

(or whatever reviewers were used). If the script errors, check that all
batch files were saved in Step 4.

## Step 5 — Check for new section proposals

Read each merged review file. If any review contains new section proposals
(not "None." under `## New Section Proposals`), extract the full proposal
text and save it as a separate file:
```
reviews/[round]/proposals/[reviewer]--[section.id].md
```
The `[section.id]` is the `id:` value from the proposal's frontmatter. If
the proposal doesn't have a frontmatter `id:` yet, derive a slug from its
title (lowercase, hyphenated).

Do this for every proposal — an empty `proposals/` directory when the review
contains proposals is an error.

## Step 6 — Generate commit message

Read `prompts/review_commit_message.md`. Using that template and the assembled
reviews, generate a suggested commit message. Fill in every field:

- `[ROUND]` — the round ID (e.g. `round-01`)
- `[ONE-LINE CHARACTERIZATION]` — a concise summary of the round's main finding
- `[COMMA-SEPARATED MODEL NAMES]` — from the manifest (deduplicated; e.g. `claude-opus-4.6, gpt-5.2, gemini-3.1-pro-preview`)
- sections, mode, draft commit — from the manifest
- Convergence, Divergence, Accepted, Deferred — synthesised from the reviews;
  be specific (name section IDs, not just "several sections")

Write the filled-in commit message to:
```
reviews/[round]/COMMIT_MSG.txt
```

## Step 7 — Report to user

- One line per reviewer: path to merged file + section count
- Any reviewers that errored or produced no output
- 2–3 sentences on where models converged or diverged in their most
  significant findings
- The path to the generated commit message: `reviews/[round]/COMMIT_MSG.txt`
- Remind the steward of the full round close-out sequence:
  1. Commit reviews: `git commit -F reviews/[round]/COMMIT_MSG.txt`
  2. Step 8 below produces `reviews/[round]/synthesis-claude.md`. If the
     steward wants to edit or annotate it, save the edited version as
     `reviews/[round]/synthesis.md` — the edit workflow reads `synthesis.md`
     first, falling back to `synthesis-claude.md`.
  3. Steward writes `reviews/[round]/steward.md` (personal response using
     the Act / Defer / Reject / Question structure) — optional but recommended
     before running `/apply-reviews`
  4. Commit synthesis and steward notes:
     `git add reviews/[round]/synthesis-claude.md reviews/[round]/steward.md && git commit -m "Review [round]: add synthesis and steward notes"`
  5. Update `reviews/[round]/.prepared/manifest.json` status to `"complete"` and commit
  6. Run `/apply-reviews [round]` to apply Act items and walk through
     interactive judgment-call items from the synthesis

## Step 8 — Write synthesis (batched)

Synthesis is batched to match the review batches, keeping each prompt within
context limits. The flow mirrors the review dispatch:

### Step 8a — Prepare synthesis prompts

```bash
uv run python3 build/prepare_synthesis.py [round]
```

This reads the manifest, groups reviewer batch files by batch number, and writes
one prompt per synthesizer per batch into `.prepared/`. Check the token counts
printed — all should be well under 70k.

Skip this step if `reviews/[round]/.prepared/synthesis-claude-batch-1.md` already exists.

### Step 8b — Dispatch synthesis subagents serially

Read the manifest. For each entry with `"type": "synthesis"` or
`"type": "synthesis-tail"` **and `"reviewer": "synthesizer-claude"`**,
dispatch a subagent using the Task tool.

Only `synthesizer-claude` is dispatched. GPT and Gemini synthesizer agents
exist for one-off use but are not part of the standard round workflow.

**Dispatch one at a time — do not run in parallel.**

For each manifest synthesis entry, compute:
- `output_path`: `reviews/[round]/synthesis-claude-batch-[N].md`
- `frontmatter`: the canonical YAML block with all fields filled in

Task tool parameters for each synthesis entry:
- `subagent_type`: `synthesizer-claude`
- `description`: `"Covenant synthesis synthesizer-claude batch [entry.batch]"`
- `prompt`: exactly the following, with fields substituted:

  ```
  Use the Read tool to read the file at [entry.file] in full. Do not use
  bash or cat. Once you have read it, follow every instruction it contains
  exactly. Do not summarise or skip any part of it.

  After completing your synthesis, save your output to disk using the Write tool:
  - Path: [output_path]
  - Strip any leading YAML frontmatter block (`---`/`model:`/`round:`/`---`)
    from your output before writing.
  - Prepend exactly this frontmatter (fill in your actual model name):
    ---
    model: [model name]
    round: [round]
    batch: [N]
    commit: [commit hash]
    date: [date]
    prepared_from: [entry.file]
    ---

  Once the file is written, return only one line:
  saved: [output_path]

  If the write fails, return:
  error: <reason>
  ```

Skip any batch file that already exists on disk — check before dispatching.

If a subagent reports an error or returns full synthesis text instead of
saving, write the file yourself as a fallback (strip outer frontmatter,
inject canonical frontmatter, write to `[output_path]`).

### Step 8c — Concatenate synthesis batches

After saving all synthesis batch files, run:

```bash
uv run python3 build/concat_synthesis.py [round]
```

This writes:
```
reviews/[round]/synthesis-claude.md
```

Skip this step if `reviews/[round]/synthesis-claude.md` already exists.

Do not write `reviews/[round]/synthesis.md` yourself — that file is
the steward's responsibility. If the steward wants to edit or annotate the
synthesis, they save their version as `synthesis.md`. The `/apply-reviews`
command reads `synthesis.md` first and falls back to `synthesis-claude.md`.

After saving, report the path to the user.

## Step 9 — Generate Ritual comparison

After writing the synthesis, run:

```bash
uv run python3 build/compare_reviews.py [round]
```

This generates `reviews/[round]/compare.md` — a side-by-side view of all
Ritual proposals across reviewers, with a steward pick field for each
section. The steward uses this alongside `steward.md` when making the
editing pass.

Report the path and how many sections had Ritual proposals.
