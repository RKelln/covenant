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
