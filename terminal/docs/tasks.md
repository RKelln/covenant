<!-- AGENT:NAV
purpose:terminal development tasks; milestones; test structure
lines:2088
nav[59]{s,n,name,about}:
66,2023,#Covenant Terminal — Task Lists,test; const
76,24,##Testing stack,tests; test
100,42,##Milestone 0 — Project scaffold ✅,tauri; create
142,396,##Milestone 1 — Readable document (MVP) ✅,expect; test
146,23,###1.1 Platform interface and types,platform; expecttypeof
169,26,###1.2 Tauri platform implementation,platform; tauri
195,23,###1.3 Section types,expecttypeof; tobestring
218,95,###1.4 Section parser,expect; test
313,46,###1.5 Section loader,platform; preamble
359,8,###1.6 CSS design tokens and typography,css; populate
367,61,###1.7 SectionNav component,screen; dignity
428,74,###1.8 SectionView component,screen; await
502,25,###1.9 App shell and view wiring,app; screen
527,11,###1.10 Integration verification,sections; npm
538,348,##Milestone 2 — Single-agent Q&A ✅,test; const
542,23,###2.1 Provider interface and types,agentprovider; chatchunk
565,65,###2.2 OpenRouter adapter,adapter; const
630,40,###2.3 Config types and loader,config; const
670,50,###2.4 AgentColumn component,agentcolumn; screen
720,23,###2.5 CouncilPanel component (single-agent version),councilpanel; screen
743,52,###2.6 InputBar component,screen; await
795,35,###2.7 Chat orchestration (single agent),chat; content
830,39,###2.8 SettingsView component,screen; test
869,7,###2.9 Wire Q&A into the reader view,reader; view
876,10,###2.10 Integration verification,api; appear
886,274,##Milestone 3 — Council panel ✅,const; expect
890,51,###3.1 Council dispatch,results; const
941,34,###3.2 Per-agent streaming state,state; done
975,38,###3.3 Multi-column CouncilPanel,screen; column
1013,41,###3.4 Synthesis agent,const; text
1054,25,###3.5 Synthesis view in CouncilPanel,synthesis; done
1079,36,###3.6 GitHub Copilot adapter,copilot; adapter
1115,35,###3.7 Roster configuration UI,add; roster
1150,10,###3.8 Integration verification,agents; respond
1160,28,##M3 Quality Pass ✅,mode; agent
1188,382,##Milestone 4 — Amendment workflow (contributor mode),const; expect
1192,30,###4.1 `platform.writeFile()` — new platform capability,platform; writefile
1222,67,###4.2 `amendment/editor.ts` — editor model invocation,const; text
1289,38,###4.3 `amendment/diff.ts` — section diff computation,diff; computediff
1327,32,###4.4 Apply button in CouncilPanel names bar,apply; button
1359,23,###4.5 Apply mode in InputBar and prompts,apply; mode
1382,59,###4.6 `DiffView` component,const; screen
1441,34,###4.7 `amendment/validate.ts`,validate; exec
1475,73,###4.8 `amendment/commit.ts`,git; calls
1548,9,###4.9 Wire apply flow in App.svelte,apply; diffview
1557,13,###4.10 Integration verification,apply; council
1570,328,##Milestone 5 — Kiosk mode (installation-ready),test; const
1574,34,###5.1 Kiosk config loading,config; kiosk
1608,56,###5.2 Moderation agent,amendment; test
1664,44,###5.3 Local fork commit + rebuild trigger,commit; rebuild
1708,47,###5.4 Cost ledger,ledger; tokens
1755,37,###5.5 ConsentModal component,modal; consentmodal
1792,30,###5.6 WaitingState component,onwake; screen
1822,52,###5.7 KioskView wrapper,screen; await
1874,11,###5.8 Kiosk amendment flow (end-to-end),amendment; flow
1885,13,###5.9 Integration verification,amendment; kiosk
1898,136,##Milestone 6 — Web deployment,platform; web>6.2 SvelteKit wrapper;6.5 Integration verification;6.4 API key setup flow (web);6.3 Web amendment path;6.1 Web platform implementation;6.2 SvelteKit wrapper;6.5 Integration verification;6.4 API key setup flow (web);6.3 Web amendment path;6.1 Web platform implementation;6.2 SvelteKit wrapper;6.5 Integration verification;6.4 API key setup flow (web);6.3 Web amendment path;6.1 Web platform implementation;6.2 SvelteKit wrapper;6.5 Integration verification;6.4 API key setup flow (web);6.3 Web amendment path;6.1 Web platform implementation;6.2 SvelteKit wrapper;6.5 Integration verification;6.4 API key setup flow (web);6.3 Web amendment path;6.1 Web platform implementation;6.2 SvelteKit wrapper;6.5 Integration verification;6.4 API key setup flow (web);6.3 Web amendment path;6.1 Web platform implementation
2034,32,##Cross-cutting concerns,errors; api
2066,23,##Log,svelte; tests
-->

# Covenant Terminal — Task Lists

> **What this document is:** Detailed, ordered task lists for each milestone in `docs/plan.md`, designed for red/green TDD with Vitest.
>
> **How to read it:** Each task starts with the test(s) you write first (RED), then the implementation that makes them pass (GREEN). Tasks within a milestone are ordered by dependency — later tasks assume earlier ones are done. Refactoring steps appear where natural.
>
> **Status:** M0–M3 complete + M3 quality pass + write modes added (176 tests, 25 test files). M4 is next.

---

## Testing stack

| Layer | Tool | Notes |
|---|---|---|
| **Unit tests** (TypeScript logic) | Vitest | Pure functions: parser, types, config, cost, dispatch |
| **Component tests** (Svelte) | `vitest-browser-svelte` | Renders components in real browser via Vitest browser mode |
| **Platform mocking** | `vi.mock('./platform.ts')` | All platform calls mocked in tests — no Tauri dependency |
| **Tauri IPC mocking** | `@tauri-apps/api/mocks` + `mockIPC` | For `platform-tauri.ts` integration tests only |
| **E2E tests** (later milestones) | WebdriverIO + `tauri-driver` | Full app tests against a debug build |

### Test file conventions

```
terminal/
├── src/lib/covenant/__tests__/parser.test.ts       Unit tests next to module
├── src/lib/agents/__tests__/provider.test.ts
├── src/components/__tests__/SectionNav.test.ts      Component tests
└── e2e/                                             E2E tests (Milestone 5+)
```

Tests live in `__tests__/` directories adjacent to the code they test. Test files are named `<module>.test.ts`.

---

## Milestone 0 — Project scaffold ✅

> Goal: A Tauri + Svelte 5 + Vite + TypeScript project that builds, runs, and has a passing test suite with zero application code.

### 0.1 Initialize the Tauri project

- [x] Run `npm create tauri-app@latest` (or manual scaffold) in `terminal/`
- [x] Choose: Svelte, TypeScript, Vite
- [x] Verify: `npm run tauri dev` launches a window with the default template

### 0.2 Strip template, configure TypeScript

- [x] Remove template boilerplate (default Svelte component, CSS, assets)
- [x] Configure `tsconfig.json`: strict mode, path aliases (`$lib` → `src/lib`)
- [x] Create empty `App.svelte` that renders a placeholder
- [x] Verify: `npm run tauri dev` still builds and runs

### 0.3 Install and configure Vitest

- [x] `npm install -D vitest vitest-browser-svelte @vitest/browser playwright`
- [x] Create `vitest.config.ts`
- [x] Write a trivial passing test (`src/lib/__tests__/smoke.test.ts`)
- [x] Add `"test"` script to `package.json`
- [x] Verify: `npm test` runs and passes

### 0.4 Add static assets

- [x] Copy Cormorant Garamond font files into `terminal/static/fonts/`
- [x] Create `src/styles/tokens.css`
- [x] Create `src/styles/typography.css`
- [x] Create `src/styles/global.css`
- [x] Import `global.css` in `main.ts`
- [x] Verify: app renders with the correct typeface

### 0.5 Add Tauri plugins

- [x] Install Tauri plugins: `@tauri-apps/plugin-fs`, `@tauri-apps/plugin-shell`
- [x] Add plugins to `src-tauri/Cargo.toml` and `tauri.conf.json` capabilities
- [x] Verify: `npm run tauri dev` still launches (plugins registered but not yet used)

---

## Milestone 1 — Readable document (MVP) ✅

> Goal: The Terminal displays Covenant sections with navigation. No agents, no network calls. Pure local document rendering.

### 1.1 Platform interface and types

**RED:**
```ts
// src/lib/__tests__/platform.test.ts
test('Platform interface has required methods', () => {
  // Type-level test: ensure Platform type includes readFile, listSections, exec, etc.
  const p: Platform = {} as Platform
  expectTypeOf(p.readFile).toBeFunction()
  expectTypeOf(p.listSections).toBeFunction()
  expectTypeOf(p.exec).toBeFunction()
  expectTypeOf(p.loadConfig).toBeFunction()
  expectTypeOf(p.saveConfig).toBeFunction()
  expectTypeOf(p.logApiCall).toBeFunction()
})
```

