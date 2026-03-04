---
description: Bump version, generate release notes from git history, rebuild all outputs, and walk the steward through tagging a release
---

You are preparing a new release of the Covenant. The full release process is
documented in `docs/releases.md`.

## Arguments

Arguments provided: $ARGUMENTS

Parse as: `[version] [description]`

- `$1` — the new version number (e.g. `0.2.0`). Required.
  Accepts with or without a `v` prefix — strip the `v` if present.
  Must be valid semver: `MAJOR.MINOR.PATCH`.
- `$2` — a short one-line description for the release title line
  (e.g. `"Post round-03 edits"`). Optional — if omitted, you will draft
  one as part of Step 3 and ask the steward to confirm.

Examples:
- `/release 0.2.0 "Post round-03 edits"`
- `/release v0.2.0`
- `/release 0.1.1 "Patch: fix enforcement cross-references"`

If no arguments are provided, read the current version from `pyproject.toml`
and ask the steward what the new version should be (suggest the next minor
bump as default).

---

## Step 1 — Read and display current version

Read `pyproject.toml` and extract the current `version = "..."` line.
Display it to the steward:

```
Current version: v{current}
New version:     v{new}
```

Validate that the new version is strictly greater than the current version
(compare as semver). If not, warn the steward and ask for confirmation
before proceeding.

## Step 2 — Gather git history since last release

Find the most recent git tag (the previous release). Run the following
commands in parallel to collect the raw material for release notes:

```bash
# Most recent tag
git describe --tags --abbrev=0

# Full commit log since that tag (one line per commit)
git log {prev_tag}..HEAD --oneline

# Detailed commit log with bodies for context
git log {prev_tag}..HEAD --format="### %s%n%n%b"

# Diff stat showing which files changed and by how much
git diff {prev_tag}..HEAD --stat

# Sections that were modified (to identify content changes)
git diff {prev_tag}..HEAD --name-only -- sections/

# Build tools and infrastructure that changed
git diff {prev_tag}..HEAD --name-only -- build/ Makefile .github/ schemas/

# Docs and website changes
git diff {prev_tag}..HEAD --name-only -- docs/ assets/
```

If there is no previous tag (first release), use the root commit as the
base: `git log --oneline` and `git diff --stat` for the full history.

## Step 3 — Draft release notes

Analyze the git history gathered in Step 2 and draft structured release
notes. Organize changes into the following categories (omit any category
with no changes):

```markdown
### v{new} — {description}

{1-2 sentence summary of what this release represents}

**Covenant text**
-   {changes to sections — new sections added, sections revised, review
    edits applied, etc. Name specific sections when possible.}

**Website & design**
-   {changes to the website, visual design, typography, assets}

**Build tools**
-   {changes to build scripts, PDF generation, validation, new commands}

**Documentation & governance**
-   {changes to governance docs, style guide, README, etc.}

**Infrastructure**
-   {CI, schemas, dependencies, repo structure}
```

Guidelines for drafting:
- Lead with content changes (covenant text) — that is what readers care about
- Be specific: name section IDs, tools, and features rather than vague
  summaries like "various improvements"
- Group related commits into single bullet points rather than listing
  every commit separately
- Use the commit messages as raw material but rewrite for clarity — commit
  messages are shorthand; release notes are for readers
- If a description was not provided as `$2`, draft a short title-line
  description from the overall theme of the changes (e.g.
  `"Website polish and watermark system"`)
- Match the style of existing entries in `docs/releases.md`

Present the full draft to the steward:

```
── Draft release notes ──────────────────────────

### v{new} — {description}

{drafted content}

──────────────────────────────────────────────────
```

Ask: **"Edit these notes or approve as-is?"**

Wait for the steward to respond. They may:
- **Approve** ("looks good", "approve", "ok") — use the draft as-is
- **Edit** — provide revised text or specific corrections. Apply their
  changes and show the updated version for confirmation.
- **Ask questions** — answer them, then re-present for approval.

Do not proceed to Step 4 until the steward has approved the release notes.

## Step 4 — Update pyproject.toml

Use the Edit tool to replace the version line in `pyproject.toml`:

```
version = "{old}"  →  version = "{new}"
```

Confirm the edit was applied. Do not touch any other lines.

## Step 5 — Validate and build

Run:

```bash
make build
```

If validation fails, stop and show the full error output. Do not proceed
until the steward fixes the errors and re-runs `/release`.

## Step 6 — Rebuild all outputs

Run the full build to regenerate PDFs and the website with the new version:

```bash
make all
```

If any step fails (PDF generation, website generation), report the error
and ask the steward how to proceed.

After success, verify the version appears in outputs by checking:
1. The first few lines of `dist/covenant.ritual.md` — should show `v{new}`
2. Grep `docs/index.html` for the version string — should show `v{new}`

Report what was built and confirm the version is correct in all outputs.

## Step 7 — Update releases.md

Read `docs/releases.md`. Append the steward-approved release notes at the
end of the file. The entry should follow the exact format used by existing
entries (see the v0.1.0 entry as a model).

## Step 8 — Save release notes for gh release

Write the release notes body (everything below the `### v{new}` heading,
without the heading itself) to a temporary file for use with `gh release`:

```
dist/RELEASE_NOTES.md
```

This file will be used in the `gh release create --notes-file` command.

## Step 9 — Show summary and next steps

Display a summary:

```
Release v{new} prepared.

Files modified:
  - pyproject.toml          (version bumped: {old} → {new})
  - docs/releases.md        (release notes appended)
  - docs/index.html         (regenerated with v{new})
  - dist/covenant.*.md      (regenerated with v{new})
  - dist/covenant.*.pdf     (regenerated with v{new})
  - dist/RELEASE_NOTES.md   (for gh release)

Next steps:

  # 1. Review changes
  git diff

  # 2. Stage and commit (git add -u covers pyproject.toml,
  #    docs/releases.md, and docs/index.html since all are tracked)
  git add -u
  git commit -m "Release v{new} — {description}"

  # 3. Tag and push
  git tag -a v{new} -m "v{new} — {description}"
  git push origin main && git push origin v{new}

  # 4. Create GitHub release with PDF artifacts
  gh release create v{new} dist/*.pdf \
    --title "v{new} — {description}" \
    --notes-file dist/RELEASE_NOTES.md
```

Ask the steward if they want you to run any of these steps, or if they
prefer to do them manually.
