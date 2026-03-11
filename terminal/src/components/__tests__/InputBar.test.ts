import { render } from 'vitest-browser-svelte'
import { expect, test, vi } from 'vitest'
import InputBar from '../InputBar.svelte'

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
  const onSubmit = vi.fn()
  const screen = render(InputBar, { sectionId: 'rights.dignity', onsubmit: onSubmit })
  const selector = screen.getByRole('combobox')
  await selector.selectOptions(['challenge'])
  await screen.getByRole('textbox').fill('test')
  await screen.getByRole('button', { name: /send|submit/i }).click()
  expect(onSubmit).toHaveBeenCalledWith(expect.objectContaining({ mode: 'challenge' }))
})

test('clears input after submit', async () => {
  const screen = render(InputBar, { sectionId: 'rights.dignity', onsubmit: vi.fn() })
  const input = screen.getByRole('textbox')
  await input.fill('test question')
  await screen.getByRole('button', { name: /send|submit/i }).click()
  await expect.element(input).toHaveValue('')
})
