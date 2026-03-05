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
