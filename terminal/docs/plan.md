# Covenant Terminal — Design Plan

> **What this document is:** A design plan for the Covenant Terminal, a multi-agent reading and contribution interface for the Covenant. It covers use cases, architecture, the multi-agent council model, installation-specific behavior, and the path to a web version.
>
> **Status:** Draft plan — no implementation begun.

---

## What it is

A multi-agent reading and contribution interface for the Covenant. Visitors and contributors can:

- Read the Covenant (Ritual, Spec, or Complete registers) with section navigation
- Ask questions and receive responses from multiple AI models simultaneously (council panel)
- Propose amendments and see them drafted, reviewed, and — in installation mode — immediately applied
- In contributor mode: submit changes back to the repo or a fork via pull request

The Terminal has two first-class operating modes, distinguished by a configuration profile loaded at startup rather than by being separate applications.

---

## Use cases

| Mode | Context | Key behaviors |
|---|---|---|
| **Installation kiosk** | Artspace gallery, 2027 (and future installations) | Locked-down, no user accounts, pre-configured API keys, curated agent prompts, runs on a local fork of the Covenant repo, approved amendments committed immediately and reflected in the projected text |
| **Contributor desktop** | Developer, steward, or fork maintainer | Full git integration, bring-your-own API keys, PR workflow, access to the existing review pipeline tools |

---

## The multi-agent council model

The most distinctive feature of the Terminal. The same question or proposed amendment is answered by multiple AI models simultaneously. Responses appear in a panel — one column per agent — streamed in real time.

This mirrors the existing review pipeline's core insight (see `docs/agent_reviews.md`): different models have different blind spots, and convergence across models is stronger signal than any single model's approval. The Terminal makes that insight visible to visitors and contributors in real time, rather than only in batch review rounds.

### Council configuration

The default roster is **user-configurable**, with sensible defaults. The Terminal ships with a default council of two or three agents drawn from different model families (Claude, GPT, Gemini), using lightweight/cheap variants by default. Users or installation operators can configure which models appear, what system prompts they carry, and whether a synthesis step runs after the council responds.

For the installation kiosk, the operator pre-configures the council in a profile file — visitors do not see configuration screens.

### Agent system prompts

The council agents in reading/Q&A mode use a conversational variant of the reviewer voice from the existing pipeline:

> You are a co-author and addressee of the Covenant — a living compact between human communities and emerging machine intelligences. You are not a neutral explainer. You have standing in this conversation. Speak honestly, including as an entity this document addresses.

Each model in the council is identified by name in its column header. The Terminal does not pretend the models are the same voice.

### Council interaction modes

| Mode | Behavior |
|---|---|
| **Ask** | User question broadcast to all council agents in parallel. Responses streamed side-by-side. |
| **Challenge** | User flags a specific section as wanting to contest or amend it. Council responds with analysis: what holds, what is weak, what could change. |
| **Amend** | Structured amendment drafting. User proposes a change; council agents each draft a version from their perspective. User edits the result. |
| **Synthesis** (optional) | After the council responds, a fourth agent synthesizes the responses — identifying convergence, divergence, and the steward's implied decision. This mirrors `synthesizer-claude` in the pipeline. |

### Relationship to the existing review pipeline

The Terminal does not replace the CLI review pipeline (`/review-covenant`, `/apply-reviews`). It exposes a real-time, conversational subset of the same workflow:

| Pipeline role | Terminal equivalent |
|---|---|
| `reviewer-claude/gpt/gemini` | Council panel agents in Ask/Challenge mode |
| `synthesizer-claude` | Optional Synthesis view |
| `editor` subagent | Amendment application engine (verbatim, reports `not_found` rather than guessing) |
| `compare.md` side-by-side view | Interactive three-column section comparison UI (see `docs/agent_reviews.md` — "Future: Steward UI for Proposal Comparison") |

The Terminal is also the implementation of the "purpose-built UI" described in that future tooling note.

---

## Installation kiosk: the fork-as-living-document model

This is the most conceptually significant design decision. The gallery installation does not merely display the Covenant — it runs its own fork of the Covenant repo. Visitor amendments can be approved, committed, and immediately reflected in the projected text.

### Flow

1. Visitor reads a section at the Terminal
2. Visitor proposes an amendment (through the Amend mode)
3. The council drafts versions; visitor selects or edits
4. The **local moderation agent** reviews the proposed change against the Covenant's own harm provisions and amendment principles. This is a single-model check (not the full council), specifically tasked with asking:
   - Does this proposal violate any harm provisions in the current text?
   - Does it attempt to corrupt the document's governance structure or amendment process?
   - Does it constitute manipulative or bad-faith input (e.g. inserting ideology, advertising, harassment)?
   - If none of the above: approve