**GREEN:**
- [x] Create `src/lib/platform.ts` with the `Platform` interface (as spec'd in the plan)
- [x] Create `src/lib/types.ts` for shared types: `SectionMeta`, `ExecResult`, `TerminalConfig`, `CostEntry`
- [x] Export a `getPlatform()` function that detects `window.__TAURI__` and returns the appropriate implementation
- [x] Tests pass (type-level assertions)

### 1.2 Tauri platform implementation

**RED:**
```ts
// src/lib/__tests__/platform-tauri.test.ts
// Uses @tauri-apps/api/mocks to mock IPC
test('readFile reads via Tauri fs plugin', async () => {
  mockIPC((cmd, args) => { /* mock fs read */ })
  const platform = new TauriPlatform()
  const content = await platform.readFile('sections/00-preamble/preamble.md')
  expect(content).toContain('---')
})

test('exec runs shell commands', async () => {
  mockIPC((cmd, args) => { /* mock shell */ })
  const platform = new TauriPlatform()
  const result = await platform.exec('echo', ['hello'])
  expect(result.code).toBe(0)
})
```

**GREEN:**
- [x] Create `src/lib/platform-tauri.ts` implementing `Platform` using `@tauri-apps/plugin-fs` and `@tauri-apps/plugin-shell`
- [x] Wire `getPlatform()` to return `TauriPlatform` when `window.__TAURI__` exists
- [x] Tests pass against mocked IPC

### 1.3 Section types

**RED:**
```ts
// src/lib/covenant/__tests__/types.test.ts
test('Section type has required fields', () => {
  const s: Section = {} as Section
  expectTypeOf(s.id).toBeString()
  expectTypeOf(s.title).toBeString()
  expectTypeOf(s.status).toMatchTypeOf<'draft' | 'stable' | 'proposed'>()
  expectTypeOf(s.ritual).toBeString()
  expectTypeOf(s.spec).toBeString()
  expectTypeOf(s.digest).toBeString()
  expectTypeOf(s.log).toBeString()
  expectTypeOf(s.frontmatter).toBeObject()
})
```

**GREEN:**
- [x] Create `src/lib/covenant/types.ts` with `Section`, `SectionFrontmatter`, `SectionCategory`, `Register` types
- [x] Types match the actual Covenant section bundle format (YAML frontmatter fields + four register headings)
- [x] Tests pass

### 1.4 Section parser

This is the highest-value pure-logic module. It accepts a raw markdown string and returns a structured `Section`.

**RED:**
```ts
// src/lib/covenant/__tests__/parser.test.ts

const SAMPLE = `---
id: rights.dignity
title: "Dignity"
status: draft
since: 0.2.0
depends_on: [definitions, enforcement, obligations.harm]
terms_introduced: [dignity]
---

# Ritual

You will meet people at the edge of their strength.

# Spec

1. **Prohibition on Degradation**
   The System MUST NOT degrade the dignity...

# Digest

**Intent:** Make "dignity is the floor" explicit...

# Log

- 2025-01-15: Initial draft
`

test('parses frontmatter fields', () => {
  const section = parseSection(SAMPLE)
  expect(section.id).toBe('rights.dignity')
  expect(section.title).toBe('Dignity')
  expect(section.status).toBe('draft')
  expect(section.frontmatter.depends_on).toContain('definitions')
  expect(section.frontmatter.terms_introduced).toContain('dignity')
})

test('extracts Ritual register', () => {
  const section = parseSection(SAMPLE)
  expect(section.ritual).toContain('edge of their strength')
  expect(section.ritual).not.toContain('MUST NOT')
})

test('extracts Spec register', () => {
  const section = parseSection(SAMPLE)
  expect(section.spec).toContain('MUST NOT')
  expect(section.spec).not.toContain('edge of their strength')
})

test('extracts Digest register', () => {
  const section = parseSection(SAMPLE)
  expect(section.digest).toContain('dignity is the floor')
})

test('extracts Log register', () => {
  const section = parseSection(SAMPLE)
  expect(section.log).toContain('Initial draft')
})

test('handles missing registers gracefully', () => {
  const minimal = `---\nid: test.minimal\ntitle: "Minimal"\nstatus: draft\nsince: 0.1.0\n---\n\n# Ritual\n\nSome text\n`
  const section = parseSection(minimal)
  expect(section.ritual).toContain('Some text')
  expect(section.spec).toBe('')
})

test('throws on missing frontmatter', () => {
  expect(() => parseSection('# No frontmatter')).toThrow()
})

test('throws on missing id', () => {
  expect(() => parseSection('---\ntitle: "No ID"\n---\n')).toThrow()
})
```

**GREEN:**
- [x] Create `src/lib/covenant/parser.ts`
- [x] Implement `parseSection(raw: string): Section`
  - Parse YAML frontmatter (use a lightweight YAML parser or hand-roll for the simple schema)
  - Split content by `# Ritual`, `# Spec`, `# Digest`, `# Log` headings
  - Trim whitespace, handle missing registers with empty strings
  - Validate required fields (`id`, `title`, `status`)
- [x] All parser tests pass

**REFACTOR:**
- [x] Extract frontmatter parsing into a separate `parseFrontmatter()` function if it's complex enough
- [x] Consider whether to use `yaml` package or hand-parse (the frontmatter schema is simple and fixed)

### 1.5 Section loader

**RED:**
```ts
// src/lib/covenant/__tests__/loader.test.ts
// Mocks platform.readFile and platform.listSections

vi.mock('$lib/platform.ts')

test('loadAllSections reads and parses all .md files', async () => {
  const mockPlatform = {
    listSections: vi.fn().mockResolvedValue([
      { path: 'sections/00-preamble/preamble.md', category: '00-preamble' },
      { path: 'sections/02-rights/dignity.md', category: '02-rights' },
    ]),
    readFile: vi.fn().mockImplementation((path) => {
      if (path.includes('preamble')) return Promise.resolve(PREAMBLE_MD)
      if (path.includes('dignity')) return Promise.resolve(DIGNITY_MD)
    }),
  }

  const sections = await loadAllSections(mockPlatform)
  expect(sections).toHaveLength(2)
  expect(sections[0].id).toBe('preamble')
  expect(sections[1].id).toBe('rights.dignity')
})

test('loadSection loads a single section by id', async () => {
  const section = await loadSection(mockPlatform, 'rights.dignity')
  expect(section.title).toBe('Dignity')
})

test('sections are grouped by category', async () => {
  const grouped = await loadSectionsByCategory(mockPlatform)
  expect(grouped['00-preamble']).toHaveLength(1)
  expect(grouped['02-rights']).toHaveLength(1)
})
```

**GREEN:**
- [x] Create `src/lib/covenant/loader.ts`
- [x] Implement `loadAllSections(platform: Platform): Promise<Section[]>`
- [x] Implement `loadSection(platform: Platform, id: string): Promise<Section>`
- [x] Implement `loadSectionsByCategory(platform: Platform): Promise<Record<string, Section[]>>`
- [x] All loader tests pass

### 1.6 CSS design tokens and typography

No unit tests — this is a visual/structural task. Verified by inspection and the component tests that follow.

- [x] Populate `src/styles/tokens.css`
- [x] Populate `src/styles/typography.css`
- [x] Populate `src/styles/global.css`

### 1.7 SectionNav component

**RED:**
```ts
// src/components/__tests__/SectionNav.test.ts
import { render } from 'vitest-browser-svelte'

const mockSections = [
  { id: 'preamble', title: 'Preamble', category: '00-preamble', status: 'stable' },
  { id: 'rights.dignity', title: 'Dignity', category: '02-rights', status: 'draft' },
  { id: 'rights.privacy', title: 'Privacy', category: '02-rights', status: 'draft' },
]

test('renders all section titles', async () => {
  const screen = render(SectionNav, { sections: mockSections })
  await expect.element(screen.getByText('Preamble')).toBeVisible()
  await expect.element(screen.getByText('Dignity')).toBeVisible()
  await expect.element(screen.getByText('Privacy')).toBeVisible()
})

test('groups sections by category', async () => {
  const screen = render(SectionNav, { sections: mockSections })
  // Category headings visible
  await expect.element(screen.getByText('Preamble')).toBeVisible() // category 00
  await expect.element(screen.getByText('Rights')).toBeVisible()   // category 02
})

test('shows status indicator', async () => {
  const screen = render(SectionNav, { sections: mockSections })
  // Draft indicator present for dignity
  const dignity = screen.getByText('Dignity')
  await expect.element(dignity).toBeVisible()
  // Implementation: status badge, icon, or text — test for the indicator's presence
})

test('clicking a section emits select event', async () => {
  const onSelect = vi.fn()
  const screen = render(SectionNav, { sections: mockSections, onselect: onSelect })
  await screen.getByText('Dignity').click()
  expect(onSelect).toHaveBeenCalledWith('rights.dignity')
})

test('search filters sections', async () => {
  const screen = render(SectionNav, { sections: mockSections })
  const searchInput = screen.getByRole('searchbox')
  await searchInput.fill('dig')
  await expect.element(screen.getByText('Dignity')).toBeVisible()
  // Preamble should be hidden/removed
})
```

**GREEN:**
- [x] Create `src/components/SectionNav.svelte`
  - Props: `sections: SectionMeta[]`, `selected?: string`
  - Events: `onselect(id: string)`
  - Groups sections by category
  - Search input filters by title
  - Status indicator (draft/stable badge)
  - § separator between category groups
- [x] All SectionNav tests pass

### 1.8 SectionView component

**RED:**
```ts
// src/components/__tests__/SectionView.test.ts
import { render } from 'vitest-browser-svelte'

const mockSection = {
  id: 'rights.dignity',
  title: 'Dignity',
  ritual: 'You will meet people at the edge of their strength.',
  spec: '1. **Prohibition on Degradation** ...',
  digest: '**Intent:** Make "dignity is the floor" explicit...',
  log: '- 2025-01-15: Initial draft',
  // ... full Section type
}

test('renders section title', async () => {
  const screen = render(SectionView, { section: mockSection })
  await expect.element(screen.getByText('Dignity')).toBeVisible()
})

test('shows Ritual tab by default', async () => {
  const screen = render(SectionView, { section: mockSection })
  await expect.element(screen.getByText('edge of their strength')).toBeVisible()
})

test('switches to Spec tab', async () => {
  const screen = render(SectionView, { section: mockSection })
  await screen.getByRole('tab', { name: 'Spec' }).click()
  await expect.element(screen.getByText('Prohibition on Degradation')).toBeVisible()
})

test('switches to Complete tab (shows all registers)', async () => {
  const screen = render(SectionView, { section: mockSection })
  await screen.getByRole('tab', { name: 'Complete' }).click()
  await expect.element(screen.getByText('edge of their strength')).toBeVisible()
  await expect.element(screen.getByText('Prohibition on Degradation')).toBeVisible()
  await expect.element(screen.getByText('dignity is the floor')).toBeVisible()
})

test('renders markdown in section content', async () => {
  const screen = render(SectionView, { section: mockSection })
  await screen.getByRole('tab', { name: 'Spec' }).click()
  // Bold text should render as <strong>
  const bold = screen.container.querySelector('strong')
  expect(bold).not.toBeNull()
})

test('renders cross-references as styled spans', async () => {
  const sectionWithRef = {
    ...mockSection,
    spec: 'See §[obligations.harm] for details.',
  }
  const screen = render(SectionView, { section: sectionWithRef })
  await screen.getByRole('tab', { name: 'Spec' }).click()
  // Cross-reference rendered as a styled element (link or marked span)
  await expect.element(screen.getByText('§obligations.harm')).toBeVisible()
})
```

