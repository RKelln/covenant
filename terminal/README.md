<!-- AGENT:NAV
purpose:covenant terminal app; setup; running; directory structure
lines:152
nav[8]{s,n,name,about}:
15,138,#Covenant Terminal,tauri; dev
23,13,##What it is,fork; full
36,11,##Prerequisites,dev; windows
47,17,##Setup,env; api
64,28,##Running,tauri; apps
92,38,##Directory structure,platform; tauri
130,14,##Milestone status,complete; started
144,9,##Documentation,docs; agent
-->

# Covenant Terminal

A multi-agent reading and contribution interface for the Covenant — a Tauri 2.x desktop application built with Svelte 5, Vite, and TypeScript.

Visitors and contributors can read Covenant sections in any register (Ritual, Spec, or Complete), ask questions to a configurable council of AI models responding in parallel, propose and draft amendments, and — in gallery kiosk mode — commit amendments directly to a living fork of the document.

---

## What it is

The Terminal has two operating modes, selected by a configuration profile at startup:

| Mode | Context |
|---|---|
| **Contributor desktop** | Developer, steward, or fork maintainer. Full git integration, bring-your-own API keys, PR workflow. |
| **Installation kiosk** | Gallery deployment. Pre-configured, locked-down, visitor amendments committed immediately to a local fork and reflected in projected text. |

For the full design rationale — architecture, the multi-agent council model, the fork-as-living-document approach — see `docs/plan.md`.

---

## Prerequisites

- **Node.js** 20+ and npm 10+
- **Rust** 1.82+ (`rustup` recommended)
- **Tauri system dependencies:**
  - Linux: `libwebkit2gtk-4.1-dev`, `libjavascriptcoregtk-4.1-dev`, `libssl-dev`, `libgtk-3-dev`, `libayatana-appindicator3-dev`, `librsvg2-dev`
  - macOS: Xcode Command Line Tools
  - Windows: WebView2 (ships with Windows 11; installer available for Windows 10)

---

## Setup

```bash
# from terminal/
npm install
```

The `.env` file lives at the **repo root** (not `terminal/`). Copy `.env.example` to `.env` and add your OpenRouter API key:

```
OPENROUTER_API_KEY=sk-or-v1-...
```

It is available in the app as `import.meta.env.VITE_OPENROUTER_API_KEY`. Do not commit `.env` — it is in the root `.gitignore`.

---

## Running

```bash
# from terminal/

# Development (hot-reload, Tauri window)
npx @tauri-apps/cli tauri dev

# Development (faster cold start, no file-watching)
npx @tauri-apps/cli tauri dev --no-watch

# Run tests (watch mode)
npm test

# Run tests once
npm test -- --run

# Production build
npx @tauri-apps/cli tauri build
```

If icons are missing from `src-tauri/icons/`, generate them:
```bash
npx @tauri-apps/cli icon assets/icon.png
```

---

## Directory structure

```
terminal/
├── docs/
│   ├── plan.md             Full design plan — read this first
│   └── tasks.md            TDD task lists per milestone
│
├── src/
│   ├── main.ts             App bootstrap, platform detection
│   ├── App.svelte          Root component (view switching, layout)
│   │
│   ├── lib/                Pure TypeScript — no Svelte, no Tauri imports*
│   │   ├── platform.ts     Platform interface (the abstraction boundary)
│   │   ├── platform-tauri.ts   Tauri implementation (*only file allowed to import @tauri-apps/*)
│   │   ├── platform-web.ts     Web implementation (fetch, localStorage, shell stubs)
│   │   ├── agents/         AI provider adapters (OpenRouter, Copilot, direct)
│   │   ├── council/        Multi-agent dispatch + synthesis
│   │   ├── covenant/       Section parser, types, loader (pure TS, no platform dep)
│   │   ├── amendment/      Amendment drafting, validation, commit, moderation
│   │   ├── cost/           Material Cost Display ledger
│   │   └── config/         TerminalConfig types and loader
│   │
│   ├── components/         Svelte UI components — import from lib/ only
│   │   └── __tests__/      Component tests (vitest-browser-svelte)
│   │
│   ├── views/              Top-level view containers
│   └── styles/             CSS design tokens, typography, global reset
│
├── src-tauri/              Tauri Rust backend (minimal — most logic is frontend)
├── static/fonts/           Cormorant Garamond typeface files
└── AGENTS.md               Agent operating manual (TDD workflow, invariants, review protocol)
```

The key structural rule: **`src/lib/` is the boundary.** Everything in `lib/` is pure TypeScript or imports only from `platform.ts`. Components import from `lib/` only. This is what makes the Milestone 6 web deployment a thin SvelteKit wrapper rather than a rewrite.

---

## Milestone status

| Milestone | Status |
|---|---|
| M0 — Project scaffold | Complete |
| M1 — Readable document | Complete |
| M2 — Single-agent Q&A | Complete |
| M3 — Council panel | Complete |
| M4 — Amendment workflow | Not started |
| M5 — Kiosk mode | Not started |
| M6 — Web deployment | Not started |

---

## Documentation

| Document | Contents |
|---|---|
| `docs/plan.md` | Architecture, use cases, technology decisions, full milestone descriptions |
| `docs/tasks.md` | Red/green TDD task lists for each milestone |
| `AGENTS.md` | Agent operating manual — TDD workflow, invariants, pitfalls, review protocol |
| `docs/design.md` (repo root) | Visual language, typography, palette, § motif |
| `docs/agent_reviews.md` (repo root) | The existing review pipeline this Terminal extends |
