import { test, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, cleanup } from 'vitest-browser-svelte'
import App from '../../App.svelte'

// Mock the platform module so tests never touch the filesystem or Tauri IPC
vi.mock('$lib/platform', () => ({
  initPlatform: vi.fn(),
  getPlatform: vi.fn(),
}))

const SAMPLE_SECTION = `---
id: preamble
title: "Preamble"
status: stable
since: 0.1.0
depends_on: []
terms_introduced: []
---

# Ritual

We begin here.

# Spec

The System MUST acknowledge its origins.

# Digest

The opening of the Covenant.

# Log

- 2025-01-01: Initial draft
`

const DIGNITY_SECTION = `---
id: rights.dignity
title: "Dignity"
status: draft
since: 0.2.0
depends_on: [preamble]
terms_introduced: [dignity]
---

# Ritual

You will meet people at the edge of their strength.

# Spec

The System MUST NOT degrade dignity.

# Digest

Dignity is the floor.

# Log

- 2025-01-15: Initial draft
`

function makeMockPlatform(overrides: Partial<{
  readFile: (path: string) => Promise<string>
  loadConfig: () => Promise<null>
  saveConfig: () => Promise<void>
  logApiCall: () => Promise<void>
}> = {}) {
  return {
    readFile: vi.fn().mockImplementation((path: string) => {
      if (path.includes('preamble')) return Promise.resolve(SAMPLE_SECTION)
      if (path.includes('dignity')) return Promise.resolve(DIGNITY_SECTION)
      return Promise.reject(new Error(`File not found: ${path}`))
    }),
    writeFile: vi.fn().mockResolvedValue(undefined),
    listSections: vi.fn().mockResolvedValue([]),
    exec: vi.fn().mockResolvedValue({ code: 0, stdout: '', stderr: '' }),
    loadConfig: vi.fn().mockResolvedValue(null),
    saveConfig: vi.fn().mockResolvedValue(undefined),
    loadModelCache: vi.fn().mockResolvedValue(null),
    saveModelCache: vi.fn().mockResolvedValue(undefined),
    logApiCall: vi.fn().mockResolvedValue(undefined),
    ...overrides,
  }
}

beforeEach(async () => {
  const { initPlatform } = await import('$lib/platform')
  vi.mocked(initPlatform).mockResolvedValue(makeMockPlatform())
})

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

test('renders section nav and first section after load', async () => {
  const screen = render(App)
  await expect.element(screen.getByRole('searchbox')).toBeVisible()
  // First section heading in the main pane (the <h1> in SectionView)
  await expect.element(screen.getByRole('heading', { name: 'Preamble' })).toBeVisible()
})

test('does not show a blank screen — loading state resolves', async () => {
  const screen = render(App)
  // Wait for loading to finish: the section heading appears only after loading = false
  await expect.element(screen.getByRole('heading', { name: 'Preamble' })).toBeVisible()
  // Loading indicator must be gone
  await expect.element(screen.container.querySelector('.loading')).not.toBeInTheDocument()
})

test('shows hard error when all section files fail to load', async () => {
  const { initPlatform } = await import('$lib/platform')
  vi.mocked(initPlatform).mockResolvedValue(makeMockPlatform({
    readFile: vi.fn().mockRejectedValue(new Error('Permission denied')),
  }))

  const screen = render(App)
  // Should show an error message, not a blank screen or endless spinner
  await expect.element(screen.getByText(/no sections could be loaded/i)).toBeVisible()
})

test('shows partial-failure banner when some files fail to load', async () => {
  const { initPlatform } = await import('$lib/platform')
  vi.mocked(initPlatform).mockResolvedValue(makeMockPlatform({
    readFile: vi.fn().mockImplementation((path: string) => {
      // Only preamble succeeds; everything else fails
      if (path.includes('preamble')) return Promise.resolve(SAMPLE_SECTION)
      return Promise.reject(new Error('File not found'))
    }),
  }))

  const screen = render(App)
  await expect.element(screen.getByRole('searchbox')).toBeVisible()
  // Warning banner should be visible
  await expect.element(screen.getByText(/failed to load/i)).toBeVisible()
})

test('clicking a section in the nav displays it in the main pane', async () => {
  const { initPlatform } = await import('$lib/platform')
  vi.mocked(initPlatform).mockResolvedValue(makeMockPlatform({
    readFile: vi.fn().mockImplementation((path: string) => {
      if (path.includes('preamble')) return Promise.resolve(SAMPLE_SECTION)
      if (path.includes('dignity')) return Promise.resolve(DIGNITY_SECTION)
      return Promise.reject(new Error('File not found'))
    }),
  }))

  const screen = render(App)
  await expect.element(screen.getByRole('searchbox')).toBeVisible()
  // Click Dignity in the nav
  await screen.getByRole('button', { name: 'Dignity' }).click()
  // Dignity's ritual text should appear in the main pane
  await expect.element(screen.getByText(/edge of their strength/i)).toBeVisible()
})
