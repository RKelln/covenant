<!-- AGENT:NAV
purpose:outreach directory structure; replaces installations/ and docs/talks/; materials subfolder rationale
lines:68
nav[6]{s,n,name,about}:
13,56,#ADR 0007: Outreach Directory Structure,outreach/ top-level directory replacing installations/ and docs/talks/
15,4,##Status,accepted
19,13,##Context,why installations/ was too narrow; talks were misplaced in docs/; materials/ motivation
32,22,##Decision,outreach/ with installations/ talks/ materials/ grants/ subfolders
54,11,##Consequences,updated paths in Makefile; build-slides.py; README; ADR 0005; terminal plan
65,4,##Related,ADR 0001 repo structure; ADR 0004 file layout conventions
-->

# ADR 0007: Outreach Directory Structure

## Status

Accepted

## Context

The repository had two locations for outreach-related content:

- `installations/` — venue-specific exhibition proposals, grant applications, budgets, and mockups
- `docs/talks/` — Marp presentation source files

Both were growing and would grow further. New content categories were anticipated: standalone grant applications not tied to a specific installation, and canonical reference materials (artist statements, project descriptions, promotional copy) that individual applications draw from but do not stay linked to.

The `installations/` name was accurate for its original contents but too narrow to describe the full scope of external-facing project work. `docs/talks/` was technically a documentation subfolder but talks are outreach artifacts, not contributor documentation.

A trigger for this change: the need for a `materials/` subfolder to hold canonical copy — the upstream reference documents that get sampled into applications at a point in time, then evolve independently.

## Decision

Introduce a top-level `outreach/` directory with eight subfolders:

```
outreach/
  installations/    ← moved from installations/; venue exhibition proposals
  talks/            ← moved from docs/talks/; presentation decks
  materials/        ← canonical descriptions, artist statements, promo copy
  grants/           ← funding applications (e.g. Canada Council)
  residencies/      ← residency and fellowship applications (e.g. Banff Centre)
  press/            ← press releases, media kit, journalist outreach
  workshops/        ← workshop proposals and educational programs
  partnerships/     ← collaboration and co-producer proposals
```

`materials/` is the source library: authoritative, evolving. Applications copy from it and freeze at submission time. The originals continue to track the project independently.

The `grants/`–`residencies/` distinction: grants are primarily about money; residencies are about time and place to work. `installations/` covers venue proposals even when those include a grant component — the primary output is a physical exhibition.

`press/`, `workshops/`, and `partnerships/` are initially empty but established to avoid future ambiguity about where those materials belong.

## Consequences

- `installations/` top-level directory removed; content lives at `outreach/installations/`
- `docs/talks/` removed; content lives at `outreach/talks/`
- `Makefile` slide targets updated (`docs/talks/` → `outreach/talks/`)
- `build/build-slides.py` `TALK_DIR` constant updated
- `README.md` directory table updated
- `adr/0005-terminal-architecture.md` and `terminal/docs/plan.md` path references updated
- Historical references in `docs/releases.md` left unchanged (they describe past state)
- `AGENTMAP.md` index updated to reflect new paths

## Related

- ADR 0001 — core repository structure
- ADR 0004 — section file layout conventions
