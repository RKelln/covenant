# ADR 0002: Two-Register Architecture

## Status

Accepted

## Context

The Covenant needs to serve two audiences simultaneously:

1. People who will encounter it as spoken word, performance, or public
   reading — who need language they can inhabit and remember
2. People who will inspect, critique, or implement it — who need precise
   definitions, obligations, and enforcement paths

A single voice cannot serve both needs without compromising one.

## Decision

We use a "two-register" structure for every section:

- **Ritual Register:** Spoken, poetic, second-person address ("you"). Found
  under the `# Ritual` heading.
- **Spec Register:** Precise, normative (RFC 2119), third-person. Found under
  the `# Spec` heading.

Every section bundle includes both.

## Consequences

- Increased authorial burden (must write two versions of everything)
- Risk of semantic divergence between registers
- Better accessibility for different learning and use styles
- Clear separation of intent (Ritual) from implementation (Spec)
