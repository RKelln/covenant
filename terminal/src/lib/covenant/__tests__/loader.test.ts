import { test, expect, vi } from 'vitest'
import { loadAllSections, loadSection, loadSectionsByCategory } from '../loader'

const PREAMBLE_MD = `---
id: preamble
title: "Preamble"
status: stable
since: 0.1.0
depends_on: []
terms_introduced: []
---

# Ritual

This Covenant begins.

# Spec

The System MUST adhere to this Covenant.

# Digest

The opening statement.

# Log

- 2025-01-01: Initial draft
`

const DIGNITY_MD = `---
id: rights.dignity
title: "Dignity"
status: draft
since: 0.2.0
depends_on: [definitions]
terms_introduced: [dignity]
---

# Ritual

You will meet people at the edge of their strength.

# Spec

1. **Prohibition on Degradation**
   The System MUST NOT degrade the dignity.

# Digest

**Intent:** Make "dignity is the floor" explicit.

# Log

- 2025-01-15: Initial draft
`

function makeMockPlatform() {
  return {
    listSections: vi.fn().mockResolvedValue([
      { id: 'preamble', path: 'sections/00-preamble/preamble.md', category: '00-preamble', title: 'preamble', status: 'stable' },
      { id: 'rights.dignity', path: 'sections/02-rights/dignity.md', category: '02-rights', title: 'dignity', status: 'draft' },
    ]),
    readFile: vi.fn().mockImplementation((path: string) => {
      if (path.includes('preamble')) return Promise.resolve(PREAMBLE_MD)
      if (path.includes('dignity')) return Promise.resolve(DIGNITY_MD)
      return Promise.reject(new Error(`Unknown path: ${path}`))
    }),
  }
}

test('loadAllSections reads and parses all .md files', async () => {
  const mockPlatform = makeMockPlatform()
  const sections = await loadAllSections(mockPlatform as any)
  expect(sections).toHaveLength(2)
  expect(sections[0].id).toBe('preamble')
  expect(sections[1].id).toBe('rights.dignity')
})

test('loadAllSections assigns category from meta', async () => {
  const mockPlatform = makeMockPlatform()
  const sections = await loadAllSections(mockPlatform as any)
  expect(sections[0].category).toBe('00-preamble')
  expect(sections[1].category).toBe('02-rights')
})

test('loadAllSections skips sections that fail to parse', async () => {
  const mockPlatform = {
    listSections: vi.fn().mockResolvedValue([
      { id: 'bad', path: 'sections/bad.md', category: 'unknown', title: 'bad', status: 'draft' },
    ]),
    readFile: vi.fn().mockResolvedValue('# No frontmatter here'),
  }
  const sections = await loadAllSections(mockPlatform as any)
  expect(sections).toHaveLength(0)
})

test('loadSection returns a single section by id', async () => {
  const mockPlatform = makeMockPlatform()
  const section = await loadSection(mockPlatform as any, 'rights.dignity')
  expect(section).not.toBeNull()
  expect(section!.title).toBe('Dignity')
})

test('loadSection returns null when id not found', async () => {
  const mockPlatform = makeMockPlatform()
  const section = await loadSection(mockPlatform as any, 'nonexistent.id')
  expect(section).toBeNull()
})

test('loadSectionsByCategory groups sections by category', async () => {
  const mockPlatform = makeMockPlatform()
  const grouped = await loadSectionsByCategory(mockPlatform as any)
  expect(grouped['00-preamble']).toHaveLength(1)
  expect(grouped['02-rights']).toHaveLength(1)
  expect(grouped['00-preamble'][0].id).toBe('preamble')
  expect(grouped['02-rights'][0].id).toBe('rights.dignity')
})
