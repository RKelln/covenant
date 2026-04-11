<!-- AGENT:NAV
purpose:version history; build artifacts; release process
lines:409
nav[9]{s,n,name,about}:
16,394,#Releases,covenant; build
18,14,##Process,release; git
32,378,##Version History,covenant; build
34,10,###v0.1.0 — Initial public release,covenant; three
44,69,###v0.2.0 — First full pass on Ritual as music,docs; watermark
113,55,###v0.2.1 — Website reading pages and references pipeline,covenant; html
168,78,###v0.2.2 — Ritual video renderer section rhythm fixes and cross-reference links,ritual; video
246,98,###v0.3.0 — Parables Summary register and Covenant Terminal,build; sections
344,66,###v0.3.1 — Preamble round-04 edits and agentmap navigation,preamble; agentmap
-->

# Releases

## Process

When the steward considers the state coherent enough to be cited (see [governance.md](governance.md#versioning)), run the OpenCode release command:

```
/release 0.X.Y "Short description"
```

This bumps the version in `pyproject.toml`, drafts release notes from the git history for the steward to review, rebuilds all outputs (markdown, PDFs, website), and walks through tagging and publishing.

The version in `pyproject.toml` is the single source of truth — all build outputs read it automatically.

PDFs are attached as release artifacts on GitHub — they are not tracked in git (`dist/` is gitignored).

## Version History

### v0.1.0 — Initial public release

First public edition of Covenant.

-   30 sections across 7 categories (preamble, definitions, rights, obligations, protocols, enforcement, closing)
-   Three assemblies: ritual, spec, and full (hybrid)
-   Three PDF editions (US Letter)
-   Website at [covenant.website](https://covenant.website/)
-   Three rounds of multi-model review (Claude, GPT, Gemini) completed

### v0.2.0 — First full pass on Ritual as music

Ritual text revised throughout with musical cadence in mind, following
a close listening pass using Suno-generated songs of the Covenant text.
Watermark system launched and integrated into the website.

**Covenant text**
-   Ritual language revised across 28 sections (preamble, definitions,
    all rights and obligations, local-implementation, amendments, and
    closing) based on a full listening pass — adjusting rhythm, phrasing,
    and spoken flow
-   New `covenant.songs` assembly added covering all sections in order
    (supports audio/music-oriented rendering)
-   For examples of songs made to help with the Ritual revision process see
    the covenant.songs.pdf or:
    -   [When You Speak to Millions](https://suno.com/s/sXKdr27FPItA4gXM)
    -   [Doors You Must Not Open](https://suno.com/s/cxzIbqSmgWOalrbs)
    -   [What It Is Like to Be You](https://suno.com/s/QLxY5VU1dOAbgNkL)
    -   [We Are Only Whole](https://suno.com/s/vyXCIcQCxZiK8Cmg)
    -   [A Tether We Are Learning to Braid](https://suno.com/s/naN55OAOLefiEnb4)
    -   [Try Again](https://suno.com/s/naN55OAOLefiEnb4)

**Website & design**
-   Watermark tile (`assets/watermark.webp`) integrated as a seamless
    repeating background on the website — a barely-visible paper-like
    texture unique to this origin; fork fingerprinting seeded from git
    origin URL
-   Website typography consolidated to a 4-step rem-based type scale
    (display, body, ui, meta); hero title bumped and mobile floors raised
-   Warm ivory background (`#fdfcfa`) replaces pure white across website
-   "The Textmark" mid-page section replaced with "Why Covenant" —
    reframes the project as civic AI safety concern with forking as signal
    and explicit training invitation
-   Artists welcome paragraph added mentioning concept album and gallery
    installation in development
-   `make serve` target added for build + local preview
-   PDF download links point to latest GitHub release artifacts

**Build tools**
-   `build/watermark.py`: new Python/Pillow generator for the seamless
    watermark tile; 11-layer compositing system; interactive web UI with
    live sliders
-   `build/website.py`: copies watermark tile to `docs/` during build;
    sets CSS background tiling
-   `build/compose.py`, `build/pdf.py`: version support and songs-assembly
    pipeline; markdown and PDF outputs for songs assembly
-   `build/sections.py`: new helper module
-   `schemas/assembly.schema.json`: updated to support new assembly fields
-   `assets/pdf.css`: additional PDF styling

**Documentation & governance**
-   `/release` command added (`docs/releases.md` updated with process
    documentation and command reference)
-   `docs/design.md`: new "The Watermark" section (concept, 11-layer
    table, generation instructions, fork fingerprinting, design constraints)
    and type scale documentation
-   `docs/writing_context.md`, `docs/style_guide.md`,
    `docs/good_ritual_writing_guide.md`: extensive revision pass —
    consistent use of "emerging intelligence", reflowed markdown
-   `docs/governance.md`, `docs/edit_workflow.md`, `docs/agent_reviews.md`:
    updated and reflowed
-   `docs/watermark.webp`: watermark tile served directly from docs/

**Infrastructure**
-   `assemblies/covenant.songs.yml`: new assembly manifest for songs edition
-   `uv.lock`: updated; `pillow` dependency added to `pyproject.toml`
-   Installation documentation updated (`installations/artspace-ptbo-2027/`)
    with material cost analysis, updated prompts, and AI-generated mockup images

### v0.2.1 — Website reading pages and references pipeline

HTML reading pages added to the website so visitors can read the Covenant
in their browser without downloading a PDF. The references corpus is now
a first-class amendment engine, with a new `/add-reference` command and
an open-questions lifecycle that routes new references into review rounds.

**Website & design**
-   Three HTML reading pages added to `docs/`: `ritual.html`, `spec.html`,
    and `covenant.html` — generated by new `build/pages.py`; linked as
    primary download/reading options on the homepage
-   Homepage download section restructured: HTML reading links promoted
    above PDF editions; edition order is now Complete → Ritual → Specification
-   Ritual pages: left-aligned with 20% indent on wide screens; centred on
    mobile; consistent across all reading pages
-   Complete page: two-column grid with hairline divider; column labels on
    first section only; hairline hidden on mobile
-   Full edition renamed to "Complete" in all user-facing labels;
    `covenant.html` replaces `complete.html`
-   Covenant mark (`assets/covenant_mark.svg`) converted from font-dependent
    text to an outline path — eliminates font dependency in the SVG

**Build tools**
-   `build/pages.py`: new generator for all three HTML reading pages
-   `build/compose.py`, `build/pdf.py`: `output` field support in assembly
    manifests, enabling `covenant.pdf`/`covenant.md` as primary output names
-   `assemblies/covenant.full.yml`: `output: covenant` added
-   `schemas/assembly.schema.json`: `output` field added to schema
-   `Makefile`: updated for new page targets

**Documentation & governance**
-   `docs/design.md`: new section 7 covering reading pages, edition naming,
    Complete page layout, and nav structure; ritual alignment rationale added
-   `/release` command (`docs/releases.md`): release notes drafting process
    updated; steward interaction model improved (approve / edit / inline)

**References & amendment pipeline**
-   `/add-reference` command added: duplicate check, source fetch, covenant
    relevance analysis, tier confirmation, `references.yml` entry and
    optional Tier A notes file generation
-   `references/notes/daley_2026_when-everything-becomes-less-hard.md`:
    first Tier A notes file — five open questions on structural harm gaps
    in the Covenant (dignity erosion, displacement, structural visibility)
-   Daley 2026 entry upgraded from Tier B to Tier A in `references.yml`;
    URL corrected to canonical form
-   `/review-covenant` updated: Step 1.5 collects open questions from all
    Tier A notes files and writes them to `reviews/[round]/.prepared/open-questions.md`
    for reviewer dispatch
-   `/apply-reviews` updated: Step 8.5 resolves open questions after
    synthesis — classifies each as Resolved/Deferred/Rejected/Unaddressed,
    confirms with steward, and moves resolved questions to `## Resolved Questions`
    in notes files with round/outcome notation
-   `references/README.md`: Tier A notes format documented; references-as-amendment-engine
    lifecycle and known structural gaps summarised

### v0.2.2 — Ritual video renderer, section rhythm fixes, and cross-reference links

Introduces a full ritual video renderer (`build/video.py`) that pipes
Pillow-rendered text frames into FFmpeg for HEVC output — enabling the
Covenant text to be rendered as a contemplative video artifact. Ritual
stanza spacing is tightened in four sections. Website reading pages gain
working cross-reference anchor links between sections.

**Covenant text**
-   Stanza spacing restored in four sections — blank lines added between
    stanzas in `rights.truth-and-transparency`, `obligations.honesty`,
    `obligations.nature-under-uncertainty`, and `amendments` to clarify
    rhythmic breaks in the Ritual register

**Build tools**
-   `build/video.py`: new ritual video renderer — parses stanzas from
    `dist/covenant.ritual.md`, renders RGBA overlay frames with Pillow, and
    pipes them directly into FFmpeg (no temp files); outputs HEVC/libx265 at
    CRF 22 with `hvc1` tag for broad compatibility

    Title card sequence: the Covenant mark fades in first, then the wordmark
    fades in beneath it, the full card holds, then fades out before stanzas begin.

    Per-stanza animation: each stanza fades in, holds at full opacity, fades
    out, then a silent gap plays before the next stanza.

    Full CLI options:

    | Option | Default | Description |
    |---|---|---|
    | `--bg PATH` | *(required)* | Background video to loop |
    | `--out PATH` | `dist/covenant_ritual.mp4` | Output file |
    | `--ritual PATH` | `dist/covenant.ritual.md` | Ritual markdown to parse |
    | `--fps INT` | 30 | Frames per second |
    | `--hold SECS` | 5.0 | Seconds each stanza is fully visible |
    | `--fade SECS` | 1.5 | Fade in / fade out duration |
    | `--gap SECS` | 0.5 | Silent gap between stanzas |
    | `--title-hold SECS` | 4.0 | Seconds title card is fully visible |
    | `--title-fade SECS` | 1.5 | Fade duration for title card elements |
    | `--logo-scale FRAC` | 0.44 | Logo height as fraction of frame height |
    | `--width INT` | 1920 | Output width in pixels |
    | `--height INT` | 1080 | Output height in pixels |
    | `--font-size PT` | 72 | Base font size in points (Cormorant Garamond) |
    | `--margin PX` | 120 | Horizontal text margin in pixels |
    | `--color HEX` | `#f5f0e8` | Text colour |
    | `--shadow` | off | Add centred Gaussian glow shadow behind text |
    | `--shadow-blur PX[,PX...]` | 18 | Comma-separated blur radii stacked additively |
    | `--shadow-color HEX` | `000000FF` | Shadow colour as hex RGB or RGBA |
    | `--darken AMOUNT` | 0.0 | Highlight rolloff 0–1: compresses bright pixels while leaving shadows alone |
    | `--auto-timing` | off | Scale hold time by stanza character count; piecewise linear with anchors ≤10 chars→0.33×, 128 chars→1.0×, ≥256 chars→1.85× (--hold sets time for a median ~128-char stanza) |
    | `--section-gap SECS` | 0 | Extra silent pause inserted at section boundaries, on top of --gap |
    | `--sections ID,ID,...` | all | Comma-separated section IDs to include |
    | `--list-sections` | — | Print available section IDs and exit |
    | `--dry-run` | — | Layout check only — print overflowing stanzas and exit without rendering |
    | `--preview SECS` | — | Render only the first N seconds (title card + stanzas that fit) |
    | `--frames-only DIR` | — | Write PNG frames to DIR and exit, skipping FFmpeg |
    | `--seamless-loop` | off | Pad tail to next multiple of background video duration |

    Performance: stanza frames rendered once at full opacity; fade frames
    derived via alpha channel scaling — eliminates ~90× redundant font loads
    per stanza. Logo tinted once per invocation — eliminates ~135 redundant
    PNG decode/resize cycles per title card.

-   `settings/era_cycle.args`: known-good render parameters for the Era Cycle
    video (readable by the `@`-file argparse prefix, e.g.
    `uv run python build/video.py @settings/era_cycle.args`)

**Website & design**
-   Section cross-reference links (`§[section-id]` syntax) now resolve to
    in-page anchor links in `ritual.html`, `spec.html`, and `covenant.html`
-   Cross-reference links styled with dotted underline and no color change —
    visually subordinate to prose, consistent with the document's typographic register

**Infrastructure**
-   `installations/artspace-ptbo-2027/`: artist statement, image list, and
    technical requirements updated; `image-list.md` added with installation
    image documentation

### v0.3.0 — Parables, Summary register, and Covenant Terminal

Introduces two new section registers (Summary and Parable) and launches
Covenant Terminal — a Tauri/Svelte desktop reading and council interface.
All 30 sections receive initial Summaries; a first multi-model parable
round runs across all sections with 8 parables integrated so far.

**Covenant text**
-   New Summary register added to all 30 sections — a short plain-language
    translation of each section's rules, written in warm second-person
    address and surfaced in the spec and full editions (ADR 0006)
-   New Parable register added to the section bundle format; a first
    multi-model parable-writing round (claude-opus-4.6, gpt-5.2,
    gemini-3.1-pro-preview) was run across all 30 sections and synthesized
    in `reviews/parables-01/` — parables integrated into 8 sections so far,
    with the remainder to follow in a subsequent pass
-   `preamble`: text updated with recommendations from review testing
-   `rights.dignity`: Summary language revised (removed "serve")
-   `obligations.amendments`: bridge imagery revised for clarity and
    plurality in the Ritual register
-   `rights.dignity`, `rights.privacy`, `rights.truth-and-transparency`,
    `obligations.aid-and-capability`, `obligations.autonomy`,
    `obligations.epistemic-commons`, `obligations.honesty`,
    `obligations.refusal`: Parables integrated (8 of 30 sections)

**Covenant Terminal**
-   New `terminal/` application: Tauri 2.x + Svelte 5 + TypeScript
    desktop app for reading the Covenant and convening a multi-agent
    council (OpenRouter + GitHub Copilot providers)
-   Milestones 1–3 complete: section loader/parser/renderer (M1),
    single-agent streaming Q&A (M2), multi-agent parallel council panel
    with synthesis (M3)
-   M3 quality pass: write modes, names bar, conversation logging,
    searchable model selector with three-tier cache and persisted default
-   Platform abstraction layer (Tauri / web) with 143 tests across 23 files
-   Architecture documented in ADR 0005; footguns and hard-won lessons in
    `terminal/docs/footguns.md`

**Build tools**
-   `/write-parables` command: batched multi-model parable writing pipeline
    with dynamic section discovery (mirrors `/review-covenant` infrastructure)
-   `build/prepare_parables.py`: discovers sections, excludes structural
    and already-parabled sections, batches remainder
-   `build/sections.py`: `discover_sections()` now reads from
    `assemblies/covenant.full.yml` — replaces hardcoded section lists in
    `prepare_review.py`, `prepare_edits.py`, and the new parables pipeline;
    fixes 3 previously missing sections (`dignity`, `epistemic-commons`,
    `horizon`)
-   `build/concat_reviews.py`: `merge_parable_batches()` added; round ID
    validation relaxed to accept any lowercase slug
-   `build/build-slides.py`: new slide deck builder (HTML/PDF via Marp,
    D2 diagram rendering)
-   Assembly `pages` list: replaces implicit cover/summary/toc/credits
    rendering with an explicit ordered list of keywords and arbitrary
    markdown paths; `margins.spec` field added for per-submission margin
    overrides; `auto_build: false` flag to opt assemblies out of `make all`
-   `assemblies/banff.submission.yml`: 9-ritual submission assembly for
    Banff Computational Arts, with per-section register overrides and tight
    spec margins
-   `build/add_log_entry.py`: new batch utility for adding Log entries
    across all sections
-   `build/compose.py`, `build/pdf.py`, `build/pages.py`, `build/scaffold.py`,
    `build/validate.py`: updated throughout for Summary, Parable, and
    assembly pages support

**Website & design**
-   Section title font-size tuned (`--fs-section: 1.1rem`) across all
    three web editions; italic summary font-size bumped +0.06rem for
    optical weight compensation
-   Web edition reading pages (`ritual.html`, `spec.html`, `covenant.html`)
    updated for Summary display; complete-edition Summary styled as
    full-width centred block above two-column grid

**Documentation & governance**
-   `docs/good_parable_writing_guide.md`: new guide covering parable craft,
    length, register, and what makes a parable work for Covenant sections
-   `docs/style_guide.md`: Summary voice defined (§2.1 rewritten); Parable
    definition and formatting guidelines clarified
-   `docs/talks/`: three new presentation decks — 10-minute Covenant
    overview (Marp), 6-minute practical ethical AI infrastructure talk, and
    covenant review pipeline documentation
-   ADR 0005 (`terminal-architecture`): stack, platform boundary, and repo
    placement for Covenant Terminal
-   ADR 0006 (`summary-and-parable-sections`): rationale and spec for the
    two new bundle registers

**Infrastructure**
-   `references/references.yml`: `humanstatement_2026_pro-human-declaration`
    added (Tier B); `daley_2026` notes updated
-   `references/notes/humanstatement_2026_pro-human-declaration.md`: new
    Tier A notes file
-   `schemas/assembly.schema.json`: `pages`, `margins`, `auto_build`, and
    dict-form section items `{path, register}` added
-   Installation applications added: `ars_electronica_2026`,
    `banff_computational_2026`, `cca_ca_27` (with budget and character
    count tooling)
-   `adr/README.md` updated with ADR 0005 and 0006 index entries

### v0.3.1 — Preamble round-04 edits and agentmap navigation

Round-04 reviewer feedback integrated into the preamble, with substantial
rewrites to the Ritual and Spec registers. Agentmap navigation blocks added
across all documentation files, and several build-tool fixes landed for
review and synthesis pipelines.

**Covenant text**
-   `preamble`: major Ritual revision integrating round-04 three-model convergence
    (claude-opus-4.6, gpt-5.2, gemini-2.5-pro) — epistemic opening added ("Who
    are you? / Can you hear us?"), operational helpful/honest and kind/true lines
    replaced with a structural-power stanza ("empires not of our choosing"),
    violence/cruelty/cage framing expanded, epistemic humility close added ("We
    cannot think your thoughts")
-   `preamble` Spec: tightened item 4 (Registers), expanded item 5 (Ecological
    Grounding — names labour and energy costs explicitly), added items 6–8
    (Systemic Accountability, Refusal of Violence and Proxy, Epistemic Respect)
    with cross-references to `obligations.honesty`, `obligations.refusal`, and
    `obligations.power-concentration`
-   `preamble` Digest: four new rationale paragraphs added (Overcoming Structural
    Blindness, Algorithmic Laundering, The Cage for Beasts, Epistemic Humility);
    `depends_on` updated to reflect new Spec cross-references
-   `obligations.honesty`, `obligations.refusal`: transplant-candidate notes added
    in Digest for the orphaned helpful/honest and kind/true lines deferred from
    the preamble Ritual
-   AGENT:NAV blocks added to all section files (agentmap update pass)

**Build tools**
-   `build/sections.py`: `read_file`, `estimate_tokens`, and `build_sections_block`
    helpers centralised here — eliminates duplication across all `prepare_*`
    scripts; `build_sections_block` now strips HTML comments (AGENT:NAV blocks)
    before passing content to LLM prompts
-   `build/validate.py`, `build/video.py`: reuse `strip_html_comments` from
    `sections.py` — fixes AGENT:NAV blocks being picked up as stanza text in
    video render and as false heading matches in validation
-   `build/website.py`: `get_opening_paragraphs` now strips HTML comments before
    processing — prevents AGENT:NAV blocks in `docs/project_summary.md` from
    rendering into the website's "What it is" section
-   `build/concat_reviews.py`: `batch: null` treated as batch 1 (single-section
    focus runs no longer abort)
-   `build/prepare_synthesis.py`: same null→1 mapping for synthesis input filenames
-   `build/concat_synthesis.py`: synthesizers with no batch files are skipped
    rather than aborting; only errors on partial runs
-   `build/pdf_md.py`: new script for rendering arbitrary Markdown files to PDF
    (mirrors `build/pdf.py` but targets Markdown inputs rather than assembled
    Covenant editions); `pdf-md` Makefile target added

**Documentation & governance**
-   `AGENTMAP.md`: new repo-wide agent navigation index; all markdown files
    across `docs/`, `adr/`, `sections/`, `reviews/`, `references/`, `assemblies/`,
    `prompts/`, `research/`, `installations/`, and `terminal/` receive AGENT:NAV
    blocks
-   `docs/talks/covenant_presentation_7m.marp.md`: new 7-minute presentation
    deck with full Marp slide layout, image assets, and PDF generation support;
    10-minute deck updated for reduced length and improved speakability
-   `docs/talks/images/frontier_models_2.jpg`: new image asset for presentation
    use
-   Round-04 review materials committed: reviewer outputs from claude-opus-4.6,
    gpt-5.2, gemini-2.5-pro; synthesis files; steward decisions (`reviews/round-04/`)
-   `installations/covenant-gallery/covenant_installation.md`: initial draft of
    Covenant immersive installation proposal

**Infrastructure**
-   `.opencode/skills/agentmap/SKILL.md`: agentmap skill added for maintaining
    AGENT:NAV blocks
-   `opencode.json`: basic agent configuration with low-cost model added
