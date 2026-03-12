import { render, cleanup } from 'vitest-browser-svelte'
import { expect, test, vi, describe, afterEach } from 'vitest'
import ModelCombobox from '../ModelCombobox.svelte'
import type { ModelInfo } from '$lib/agents/provider'

afterEach(() => cleanup())

const MODELS: (ModelInfo & { recommended?: boolean })[] = [
  { id: 'anthropic/claude-opus-4.6', name: 'Anthropic: Claude Opus 4.6', provider: 'openrouter', context_length: 1000000, recommended: true },
  { id: 'openai/gpt-5.4', name: 'OpenAI: GPT-5.4', provider: 'openrouter', context_length: 1047576, recommended: true },
  { id: 'openai/gpt-4o-mini', name: 'OpenAI: GPT-4o mini', provider: 'openrouter', context_length: 128000 },
  { id: 'mistralai/mistral-large', name: 'Mistral: Mistral Large', provider: 'openrouter', context_length: 32000 },
]

describe('ModelCombobox', () => {
  test('renders input with placeholder', async () => {
    const screen = render(ModelCombobox, { models: MODELS, value: '' })
    await expect.element(screen.getByPlaceholder(/search models/i)).toBeVisible()
  })

  test('shows dropdown when input is focused', async () => {
    const screen = render(ModelCombobox, { models: MODELS, value: '' })
    await screen.getByPlaceholder(/search models/i).click()
    // Should see recommended models
    await expect.element(screen.getByText('Anthropic: Claude Opus 4.6')).toBeVisible()
  })

  test('recommended models appear first with header', async () => {
    const screen = render(ModelCombobox, { models: MODELS, value: '' })
    await screen.getByPlaceholder(/search models/i).click()
    await expect.element(screen.getByText(/recommended/i)).toBeVisible()
  })

  test('filters models as user types', async () => {
    const screen = render(ModelCombobox, { models: MODELS, value: '' })
    await screen.getByPlaceholder(/search models/i).fill('mistral')
    await expect.element(screen.getByText('Mistral: Mistral Large')).toBeVisible()
    // Recommended header should not appear when no recommended models match
    expect(screen.container.querySelector('[data-recommended-header]')).toBeNull()
  })

  test('selects model on click and emits onselect', async () => {
    const onSelect = vi.fn()
    const screen = render(ModelCombobox, { models: MODELS, value: '', onselect: onSelect })
    await screen.getByPlaceholder(/search models/i).click()
    await screen.getByText('Anthropic: Claude Opus 4.6').click()
    expect(onSelect).toHaveBeenCalledWith('anthropic/claude-opus-4.6')
  })

  test('displays current value in input', async () => {
    const screen = render(ModelCombobox, { models: MODELS, value: 'openai/gpt-4o-mini' })
    const input = screen.getByPlaceholder(/search models/i)
    await expect.element(input).toHaveValue('openai/gpt-4o-mini')
  })

  test('allows manual entry of model ID not in list', async () => {
    const onSelect = vi.fn()
    const screen = render(ModelCombobox, { models: MODELS, value: '', onselect: onSelect })
    const input = screen.getByPlaceholder(/search models/i)
    await input.fill('custom/my-model')
    // Blur triggers selection of typed value (after a short delay)
    ;(input.element() as HTMLInputElement).blur()
    await new Promise(r => setTimeout(r, 200))
    expect(onSelect).toHaveBeenCalledWith('custom/my-model')
  })
})
