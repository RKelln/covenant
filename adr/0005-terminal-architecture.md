# ADR 0005: Terminal Architecture

## Status

Accepted

## Context

The Covenant needs a reading, Q&A, and contribution interface for two audiences:

1. **Gallery visitors** at the Artspace Peterborough 2027 exhibition (and future installations), interacting with the document at a kiosk
2. **Contributors and stewards** working with the document on their own machines

ADR 0001 noted that "web accessibility for non-technical readers requires a separate frontend (deferred to a later phase)." This ADR records the architectural decisions for that frontend.

Requirements:

- Must run as a desktop application on a gallery kiosk (Linux, macOS, or Windows)
- Must eventually run in a browser with no Tauri dependency
- Must support real-time multi-model AI responses (the council panel pattern already proven in the review pipeline)
- Must support the fork-as-living-document model: gallery visitors propose amendments, an automated moderation agent checks them, and approved changes are committed to a local fork and immediately reflected in the projected text
- Must invoke the existing `make validate` and `make compose` tooling for amendment workflows
- Must match the Covenant's visual design language (Cormorant Garamond, § motif, ivory/charcoal palette)

## Decision

### The Terminal lives inside the Covenant repo

The Terminal is built as `terminal/` at the repo root, not as a separate repository. It is part of the project — not a separate product. This gives it native access to section files, glossary, build tooling, and the existing review pipeline. The `terminal/` directory is self-contained: its own `package.json`, build config, and documentation.

### Stack: Tauri 2.x + Svelte 5 + Vite + TypeScript

- **Tauri 2.x** for the desktop shell: Rust backend, OS-native webview, small binary (~5-15 MB), cross-platform. Plugins for filesystem and shell access.
- **Svelte 5** for the UI: compiles to vanilla JS (no framework runtime shipped), reactive state for streaming responses, minimal dependency footprint.
- **Vite** as the bundler: Tauri's recommended frontend toolchain, fast dev server, fast builds.
- **TypeScript** throughout: type safety constrains what agents and contributors can get wrong.
- **Not SvelteKit** at this stage. SvelteKit adds file-based routing, SSR, and adapter conventions — most of which must be disabled for Tauri. It is deferred to Milestone 6 as a thin deployment wrapper for the web build.

### Platform abstraction layer

The single most important architectural decision for portability. All Tauri-specific operations (filesystem, shell, persistence) are isolated behind a `Platform` interface in `src/lib/platform.ts`. Two implementations exist:

- `platform-tauri.ts` — calls `@tauri-apps/plugin-fs`, `@tauri-apps/plugin-shell`
- `platform-web.ts` — fetches from GitHub API, uses localStorage, stubs shell operations

**No component or library module imports from `@tauri-apps/*` directly.** Only `platform-tauri.ts` touches Tauri APIs. This boundary enables the web deployment (Milestone 6) with zero component rewrites.

### SvelteKit migration path

All `.svelte` components and `src/lib/` modules are 100% SvelteKit-compatible. Web deployment requires only: install SvelteKit + `@sveltejs/adapter-static`, add `svelte.config.js`, move root component to `src/routes/+page.svelte`. Estimated migration: ~1 hour.

### AI provider abstraction

A thin `AgentProvider` interface with `chat(params): AsyncIterable<ChatChunk>` for streaming. Adapters for OpenRouter (default), GitHub Copilot, and direct provider APIs. The council dispatches the same query to N providers in parallel. This is the real-time, conversational counterpart to the batch review pipeline in `.opencode/commands/review-covenant.md`.

### Testing: Vitest + vitest-browser-svelte

- Unit tests (pure TypeScript logic): Vitest
- Component tests (Svelte): `vitest-browser-svelte` with Playwright browser mode
- Tauri IPC mocking: `@tauri-apps/api/mocks` + `mockIPC`
- Red/green TDD throughout — tests are written before implementation

### Two modes, one app

Installation kiosk and contributor desktop are distinguished by a configuration profile, not separate applications. A `terminal-config.json` file (in `installations/<venue>/`) controls the kiosk's council roster, moderation model, session timeout, and amendment workflow.

## Consequences

- The `terminal/` directory adds a Node.js + Rust toolchain requirement for contributors working on the Terminal (not for contributors working only on Covenant text)
- The platform abstraction is a hard constraint: every new platform-touching feature must go through `platform.ts`
- Tauri plugins must be explicitly registered in capabilities config — no ambient OS access
- The SvelteKit migration is trivial but must not be done prematurely (it adds complexity before it adds value)
- Gallery installations run on forks, not on `main` — fork management workflow must be specified before the first installation build
- The moderation agent is the most consequential single component — it mediates the public's relationship to a living document and must be designed and tested with corresponding care

## Related

- ADR 0001 — repo structure (this ADR fulfills the deferred frontend noted there)
- `terminal/docs/plan.md` — full design plan
- `terminal/docs/tasks.md` — TDD task lists for all milestones
- `docs/agent_reviews.md` — the batch review pipeline the Terminal extends into real-time
- `installations/artspace-ptbo-2027/` — the first installation context
