import { render } from 'vitest-browser-svelte'
import { expect, test } from 'vitest'
import AgentColumn from '../AgentColumn.svelte'

test('renders streamed text as it arrives', async () => {
  const screen = render(AgentColumn, {
    agentName: 'Claude',
    chunks: [{ content: 'Hello ', done: false }, { content: 'world', done: false }],
    streaming: true,
  })
  await expect.element(screen.getByText('Hello world')).toBeVisible()
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
