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
    | `--auto-timing` | off | Scale hold time with stanza line count using sqrt curve (sublinear) |
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