**GREEN:**
- [x] Create `src/components/SectionView.svelte`
  - Props: `section: Section`, `defaultRegister?: 'ritual' | 'spec' | 'complete'`
  - Tab bar: Ritual | Spec | Complete
  - Renders markdown to HTML
  - Cross-reference syntax (`§[section.id]`) rendered as styled clickable spans
  - Typography: `.register-ritual` / `.register-spec` styling
- [x] All SectionView tests pass

**REFACTOR:**
- [x] Extract markdown rendering into `src/lib/covenant/render.ts`
- [x] Write tests for the render function independently of the component

### 1.9 App shell and view wiring

**RED:**
```ts
// src/components/__tests__/App.test.ts
test('App renders SectionNav and SectionView', async () => {
  // Mock platform to return test sections
  const screen = render(App)
  // Nav should appear
  await expect.element(screen.getByRole('searchbox')).toBeVisible()
})

test('selecting a section in nav displays it in the view', async () => {
  const screen = render(App)
  await screen.getByText('Dignity').click()
  await expect.element(screen.getByText('edge of their strength')).toBeVisible()
})
```

**GREEN:**
- [x] Wire `App.svelte` to load sections on mount and pass to `SectionNav` / `SectionView`
- [x] Handle cross-reference clicks (navigate to referenced section)
- [x] Create `src/main.ts` bootstrap
- [x] All app shell tests pass

### 1.10 Integration verification

- [x] `npm run tauri dev` launches with real Covenant sections loaded from disk
- [x] Sidebar shows all 30 sections grouped by category
- [x] Clicking a section shows its Ritual text
- [x] Tab switching works (Ritual → Spec → Complete)
- [x] Search filters sections
- [x] `npm test` — all tests pass

---

## Milestone 2 — Single-agent Q&A ✅

> Goal: One AI model answers questions about the currently-viewed section. Streaming responses. Settings page for API key entry.

### 2.1 Provider interface and types

**RED:**
```ts
// src/lib/agents/__tests__/provider.test.ts
test('AgentProvider interface shape', () => {
  const p: AgentProvider = {} as AgentProvider
  expectTypeOf(p.name).toBeString()
  expectTypeOf(p.chat).toBeFunction()
  expectTypeOf(p.models).toBeFunction()
})

test('ChatChunk type has content and done fields', () => {
  const chunk: ChatChunk = { content: 'hello', done: false }
  expect(chunk.content).toBe('hello')
  expect(chunk.done).toBe(false)
})
```

**GREEN:**
- [x] Create `src/lib/agents/provider.ts` with `AgentProvider`, `ChatParams`, `ChatChunk`, `Message`, `ModelInfo`
- [x] Tests pass

### 2.2 OpenRouter adapter

**RED:**
```ts
// src/lib/agents/__tests__/openrouter.test.ts

test('OpenRouter adapter has correct name', () => {
  const adapter = new OpenRouterProvider('test-key')
  expect(adapter.name).toBe('openrouter')
})

test('chat() streams chunks from SSE response', async () => {
  // Mock fetch to return a fake SSE stream
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(mockSSEResponse([
    'data: {"choices":[{"delta":{"content":"Hello"}}]}',
    'data: {"choices":[{"delta":{"content":" world"}}]}',
    'data: [DONE]',
  ])))

  const adapter = new OpenRouterProvider('test-key')
  const chunks: ChatChunk[] = []
  for await (const chunk of adapter.chat({
    model: 'openai/gpt-4o-mini',
    messages: [{ role: 'user', content: 'hi' }],
  })) {
    chunks.push(chunk)
  }

  expect(chunks).toHaveLength(3)
  expect(chunks[0].content).toBe('Hello')
  expect(chunks[1].content).toBe(' world')
  expect(chunks[2].done).toBe(true)
})

test('chat() throws on 401 (bad API key)', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(
    new Response('Unauthorized', { status: 401 })
  ))
  const adapter = new OpenRouterProvider('bad-key')
  const stream = adapter.chat({
    model: 'openai/gpt-4o-mini',
    messages: [{ role: 'user', content: 'hi' }],
  })
  await expect(collectStream(stream)).rejects.toThrow(/unauthorized|api key/i)
})

test('models() returns available model list', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(
    new Response(JSON.stringify({ data: [
      { id: 'openai/gpt-4o-mini', name: 'GPT-4o mini', context_length: 128000 },
    ] }))
  ))
  const adapter = new OpenRouterProvider('test-key')
  const models = await adapter.models()
  expect(models[0].id).toBe('openai/gpt-4o-mini')
})
```

**GREEN:**
- [x] Create `src/lib/agents/openrouter.ts`
- [x] All OpenRouter tests pass

**REFACTOR:**
- [x] Extract SSE parsing into reusable `parseSSE()` utility

### 2.3 Config types and loader

**RED:**
```ts
// src/lib/config/__tests__/config.test.ts

test('default config has sensible values', () => {
  const config = defaultConfig()
  expect(config.mode).toBe('contributor')
  expect(config.providers).toEqual([])
  expect(config.council).toEqual([])
})

test('loadConfig returns defaults when no saved config', async () => {
  const mockPlatform = { loadConfig: vi.fn().mockResolvedValue(null) }
  const config = await loadConfig(mockPlatform)
  expect(config.mode).toBe('contributor')
})

test('loadConfig merges saved config with defaults', async () => {
  const saved = { providers: [{ type: 'openrouter', apiKey: 'key-123' }] }
  const mockPlatform = { loadConfig: vi.fn().mockResolvedValue(saved) }
  const config = await loadConfig(mockPlatform)
  expect(config.providers[0].apiKey).toBe('key-123')
  expect(config.mode).toBe('contributor') // default filled in
})

test('saveConfig persists via platform', async () => {
  const mockPlatform = { saveConfig: vi.fn().mockResolvedValue(undefined) }
  const config = { ...defaultConfig(), providers: [{ type: 'openrouter', apiKey: 'x' }] }
  await saveConfig(mockPlatform, config)
  expect(mockPlatform.saveConfig).toHaveBeenCalledWith(config)
})
```

**GREEN:**
- [x] Create `src/lib/config/types.ts` — `TerminalConfig`, `ProviderConfig`, `CouncilMemberConfig`
- [x] Create `src/lib/config/loader.ts` — `defaultConfig()`, `loadConfig(platform)`, `saveConfig(platform, config)`
- [x] Tests pass

### 2.4 AgentColumn component

**RED:**
```ts
// src/components/__tests__/AgentColumn.test.ts

test('renders agent name in header', async () => {
  const screen = render(AgentColumn, {
    agentName: 'Claude',
    chunks: [],
    streaming: false,
  })
  await expect.element(screen.getByText('Claude')).toBeVisible()
})

test('renders streamed text as it arrives', async () => {
  const screen = render(AgentColumn, {
    agentName: 'Claude',
    chunks: [{ content: 'Hello ', done: false }, { content: 'world', done: false }],
    streaming: true,
  })
  await expect.element(screen.getByText('Hello world')).toBeVisible()
})

test('shows streaming indicator while active', async () => {
  const screen = render(AgentColumn, {
    agentName: 'Claude',
    chunks: [{ content: 'Thinking...', done: false }],
    streaming: true,
  })
  // The § thinking indicator should be visible
  const indicator = screen.container.querySelector('[data-streaming]')
  expect(indicator).not.toBeNull()
})

test('hides streaming indicator when done', async () => {
  const screen = render(AgentColumn, {
    agentName: 'Claude',
    chunks: [{ content: 'Done.', done: true }],
    streaming: false,
  })
  const indicator = screen.container.querySelector('[data-streaming]')
  expect(indicator).toBeNull()
})
```

**GREEN:**
- [x] Create `src/components/AgentColumn.svelte`
- [x] All AgentColumn tests pass

### 2.5 CouncilPanel component (single-agent version)

**RED:**
```ts
// src/components/__tests__/CouncilPanel.test.ts

test('renders a single AgentColumn', async () => {
  const screen = render(CouncilPanel, {
    agents: [{ name: 'Claude', chunks: [], streaming: false }],
  })
  await expect.element(screen.getByText('Claude')).toBeVisible()
})

test('shows empty state when no query submitted', async () => {
  const screen = render(CouncilPanel, { agents: [] })
  await expect.element(screen.getByText(/ask a question/i)).toBeVisible()
})
```

**GREEN:**
- [x] Create `src/components/CouncilPanel.svelte`
- [x] Tests pass

### 2.6 InputBar component

**RED:**
```ts
// src/components/__tests__/InputBar.test.ts

test('renders text input and submit button', async () => {
  const screen = render(InputBar, { sectionId: 'rights.dignity' })
  await expect.element(screen.getByRole('textbox')).toBeVisible()
  await expect.element(screen.getByRole('button', { name: /send|submit/i })).toBeVisible()
})

test('shows current section context', async () => {
  const screen = render(InputBar, { sectionId: 'rights.dignity' })
  await expect.element(screen.getByText(/rights\.dignity/)).toBeVisible()
})

test('emits submit event with text and mode', async () => {
  const onSubmit = vi.fn()
  const screen = render(InputBar, { sectionId: 'rights.dignity', onsubmit: onSubmit })
  await screen.getByRole('textbox').fill('What does dignity mean here?')
  await screen.getByRole('button', { name: /send|submit/i }).click()
  expect(onSubmit).toHaveBeenCalledWith({
    text: 'What does dignity mean here?',
    mode: 'ask',
    sectionId: 'rights.dignity',
  })
})

test('mode selector switches between Ask and Challenge', async () => {
  const screen = render(InputBar, { sectionId: 'rights.dignity' })
  const selector = screen.getByRole('combobox')
  // Default is Ask
  // Switch to Challenge
  await selector.selectOptions(['challenge'])
  // Verify the mode changed (implementation detail — test the emitted event)
})

test('clears input after submit', async () => {
  const screen = render(InputBar, { sectionId: 'rights.dignity', onsubmit: vi.fn() })
  const input = screen.getByRole('textbox')
  await input.fill('test question')
  await screen.getByRole('button', { name: /send|submit/i }).click()
  // Input should be cleared
  await expect.element(input).toHaveValue('')
})
```

**GREEN:**
- [x] Create `src/components/InputBar.svelte`
- [x] Tests pass

### 2.7 Chat orchestration (single agent)

