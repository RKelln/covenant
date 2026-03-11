import { test, expect, vi } from 'vitest'
import { render } from 'vitest-browser-svelte'
import SectionView from '../SectionView.svelte'
import type { Section } from '$lib/covenant/types'

const mockSection: Section = {
  id: 'rights.dignity',
  title: 'Dignity',
  status: 'draft',
  since: '0.2.0',
  category: '02-rights',
  ritual: 'You will meet people at the edge of their strength.',
  spec: '1. **Prohibition on Degradation** The System MUST NOT degrade the dignity.',
  digest: '**Intent:** Make "dignity is the floor" explicit.',
  log: '- 2025-01-15: Initial draft',
  frontmatter: {
    id: 'rights.dignity',
    title: 'Dignity',
    status: 'draft',
    since: '0.2.0',
    depends_on: [],
    terms_introduced: ['dignity'],
  },
}

test('renders section title', async () => {
  const screen = render(SectionView, { section: mockSection })
  await expect.element(screen.getByRole('heading', { name: 'Dignity' })).toBeVisible()
})

test('shows Ritual tab by default', async () => {
  const screen = render(SectionView, { section: mockSection })
  await expect.element(screen.getByText(/edge of their strength/)).toBeVisible()
})

test('Ritual content is not shown when Spec tab is active initially', async () => {
  const screen = render(SectionView, { section: mockSection, defaultRegister: 'spec' })
  // Ritual text should not be visible
  await expect.element(screen.getByText(/Prohibition on Degradation/)).toBeVisible()
})

test('switches to Spec tab', async () => {
  const screen = render(SectionView, { section: mockSection })
  await screen.getByRole('tab', { name: 'Spec' }).click()
  await expect.element(screen.getByText(/Prohibition on Degradation/)).toBeVisible()
})

test('Complete tab shows both ritual and spec content', async () => {
  const screen = render(SectionView, { section: mockSection })
  await screen.getByRole('tab', { name: 'Complete' }).click()
  await expect.element(screen.getByText(/edge of their strength/)).toBeVisible()
  await expect.element(screen.getByText(/Prohibition on Degradation/)).toBeVisible()
  await expect.element(screen.getByText(/dignity is the floor/)).toBeVisible()
})

test('renders markdown bold as <strong>', async () => {
  const screen = render(SectionView, { section: mockSection })
  await screen.getByRole('tab', { name: 'Spec' }).click()
  const bold = screen.container.querySelector('strong')
  expect(bold).not.toBeNull()
})

test('renders cross-references as styled spans', async () => {
  const sectionWithRef: Section = {
    ...mockSection,
    spec: 'See §[obligations.harm] for details.',
  }
  const screen = render(SectionView, { section: sectionWithRef })
  await screen.getByRole('tab', { name: 'Spec' }).click()
  await expect.element(screen.getByText('§obligations.harm')).toBeVisible()
})

test('clicking a cross-reference calls onxref with the section id', async () => {
  const onxref = vi.fn()
  const sectionWithRef: Section = {
    ...mockSection,
    spec: 'See §[obligations.harm] for details.',
  }
  const screen = render(SectionView, { section: sectionWithRef, onxref })
  await screen.getByRole('tab', { name: 'Spec' }).click()
  await screen.getByText('§obligations.harm').click()
  expect(onxref).toHaveBeenCalledWith('obligations.harm')
})

test('shows section id in header', async () => {
  const screen = render(SectionView, { section: mockSection })
  await expect.element(screen.getByText('§rights.dignity')).toBeVisible()
})