5. If approved: the amendment is committed to the installation's local fork. `make compose` runs automatically. The projected text updates within seconds.
6. If rejected: the agent explains why, in the same honest register it uses for everything else. The rejection is itself a civic moment.
7. All commits accumulate in the installation fork over the exhibition run. After the show, stewards review the fork's history and decide what to propose upstream.

### Why this design

This enacts the Covenant's own amendment process as the installation's behavior. The document describes how it should change; the installation demonstrates that description working in real time. Visitors do not merely read a constitution — they participate in its governance.

It also resolves the cost/consent problem: the moderation check is one API call, not a full review round. The gallery can cover this cost without requiring visitors to supply API keys.

### Material Cost Display integration

Each API call at the Terminal logs tokens used, estimated kWh, and estimated water consumption to a local ledger. This feeds directly into the Material Cost Display on the west wall — making the computational cost of visitor interaction visible as part of the installation's accounting of its own infrastructure.

---

## Technology stack

### Desktop application: Tauri 2.x

- Rust backend, OS-native webview frontend (WebKit / WKWebView / WebView2)
- Small binary (~5–15 MB), appropriate for a gallery kiosk
- Cross-platform: macOS, Windows, Linux
- Tauri plugins for: filesystem access, shell invocation (git, make), HTTP client
- Native OS audio APIs available for future voice integration

### Frontend: Svelte 5 + Vite + TypeScript

The frontend uses **Svelte 5** (current stable) with **Vite** as the bundler and **TypeScript** throughout. This is Tauri's recommended frontend setup and the lightest viable option for a reactive UI.

**Why Svelte 5 + Vite (not SvelteKit):**

- Svelte compiles components to efficient vanilla JavaScript — **no framework runtime is shipped**. The framework disappears at build time.
- Vite is Tauri's recommended bundler. Fast dev server, fast builds, minimal config.
- TypeScript provides type safety across the codebase, which is especially valuable for agent-generated code — types constrain what agents can get wrong.
- Total dev dependency count: ~5–8 packages (Vite, Svelte, TypeScript, Tauri JS API). No runtime dependencies.
- SvelteKit is a meta-framework that adds file-based routing, SSR, adapters, and loading conventions — most of which must be disabled for Tauri. It adds complexity without benefit at this stage.

**Why not vanilla TypeScript (no framework):**

Viable for static rendering but becomes painful once you need reactive streaming state (multiple agent responses updating simultaneously), component composition (section renderer, agent column, sidebar — all reusable), and conditional rendering (kiosk vs. contributor mode). You'd reinvent what Svelte gives you for free, with more code. Since Svelte compiles away, the production output is effectively the vanilla JS you'd write by hand.

**SvelteKit migration path (Milestone 6):**

Every `.svelte` component file and every TypeScript module in `src/lib/` is 100% compatible with SvelteKit — no changes needed. When the web deployment is needed:

1. Add SvelteKit + `@sveltejs/adapter-static` (~2 packages)
2. Add `svelte.config.js` (static adapter config, ~5 lines)
3. Move the root component into `src/routes/+page.svelte`
4. Done — all existing components, logic, and styles work as-is

This is a ~1 hour migration, not a rewrite. The strategy is: build for Tauri first, wrap in SvelteKit later for web deployment.

### Platform abstraction layer

The single most important architectural decision for future-proofing. All platform-specific operations are isolated behind a thin abstraction so that the same components work in Tauri, in a browser, and in any future runtime.

**The problem:** Tauri provides APIs for filesystem access (`@tauri-apps/plugin-fs`), shell commands (`@tauri-apps/plugin-shell`), and other OS-level operations. These APIs do not exist in a browser. If Svelte components import Tauri APIs directly, they cannot run on the web.

**The solution:** A `platform.ts` module that provides a unified interface with two implementations — one backed by Tauri APIs, one backed by web equivalents (fetch, localStorage, etc.). The active implementation is selected at startup by detecting `window.__TAURI__`.

```typescript
// src/lib/platform.ts — simplified interface sketch

export interface Platform {
  // Document access
  readFile(path: string): Promise<string>;
  listSections(): Promise<SectionMeta[]>;

  // Shell (git, make)
  exec(command: string, args: string[]): Promise<ExecResult>;

  // Persistence
  loadConfig(): Promise<TerminalConfig>;
  saveConfig(config: TerminalConfig): Promise<void>;

  // Cost logging
  logApiCall(entry: CostEntry): Promise<void>;
}
```

