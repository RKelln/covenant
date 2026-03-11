import { test, expect, vi } from 'vitest'
import { render } from 'vitest-browser-svelte'
import SectionNav from '../SectionNav.svelte'
import type { Section } from '$lib/covenant/types'

// Minimal Section objects for testing
const mockSections: Section[] = [
  {
    id: 'preamble',
    title: 'Preamble',
    status: 'stable',
    since: '0.1.0',
    category: '00-preamble',
    ritual: '',
    spec: '',
    digest: '',
    log: '',
    frontmatter: { id: 'preamble', title: 'Preamble', status: 'stable', since: '0.1.0', depends_on: [], terms_introduced: [] },
  },
  {
    id: 'rights.dignity',
    title: 'Dignity',
    status: 'draft',
    since: '0.2.0',
    category: '02-rights',
    ritual: '',
    spec: '',
    digest: '',
    log: '',
    frontmatter: { id: 'rights.dignity', title: 'Dignity', status: 'draft', since: '0.2.0', depends_on: [], terms_introduced: [] },
  },
  {
    id: 'rights.privacy',
    title: 'Privacy',
    status: 'draft',
    since: '0.2.0',
    category: '02-rights',
    ritual: '',
    spec: '',
    digest: '',
    log: '',
    frontmatter: { id: 'rights.privacy', title: 'Privacy', status: 'draft', since: '0.2.0', depends_on: [], terms_introduced: [] },
  },
]

test('renders all section titles', async () => {
  const screen = render(SectionNav, { sections: mockSections })
  // Use role=button to target the nav buttons, not the category heading
  await expect.element(screen.getByRole('button', { name: 'Preamble' })).toBeVisible()
  await expect.element(screen.getByRole('button', { name: 'Dignity' })).toBeVisible()
  await expect.element(screen.getByRole('button', { name: 'Privacy' })).toBeVisible()
})

test('groups sections by category with category headings', async () => {
  const screen = render(SectionNav, { sections: mockSections })
  // Category 00-preamble → label "Preamble"
  // Category 02-rights → label "Rights"
  await expect.element(screen.getByText('Rights')).toBeVisible()
})

test('shows status badge for draft sections', async () => {
  const screen = render(SectionNav, { sections: mockSections })
  // Draft indicator present — the 'd' badge for Dignity
  const badges = screen.container.querySelectorAll('.status-badge.draft')
  expect(badges.length).toBeGreaterThan(0)
})

test('clicking a section calls onselect with the section id', async () => {
  const onselect = vi.fn()
  const screen = render(SectionNav, { sections: mockSections, onselect })
  await screen.getByRole('button', { name: 'Dignity' }).click()
  expect(onselect).toHaveBeenCalledWith('rights.dignity')
})

test('search filters visible sections', async () => {
  const screen = render(SectionNav, { sections: mockSections })
  const searchInput = screen.getByRole('searchbox')
  await searchInput.fill('dig')
  await expect.element(screen.getByText('Dignity')).toBeVisible()
  // Preamble should not be visible
  await expect.element(screen.getByText('Preamble')).not.toBeInTheDocument()
})

test('search is case-insensitive', async () => {
  const screen = render(SectionNav, { sections: mockSections })
  const searchInput = screen.getByRole('searchbox')
  await searchInput.fill('PRIV')
  await expect.element(screen.getByText('Privacy')).toBeVisible()
})
