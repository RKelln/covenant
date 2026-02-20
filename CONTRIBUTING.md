# Contributing to Covenant

Thank you for your interest in contributing to the Covenant.

## How to Contribute

All contributions happen through GitHub Pull Requests.

### Proposing a Text Change

1. Fork this repository
2. Create a branch for your change
3. Edit the relevant section `.md` file(s)
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