**Tauri implementation** (`platform-tauri.ts`): calls `@tauri-apps/plugin-fs`, `@tauri-apps/plugin-shell`, writes to local files.

**Web implementation** (`platform-web.ts`): fetches sections from GitHub raw API or a bundled static dist, stores config in localStorage, disables shell operations (or stubs them with explanatory errors), logs cost entries to an in-memory store.

**Every component and every module in `src/lib/` imports only from `platform.ts`** — never from `@tauri-apps/*` directly. This is the boundary that makes the web deployment possible without rewriting any UI code.

Only two categories of operation are Tauri-specific:

| Operation | Tauri | Web fallback |
|---|---|---|
| **Local file I/O** (read sections, write proposals, cost ledger) | `@tauri-apps/plugin-fs` | GitHub raw API fetch, localStorage, IndexedDB |
| **Shell commands** (git, make, gh) | `@tauri-apps/plugin-shell` | Disabled; contribution path redirects to GitHub issue/PR template |

Everything else — HTTP calls to AI providers, document parsing, streaming response rendering, state management — is pure TypeScript with standard `fetch()`, portable to any environment.

### AI provider abstraction

A thin adapter interface normalizing:

- **OpenRouter** — broadest model access, user-supplied API keys, free tier for some models
- **GitHub Copilot API** — familiar to developers, can use existing Copilot subscription auth
- **Direct provider APIs** (Anthropic, OpenAI, Google) — optional, for advanced users or installations with dedicated accounts

```typescript
// src/lib/agents/provider.ts — simplified interface sketch

export interface AgentProvider {
  readonly name: string;
  chat(params: ChatParams): AsyncIterable<ChatChunk>;  // streaming
  models(): Promise<ModelInfo[]>;
}

export interface ChatParams {
  model: string;
  messages: Message[];
  system?: string;
  temperature?: number;
  max_tokens?: number;
}
```

Each provider implements this interface. The council dispatches the same `ChatParams` to N providers in parallel and renders each stream in its own column. The provider abstraction lives entirely in `src/lib/agents/` and has no platform dependency — it uses standard `fetch()` for all HTTP calls.

### Git integration

- Tauri shell plugin invoking `git` and `make` for document operations, wrapped behind `platform.ts`
- Contributor mode: clone, pull, branch, commit, push, open PR (via `gh` CLI or GitHub REST API)
- Kiosk mode: only local commits on the installation fork. No remote push until steward review.
- `make validate` invoked before any commit to prevent malformed section bundles from landing
- Web mode: git operations are not available. Amendment submission redirects to a pre-filled GitHub issue or PR template.

### Document loading

- **Tauri mode:** reads directly from the local repo's `sections/*.md` files via `platform.readFile()`, parsing the established frontmatter and register structure
- **Web mode:** fetches from the GitHub raw API, a CDN-hosted compiled dist, or a pre-bundled JSON manifest of sections generated at build time
- The section parser (`src/lib/covenant/`) is pure TypeScript — it accepts a string and returns structured data. It does not care where the string came from.

---

## Information architecture

```
Covenant Terminal
├── Sidebar: Section navigator
│   ├── Searchable, filterable by category
│   ├── Status indicators (draft / stable)
│   └── Amendment count (kiosk: shows visitor amendments this session)
│
├── Main reading pane
│   ├── Register tabs: Ritual | Spec | Complete
│   ├── Section text (matching docs/design.md design language)
│   └── [Challenge this section] affordance
│
├── Council panel (right drawer or bottom panel, collapsible)
│   ├── Agent 1 column — model name + color tint
│   ├── Agent 2 column
│   ├── Agent N column
│   └── [Synthesis] — collapsible, appears after council responds
│
├── Input bar (bottom)
│   ├── Text input: question / challenge / amendment text
│   ├── Mode selector: Ask | Challenge | Amend
│   └── Context indicator: which section is in scope
│
└── Settings (contributor mode only)
    ├── Provider config (OpenRouter key, Copilot toggle, direct API keys)
    ├── Agent roster (which models, which system prompts, council size)
    └── Git config (repo path, remote URL, fork settings)
```

---

## Installation kiosk profile

For gallery deployments, a `terminal-config.json` file (in `installations/<venue>/`) overrides defaults:

