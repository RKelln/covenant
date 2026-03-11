# Covenant Terminal — Task Lists

> **What this document is:** Detailed, ordered task lists for each milestone in `docs/terminal-plan.md`, designed for red/green TDD with Vitest.
>
> **How to read it:** Each task starts with the test(s) you write first (RED), then the implementation that makes them pass (GREEN). Tasks within a milestone are ordered by dependency — later tasks assume earlier ones are done. Refactoring steps appear where natural.

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

## Milestone 0 — Project scaffold

> Goal: A Tauri + Svelte 5 + Vite + TypeScript project that builds, runs, and has a passing test suite with zero application code.

### 0.1 Initialize the Tauri project

- [ ] Run `npm create tauri-app@latest` (or manual scaffold) in `terminal/`
- [ ] Choose: Svelte, TypeScript, Vite
- [ ] Verify: `npm run tauri dev` launches a window with the default template

### 0.2 Strip template, configure TypeScript

- [ ] Remove template boilerplate (default Svelte component, CSS, assets)
- [ ] Configure `tsconfig.json`: strict mode, path aliases (`$lib` → `src/lib`)
- [ ] Create empty `App.svelte` that renders a placeholder
- [ ] Verify: `npm run tauri dev` still builds and runs

### 0.3 Install and configure Vitest

- [ ] `npm install -D vitest vitest-browser-svelte @vitest/browser playwright`
- [ ] Create `vitest.config.ts`:
  ```ts
  import { defineConfig } from 'vitest/config'
  import { svelte } from '@sveltejs/vite-plugin-svelte'

  export default defineConfig({
    plugins: [svelte()],
    test: {
      setupFiles: ['vitest-browser-svelte'],
      browser: {
        enabled: true,
        provider: 'playwright',
        name: 'chromium',
      },
      include: ['src/**/*.test.ts'],
    },
  })
  ```
- [ ] Write a trivial passing test (`src/lib/__tests__/smoke.test.ts`):
  ```ts
  import { test, expect } from 'vitest'
  test('vitest is configured', () => { expect(1 + 1).toBe(2) })
  ```
- [ ] Add `"test"` script to `package.json`
- [ ] Verify: `npm test` runs and passes

### 0.4 Add static assets

- [ ] Copy Cormorant Garamond font files into `terminal/static/fonts/`
- [ ] Create `src/styles/tokens.css` (empty or with a single CSS custom property)
- [ ] Create `src/styles/typography.css` (font-face declarations for Cormorant Garamond)
- [ ] Create `src/styles/global.css` (minimal reset, imports tokens + typography)
- [ ] Import `global.css` in `main.ts`
- [ ] Verify: app renders with the correct typeface

### 0.5 Add Tauri plugins

- [ ] Install Tauri plugins: `@tauri-apps/plugin-fs`, `@tauri-apps/plugin-shell`
- [ ] Add plugins to `src-tauri/Cargo.toml` and `tauri.conf.json` capabilities
- [ ] Verify: `npm run tauri dev` still launches (plugins registered but not yet used)

---

