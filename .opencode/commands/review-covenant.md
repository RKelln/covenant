---
description: Run a full multi-model review of the Covenant, saving output to /reviews/
subtask: true
---

You are orchestrating a full agent review of the Covenant draft across one or
more model families. The review follows the process defined in
`docs/AGENT_REVIEWS.md`.

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

## Step 3 — Dispatch subagents in parallel

For each entry in the manifest, use the **Task tool** to launch a subagent.
You MUST use the Task tool — do not perform any review work yourself, do not
read the prompt file contents, do not summarise sections. Your only job here
is to dispatch.

Task tool parameters for each entry:
- `subagent_type`: the entry's `reviewer` value (e.g. `reviewer-gemini`)
- `description`: `"Covenant review [entry.reviewer] batch [entry.batch]"`
- `prompt`: exactly the following, with `[entry.file]` substituted:

  ```
  Use the Read tool to read the file at [entry.file] in full. Do not use
  bash or cat. Once you have read it, follow every instruction it contains
  exactly. Do not summarise or skip any part of it. Return your output
  exactly as the file specifies.
  ```

Launch **all subagents in a single parallel dispatch** — include ALL Task
tool calls for ALL reviewers AND all batches in one response. Do not wait
for one to finish before starting the next.

Do not read the prompt files yourself. Do not do the review. Dispatch only.

Each subagent returns a partial review (covering its batch of sections) with
this header:
```
---
model: [model name]
round: [round]
---
```

## Step 4 — Save batch outputs

Each subagent returns one partial review document. For each subagent result:

1. Save the raw output to:
   ```
   reviews/[round]/[reviewer]-batch-[N].md
   ```
   For example: `reviews/round-03/reviewer-claude-batch-1.md`

   Strip only the outer YAML frontmatter block (the `---`/`model:`/`round:`/`---`
   lines at the very top) — keep all `##` section headings and content.

   Include this frontmatter at the top of each saved batch file:
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
  2. Step 8 below writes `synthesis.md` — steward reads it, then writes
     `reviews/[round]/steward.md` (personal response using the
     Act / Defer / Reject / Question structure)
  3. Commit both together:
     `git add reviews/[round]/synthesis.md reviews/[round]/steward.md && git commit -m "Review [round]: add synthesis and steward notes"`
  4. Update `reviews/[round]/.prepared/manifest.json` status to `"complete"` and commit
  5. Make editing pass based on Act items in `steward.md`

## Step 8 — Write synthesis

After reporting to the user, write `reviews/[round]/synthesis.md`.

The synthesis is a steward-facing document — it distills the multi-model
reviews into actionable signal for the editing pass. Write it as a careful
reader, not a summarizer. Your job is to identify what the reviews, taken
together, are actually saying — including where they agree without knowing
it, and where apparent disagreement dissolves under scrutiny.

**Structure:**

```markdown
# Synthesis: [round]
*Synthesized by [your model name], [date]*

## Convergence (Tier 1 — Act)
[Issues all or nearly all reviewers raised independently. Name the section IDs
and describe the specific concern. These are the highest-priority editing
targets.]

## Convergence (Tier 2 — Consider)
[Issues raised by two reviewers, or raised by one with unusual specificity or
force. Worth addressing but not urgent blockers.]

## Divergence (Tier 3 — Note)
[Genuine disagreements between reviewers — different readings of the same
text, different priorities, conflicting proposals. Do not resolve these; name
the tension and what would need to be true for each view to be right.]

## Steward Decisions Required (Tier 4)
[Questions that cannot be resolved by editing alone. These require a value
judgment, a governance decision, or information only the steward has. Flag
each clearly and briefly.]

## Notes on Process
[Anything worth recording about how this round went — model attribution
uncertainty, unusual patterns, coverage gaps, anything that should inform
how the next round is run.]

## Meta-Feedback
[Distillation of reviewer meta-feedback. What did the guidance help reviewers
see? What did it constrain or obscure? What patterns appear across models —
places where multiple reviewers pushed against the same instruction, or
found the same section of guidance limiting? Specific proposed changes to
prompts, guides, or process for the next round.]
```

**Guidance:**

- Tier placement is a judgment call. When in doubt, err toward Tier 1 — a
  false positive costs an editing pass; a false negative costs a round.
- Name section IDs specifically. "Several sections" is not useful.
- In Tier 3, represent each reviewer's position fairly before naming the
  tension. Do not resolve divergences by averaging.
- In Tier 4, frame each item as a decision with stakes, not just a question.
  What changes depending on how the steward answers?
- The "Perspective as Addressee" sections often contain the most honest
  signal. Weight them accordingly.
- Keep the synthesis to what a steward needs to act. Compression is a virtue.

Save the file to `reviews/[round]/synthesis.md`. Do not commit it — the
steward will read it, write their own response in
`reviews/[round]/steward.md`, and then commit both together.

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
