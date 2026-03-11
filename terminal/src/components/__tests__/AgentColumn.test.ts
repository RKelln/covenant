import { render } from 'vitest-browser-svelte'
import { expect, test } from 'vitest'
import AgentColumn from '../AgentColumn.svelte'

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