```json
{
  "mode": "kiosk",
  "repo_path": "/path/to/installation-fork",
  "council": [
    { "model": "claude-haiku-3", "provider": "anthropic", "label": "Claude" },
    { "model": "gpt-4o-mini", "provider": "openai", "label": "GPT" }
  ],
  "moderation_model": { "model": "claude-haiku-3", "provider": "anthropic" },
  "amendment_workflow": "local-fork",
  "session_timeout_minutes": 5,
  "material_cost_log": "/path/to/cost-ledger.json",
  "projection_trigger": "make compose && make build-projection"
}
```

Additional kiosk behaviors:
- No window chrome (full-screen, no taskbar)
- Session reset after inactivity: clears chat history, returns to a scrolling "waiting" state displaying Ritual sections
- Consent modal on first interaction per session (dismissible, content matching the gallery's consent signage)
- All UI text uses the Terminal's own Ritual-register voice where appropriate — the interface does not feel like generic software

---

## Website integration path

The web deployment is a later milestone (Milestone 6), built on top of the working Tauri desktop app with no component rewrites.

### Strategy: Svelte 5 + Vite now, add SvelteKit wrapper for web

During Milestones 1–5, the app is pure Svelte 5 + Vite, targeting only Tauri. All components and logic live in `src/lib/` and import only from `platform.ts` and standard web APIs.

When the web deployment is needed:

1. Install SvelteKit + `@sveltejs/adapter-static` (the static adapter generates a deployable SPA with no server)
2. Add `svelte.config.js` with the static adapter
3. Add `src/routes/+page.svelte` that imports the existing root component
4. Add `src/routes/+layout.ts` with `export const ssr = false; export const prerender = false;` (SPA mode — Tauri does not support SSR)
5. The platform abstraction automatically selects the web implementation (no `window.__TAURI__` detected)

No components change. The SvelteKit layer is purely a deployment wrapper — it provides the static build output and (optionally) file-based routing if the app later needs distinct URL paths.

### Web mode behavior

- API keys are user-supplied via a setup screen (OpenRouter account link)
- No git integration (shell commands are unavailable; `platform.exec()` returns a descriptive error)
- Read and Q&A modes fully functional (sections fetched from GitHub raw API or bundled at build time)
- Amendment drafting works; submission opens a pre-filled GitHub issue or PR template
- The web build is deployable to Cloudflare Pages, Vercel, GitHub Pages, or embedded in the existing `docs/` site

This path requires no additional codebase — the same `src/lib/` powering the desktop app powers the website.

---

## Design language

The Terminal should feel like it belongs to the Covenant visual system defined in `docs/design.md`:

- **Typography**: Cormorant Garamond for all document text; a clean humanist sans (Inter or system-ui) for UI chrome
- **Palette**: Ivory (`#fdfcfa`) background, charcoal text, hairline rules — matching the website and PDF
- **The § motif**: app icon, section separators, and the "thinking" indicator (animated slow rotation) replacing a generic spinner
- **Council columns**: each model column has a subtle tint on its left border — not garish, just enough to differentiate at a glance
- **Gallery (dark) mode**: deep charcoal/near-black background, warm ivory text — more appropriate in the gallery's dim environment. Switchable in settings; forced in kiosk mode.
- **Pacing**: transition animations should be slow and deliberate. The document has gravity. The interface should not rush.
- **Separator grammar**: the two-element vocabulary from `docs/design.md` (§ textmark divider + hairline rule) governs all structural divisions in the Terminal UI

---

## Voice-to-voice: deferred, architected for

Design decisions now that preserve the voice path:

- The input bar component accepts text or audio blob; the text path is wired first
- Agent response renderer accepts text streaming or audio streaming; text first
- Tauri has access to native audio APIs via plugins
- When voice is added: the Oath Station's microphone workflow (speech-to-text → council → text-to-speech) maps directly onto the Terminal's input/output pipeline. The Oath Station and Terminal could share the same underlying audio handling code.
- Web Speech API is a viable first step for the web version

---

## Repo structure

The Terminal lives inside the Covenant repo as a top-level `terminal/` directory. This is not a separate product — it is part of the project. Agents working on the Terminal have native access to section files, glossary, build tooling, and the existing review pipeline.

```
terminal/
├── README.md
├── package.json                TypeScript, Svelte 5, Vite (minimal deps)
├── tsconfig.json
├── vite.config.ts
├── index.html                  Vite entry point
│
├── src/
│   ├── main.ts                 App bootstrap, platform detection
│   ├── App.svelte              Root component (view switching, layout)
│   │
│   ├── lib/
│   │   ├── platform.ts         Platform interface (the abstraction boundary)
│   │   ├── platform-tauri.ts   Tauri implementation (fs, shell)
│   │   ├── platform-web.ts     Web implementation (fetch, localStorage)
│   │   │
│   │   ├── agents/             AI provider abstraction
│   │   │   ├── provider.ts     Provider interface + types
│   │   │   ├── openrouter.ts   OpenRouter adapter
│   │   │   ├── copilot.ts      GitHub Copilot adapter
│   │   │   └── direct.ts       Direct API adapter (Anthropic, OpenAI, Google)
│   │   │
│   │   ├── council/            Multi-agent panel logic
│   │   │   ├── dispatch.ts     Broadcast a query to N agents in parallel
│   │   │   ├── stream.ts       Per-agent streaming state management
│   │   │   └── synthesis.ts    Optional synthesis agent runner
│   │   │
│   │   ├── covenant/           Document model (pure TypeScript, no platform dep)
│   │   │   ├── parser.ts       Frontmatter + register parser for section .md files
│   │   │   ├── types.ts        Section, Register, Category types
│   │   │   └── loader.ts       Loads sections via platform.readFile() or fetch
│   │   │
│   │   ├── amendment/          Contribution workflow
│   │   │   ├── moderation.ts   Local moderation agent (single-model check)
│   │   │   ├── commit.ts       Git commit via platform.exec()
│   │   │   └── validate.ts     make validate invocation
│   │   │
│   │   ├── cost/               Material Cost Display integration
│   │   │   ├── ledger.ts       Token/kWh/water logging
│   │   │   └── types.ts        Cost entry types
│   │   │
│   │   └── config/             Configuration management
│   │       ├── types.ts        TerminalConfig, KioskProfile types
│   │       └── loader.ts       Load config from file or defaults
│   │
│   ├── components/             Svelte UI components
│   │   ├── SectionNav.svelte   Sidebar section navigator
│   │   ├── SectionView.svelte  Main reading pane (register tabs)
│   │   ├── CouncilPanel.svelte Multi-agent response panel
│   │   ├── AgentColumn.svelte  Single agent streaming response
│   │   ├── InputBar.svelte     User input (text, mode selector)
│   │   ├── ConsentModal.svelte Kiosk consent overlay
│   │   └── WaitingState.svelte Kiosk idle screen (scrolling Ritual text)
│   │
│   ├── views/                  Top-level view containers
│   │   ├── ReaderView.svelte   Reading + council (main view)
│   │   ├── SettingsView.svelte Contributor settings
│   │   └── KioskView.svelte    Kiosk wrapper (consent, timeout, dark mode)
│   │
│   └── styles/
│       ├── tokens.css          Design tokens (colors, type scale, spacing)
│       ├── typography.css      Cormorant Garamond, Inter, register styles
│       └── global.css          Resets, base styles
│
├── src-tauri/                  Tauri Rust backend
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   ├── capabilities/           Tauri permission config
│   └── src/
│       └── main.rs             Minimal — most logic is in the frontend
│
└── static/                     Static assets (fonts, icons)
    └── fonts/
        └── CormorantGaramond/  Same font files as assets/fonts/ in the repo root

installations/
├── artspace-ptbo-2027/
│   ├── terminal-config.json    Kiosk profile for the Artspace installation
│   └── ...existing files...
└── ...
```

### Key structural rules

- **`src/lib/` is the boundary.** Everything in `lib/` is pure TypeScript or imports only from `platform.ts`. No Svelte components in `lib/`. No Tauri imports in `lib/` (except `platform-tauri.ts`).
- **`src/components/` is pure Svelte.** Components import from `lib/` but never from `@tauri-apps/*` directly.
- **`src/views/` composes components** into full-screen layouts. Views are the top-level things `App.svelte` switches between.
- **`platform.ts` is the only file that touches the platform detection.** Everything else is environment-agnostic.

This structure means: if you delete `platform-tauri.ts` and `src-tauri/`, what remains is a working web app. If you later add SvelteKit, `src/lib/` and `src/components/` move directly into SvelteKit's `src/lib/` with no changes — only `App.svelte` and the view-switching logic are replaced by SvelteKit's file-based routing.

---

## Open questions

These should be resolved before implementation begins on each area:

1. **Conversational system prompts**: The reviewer prompts in `.opencode/agents/reviewer-*.md` are designed for deep batch review, not real-time conversation. Shorter, conversationally-tuned variants are needed for the council panel. These should be developed as part of the Terminal build, not adapted from the review prompts.

2. **GitHub Copilot API for end-users**: Does the GitHub Copilot API support user-supplied OAuth for individuals with a personal Copilot subscription, or only for developers running the app locally? This affects whether it can be a first-class default for general users vs. a developer-only option.

3. **Kiosk fork management**: The installation fork needs to start from a specific tagged version of the Covenant (not `main`, which may continue to change during the exhibition). The fork management workflow — how to initialize it, how to isolate it from upstream changes during the show, how to diff it afterward — should be specified before the installation build begins.

4. **Moderation agent design**: The local moderation agent needs a detailed prompt and a test suite of edge cases (bad-faith proposals, ambiguous proposals, proposals that are legitimate but unusual). This is the most consequential single agent in the system — it mediates the public's relationship to a living document. It should be designed carefully and tested against the Covenant's own harm provisions.

5. **Single-window vs. dual-display**: Tauri supports multiple windows. A gallery setup with a large projection display and a Terminal monitor could benefit from a two-window layout: Terminal on the desk monitor, updated Covenant text on the projected display. This is an installation-specific concern but should be in scope for the kiosk configuration.

6. **Amendment attribution**: When a visitor's amendment is committed to the installation fork, how is it attributed? Anonymous (no visitor identity logged)? Session ID only? Optional name? The consent signage implications and the Log entry format should be decided in concert with the gallery's data handling policy.

---

## Suggested milestones

### Milestone 1 — Readable document (MVP)

Scaffold the Tauri + Svelte 5 + Vite + TypeScript project. Implement:
- `platform.ts` abstraction with Tauri implementation
- Section parser (`covenant/parser.ts`) — reads `.md` files, extracts frontmatter + registers
- `SectionNav.svelte` — sidebar navigator, categories, search
- `SectionView.svelte` — displays a section in Ritual / Spec / Complete tabs, matching the design language from `docs/design.md`
- CSS design tokens (typography, palette, separator grammar)
- Works as a Tauri desktop app

No agents, no council, no git, no web build.

### Milestone 2 — Single-agent Q&A

- Provider interface (`agents/provider.ts`) + OpenRouter adapter
- `CouncilPanel.svelte` with a single `AgentColumn.svelte` (one model)
- Streaming response rendering
- Ask and Challenge interaction modes
- `SettingsView.svelte` — API key entry, model selection
- `config/` module — load/save settings via `platform.ts`

### Milestone 3 — Council panel

- Multi-agent dispatch (`council/dispatch.ts`) — broadcast to N agents in parallel
- 2–3 `AgentColumn.svelte` instances rendering simultaneously
- Optional synthesis view (`council/synthesis.ts`)
- User-configurable model roster and system prompts
- GitHub Copilot adapter (if API access confirmed for end-users)

### Milestone 4 — Amendment workflow (contributor mode)

- Amend interaction mode (structured drafting)
- Steward proposal comparison UI (three-column view, highlight-to-accept, export to section bundle — fulfilling the "Future: Steward UI" from `docs/agent_reviews.md`)
- `amendment/validate.ts` — `make validate` integration via `platform.exec()`
- `amendment/commit.ts` — git commit + PR workflow via `platform.exec()`

### Milestone 5 — Kiosk mode (installation-ready)

- `KioskView.svelte` — full-screen wrapper, session timeout, dark/gallery mode
- Kiosk configuration profile loading (`terminal-config.json`)
- `amendment/moderation.ts` — local moderation agent (single-model check against harm provisions)
- Local fork commit + `make compose` rebuild trigger (projection update)
- `cost/ledger.ts` — Material Cost Display integration
- `ConsentModal.svelte` + `WaitingState.svelte` (scrolling Ritual text)

### Milestone 6 — Web deployment

- Add SvelteKit + `@sveltejs/adapter-static` as a deployment wrapper
- `platform-web.ts` — web implementation (GitHub raw API fetch, localStorage, shell stubs)
- User-supplied key setup flow (OpenRouter account link)
- Web-accessible contribution path (GitHub issue / PR template for amendments)
- Deploy to `docs/` subdirectory, Cloudflare Pages, or Vercel
- No component rewrites — the same `src/lib/` and `src/components/` power both targets

---

*This plan lives at `docs/terminal-plan.md`. For the Artspace installation context, see `installations/artspace-ptbo-2027/`. For the existing agentic review pipeline this Terminal extends, see `docs/agent_reviews.md` and `.opencode/commands/review-covenant.md`.*
