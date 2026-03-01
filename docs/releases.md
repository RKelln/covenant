# Releases

## Process

Releases are manual. When the steward considers the state coherent
enough to be cited (see [governance.md](governance.md#versioning)):

```bash
# 1. Ensure everything builds cleanly
make all

# 2. Tag the release
git tag -a v0.X.Y -m "vX.Y.Z — short description"
git push origin v0.X.Y

# 3. Create the GitHub release with PDF artifacts
gh release create v0.X.Y dist/*.pdf \
  --title "v0.X.Y — short description" \
  --notes "Release notes here."
```

PDFs are attached as release artifacts on GitHub — they are not
tracked in git (`dist/` is gitignored).

## Version History

### v0.1.0 — Initial public release

First public edition of the Covenant.

- 30 sections across 7 categories (preamble, definitions, rights,
  obligations, protocols, enforcement, closing)
- Three assemblies: ritual, spec, and full (hybrid)
- Three PDF editions (US Letter)
- Website at [covenant.website](https://covenant.website/)
- Three rounds of multi-model review (Claude, GPT, Gemini) completed
