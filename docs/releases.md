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
