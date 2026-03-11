import { render, cleanup } from 'vitest-browser-svelte'
import { expect, test, describe, afterEach } from 'vitest'
import CouncilPanel from '../CouncilPanel.svelte'

afterEach(() => cleanup())

describe('CouncilPanel — basic', () => {
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
})

describe('CouncilPanel — multi-column', () => {
  test('renders multiple agent columns', async () => {
    const agents = [
      { name: 'Claude-M', chunks: [{ content: 'From Claude-M', done: true }], streaming: false },
      { name: 'GPT-M', chunks: [{ content: 'From GPT-M', done: true }], streaming: false },
      { name: 'Gemini-M', chunks: [{ content: 'From Gemini-M', done: true }], streaming: false },
    ]
    const screen = render(CouncilPanel, { agents })
    // Use container-scoped queries to avoid strict-mode issues with page-wide locators
    const agentNames = screen.container.querySelectorAll('.agent-name')
    expect(agentNames).toHaveLength(3)
    const nameTexts = Array.from(agentNames).map(el => el.textContent?.trim())
    expect(nameTexts).toContain('Claude-M')
    expect(nameTexts).toContain('GPT-M')
    expect(nameTexts).toContain('Gemini-M')
  })

  test('columns have data-agent-column attribute', async () => {
    const agents = [
      { name: 'Claude', chunks: [], streaming: false, tint: '#e8d5b7' },
      { name: 'GPT', chunks: [], streaming: false, tint: '#b7d5e8' },
    ]
    const screen = render(CouncilPanel, { agents })
    const columns = screen.container.querySelectorAll('[data-agent-column]')
    expect(columns).toHaveLength(2)
  })

  test('columns have distinct tint colors via CSS variable', async () => {
    const agents = [
      { name: 'Claude', chunks: [], streaming: false, tint: '#e8d5b7' },
      { name: 'GPT', chunks: [], streaming: false, tint: '#b7d5e8' },
    ]
    const screen = render(CouncilPanel, { agents })
    const columns = screen.container.querySelectorAll('[data-agent-column]')
    const tints = Array.from(columns).map(col =>
      (col as HTMLElement).style.getPropertyValue('--column-tint')
        || (col as HTMLElement).style.borderLeftColor
        || (col as HTMLElement).getAttribute('data-tint')
    )
    // The two tint values should be distinct
    expect(tints[0]).not.toBe(tints[1])
  })
})

describe('CouncilPanel — synthesis', () => {
  test('shows synthesis section when synthesis prop is provided', async () => {
    const agents = [
      { name: 'Claude-Synth', chunks: [{ content: 'Done', done: true }], streaming: false },
    ]
    const synthesis = { chunks: [{ content: 'Synthesis text here', done: true }], streaming: false }
    const screen = render(CouncilPanel, { agents, synthesis })
    // Check for synthesis heading class, not text (to avoid ambiguity)
    const heading = screen.container.querySelector('.synthesis-heading')
    expect(heading).not.toBeNull()
    await expect.element(screen.getByText('Synthesis text here')).toBeVisible()
  })

  test('does not show synthesis section when synthesis is absent', async () => {
    const agents = [
      { name: 'Claude', chunks: [{ content: 'hi', done: true }], streaming: false },
    ]
    const screen = render(CouncilPanel, { agents })
    // No synthesis header
    const heading = screen.container.querySelector('.synthesis-heading')
    expect(heading).toBeNull()
  })
})