## Milestone 1 — Readable document (MVP)

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
- [ ] Create `src/lib/platform.ts` with the `Platform` interface (as spec'd in the plan)
- [ ] Create `src/lib/types.ts` for shared types: `SectionMeta`, `ExecResult`, `TerminalConfig`, `CostEntry`
- [ ] Export a `getPlatform()` function that detects `window.__TAURI__` and returns the appropriate implementation
- [ ] Tests pass (type-level assertions)

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
- [ ] Create `src/lib/platform-tauri.ts` implementing `Platform` using `@tauri-apps/plugin-fs` and `@tauri-apps/plugin-shell`
- [ ] Wire `getPlatform()` to return `TauriPlatform` when `window.__TAURI__` exists
- [ ] Tests pass against mocked IPC

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
- [ ] Create `src/lib/covenant/types.ts` with `Section`, `SectionFrontmatter`, `SectionCategory`, `Register` types
- [ ] Types match the actual Covenant section bundle format (YAML frontmatter fields + four register headings)
- [ ] Tests pass

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
- [ ] Create `src/lib/covenant/parser.ts`
- [ ] Implement `parseSection(raw: string): Section`
  - Parse YAML frontmatter (use a lightweight YAML parser or hand-roll for the simple schema)
  - Split content by `# Ritual`, `# Spec`, `# Digest`, `# Log` headings
  - Trim whitespace, handle missing registers with empty strings
  - Validate required fields (`id`, `title`, `status`)
- [ ] All parser tests pass

**REFACTOR:**
- [ ] Extract frontmatter parsing into a separate `parseFrontmatter()` function if it's complex enough
- [ ] Consider whether to use `yaml` package or hand-parse (the frontmatter schema is simple and fixed)

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
- [ ] Create `src/lib/covenant/loader.ts`
- [ ] Implement `loadAllSections(platform: Platform): Promise<Section[]>`
- [ ] Implement `loadSection(platform: Platform, id: string): Promise<Section>`
- [ ] Implement `loadSectionsByCategory(platform: Platform): Promise<Record<string, Section[]>>`
- [ ] All loader tests pass

### 1.6 CSS design tokens and typography

No unit tests — this is a visual/structural task. Verified by inspection and the component tests that follow.

- [ ] Populate `src/styles/tokens.css`:
  - Color tokens: `--color-ivory: #fdfcfa`, `--color-charcoal: #2a2a2a`, `--color-rule: ...`, etc.
  - Type scale: 4-step scale from `docs/design.md`
  - Spacing scale
  - Separator tokens (hairline rule width, § character styling)
- [ ] Populate `src/styles/typography.css`:
  - `@font-face` for Cormorant Garamond (regular, italic, semibold)
  - `.register-ritual` — Cormorant, italic, larger line height
  - `.register-spec` — system UI sans-serif, tighter
  - `.register-digest` — system UI, muted color
- [ ] Populate `src/styles/global.css`:
  - Box-sizing reset
  - Import tokens + typography
  - Default body styles matching `docs/design.md`
  - Gallery dark mode variant (CSS custom properties swap under `[data-theme="dark"]`)

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
- [ ] Create `src/components/SectionNav.svelte`
  - Props: `sections: SectionMeta[]`, `selected?: string`
  - Events: `onselect(id: string)`
  - Groups sections by category (derived from the `NN-name` prefix)
  - Search input filters by title (case-insensitive substring match)
  - Status indicator (draft/stable badge or icon)
  - Uses design tokens (Cormorant for section titles, system UI for chrome)
  - § separator between category groups
- [ ] All SectionNav tests pass

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
- [ ] Create `src/components/SectionView.svelte`
  - Props: `section: Section`, `defaultRegister?: 'ritual' | 'spec' | 'complete'`
  - Tab bar: Ritual | Spec | Complete (uses `role="tab"` for accessibility)
  - Renders markdown to HTML (use a lightweight markdown renderer — `marked`, `markdown-it`, or hand-rolled for the subset needed)
  - Cross-reference syntax (`§[section.id]`) rendered as styled clickable spans
  - Emits event when a cross-reference is clicked (for navigation)
  - Typography: Ritual register uses `.register-ritual` styling, Spec uses `.register-spec`
  - § separator and hairline rules between registers in Complete view
- [ ] All SectionView tests pass

**REFACTOR:**
- [ ] Extract markdown rendering into `src/lib/covenant/render.ts` (pure function: markdown string → HTML string, with cross-reference handling)
- [ ] Write tests for the render function independently of the component

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
- [ ] Wire `App.svelte` to:
  - Call `loadSectionsByCategory()` on mount (using the platform instance)
  - Pass sections to `SectionNav`
  - Display selected section in `SectionView`
  - Handle cross-reference clicks (navigate to the referenced section)
- [ ] Create `src/main.ts` bootstrap: detect platform, initialize, mount `App.svelte`
- [ ] All app shell tests pass

### 1.10 Integration verification

- [ ] `npm run tauri dev` launches the Terminal with real Covenant sections loaded from disk
- [ ] Sidebar shows all 30 sections grouped by category
- [ ] Clicking a section shows its Ritual text
- [ ] Tab switching works (Ritual → Spec → Complete)
- [ ] Search filters sections
- [ ] Design language matches `docs/design.md` (typography, colors, § separators)
- [ ] `npm test` — all tests pass

---

## Milestone 2 — Single-agent Q&A

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
- [ ] Create `src/lib/agents/provider.ts` with:
  - `AgentProvider` interface (`name`, `chat(params) → AsyncIterable<ChatChunk>`, `models()`)
  - `ChatParams` type (model, messages, system, temperature, max_tokens)
  - `ChatChunk` type (content string, done boolean, optional metadata)
  - `Message` type (role: 'user' | 'assistant' | 'system', content: string)
  - `ModelInfo` type (id, name, provider, context_length)
- [ ] Tests pass

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
- [ ] Create `src/lib/agents/openrouter.ts`
  - Implements `AgentProvider`
  - `chat()` calls OpenRouter's `/api/v1/chat/completions` with `stream: true`
  - Parses SSE (`data: ...` lines) into `ChatChunk` objects
  - Yields chunks as an `AsyncIterable`
  - Handles errors (401, 429 rate limit, network failures)
  - `models()` calls OpenRouter's `/api/v1/models`
- [ ] All OpenRouter tests pass

**REFACTOR:**
- [ ] Extract SSE parsing into a reusable `parseSSE(reader: ReadableStreamDefaultReader): AsyncIterable<string>` utility — other providers (Copilot, direct APIs) use the same SSE format

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
- [ ] Create `src/lib/config/types.ts` — `TerminalConfig`, `ProviderConfig`, `CouncilMemberConfig`
- [ ] Create `src/lib/config/loader.ts` — `defaultConfig()`, `loadConfig(platform)`, `saveConfig(platform, config)`
- [ ] Tests pass

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
- [ ] Create `src/components/AgentColumn.svelte`
  - Props: `agentName: string`, `chunks: ChatChunk[]`, `streaming: boolean`, `tintColor?: string`
  - Concatenates chunk content into rendered text
  - Renders response text as markdown (reuse render utility from 1.8)
  - Shows animated § indicator while streaming
  - Left border tint for visual differentiation
- [ ] All AgentColumn tests pass

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
- [ ] Create `src/components/CouncilPanel.svelte`
  - Props: `agents: AgentState[]` (array of `{ name, chunks, streaming }` objects)
  - Renders one `AgentColumn` per agent
  - Shows empty state prompt when no agents are active
  - Collapsible (drawer behavior — for now, a simple show/hide toggle)
- [ ] Tests pass

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
- [ ] Create `src/components/InputBar.svelte`
  - Props: `sectionId: string`, `modes?: string[]` (default: `['ask', 'challenge']`)
  - Events: `onsubmit({ text, mode, sectionId })`
  - Text input, mode selector (dropdown or segmented control), submit button
  - Context indicator showing which section is in scope
  - Clears input on submit
  - Disabled state while agents are streaming
- [ ] Tests pass

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
- [ ] Create `src/lib/agents/chat.ts`
  - `sendQuery(provider, params): AsyncIterable<ChatChunk>` — thin wrapper that constructs the correct `ChatParams` and delegates to the provider
  - Adds system prompt (the Covenant co-author prompt) if not already present
  - Handles provider errors with structured error types
- [ ] Tests pass

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
- [ ] Create `src/views/SettingsView.svelte`
  - API key entry for each provider type (OpenRouter initially)
  - Model selection (dropdown populated from `provider.models()`)
  - Save button persists config via `platform.saveConfig()`
  - Validate API key (attempt a lightweight request on save)
  - Navigation back to reader view
- [ ] Tests pass

### 2.9 Wire Q&A into the reader view

- [ ] Update `App.svelte` / `ReaderView.svelte` to:
  - Show `InputBar` at the bottom
  - Show `CouncilPanel` (single agent) as a collapsible right panel or bottom drawer
  - On submit: construct messages (system prompt + section context + user question), call `sendQuery()`, pipe chunks into the `AgentColumn`
  - Handle streaming state (disable input, show § indicator)
- [ ] Add view switching: Reader ↔ Settings (simple state toggle or route)

### 2.10 Integration verification

- [ ] Enter an OpenRouter API key in Settings
- [ ] Select a model
- [ ] Navigate to a section, type a question, submit
- [ ] Watch streaming response appear in the council panel
- [ ] Try Challenge mode on a section
- [ ] `npm test` — all tests pass

---

## Milestone 3 — Council panel

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
- [ ] Create `src/lib/council/dispatch.ts`
  - `dispatchToCouncil(agents: CouncilAgent[], params: ChatParams): CouncilStream[]`
  - Each `CouncilStream` has: `providerName`, `stream: AsyncIterable<ChatChunk>`
  - All providers called simultaneously (not sequentially)
  - Individual provider errors are caught and surfaced as error chunks, not exceptions
- [ ] Tests pass

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
- [ ] Create `src/lib/council/stream.ts`
  - `createAgentStreamState(name: string): AgentStreamState`
  - Accumulates text from chunks
  - Tracks streaming/done/error state
  - This is the reactive state object that components bind to
- [ ] Tests pass

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
- [ ] Update `CouncilPanel.svelte` to render N agent columns side-by-side
- [ ] Responsive layout: 2-3 columns on wide screens, stacked on narrow
- [ ] Each column has a distinct tint from a predefined palette
- [ ] Tests pass

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
- [ ] Create `src/lib/council/synthesis.ts`
  - `synthesize(provider, responses, params): AsyncIterable<ChatChunk>`
  - Constructs a synthesis prompt that includes all council responses, asking the synthesizer to identify convergence, divergence, and implied decisions
  - Uses the synthesizer system prompt (conversational variant of `synthesizer-claude`)
- [ ] Tests pass

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
- [ ] Add synthesis section to `CouncilPanel.svelte` — appears below agent columns after all streams complete
- [ ] Collapsible (default collapsed, user can expand)
- [ ] Uses the same streaming render as agent columns
- [ ] Tests pass

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
- [ ] Create `src/lib/agents/copilot.ts` implementing `AgentProvider`
- [ ] Uses GitHub Copilot Chat API (OpenAI-compatible SSE format)
- [ ] Reuses the SSE parser from 2.2
- [ ] Tests pass

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
- [ ] Add roster management to `SettingsView.svelte`
  - List of configured council members (label, provider, model)
  - Add/remove agents
  - Reorder agents (drag or up/down buttons)
  - Each agent's system prompt is editable (advanced, collapsed by default)
  - Synthesis toggle (on/off, with model selector)
- [ ] Tests pass

### 3.8 Integration verification

- [ ] Configure 2-3 agents in Settings (e.g., Claude Haiku + GPT-4o mini via OpenRouter)
- [ ] Ask a question — all agents respond simultaneously in parallel columns
- [ ] Enable synthesis — synthesis appears after all agents finish
- [ ] Verify error handling: disable one agent's API key, ensure others still respond
- [ ] `npm test` — all tests pass

---

## Milestone 4 — Amendment workflow (contributor mode)

> Goal: Structured amendment drafting, section comparison UI, git integration.

### 4.1 Amend mode in InputBar

**RED:**
```ts
test('InputBar shows Amend mode option', async () => {
  const screen = render(InputBar, { sectionId: 'rights.dignity', modes: ['ask', 'challenge', 'amend'] })
  const selector = screen.getByRole('combobox')
  // Amend should be available
})

test('Amend mode emits with mode "amend"', async () => {
  const onSubmit = vi.fn()
  const screen = render(InputBar, {
    sectionId: 'rights.dignity',
    modes: ['ask', 'challenge', 'amend'],
    onsubmit: onSubmit,
  })
  // Select Amend mode, type amendment, submit
  await screen.getByRole('combobox').selectOptions(['amend'])
  await screen.getByRole('textbox').fill('I propose changing "dignity" to...')
  await screen.getByRole('button', { name: /send|submit/i }).click()
  expect(onSubmit).toHaveBeenCalledWith(expect.objectContaining({ mode: 'amend' }))
})
```

**GREEN:**
- [ ] Add `'amend'` to InputBar's mode options
- [ ] Amend mode adds structured context to the prompt (current section text + user's proposed change)
- [ ] Tests pass

### 4.2 Amendment drafting logic

**RED:**
```ts
// src/lib/amendment/__tests__/draft.test.ts

test('buildAmendmentPrompt includes section text and user proposal', () => {
  const prompt = buildAmendmentPrompt(
    mockSection,
    'I want to add a clause about collective dignity'
  )
  expect(prompt).toContain('rights.dignity')
  expect(prompt).toContain('edge of their strength') // section ritual text
  expect(prompt).toContain('collective dignity')      // user proposal
})

test('each council agent receives the amendment prompt', async () => {
  // Verifies dispatch sends the structured amendment prompt to all agents
})
```

**GREEN:**
- [ ] Create `src/lib/amendment/draft.ts`
  - `buildAmendmentPrompt(section: Section, proposal: string): Message[]`
  - Constructs a system+user message sequence that gives the agent the full section text and asks it to draft an amendment based on the user's proposal
  - Each council agent independently drafts its version
- [ ] Tests pass

### 4.3 Proposal comparison view

This is the "Future: Steward UI for Proposal Comparison" described in `docs/agent_reviews.md`.

**RED:**
```ts
// src/components/__tests__/ProposalComparison.test.ts

test('renders three columns: original + N agent drafts', async () => {
  const screen = render(ProposalComparison, {
    original: mockSection,
    proposals: [
      { agent: 'Claude', text: 'Amended ritual text from Claude...' },
      { agent: 'GPT', text: 'Amended ritual text from GPT...' },
    ],
  })
  await expect.element(screen.getByText('Original')).toBeVisible()
  await expect.element(screen.getByText('Claude')).toBeVisible()
  await expect.element(screen.getByText('GPT')).toBeVisible()
})

test('highlight-to-accept copies text to editor', async () => {
  // User selects text from one proposal → it appears in the edit area
})

test('export produces valid section bundle markdown', async () => {
  const onExport = vi.fn()
  const screen = render(ProposalComparison, {
    original: mockSection,
    proposals: [...],
    onexport: onExport,
  })
  await screen.getByRole('button', { name: /export/i }).click()
  const exported = onExport.mock.calls[0][0]
  // Exported string should be valid section markdown
  expect(exported).toContain('---')
  expect(exported).toContain('# Ritual')
})
```

**GREEN:**
- [ ] Create `src/components/ProposalComparison.svelte`
  - Multi-column layout: original section + one column per agent proposal
  - Highlight-to-accept: selecting text in a proposal column copies it to an editable draft area
  - Editable draft area: the user's final amended text
  - Export button: produces a valid section bundle `.md` string
- [ ] Tests pass

### 4.4 Validate integration

**RED:**
```ts
// src/lib/amendment/__tests__/validate.test.ts

test('validate calls make validate via platform.exec', async () => {
  const mockPlatform = {
    exec: vi.fn().mockResolvedValue({ code: 0, stdout: 'All checks passed', stderr: '' })
  }
  const result = await validateSection(mockPlatform)
  expect(mockPlatform.exec).toHaveBeenCalledWith('make', ['validate'])
  expect(result.valid).toBe(true)
})

test('reports validation errors', async () => {
  const mockPlatform = {
    exec: vi.fn().mockResolvedValue({
      code: 1,
      stdout: '',
      stderr: 'ERROR: Section rights.dignity missing required field: title'
    })
  }
  const result = await validateSection(mockPlatform)
  expect(result.valid).toBe(false)
  expect(result.errors).toContain('missing required field')
})
```

**GREEN:**
- [ ] Create `src/lib/amendment/validate.ts`
  - `validateSection(platform): Promise<ValidationResult>`
  - Calls `make validate` via `platform.exec()`
  - Parses output into structured result
- [ ] Tests pass

### 4.5 Git commit integration

**RED:**
```ts
// src/lib/amendment/__tests__/commit.test.ts

test('commitAmendment stages, commits, and returns hash', async () => {
  const mockPlatform = {
    exec: vi.fn()
      .mockResolvedValueOnce({ code: 0, stdout: '', stderr: '' })   // git add
      .mockResolvedValueOnce({ code: 0, stdout: '', stderr: '' })   // git commit
      .mockResolvedValueOnce({ code: 0, stdout: 'abc123', stderr: '' }) // git rev-parse HEAD
  }
  const result = await commitAmendment(mockPlatform, {
    sectionPath: 'sections/02-rights/dignity.md',
    message: 'amend: add collective dignity clause to §rights.dignity',
  })
  expect(result.hash).toBe('abc123')
  expect(mockPlatform.exec).toHaveBeenCalledTimes(3)
})

test('commitAmendment runs validate before committing', async () => {
  const calls: string[] = []
  const mockPlatform = {
    exec: vi.fn().mockImplementation((cmd, args) => {
      calls.push(`${cmd} ${args.join(' ')}`)
      return { code: 0, stdout: '', stderr: '' }
    })
  }
  await commitAmendment(mockPlatform, { sectionPath: '...', message: '...' })
  // make validate should come before git commit
  const validateIdx = calls.findIndex(c => c.includes('make validate'))
  const commitIdx = calls.findIndex(c => c.includes('git commit'))
  expect(validateIdx).toBeLessThan(commitIdx)
})

test('aborts if validation fails', async () => {
  const mockPlatform = {
    exec: vi.fn().mockResolvedValueOnce({ code: 1, stdout: '', stderr: 'validation error' })
  }
  await expect(commitAmendment(mockPlatform, { sectionPath: '...', message: '...' }))
    .rejects.toThrow(/validation/i)
})
```

**GREEN:**
- [ ] Create `src/lib/amendment/commit.ts`
  - `commitAmendment(platform, options): Promise<CommitResult>`
  - Sequence: write amended file → `make validate` → `git add` → `git commit` → return hash
  - Aborts if validation fails (never commits invalid section bundles)
  - Contributor mode: can also branch and push for PR workflow
- [ ] Tests pass

### 4.6 Integration verification

- [ ] In Amend mode: type a proposal, see council draft versions
- [ ] Proposal comparison view shows original + agent drafts side-by-side
- [ ] Edit the draft, export as section markdown
- [ ] Commit the amendment (git commit appears in repo)
- [ ] Verify `make validate` runs before commit
- [ ] `npm test` — all tests pass

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

*This task list corresponds to `docs/terminal-plan.md`. Tasks are designed for red/green TDD with Vitest. Test code in RED blocks is illustrative — actual test code should be adapted to the real API surfaces as they emerge.*