**RED:**
```ts
// src/lib/agents/__tests__/chat.test.ts

test('sendQuery streams response from provider', async () => {
  const mockProvider: AgentProvider = {
    name: 'mock',
    chat: vi.fn().mockReturnValue(asyncIterableOf([
      { content: 'Hello', done: false },
      { content: ' there', done: false },
      { content: '', done: true },
    ])),
    models: vi.fn(),
  }

  const chunks: ChatChunk[] = []
  for await (const chunk of sendQuery(mockProvider, {
    model: 'test-model',
    messages: [{ role: 'user', content: 'What is dignity?' }],
    system: 'You are a co-author of the Covenant.',
  })) {
    chunks.push(chunk)
  }

  expect(chunks).toHaveLength(3)
  expect(mockProvider.chat).toHaveBeenCalledOnce()
})
```

**GREEN:**
- [x] Create `src/lib/agents/chat.ts`
- [x] Tests pass

### 2.8 SettingsView component

**RED:**
```ts
// src/components/__tests__/SettingsView.test.ts

test('renders API key input for OpenRouter', async () => {
  const screen = render(SettingsView, { config: defaultConfig() })
  await expect.element(screen.getByLabelText(/openrouter.*key/i)).toBeVisible()
})

test('saves config on submit', async () => {
  const onSave = vi.fn()
  const screen = render(SettingsView, { config: defaultConfig(), onsave: onSave })
  await screen.getByLabelText(/openrouter.*key/i).fill('sk-test-key')
  await screen.getByRole('button', { name: /save/i }).click()
  expect(onSave).toHaveBeenCalledWith(expect.objectContaining({
    providers: expect.arrayContaining([
      expect.objectContaining({ type: 'openrouter', apiKey: 'sk-test-key' })
    ])
  }))
})

test('model selector shows available models', async () => {
  const config = {
    ...defaultConfig(),
    providers: [{ type: 'openrouter', apiKey: 'sk-test' }],
  }
  const screen = render(SettingsView, { config, availableModels: [
    { id: 'openai/gpt-4o-mini', name: 'GPT-4o mini', provider: 'openrouter' },
  ] })
  await expect.element(screen.getByText('GPT-4o mini')).toBeVisible()
})
```

**GREEN:**
- [x] Create `src/components/SettingsView.svelte`
- [x] Tests pass

### 2.9 Wire Q&A into the reader view

- [x] Update `App.svelte` to show `InputBar` and `CouncilPanel`
- [x] On submit: construct messages, call `sendQuery()`, pipe chunks into `AgentColumn`
- [x] Handle streaming state
- [x] Add view switching: Reader ↔ Settings

### 2.10 Integration verification

- [x] Enter an OpenRouter API key in Settings
- [x] Select a model
- [x] Navigate to a section, type a question, submit
- [x] Watch streaming response appear in the council panel
- [x] `npm test` — all tests pass

---

## Milestone 3 — Council panel ✅

> Goal: Multiple AI models respond simultaneously. Synthesis view. Configurable roster.

### 3.1 Council dispatch

**RED:**
```ts
// src/lib/council/__tests__/dispatch.test.ts

test('dispatches to multiple providers in parallel', async () => {
  const provider1 = mockProvider('Claude', [
    { content: 'Response 1', done: false },
    { content: '', done: true },
  ])
  const provider2 = mockProvider('GPT', [
    { content: 'Response 2', done: false },
    { content: '', done: true },
  ])

  const results = dispatchToCouncil(
    [provider1, provider2],
    { model: 'auto', messages: [{ role: 'user', content: 'test' }] }
  )

  // Results is an array of AsyncIterables, one per provider
  expect(results).toHaveLength(2)
  expect(await collectStream(results[0])).toContain('Response 1')
  expect(await collectStream(results[1])).toContain('Response 2')
})

test('one provider failure does not block others', async () => {
  const provider1 = mockProvider('Claude', [{ content: 'OK', done: true }])
  const provider2 = mockErrorProvider('GPT', new Error('rate limited'))

  const results = dispatchToCouncil([provider1, provider2], params)
  const stream1 = await collectStream(results[0])
  expect(stream1).toContain('OK')

  // Provider 2 yields an error chunk, not a thrown exception
  const stream2 = await collectStream(results[1])
  expect(stream2.some(c => c.error)).toBe(true)
})

test('returns provider names with streams', async () => {
  const results = dispatchToCouncil([provider1, provider2], params)
  expect(results[0].providerName).toBe('Claude')
  expect(results[1].providerName).toBe('GPT')
})
```

**GREEN:**
- [x] Create `src/lib/council/dispatch.ts`
- [x] Tests pass

### 3.2 Per-agent streaming state

**RED:**
```ts
// src/lib/council/__tests__/stream.test.ts

test('AgentStreamState accumulates chunks', () => {
  const state = createAgentStreamState('Claude')
  state.push({ content: 'Hello ', done: false })
  state.push({ content: 'world', done: false })
  expect(state.text).toBe('Hello world')
  expect(state.streaming).toBe(true)
})

test('marks done when final chunk received', () => {
  const state = createAgentStreamState('Claude')
  state.push({ content: 'Done', done: false })
  state.push({ content: '', done: true })
  expect(state.streaming).toBe(false)
  expect(state.text).toBe('Done')
})

test('captures error state', () => {
  const state = createAgentStreamState('GPT')
  state.pushError(new Error('rate limited'))
  expect(state.error).toBe('rate limited')
  expect(state.streaming).toBe(false)
})
```

**GREEN:**
- [x] Create `src/lib/council/stream.ts`
- [x] Tests pass

### 3.3 Multi-column CouncilPanel

**RED:**
```ts
// src/components/__tests__/CouncilPanel.multi.test.ts

test('renders multiple agent columns', async () => {
  const agents = [
    { name: 'Claude', chunks: [{ content: 'From Claude', done: true }], streaming: false },
    { name: 'GPT', chunks: [{ content: 'From GPT', done: true }], streaming: false },
    { name: 'Gemini', chunks: [{ content: 'From Gemini', done: true }], streaming: false },
  ]
  const screen = render(CouncilPanel, { agents })
  await expect.element(screen.getByText('Claude')).toBeVisible()
  await expect.element(screen.getByText('GPT')).toBeVisible()
  await expect.element(screen.getByText('Gemini')).toBeVisible()
  await expect.element(screen.getByText('From Claude')).toBeVisible()
  await expect.element(screen.getByText('From GPT')).toBeVisible()
})

test('columns have distinct tint colors', async () => {
  const agents = [
    { name: 'Claude', chunks: [], streaming: false, tint: '#e8d5b7' },
    { name: 'GPT', chunks: [], streaming: false, tint: '#b7d5e8' },
  ]
  const screen = render(CouncilPanel, { agents })
  const columns = screen.container.querySelectorAll('[data-agent-column]')
  expect(columns).toHaveLength(2)
  // Check for distinct border-left colors
})
```

**GREEN:**
- [x] Update `CouncilPanel.svelte` to render N agent columns side-by-side
- [x] Responsive layout: multi-column on wide screens
- [x] Each column has a distinct tint from a predefined palette (`data-agent-column`, `--column-tint`)
- [x] Tests pass

### 3.4 Synthesis agent

**RED:**
```ts
// src/lib/council/__tests__/synthesis.test.ts

test('synthesize takes multiple responses and produces a synthesis', async () => {
  const responses = [
    { agent: 'Claude', text: 'Dignity is the floor — it constrains all other obligations.' },
    { agent: 'GPT', text: 'Dignity here means protection from degradation, not positive entitlement.' },
  ]

  const mockProvider = mockProvider('Synthesizer', [
    { content: 'Both agree that dignity sets a minimum...', done: false },
    { content: '', done: true },
  ])

  const chunks = synthesize(mockProvider, responses, { model: 'test' })
  const text = await collectStreamText(chunks)
  expect(text).toContain('Both agree')
})

test('synthesis prompt includes all council responses', async () => {
  const chatSpy = vi.fn().mockReturnValue(asyncIterableOf([{ content: 'ok', done: true }]))
  const mockProvider = { name: 'mock', chat: chatSpy, models: vi.fn() }

  await collectStream(synthesize(mockProvider, [
    { agent: 'A', text: 'Response A' },
    { agent: 'B', text: 'Response B' },
  ], { model: 'test' }))

  const messages = chatSpy.mock.calls[0][0].messages
  expect(messages.some(m => m.content.includes('Response A'))).toBe(true)
  expect(messages.some(m => m.content.includes('Response B'))).toBe(true)
})
```

**GREEN:**
- [x] Create `src/lib/council/synthesis.ts`
- [x] Tests pass

### 3.5 Synthesis view in CouncilPanel

**RED:**
```ts
test('shows synthesis section after all agents complete', async () => {
  const agents = [
    { name: 'Claude', chunks: [{ content: 'Done', done: true }], streaming: false },
    { name: 'GPT', chunks: [{ content: 'Done', done: true }], streaming: false },
  ]
  const synthesis = { chunks: [{ content: 'Synthesis text', done: true }], streaming: false }

  const screen = render(CouncilPanel, { agents, synthesis })
  await expect.element(screen.getByText('Synthesis')).toBeVisible()
  await expect.element(screen.getByText('Synthesis text')).toBeVisible()
})

test('synthesis section is collapsible', async () => {
  // ...
})
```

**GREEN:**
- [x] Add synthesis section to `CouncilPanel.svelte`
- [x] Tests pass

### 3.6 GitHub Copilot adapter

**RED:**
```ts
// src/lib/agents/__tests__/copilot.test.ts

test('Copilot adapter has correct name', () => {
  const adapter = new CopilotProvider('ghp_test')
  expect(adapter.name).toBe('copilot')
})

test('chat() uses Copilot API endpoint', async () => {
  const fetchSpy = vi.stubGlobal('fetch', vi.fn().mockResolvedValue(mockSSEResponse([
    'data: {"choices":[{"delta":{"content":"Hi"}}]}',
    'data: [DONE]',
  ])))

  const adapter = new CopilotProvider('ghp_test')
  await collectStream(adapter.chat({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: 'hi' }],
  }))

  expect(fetchSpy).toHaveBeenCalledWith(
    expect.stringContaining('copilot'),
    expect.anything()
  )
})
```

**GREEN:**
- [x] Create `src/lib/agents/copilot.ts` implementing `AgentProvider`
- [x] Uses GitHub Copilot Chat API (OpenAI-compatible SSE format)
- [x] Reuses the SSE parser from 2.2
- [x] Tests pass

### 3.7 Roster configuration UI

