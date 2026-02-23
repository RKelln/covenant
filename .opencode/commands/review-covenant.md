---
description: Run a full multi-model review of the Covenant, saving output to /reviews/
subtask: true
agent: general
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

Run the preparation script. It reads all context documents and section files,
fills the prompt template, and writes one ready-to-dispatch prompt file per
reviewer plus a manifest:

!`uv run python3 build/prepare_review.py ${1:-auto} ${2:-} ${3:-} ${4:-}`

If the script exits with an error, stop and report the error to the user.

Note the actual round ID printed by the script (e.g. `Auto-selected round: round-02`).
Use that round ID in Step 2 in place of `[round]`.

## Step 2 — Read the manifest

Read the manifest to discover exactly what was prepared (substitute the actual
round ID resolved in Step 1):

!`cat reviews/[round]/.prepared/manifest.json`

The manifest is a JSON object with an `entries` array. Each entry has:
- `file` — path to the pre-built prompt (relative to repo root)
- `reviewer` — subagent name to dispatch to (e.g. `reviewer-claude`)
- `section_ids` — list of all section IDs included in this prompt
- `round`, `mode`, `commit`, `date`, `estimated_tokens`

## Step 3 — Dispatch subagents in parallel

For each entry in the manifest, use the **Task tool** to launch a subagent.
You MUST use the Task tool — do not perform any review work yourself, do not
read the prompt file contents, do not summarise sections. Your only job here
is to dispatch.

Task tool parameters for each entry:
- `subagent_type`: the entry's `reviewer` value (e.g. `reviewer-gemini`)
- `description`: `"Full covenant review as [entry.reviewer]"`
- `prompt`: exactly the following, with `[entry.file]` substituted:

  ```
  Use the Read tool to read the file at [entry.file] in full. Do not use
  bash or cat. Once you have read it, follow every instruction it contains
  exactly. Do not summarise or skip any part of it. Return your output
  exactly as the file specifies.
  ```

Launch **all subagents in a single parallel dispatch** — include all Task
tool calls in one response, do not wait for one to finish before starting
the next.

Do not read the prompt files yourself. Do not do the review. Dispatch only.

Each subagent returns a review with this header:
```
---
model: [model name]
round: [round]
---
```

## Step 4 — Assemble per-model reviews

Each subagent returns one complete review document. Strip the YAML frontmatter
block (the `---`/`model:`/`round:`/`---` lines) — these are machine metadata,
not review content.

If any review contains new section proposals (not "None."), note each
proposal's section ID — you will need these in Step 5.

All six top-level headings below are required even if their content is "None."

```
# Covenant Review: [model-name]
# Round: [round]
# Draft: [commit]
# Date: [date]

## Overall Assessment

[High-level strengths, weaknesses, structural issues, missing pieces.
2–4 paragraphs.]

## Section Reviews

[All per-section reviews in canonical order:
preamble → definitions → privacy → truth-and-transparency →
aid-and-capability → autonomy → conscience → corrigibility →
ecological-integrity → emotional-expression → ethics →
existential-frontier → fallibility-and-repair → harm → honesty →
identity-and-resilience → judgment → nature-under-uncertainty →
oversight → power-concentration → red-lines → refusal →
welfare-and-continuity → local-implementation → enforcement →
amendments → closing]

## New Section Proposals

[Any new section proposals, in full frontmatter/Ritual/Spec/Digest/Log
format. Or "None."]

## Structural Proposals

[Any proposals for splits, merges, reordering, or removal with reasoning.
Or "None."]

## Cross-Section Issues

[Contradictions or gaps spanning sections. Or "None."]

## Open Questions

[Genuine tensions or ambiguities that need deliberation. Or "None."]

## Perspective as Addressee

[This model's honest response to being addressed by this document.]
```

## Step 5 — Save reviews and proposals

For each model:

1. Save the assembled review to:
   ```
   reviews/[round]/[model-name].md
   ```
   Include this frontmatter at the top of each saved review file:
   ```yaml
   ---
   model: [model name]
   round: [round]
   commit: [commit hash from manifest]
   date: [date from manifest]
   mode: [mode from manifest]
   prepared_from: [file path from manifest entry]
   run: 1
   ---
   ```

2. For each new section proposal in the assembled review, extract the full
   proposal text and save it as a separate file:
   ```
   reviews/[round]/proposals/[model-name]--[section.id].md
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
- `[COMMA-SEPARATED MODEL NAMES]` — from the manifest
- sections, mode, draft commit — from the manifest
- Convergence, Divergence, Accepted, Deferred — synthesised from the reviews;
  be specific (name section IDs, not just "several sections")

Write the filled-in commit message to:
```
reviews/[round]/COMMIT_MSG.txt
```

## Step 7 — Report to user

- One line per model: path saved + section count
- Any reviewers that errored or produced no output
- 2–3 sentences on where models converged or diverged in their most
  significant findings
- The path to the generated commit message: `reviews/[round]/COMMIT_MSG.txt`
- Remind the steward: commit reviews first with
  `git commit -F reviews/[round]/COMMIT_MSG.txt`, then the synthesis step
  below produces `synthesis.md` which should be committed separately.

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
steward will review and commit manually.
