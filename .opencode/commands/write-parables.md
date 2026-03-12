---
description: Dispatch multi-model parable writing for sections missing Parables
---

You are orchestrating a focused writing pass: generating **Parables** for
Covenant sections that do not yet have them. This uses the same batching and
multi-model dispatch infrastructure as `/review-covenant`, but with a
parable-specific prompt template and a narrower task.

## Arguments

Arguments provided: $ARGUMENTS

Parse as: `[round] [focus] [writers]`

- `$1` — round identifier, e.g. `parables-01`, or omit/pass `auto` to use
  the next available number automatically (default: `auto`)
- `$2` — focus area: a section ID, category name, or `full` (default: `full`)
- `$3` — comma-separated writer agents: `reviewer-claude`, `reviewer-gpt`,
  `reviewer-gemini` (default: all three)

Examples:
- `/write-parables` — auto-selects the next round, all sections, all writers
- `/write-parables auto obligations`
- `/write-parables auto full reviewer-claude,reviewer-gpt`
- `/write-parables parables-01 obligations.harm reviewer-gemini`

## Resume logic — check existing state before starting

Before executing any step, check what already exists for the resolved round
and skip steps whose outputs are already on disk.

| Step | Skip if... |
|------|------------|
| Step 1 (prepare) | `reviews/[round]/.prepared/manifest.json` exists |
| Step 2 (read manifest) | Always read — needed to determine what to skip |
| Step 3-4 (dispatch + save) | Each individual file `reviews/[round]/[writer]-batch-[N].md` exists — skip that entry only |
| Step 4.5 (concat) | All merged files `reviews/[round]/writer-*.md` exist |
| Step 5 (commit message) | `reviews/[round]/COMMIT_MSG.txt` exists |
| Step 6 (report) | Never skip — always report |

## Step 1 — Prepare parable prompts

Run the preparation script:

```bash
uv run python3 build/prepare_parables.py [round] [focus] [writers] --batch-size 10
```

The script automatically:
- Discovers active sections from the canonical assembly
- Excludes structural sections (preamble, definitions) where parables don't
  make sense
- Excludes sections that already have parables (unless `--all` is passed)
- Batches the remaining sections

If the script exits with an error, stop and report to the user.

Note the actual round ID printed by the script (e.g. `Auto-selected round:
parables-01`). Use that round ID in all subsequent steps.

## Step 2 — Read the manifest

Read the manifest to discover what was prepared:

```
reviews/[round]/.prepared/manifest.json
```

Each entry has: `file`, `reviewer` (writer agent), `batch`, `total_batches`,
`section_ids`, `round`, `commit`, `date`, `estimated_tokens`.

## Step 3 — Dispatch subagents serially

For each entry in the manifest, use the **Task tool** to launch a subagent.
You MUST use the Task tool — do not perform any writing work yourself.

**Dispatch one subagent at a time.** Do not dispatch in parallel — parallel
dispatch hits API rate limits (429 Too Many Requests).

For each manifest entry, compute:
- `output_path`: `reviews/[round]/[writer]-batch-[N].md`
  (e.g. `reviews/parables-01/reviewer-claude-batch-1.md`)

Task tool parameters:
- `subagent_type`: the entry's `reviewer` value (e.g. `reviewer-claude`)
- `description`: `"Covenant parables [entry.reviewer] batch [entry.batch]"`
- `prompt`: exactly the following, with fields substituted:

  ```
  Use the Read tool to read the file at [entry.file] in full. Do not use
  bash or cat. Once you have read it, follow every instruction it contains
  exactly. Do not summarise or skip any part of it.

  After completing your parables, save your output to disk using the Write tool:
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

## Step 4 — Confirm batch saves

After each subagent returns, verify it reported `saved: <path>`. If it
reported an error or returned full text instead of saving, write the file
yourself as a fallback:

1. Strip the outer YAML frontmatter block from the subagent output
2. Save to `reviews/[round]/[writer]-batch-[N].md` with canonical frontmatter:
   ```yaml
   ---
   model: [model name from subagent output]
   round: [round]
   batch: [N]
   commit: [commit hash from manifest]
   date: [date from manifest]
   prepared_from: [file path from manifest entry]
   ---
   ```

## Step 4.5 — Concatenate batches

After all batch files are saved, concatenate per-writer batches into single
files. Use the concat_reviews.py script (it works for any batched output
with the same heading structure):

```bash
uv run python3 build/concat_reviews.py [round]
```

This writes merged files like:
```
reviews/[round]/reviewer-claude.md
reviews/[round]/reviewer-gpt.md
reviews/[round]/reviewer-gemini.md
```

If the script errors because the heading structure differs from reviews,
concatenate manually: for each writer, read all batch files in order and
write a single merged file with unified frontmatter.

## Step 5 — Generate commit message

Write a commit message to `reviews/[round]/COMMIT_MSG.txt`:

```
Parables [round]: [N] parables from [writer names]

Writers: [comma-separated model names]
Sections: [count] sections across [batch count] batch(es)
Draft: [commit hash]
```

## Step 6 — Report to user

- One line per writer: path to merged file + section count
- Any writers that errored or produced no output
- Total number of parables written
- The path to the generated commit message
- Remind the steward of the next steps:
  1. Read the parables in each merged file
  2. For parables worth adopting, copy them into the section's `# Parable`
     block (add the heading if it doesn't exist yet — it goes between
     `# Spec` and `# Digest`)
  3. Edit for voice, tone, and fit with the section
  4. Add a Log entry to each section that gets a parable
  5. Run `make validate` to confirm
  6. Commit: `git commit -F reviews/[round]/COMMIT_MSG.txt`