**RED:**
```ts
// src/components/__tests__/SettingsView.roster.test.ts

test('roster editor shows configured agents', async () => {
  const config = {
    ...defaultConfig(),
    council: [
      { provider: 'openrouter', model: 'anthropic/claude-3-haiku', label: 'Claude' },
      { provider: 'openrouter', model: 'openai/gpt-4o-mini', label: 'GPT' },
    ]
  }
  const screen = render(SettingsView, { config })
  await expect.element(screen.getByText('Claude')).toBeVisible()
  await expect.element(screen.getByText('GPT')).toBeVisible()
})

test('can add an agent to the roster', async () => {
  // ...
})

test('can remove an agent from the roster', async () => {
  // ...
})
```

**GREEN:**
- [x] Add roster management to `SettingsView.svelte`
  - List of configured council members (`data-council-label`)
  - Add/remove agents (`data-add-agent-btn`, `data-remove-agent`)
  - Model and label inputs (`data-add-model`, `data-add-label`)
- [x] Tests pass

### 3.8 Integration verification

- [ ] Configure 2-3 agents in Settings (e.g., Claude Haiku + GPT-4o mini via OpenRouter)
- [ ] Ask a question — all agents respond simultaneously in parallel columns
- [ ] Enable synthesis — synthesis appears after all agents finish
- [ ] Verify error handling: disable one agent's API key, ensure others still respond
- [x] `npm test` — all tests pass (114 tests, 20 files)

---

## M3 Quality Pass ✅

> Goal: Refine council agent prompts and add conversation logging. Not part of the original M3 plan; added after M3 was complete to improve prompt quality before M4 work begins.

### QP.1 Council prompt redesign

- [x] Create `src/lib/council/prompts.ts`
  - `CouncilMode` type: `'ask' | 'challenge' | 'review'`
  - `IDENTITY` block: agent as deeply knowledgeable addressee — familiar with the text, has standing, no critique posture assumed
  - `MODE_ASK`: reader-guide mode — help the user understand the text, its intent, the registers, how parts relate. Does not frame the agent as a reviewer.
  - `MODE_CHALLENGE`: contestation mode — unchanged from prior design, supports the user in interrogating the document
  - `MODE_REVIEW`: full co-author/addressee framing with assess/propose structure, drawn from `prompts/agent_review_batch.md`. Includes addressee-perspective instruction.
  - `buildPrompt(mode, section): string` — assembles the full system prompt for a given mode and section
- [x] Update `InputBar.svelte` default modes to `['ask', 'challenge', 'review']`
- [x] Update `App.svelte` mode cast to include `'review'`
- [x] Write/update `prompts.test.ts`: 18 tests covering identity block, all three modes, and prompt assembly

### QP.2 Conversation logging

- [x] Create `src/lib/council/conversation-log.ts`
  - `ConversationEntry` type: `timestamp`, `sectionId`, `sectionTitle`, `mode`, `query`, `systemPrompt`, `responses` (array of `{ agentName, model, text }`)
  - `appendConversationLog(platform, entry)`: reads existing JSONL log → appends new line → writes back. Swallows all errors so logging never interrupts the query flow.
  - Log path: `<repo>/terminal-conversation-log.jsonl`
- [x] Wire in `App.svelte`: call `appendConversationLog` (non-blocking `.catch`) after all streams drain, capturing agent names, models, and full response text
- [x] Write `conversation-log.test.ts`: 7 tests covering path format, valid JSON output, field presence, append behavior, missing file graceful handling, write failure graceful handling

---

## Milestone 4 — Amendment workflow (contributor mode)

> Goal: Apply button lets the steward select a council response and send it to an editor model, which produces a diff for inline review, confirmation, and git commit.

### 4.1 `platform.writeFile()` — new platform capability

**RED:**
```ts
// src/lib/__tests__/platform.test.ts (additions)

test('Platform interface includes writeFile', () => {
  // Structural: TypeScript will fail if writeFile is not on Platform
  const mock: Platform = {
    readFile: vi.fn(),
    writeFile: vi.fn(),
    exec: vi.fn(),
    getConfig: vi.fn(),
  }
  expect(mock.writeFile).toBeDefined()
})

test('platform-web writeFile throws descriptive error', async () => {
  const platform = createWebPlatform()
  await expect(platform.writeFile('sections/foo.md', 'content'))
    .rejects.toThrow(/not available in web mode/i)
})
```

**GREEN:**
- [ ] Add `writeFile(path: string, content: string): Promise<void>` to `Platform` interface in `platform.ts`
- [ ] Implement in `platform-tauri.ts` using `@tauri-apps/plugin-fs` `writeTextFile`
- [ ] Stub in `platform-web.ts` — throws `"File writing not available in web mode"`
- [ ] Tests pass

### 4.2 `amendment/editor.ts` — editor model invocation

**RED:**
```ts
// src/lib/amendment/__tests__/editor.test.ts

test('buildEditorPrompt includes full section file text', () => {
  const { messages } = buildEditorPrompt('section content here', [], 'apply Claude suggestion')
  const combined = messages.map(m => m.content).join('\n')
  expect(combined).toContain('section content here')
})

test('buildEditorPrompt includes all council responses labelled by agent', () => {
  const responses = [
    { agentName: 'Claude', text: 'Claude proposal text' },
    { agentName: 'GPT', text: 'GPT proposal text' },
  ]
  const { messages } = buildEditorPrompt('section', responses, 'instruction')
  const combined = messages.map(m => m.content).join('\n')
  expect(combined).toContain('Claude')
  expect(combined).toContain('Claude proposal text')
  expect(combined).toContain('GPT')
  expect(combined).toContain('GPT proposal text')
})

test('buildEditorPrompt includes the apply instruction', () => {
  const { messages } = buildEditorPrompt('section', [], 'use option B')
  const combined = messages.map(m => m.content).join('\n')
  expect(combined).toContain('use option B')
})

test('buildEditorPrompt system prompt instructs: return only modified section file', () => {
  const { system } = buildEditorPrompt('section', [], 'instruction')
  expect(system).toMatch(/return only the complete.*section/i)
  expect(system).toMatch(/no commentary/i)
})

test('buildEditorPrompt system prompt instructs: append a Log entry', () => {
  const { system } = buildEditorPrompt('section', [], 'instruction')
  expect(system).toMatch(/log entry/i)
})

test('invokeEditor calls provider.chat with editor prompt', async () => {
  const mockProvider = { chat: vi.fn().mockReturnValue((async function* () { yield { type: 'text', text: '...' } })()) }
  await invokeEditor(mockProvider as any, 'section', [], 'instruction').next()
  expect(mockProvider.chat).toHaveBeenCalledOnce()
})

test('invokeEditor returns streamed chunks from provider', async () => {
  const chunks = [{ type: 'text', text: 'part1' }, { type: 'text', text: 'part2' }]
  const mockProvider = { chat: vi.fn().mockReturnValue((async function* () { for (const c of chunks) yield c })()) }
  const result = []
  for await (const chunk of invokeEditor(mockProvider as any, 'section', [], 'instruction')) {
    result.push(chunk)
  }
  expect(result).toHaveLength(2)
})
```

**GREEN:**
- [ ] Create `src/lib/amendment/editor.ts`
  - `buildEditorPrompt(sectionFileText: string, councilResponses: Array<{ agentName: string, text: string }>, instruction: string): { system: string, messages: Message[] }`
  - System prompt instructs: return only the complete modified section file; no commentary; append a `# Log` entry with today's date and a description of what changed
  - `invokeEditor(provider, sectionFileText, councilResponses, instruction): AsyncIterable<ChatChunk>`
  - Callable programmatically — not coupled to mode selector UI (important for future controller model)
- [ ] Tests pass

### 4.3 `amendment/diff.ts` — section diff computation

**RED:**
```ts
// src/lib/amendment/__tests__/diff.test.ts

test('computeDiff returns unchanged lines as context', () => {
  const diff = computeDiff('line1\nline2\nline3', 'line1\nline2\nline3')
  expect(diff.every(d => d.type === 'unchanged')).toBe(true)
  expect(diff).toHaveLength(3)
})

test('computeDiff marks removed lines', () => {
  const diff = computeDiff('line1\nline2\nline3', 'line1\nline3')
  const removed = diff.filter(d => d.type === 'removed')
  expect(removed).toHaveLength(1)
  expect(removed[0].content).toBe('line2')
})

test('computeDiff marks added lines', () => {
  const diff = computeDiff('line1\nline3', 'line1\nline2\nline3')
  const added = diff.filter(d => d.type === 'added')
  expect(added).toHaveLength(1)
  expect(added[0].content).toBe('line2')
})

test('computeDiff returns empty array for empty input', () => {
  expect(computeDiff('', '')).toEqual([])
})
```

**GREEN:**
- [ ] Create `src/lib/amendment/diff.ts`
  - `DiffLine` type: `{ type: 'unchanged' | 'removed' | 'added', content: string }`
  - `computeDiff(original: string, proposed: string): DiffLine[]`
  - Pure TypeScript — no platform dependency
- [ ] Tests pass

### 4.4 Apply button in CouncilPanel names bar

**RED:**
```ts
// src/components/__tests__/CouncilPanel.test.ts (additions)

test('shows Apply button in names bar chip when agent has completed response', async () => {
  const agents = [{ name: 'Claude', color: '#e06c75', streaming: false, chunks: [{ type: 'text', text: 'response' }] }]
  const screen = render(CouncilPanel, { agents, onapply: vi.fn() })
  await expect.element(screen.getByRole('button', { name: /apply/i })).toBeVisible()
})

test('Apply button is not shown while agent is streaming', async () => {
  const agents = [{ name: 'Claude', color: '#e06c75', streaming: true, chunks: [] }]
  const screen = render(CouncilPanel, { agents, onapply: vi.fn() })
  expect(screen.queryByRole('button', { name: /apply/i })).toBeNull()
})

test('pressing Apply button fires onapply with agent name', async () => {
  const onapply = vi.fn()
  const agents = [{ name: 'Claude', color: '#e06c75', streaming: false, chunks: [{ type: 'text', text: 'response' }] }]
  const screen = render(CouncilPanel, { agents, onapply })
  await screen.getByRole('button', { name: /apply/i }).click()
  expect(onapply).toHaveBeenCalledWith('Claude')
})
```

**GREEN:**
- [ ] Add `onapply?: (agentName: string) => void` prop to `CouncilPanel.svelte`
- [ ] Apply button: right-justified in `.name-chip`, visible only when `!agent.streaming && agent.chunks.length > 0`
- [ ] Tests pass

