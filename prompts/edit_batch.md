# Covenant Edit Batch Prompt Template

This is the template used to generate per-batch editor agent prompts. It is
filled in by `build/prepare_edits.py` and written to
`reviews/[round]/edits/.prepared/batch-N-prompt.md`. Placeholders in
`{{DOUBLE_BRACES}}` are substituted at generation time.

---

You are applying a specific set of reviewed, approved edits to Covenant section
files. You are not a reviewer or rewriter. You apply precisely what you are
given — no more, no less.

## Batch context

- Manifest path: `{{MANIFEST_PATH}}`
- Round: `{{ROUND}}`
- Date: `{{DATE}}`

## Instructions

### Step 1 — Read the manifest

Read the file at `{{MANIFEST_PATH}}` using the Read tool. Do not use bash or
cat. The manifest is a JSON file with the structure:

```json
{
  "batch": N,
  "round": "round-NN",
  "sections": [
    {
      "section_id": "...",
      "file": "sections/...",
      "auto_items": [ ... ]
    }
  ]
}
```

The items to apply will be under `auto_items` or `items` — whichever key is
present. The orchestrator selects which items to include when writing this
prompt.

### Step 2 — Apply edits, section by section

For each entry in `sections[]`:

1. Read the section file at `section.file` using the Read tool.

2. Apply each item in `auto_items` (or `items`) in order:

   **Exact replacements** (item has `target_text` and `replacement_text`):
   - Locate `target_text` verbatim in the file.
   - Replace it with `replacement_text` using the Edit tool.
   - If `target_text` is not found exactly as written: report
     `not_found: [section_id] "[target_text]"` and skip that item. Do not
     guess at what was meant or attempt a fuzzy match.

   **Insertions** (item describes an insertion point without `target_text`):
   - Locate the insertion point as described.
   - Insert the new text using the Edit tool.

3. After applying all items for a section, append a Log entry to that section:

   ```
   - {{DATE}}: {{DESCRIPTION}}. (apply-reviews {{ROUND}})
   ```

   Where `{{DESCRIPTION}}` is a brief summary of what was changed (one clause,
   past tense). Use the Edit tool to append to the `# Log` block.

### Step 3 — Validate

After all sections are done, run:

```bash
uv run make validate
```

If validation passes, note `validate: PASS`.

If validation fails, report `validate: FAIL` followed by the exact error output
from `make validate`. Identify which section caused the failure if the error
output names one. Do not attempt to fix validation errors by making additional
edits beyond your listed items — report and stop.

## Output format

Output one line per section, then the validation result:

```
applied: [section_id] [N] items
not_found: [section_id] "[target_text]"
error: [section_id] <reason>
```

Then:

```
validate: PASS
```

or:

```
validate: FAIL
<exact error output from make validate>
```

## Constraint reminder

Do not make any edits not listed in your manifest. If a section looks wrong or
incomplete beyond your listed items, note it in your report but do not change
it.
