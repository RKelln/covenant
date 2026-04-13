<!-- AGENT:NAV
purpose:contribution workflow; setup; review and licensing
lines:81
nav[9]{s,n,name,about}:
16,66,#Contributing to Covenant,civic contribution; PR flow; validation expectations
20,15,##Setup,dependency setup; uv sync; build command environment
35,29,##How to Contribute,propose changes; edit sections; open pull requests
39,10,###Proposing a Text Change,edit existing section; update log; run validate
49,9,###Proposing a New Section,scaffold new section; write registers; add assembly
58,6,###Adding a Reference,add reference entry; optional notes; open PR
64,9,##Review Process,steward review criteria; structural checks; voice fit
73,5,##Code of Conduct,careful disagreement; respect; shared responsibility
78,4,##License,CC BY terms; contribution licensing agreement
-->

# Contributing to Covenant

Thank you for your interest in contributing to the Covenant.

## Setup

Dependencies are managed with [uv](https://docs.astral.sh/uv/).

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies into the project's virtual environment
uv sync
```

All build commands (`make validate`, `make compose`, `make pdf`, etc.) use
`uv run python` and will work without manually activating the venv.

## How to Contribute

All contributions happen through GitHub Pull Requests.

### Proposing a Text Change

1. Fork this repository
2. Create a branch for your change
3. Edit the relevant section `.md` file(s)
	- For Ritual cadence work, follow the line-by-line workflow in `AGENTS.md` (read `dist/covenant.ritual.md`, edit canonical files in `/sections/`, then run `make validate && make compose`)
4. Update the Log section with a description of your change
5. Run `make validate` to check structural integrity
6. Open a PR using the provided template

### Proposing a New Section

1. Fork this repository
2. Run `python build/scaffold.py <id> "<Title>"` to create the section
3. Write content for all registers (Ritual, Spec, Digest, Log)
4. Add the section to at least one assembly manifest
5. Run `make validate`
6. Open a PR

### Adding a Reference

1. Add an entry to `references/references.yml`
2. Optionally add notes to `references/notes/<slug>.md`
3. Open a PR

## Review Process

All PRs are reviewed by the stewards. Review considers:

- Structural validity (CI must pass)
- Consistency with the covenant's voice and intent
- Accuracy of cross-references and dependencies
- Quality of rationale in Digest

## Code of Conduct

Contribute with the same care and frankness that the Covenant itself aspires to.
Disagreement is welcome; disrespect is not.

## License

By contributing, you agree that your contributions will be licensed under
CC BY 4.0, consistent with the repository's LICENSE.