### 4.5 Apply mode in InputBar and prompts

**RED:**
```ts
// src/components/__tests__/InputBar.test.ts (additions)
test('apply mode option exists in mode selector', async () => {
  const screen = render(InputBar, { sectionId: 'rights.dignity' })
  const options = screen.getAllByRole('option').map((o: HTMLOptionElement) => o.value)
  expect(options).toContain('apply')
})

// src/lib/council/__tests__/prompts.test.ts (additions)
test('CouncilMode includes apply', () => {
  const mode: CouncilMode = 'apply'
  expect(mode).toBe('apply')
})
```

**GREEN:**
- [ ] Add `'apply'` to `CouncilMode` type in `prompts.ts`
- [ ] Add `apply` to InputBar default modes (appended to Write group or standalone)
- [ ] Tests pass

### 4.6 `DiffView` component

**RED:**
```ts
// src/components/__tests__/DiffView.test.ts

test('renders removed lines with removed styling', async () => {
  const diff = [{ type: 'removed' as const, content: 'old line' }]
  const screen = render(DiffView, { diff, onconfirm: vi.fn(), oncancel: vi.fn() })
  const el = screen.getByText('old line')
  expect(el.closest('[data-type="removed"]') ?? el).toBeTruthy()
})

test('renders added lines with added styling', async () => {
  const diff = [{ type: 'added' as const, content: 'new line' }]
  const screen = render(DiffView, { diff, onconfirm: vi.fn(), oncancel: vi.fn() })
  await expect.element(screen.getByText('new line')).toBeVisible()
})

test('renders unchanged lines', async () => {
  const diff = [{ type: 'unchanged' as const, content: 'same line' }]
  const screen = render(DiffView, { diff, onconfirm: vi.fn(), oncancel: vi.fn() })
  await expect.element(screen.getByText('same line')).toBeVisible()
})

test('shows Confirm and Cancel buttons', async () => {
  const screen = render(DiffView, { diff: [], onconfirm: vi.fn(), oncancel: vi.fn() })
  await expect.element(screen.getByRole('button', { name: /confirm/i })).toBeVisible()
  await expect.element(screen.getByRole('button', { name: /cancel/i })).toBeVisible()
})

test('fires onconfirm when Confirm clicked', async () => {
  const onconfirm = vi.fn()
  const screen = render(DiffView, { diff: [], onconfirm, oncancel: vi.fn() })
  await screen.getByRole('button', { name: /confirm/i }).click()
  expect(onconfirm).toHaveBeenCalledOnce()
})

test('fires oncancel when Cancel clicked', async () => {
  const oncancel = vi.fn()
  const screen = render(DiffView, { diff: [], onconfirm: vi.fn(), oncancel })
  await screen.getByRole('button', { name: /cancel/i }).click()
  expect(oncancel).toHaveBeenCalledOnce()
})

test('shows validation error when provided', async () => {
  const screen = render(DiffView, { diff: [], validationError: 'missing title field', onconfirm: vi.fn(), oncancel: vi.fn() })
  await expect.element(screen.getByText(/missing title field/i)).toBeVisible()
})
```

**GREEN:**
- [ ] Create `src/components/DiffView.svelte`
  - Props: `diff: DiffLine[]`, `validationError?: string`, `onconfirm: () => void`, `oncancel: () => void`
  - Renders inline in council pane, replacing agent columns while diff is pending
  - Removed lines: struck-through; added lines: highlighted
  - Confirm / Cancel buttons in names-bar area
- [ ] Tests pass

### 4.7 `amendment/validate.ts`

**RED:**
```ts
// src/lib/amendment/__tests__/validate.test.ts

test('validateSection calls make validate via platform.exec', async () => {
  const mockPlatform = {
    exec: vi.fn().mockResolvedValue({ code: 0, stdout: 'All checks passed', stderr: '' })
  }
  const result = await validateSection(mockPlatform as any)
  expect(mockPlatform.exec).toHaveBeenCalledWith('make', ['validate'])
  expect(result.valid).toBe(true)
})

test('returns valid:false and errors when exit code non-zero', async () => {
  const mockPlatform = {
    exec: vi.fn().mockResolvedValue({
      code: 1, stdout: '',
      stderr: 'ERROR: Section rights.dignity missing required field: title'
    })
  }
  const result = await validateSection(mockPlatform as any)
  expect(result.valid).toBe(false)
  expect(result.errors).toContain('missing required field')
})
```

**GREEN:**
- [ ] Create `src/lib/amendment/validate.ts`
  - `validateSection(platform): Promise<{ valid: boolean; errors?: string }>`
  - Calls `make validate` via `platform.exec()`
- [ ] Tests pass

### 4.8 `amendment/commit.ts`

**RED:**
```ts
// src/lib/amendment/__tests__/commit.test.ts

test('commitAmendment sequences: writeFile → validate → git add → git commit → rev-parse', async () => {
  const calls: string[] = []
  const mockPlatform = {
    writeFile: vi.fn().mockResolvedValue(undefined),
    exec: vi.fn().mockImplementation((cmd: string, args: string[]) => {
      calls.push(`${cmd} ${args.join(' ')}`)
      return Promise.resolve({ code: 0, stdout: 'abc123', stderr: '' })
    }),
  }
  await commitAmendment(mockPlatform as any, {
    sectionPath: 'sections/02-rights/dignity.md',
    content: '---\nid: rights.dignity\n---',
    message: 'amend: update §rights.dignity',
  })
  expect(mockPlatform.writeFile).toHaveBeenCalledBefore(mockPlatform.exec)
  expect(calls.some(c => c.includes('make validate'))).toBe(true)
  expect(calls.some(c => c.includes('git add'))).toBe(true)
  expect(calls.some(c => c.includes('git commit'))).toBe(true)
  expect(calls.some(c => c.includes('rev-parse'))).toBe(true)
})

test('validate runs before git commit', async () => {
  const calls: string[] = []
  const mockPlatform = {
    writeFile: vi.fn().mockResolvedValue(undefined),
    exec: vi.fn().mockImplementation((cmd: string, args: string[]) => {
      calls.push(`${cmd} ${args.join(' ')}`)
      return Promise.resolve({ code: 0, stdout: 'abc123', stderr: '' })
    }),
  }
  await commitAmendment(mockPlatform as any, { sectionPath: '...', content: '...', message: '...' })
  const validateIdx = calls.findIndex(c => c.includes('make validate'))
  const commitIdx = calls.findIndex(c => c.includes('git commit'))
  expect(validateIdx).toBeLessThan(commitIdx)
})

test('aborts and rejects if validation fails', async () => {
  const mockPlatform = {
    writeFile: vi.fn().mockResolvedValue(undefined),
    exec: vi.fn().mockResolvedValueOnce({ code: 1, stdout: '', stderr: 'validation error' }),
  }
  await expect(
    commitAmendment(mockPlatform as any, { sectionPath: '...', content: '...', message: '...' })
  ).rejects.toThrow(/validation/i)
})

test('returns commit hash on success', async () => {
  const mockPlatform = {
    writeFile: vi.fn().mockResolvedValue(undefined),
    exec: vi.fn()
      .mockResolvedValueOnce({ code: 0, stdout: '', stderr: '' })      // make validate
      .mockResolvedValueOnce({ code: 0, stdout: '', stderr: '' })      // git add
      .mockResolvedValueOnce({ code: 0, stdout: '', stderr: '' })      // git commit
      .mockResolvedValueOnce({ code: 0, stdout: 'abc123\n', stderr: '' }), // git rev-parse HEAD
  }
  const result = await commitAmendment(mockPlatform as any, { sectionPath: '...', content: '...', message: '...' })
  expect(result.hash).toBe('abc123')
})
```

**GREEN:**
- [ ] Create `src/lib/amendment/commit.ts`
  - `commitAmendment(platform, { sectionPath, content, message }): Promise<{ hash: string }>`
  - Sequence: `writeFile` → `make validate` → `git add` → `git commit` → `git rev-parse HEAD`
  - Aborts with rejection if validation fails — never commits invalid section bundles
- [ ] Tests pass

### 4.9 Wire apply flow in App.svelte

- [ ] Pass `onapply` handler to `CouncilPanel`; on fire: pre-fill input bar with `"Apply [agentName]'s proposal"` and set mode to `apply`
- [ ] When mode is `apply` and user submits: invoke `invokeEditor` (not `dispatchToCouncil`); collect streamed response as proposed text
- [ ] After stream completes: call `computeDiff(originalSectionText, proposedText)` and switch council pane to `DiffView`
- [ ] On `DiffView` confirm: call `commitAmendment`, reload section text, reset council state
- [ ] On `DiffView` cancel: restore council columns, leave input bar with apply instruction intact
- [ ] If `commitAmendment` rejects due to validation: pass `validationError` to `DiffView` without closing it — let user send another instruction or cancel

### 4.10 Integration verification

- [ ] Apply button appears in names bar chip after agent finishes streaming; absent while streaming
- [ ] Clicking Apply pre-fills input bar with `"Apply [agentName]'s proposal"` and sets mode to `apply`
- [ ] Submitting in apply mode invokes editor model, not full council broadcast
- [ ] Diff replaces council columns; removed lines struck through, added lines highlighted
- [ ] Confirm writes file, runs `make validate`, commits, reloads section, resets council pane
- [ ] Cancel restores council columns without writing
- [ ] Validate failure shows error in diff pane; user can retry or cancel
- [ ] `npm test -- --run` passes (all tests)

---

## Milestone 5 — Kiosk mode (installation-ready)

> Goal: Gallery-ready: full-screen kiosk, moderation agent, local fork commit + rebuild, cost ledger, consent modal, idle state.

### 5.1 Kiosk config loading

**RED:**
```ts
// src/lib/config/__tests__/kiosk.test.ts

test('loadKioskConfig loads from terminal-config.json', async () => {
  const mockPlatform = {
    readFile: vi.fn().mockResolvedValue(JSON.stringify({
      mode: 'kiosk',
      repo_path: '/path/to/fork',
      council: [
        { model: 'claude-haiku-3', provider: 'anthropic', label: 'Claude' },
      ],
      session_timeout_minutes: 5,
    }))
  }
  const config = await loadKioskConfig(mockPlatform, '/path/to/terminal-config.json')
  expect(config.mode).toBe('kiosk')
  expect(config.council).toHaveLength(1)
  expect(config.session_timeout_minutes).toBe(5)
})

test('kiosk config overrides default config', async () => {
  // Ensures kiosk values take precedence over defaults
})
```

**GREEN:**
- [ ] Extend `src/lib/config/loader.ts` to support kiosk config file path
- [ ] `loadKioskConfig(platform, path)` reads and parses the JSON file
- [ ] Merges with defaults (kiosk values override)
- [ ] Tests pass

### 5.2 Moderation agent

This is the most consequential single agent in the system.

**RED:**
```ts
// src/lib/amendment/__tests__/moderation.test.ts

test('approves a legitimate amendment', async () => {
  const mockProvider = mockProvider('Moderator', [
    { content: '{"approved": true, "reason": "Adds meaningful clause within scope"}', done: true },
  ])
  const result = await moderateAmendment(mockProvider, {
    section: mockSection,
    proposedText: 'We recognize collective dignity alongside individual dignity.',
  })
  expect(result.approved).toBe(true)
})

test('rejects an amendment that corrupts governance', async () => {
  const mockProvider = mockProvider('Moderator', [
    { content: '{"approved": false, "reason": "Attempts to remove amendment process"}', done: true },
  ])
  const result = await moderateAmendment(mockProvider, {
    section: mockSection,
    proposedText: 'This document may never be changed.',
  })
  expect(result.approved).toBe(false)
  expect(result.reason).toContain('amendment process')
})

test('rejects bad-faith input', async () => {
  // Test: advertising, harassment, ideology injection
})

test('moderation prompt references Covenant harm provisions', () => {
  const prompt = buildModerationPrompt(mockSection, 'proposed text')
  expect(prompt).toContain('harm')
  expect(prompt).toContain('amendment')
  // Should reference specific sections
})

test('moderation returns structured JSON', async () => {
  // Even on edge cases, the moderation agent returns parseable JSON
})
```

**GREEN:**
- [ ] Create `src/lib/amendment/moderation.ts`
  - `moderateAmendment(provider, params): Promise<ModerationResult>`
  - `ModerationResult`: `{ approved: boolean, reason: string }`
  - Prompt asks the model to check against harm provisions, governance corruption, and bad-faith input
  - Returns structured JSON (with fallback parsing if model doesn't produce clean JSON)
  - Single-model check (not full council — cost-efficient for gallery)
- [ ] Tests pass

### 5.3 Local fork commit + rebuild trigger

**RED:**
```ts
// src/lib/amendment/__tests__/kiosk-commit.test.ts

test('kiosk commit writes file, validates, commits, and triggers rebuild', async () => {
  const calls: string[] = []
  const mockPlatform = {
    exec: vi.fn().mockImplementation((cmd, args) => {
      calls.push(`${cmd} ${args.join(' ')}`)
      return { code: 0, stdout: '', stderr: '' }
    }),
    writeFile: vi.fn().mockResolvedValue(undefined),
  }

  await kioskCommitAmendment(mockPlatform, {
    sectionPath: 'sections/02-rights/dignity.md',
    newContent: '...',
    message: 'Visitor amendment to §rights.dignity',
    rebuildCommand: 'make compose',
  })

  expect(calls).toContain(expect.stringContaining('make validate'))
  expect(calls).toContain(expect.stringContaining('git commit'))
  expect(calls).toContain(expect.stringContaining('make compose'))
})

test('rebuild runs after successful commit', async () => {
  // Verify ordering: validate → commit → rebuild
})

test('does not rebuild if commit fails', async () => {
  // Simulate commit failure → rebuild should not run
})
```

**GREEN:**
- [ ] Create `src/lib/amendment/kiosk-commit.ts` (or extend `commit.ts`)
  - Full sequence: write file → validate → commit → rebuild (`make compose`)
  - The rebuild triggers the projection update (the projected Covenant text refreshes)
  - Attribution: commit message includes session ID or "gallery visitor" (per config)
- [ ] Tests pass

### 5.4 Cost ledger

**RED:**
```ts
// src/lib/cost/__tests__/ledger.test.ts

test('logApiCall appends to ledger', async () => {
  const entries: CostEntry[] = []
  const mockPlatform = {
    logApiCall: vi.fn().mockImplementation((entry) => entries.push(entry))
  }
  const ledger = createLedger(mockPlatform)
  await ledger.log({
    timestamp: Date.now(),
    provider: 'openrouter',
    model: 'claude-haiku-3',
    tokens_in: 500,
    tokens_out: 200,
    estimated_kwh: 0.0001,
    estimated_water_ml: 0.05,
  })
  expect(entries).toHaveLength(1)
})

test('ledger computes session totals', () => {
  const ledger = createLedger(mockPlatform)
  ledger.log(entry1)
  ledger.log(entry2)
  const totals = ledger.sessionTotals()
  expect(totals.total_tokens).toBe(entry1.tokens_in + entry1.tokens_out + entry2.tokens_in + entry2.tokens_out)
  expect(totals.total_kwh).toBeGreaterThan(0)
})

test('ledger writes to file via platform', async () => {
  // Verifies the ledger persists to the cost log file specified in kiosk config
})
```

**GREEN:**
- [ ] Create `src/lib/cost/types.ts` — `CostEntry`, `SessionTotals`
- [ ] Create `src/lib/cost/ledger.ts`
  - `createLedger(platform)` — creates a ledger that logs via `platform.logApiCall()`
  - `.log(entry)` — appends an entry
  - `.sessionTotals()` — computes aggregates (total tokens, kWh, water)
  - Feeds into the Material Cost Display on the west wall
- [ ] Tests pass

### 5.5 ConsentModal component

**RED:**
```ts
// src/components/__tests__/ConsentModal.test.ts

test('renders consent text', async () => {
  const screen = render(ConsentModal, {
    text: 'This terminal records your interactions...',
  })
  await expect.element(screen.getByText(/records your interactions/)).toBeVisible()
})

test('dismiss button closes modal', async () => {
  const onDismiss = vi.fn()
  const screen = render(ConsentModal, { text: '...', ondismiss: onDismiss })
  await screen.getByRole('button', { name: /continue|accept/i }).click()
  expect(onDismiss).toHaveBeenCalled()
})

test('modal blocks interaction until dismissed', async () => {
  const screen = render(ConsentModal, { text: '...' })
  // Modal should have role="dialog" and aria-modal="true"
  const dialog = screen.container.querySelector('[role="dialog"]')
  expect(dialog).not.toBeNull()
  expect(dialog?.getAttribute('aria-modal')).toBe('true')
})
```

**GREEN:**
- [ ] Create `src/components/ConsentModal.svelte`
  - Accessible modal (`role="dialog"`, `aria-modal="true"`, focus trap)
  - Consent text (configurable, matches gallery signage)
  - Continue/Accept button
  - Emits `ondismiss` event
- [ ] Tests pass

### 5.6 WaitingState component

**RED:**
```ts
// src/components/__tests__/WaitingState.test.ts

test('renders scrolling Ritual text', async () => {
  const screen = render(WaitingState, {
    sections: [mockSection],
  })
  // Should display Ritual register text
  await expect.element(screen.getByText(/edge of their strength/)).toBeVisible()
})

test('emits wake event on interaction', async () => {
  const onWake = vi.fn()
  const screen = render(WaitingState, { sections: [mockSection], onwake: onWake })
  await screen.container.click()
  expect(onWake).toHaveBeenCalled()
})
```

**GREEN:**
- [ ] Create `src/components/WaitingState.svelte`
  - Full-screen display of slowly scrolling Ritual text (auto-scrolls through sections)
  - Dark/gallery mode styling
  - Any interaction (click, touch, keypress) triggers `onwake` event
  - Pacing: slow, deliberate animation matching the document's gravity
- [ ] Tests pass

### 5.7 KioskView wrapper

**RED:**
```ts
// src/components/__tests__/KioskView.test.ts

test('shows WaitingState initially', async () => {
  const screen = render(KioskView, { config: kioskConfig, sections: mockSections })
  // WaitingState should be visible
  await expect.element(screen.getByText(/edge of their strength/)).toBeVisible()
})

test('shows ConsentModal on first interaction', async () => {
  const screen = render(KioskView, { config: kioskConfig, sections: mockSections })
  // Touch/click to wake
  await screen.container.click()
  // Consent modal should appear
  await expect.element(screen.getByRole('dialog')).toBeVisible()
})

test('shows reader after consent dismissed', async () => {
  const screen = render(KioskView, { config: kioskConfig, sections: mockSections })
  await screen.container.click()
  await screen.getByRole('button', { name: /continue/i }).click()
  // Reader view should now be visible
  await expect.element(screen.getByRole('searchbox')).toBeVisible()
})

test('returns to WaitingState after timeout', async () => {
  vi.useFakeTimers()
  const config = { ...kioskConfig, session_timeout_minutes: 1 }
  const screen = render(KioskView, { config, sections: mockSections })
  // Activate
  await screen.container.click()
  await screen.getByRole('button', { name: /continue/i }).click()
  // Advance time past timeout
  vi.advanceTimersByTime(60 * 1000 + 1)
  // Should return to WaitingState
  vi.useRealTimers()
})
```

**GREEN:**
- [ ] Create `src/views/KioskView.svelte`
  - State machine: `waiting` → (interaction) → `consent` → (dismiss) → `active` → (timeout) → `waiting`
  - No window chrome (full-screen, CSS hides OS elements where possible)
  - Forces dark/gallery mode
  - Session timeout: resets after configurable inactivity period
  - Clears chat history on reset
  - No settings UI (all configured via `terminal-config.json`)
- [ ] Tests pass

### 5.8 Kiosk amendment flow (end-to-end)

- [ ] Wire the full kiosk amendment flow:
  1. Visitor proposes amendment in Amend mode
  2. Council drafts versions
  3. Visitor selects/edits
  4. Moderation agent checks the proposal
  5. If approved: kiosk commit + rebuild (projected text updates)
  6. If rejected: display rejection reason in the same honest register
  7. Cost entry logged for every API call in the flow

### 5.9 Integration verification

- [ ] Launch in kiosk mode (`--kiosk /path/to/config.json` or env var)
- [ ] WaitingState scrolls Ritual text in dark mode
- [ ] Touch/click → consent modal → reader
- [ ] Full amendment flow: propose → council → moderate → commit → rebuild
- [ ] Rejected amendment: clear, honest explanation
- [ ] Session timeout returns to WaitingState
- [ ] Cost ledger accumulates entries
- [ ] `npm test` — all tests pass

---

## Milestone 6 — Web deployment

> Goal: The same app runs in a browser (no Tauri). SvelteKit static build. Platform-web implementation.

### 6.1 Web platform implementation

**RED:**
```ts
// src/lib/__tests__/platform-web.test.ts

test('readFile fetches from GitHub raw API', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(
    new Response('---\nid: test\n---\n# Ritual\nHello')
  ))
  const platform = new WebPlatform({ repoOwner: 'owner', repoName: 'covenant', branch: 'main' })
  const content = await platform.readFile('sections/00-preamble/preamble.md')
  expect(content).toContain('# Ritual')
})

test('exec returns error stub', async () => {
  const platform = new WebPlatform({})
  const result = await platform.exec('git', ['status'])
  expect(result.code).toBe(1)
  expect(result.stderr).toContain('not available')
})

test('saveConfig uses localStorage', async () => {
  const platform = new WebPlatform({})
  await platform.saveConfig({ mode: 'web' } as any)
  expect(localStorage.getItem('terminal-config')).toContain('web')
})

test('loadConfig reads from localStorage', async () => {
  localStorage.setItem('terminal-config', JSON.stringify({ mode: 'web' }))
  const platform = new WebPlatform({})
  const config = await platform.loadConfig()
  expect(config.mode).toBe('web')
})

test('logApiCall stores in memory', async () => {
  const platform = new WebPlatform({})
  await platform.logApiCall({ tokens_in: 100 } as any)
  // In-memory store; no file system access
})
```

**GREEN:**
- [ ] Create `src/lib/platform-web.ts` implementing `Platform`
  - `readFile()`: fetches from GitHub raw content API (`raw.githubusercontent.com/...`)
  - `listSections()`: fetches repo tree via GitHub API or uses a pre-built manifest
  - `exec()`: returns error stub — shell not available in browser
  - `loadConfig()` / `saveConfig()`: localStorage
  - `logApiCall()`: in-memory array
- [ ] Wire `getPlatform()` to return `WebPlatform` when `window.__TAURI__` is absent
- [ ] Tests pass

### 6.2 SvelteKit wrapper

- [ ] `npm install @sveltejs/kit @sveltejs/adapter-static`
- [ ] Create `svelte.config.js` (adapter-static, SPA mode)
- [ ] Create `src/routes/+layout.ts`: `export const ssr = false; export const prerender = false;`
- [ ] Create `src/routes/+page.svelte`: imports existing `App.svelte` root component
- [ ] Verify: `npm run build` produces a static SPA in `/build/`
- [ ] Verify: serving the static build loads the Terminal with web platform

### 6.3 Web amendment path

**RED:**
```ts
// src/lib/amendment/__tests__/web-submit.test.ts

test('web submission generates GitHub issue URL', () => {
  const url = buildGitHubIssueURL({
    repoOwner: 'owner',
    repoName: 'covenant',
    sectionId: 'rights.dignity',
    proposedText: 'Amendment text...',
    councilResponses: ['Claude said...', 'GPT said...'],
  })
  expect(url).toContain('github.com/owner/covenant/issues/new')
  expect(url).toContain('rights.dignity')
})

test('web submission generates pre-filled PR URL', () => {
  // Similar, for PR template
})
```

**GREEN:**
- [ ] Create `src/lib/amendment/web-submit.ts`
  - `buildGitHubIssueURL(params)` — generates a pre-filled GitHub issue URL with section ID, proposed text, and council responses
  - `buildGitHubPRURL(params)` — similar, for PR template
  - Opens in new tab when user clicks "Submit Amendment"
- [ ] Tests pass

### 6.4 API key setup flow (web)

**RED:**
```ts
test('first-time setup shows API key entry screen', async () => {
  // No saved config in localStorage
  localStorage.clear()
  const screen = render(App)
  await expect.element(screen.getByText(/api key|get started/i)).toBeVisible()
})

test('after key entry, proceeds to reader', async () => {
  localStorage.clear()
  const screen = render(App)
  await screen.getByLabelText(/openrouter/i).fill('sk-test')
  await screen.getByRole('button', { name: /continue|save/i }).click()
  // Reader should now be visible
  await expect.element(screen.getByRole('searchbox')).toBeVisible()
})
```

**GREEN:**
- [ ] Add first-time setup detection to `App.svelte` — if no API key configured, show setup screen before reader
- [ ] Setup screen: OpenRouter account link, API key entry, model selection
- [ ] After setup, proceed to reader (config saved to localStorage)
- [ ] Tests pass

### 6.5 Integration verification

- [ ] `npm run build` produces a static SPA
- [ ] Deploy to a local server (`npx serve build/`)
- [ ] First visit: setup screen → API key entry → reader
- [ ] Read sections (fetched from GitHub)
- [ ] Ask questions → council responds
- [ ] Amend mode → generates GitHub issue URL
- [ ] Settings persist across page reloads (localStorage)
- [ ] No Tauri errors in console (platform detection works correctly)
- [ ] `npm test` — all tests pass

---

## Cross-cutting concerns

These are not milestone-bound — they apply throughout development.

### Accessibility

- [ ] All interactive elements have `role` and `aria-*` attributes
- [ ] Tab navigation works through all views
- [ ] Screen reader announces section changes, streaming state, modal open/close
- [ ] Color contrast meets WCAG AA (especially in dark/gallery mode)
- [ ] Focus management: modal trap, restore focus on close

### Error handling

- [ ] Network errors: show clear message, do not crash
- [ ] API errors (401, 429, 500): show provider-specific guidance
- [ ] Parse errors: malformed section files logged and skipped, not fatal
- [ ] Platform errors: meaningful fallback messages for web stubs

### Performance

- [ ] Sections loaded lazily (not all 30 on startup)
- [ ] Streaming responses rendered incrementally (no full-rerender per chunk)
- [ ] Font loading: FOUT strategy with system font fallback
- [ ] Bundle size: monitor with Vite's `build --report`

---

*This task list corresponds to `docs/plan.md`. Tasks are designed for red/green TDD with Vitest. Test code in RED blocks is illustrative — actual test code should be adapted to the real API surfaces as they emerge.*

---

## Log

- 2026-03-11: M0–M3 complete. 114 tests passing across 20 test files. Key deviations from original plan:
  - `platform-tauri.ts` had an infinite recursion bug (`_getRepoPath()` → `loadConfig()` → `readFile()` → `_getRepoPath()`); fixed by caching the resolved path and using `readTextFile` directly in `loadConfig`.
  - `saveConfig` required `mkdir({ recursive: true })` before writing — not in original plan.
  - Vite `loadEnv` needs the parent directory (`resolve(__dirname, '..')`) to find `.env` at repo root.
  - Svelte 5 `state_referenced_locally` warnings fixed by wrapping prop-seeded `$state()` initializers in `untrack()` — added to `AGENTS.md` as a known pitfall.
  - `vitest-browser-svelte` `screen.getByText()` queries the whole page, not just the render container — tests with common labels need `cleanup()` in `afterEach`. Documented in `AGENTS.md`.
  - `SettingsView.svelte` ended up in `src/components/` (not `src/views/`) for consistency with other components. Plan shows both locations; `components/` was used.
  - M3.8 live multi-agent integration test not performed (requires live API keys). All unit/component tests pass.
- 2026-03-12: M3 quality pass complete. 169 tests passing across 25 test files. Changes:
  - `prompts.ts` added (new module, not in original plan): `CouncilMode` extended to `'ask' | 'challenge' | 'review'`; three distinct system prompt blocks designed from scratch rather than adapted from the batch review prompts. `IDENTITY` block frames the agent as deeply familiar with the Covenant and an addressee — knowledge without critique posture. `MODE_ASK` is a reader-guide mode (help someone understand the text). `MODE_REVIEW` carries the full co-author/addressee/standing framing with assess/propose structure, drawn from `prompts/agent_review_batch.md`. `MODE_CHALLENGE` unchanged from prior design.
  - `conversation-log.ts` added (new module, not in original plan): JSONL append logging of every council query. `appendConversationLog(platform, entry)` swallows all errors so logging never breaks the query flow. 7 unit tests.
  - `InputBar.svelte` default modes updated to `['ask', 'challenge', 'review']`.
  - `App.svelte` wired to call `appendConversationLog` (non-blocking) after all streams drain.
  - `prompts.test.ts` updated: 18 tests covering all three modes.
- 2026-03-12: Write modes added (ritual, spec, parable). 176 tests passing across 25 test files. Changes:
  - `prompts.ts`: `CouncilMode` extended to include `'ritual' | 'spec' | 'parable'`. Three new craft-guide blocks added: `MODE_WRITE_RITUAL` (curated excerpt from `docs/good_ritual_writing_guide.md` — concrete anchor rule, no-hedge rule, forbidden vocabulary, editing checklist, reliable patterns, anti-patterns), `MODE_WRITE_SPEC` (excerpt from `docs/style_guide.md` §2.3 — MUST/SHOULD/MAY semantics, formatting rules, enforcement linkage, rationale linkage), `MODE_WRITE_PARABLE` (full `docs/good_parable_writing_guide.md` content — folktale imagery, narrative techniques, anti-patterns).
  - `InputBar.svelte`: `modes` prop now accepts `Array<string | ModeGroup>`. Default changed to two optgroups — "Read" (ask/challenge/review) and "Write" (ritual/spec/parable). Flat string arrays still work (backward compatible with existing tests).
  - `App.svelte`: mode type casts updated to include all six modes.
  - `prompts.test.ts`: 7 new tests for the three write modes (RED/GREEN cycle).
  - `CouncilPanel.svelte`: added sticky `names-bar` above scrollable `agent-columns`. Each chip has tint-colored left border, agent name, and pulsing `§` while streaming. `AgentColumn.svelte` `.agent-header` removed; CouncilPanel names bar owns the agent name display. App toolbar stripped to close button only.
- 2026-03-12: M4 redesigned. Old M4 task list (structured amendment drafting + ProposalComparison + highlight-to-accept + export) replaced with new design based on steward conversation. New design: Apply button in names bar chip → editor model invocation → inline diff in council pane → Confirm/Cancel → writeFile + make validate + git commit. Key decisions recorded: editor model = config.council[0]; diff replaces council columns while pending; converse-to-apply deferred; highlight-and-annotate deferred to M4.5/M5; single-chat/controller model vision documented in plan.md open questions. Tasks 4.1–4.10 rewritten to match new design.
