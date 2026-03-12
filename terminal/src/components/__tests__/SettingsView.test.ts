import { render, cleanup } from 'vitest-browser-svelte'
import { expect, test, vi, describe, afterEach } from 'vitest'
import SettingsView from '../SettingsView.svelte'
import { defaultConfig } from '$lib/config/loader'
import type { ModelInfo } from '$lib/agents/provider'

afterEach(() => cleanup())

describe('SettingsView — provider config', () => {
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

  test('model selector shows available models in combobox', async () => {
    const config = {
      ...defaultConfig(),
      providers: [{ type: 'openrouter' as const, apiKey: 'sk-test' }],
    }
    const availableModels: ModelInfo[] = [
      { id: 'openai/gpt-4o-mini', name: 'GPT-4o mini', provider: 'openrouter' },
    ]
    const screen = render(SettingsView, { config, availableModels })
    // Click the model search input to open the dropdown
    const modelInput = screen.getByPlaceholder(/search models/i)
    await modelInput.click()
    // The model should appear in the dropdown
    await expect.element(screen.getByText('GPT-4o mini')).toBeVisible()
  })
})

describe('SettingsView — roster management', () => {
  test('roster editor shows configured agents', async () => {
    const config = {
      ...defaultConfig(),
      council: [
        { provider: 'openrouter', model: 'anthropic/claude-3-haiku', label: 'Claude' },
        { provider: 'openrouter', model: 'openai/gpt-4o-mini', label: 'GPT' },
      ]
    }
    const screen = render(SettingsView, { config })
    // Check council members are listed
    const labels = screen.container.querySelectorAll('[data-council-label]')
    const texts = Array.from(labels).map(el => el.textContent?.trim())
    expect(texts).toContain('Claude')
    expect(texts).toContain('GPT')
  })

  test('can remove an agent from the roster', async () => {
    const onSave = vi.fn()
    const config = {
      ...defaultConfig(),
      council: [
        { provider: 'openrouter', model: 'anthropic/claude-3-haiku', label: 'Claude' },
        { provider: 'openrouter', model: 'openai/gpt-4o-mini', label: 'GPT' },
      ]
    }
    const screen = render(SettingsView, { config, onsave: onSave })

    // Click the remove button for the first agent
    const removeButtons = screen.container.querySelectorAll('[data-remove-agent]')
    expect(removeButtons.length).toBe(2)
    ;(removeButtons[0] as HTMLElement).click()

    // Save and verify council has one member
    await screen.getByRole('button', { name: /save/i }).click()
    expect(onSave).toHaveBeenCalledWith(expect.objectContaining({
      council: expect.arrayContaining([
        expect.objectContaining({ label: 'GPT' })
      ])
    }))
    const savedCouncil = onSave.mock.calls[0][0].council
    expect(savedCouncil).toHaveLength(1)
  })

  test('can add an agent to the roster', async () => {
    const onSave = vi.fn()
    const availableModels: ModelInfo[] = [
      { id: 'openai/gpt-4o-mini', name: 'GPT-4o mini', provider: 'openrouter' },
    ]
    const screen = render(SettingsView, { config: defaultConfig(), availableModels, onsave: onSave })

    // Fill model ID via combobox — type and select from dropdown
    const modelInput = screen.getByPlaceholder('Model ID (e.g. anthropic/claude-3-haiku)')
    await modelInput.fill('openai/gpt-4o-mini')
    // Click the dropdown option to trigger onselect
    await screen.getByText('GPT-4o mini').click()
    // Fill label
    await screen.getByPlaceholder('Label (e.g. Claude)').fill('NewAgent')
    await screen.getByRole('button', { name: /^add$/i }).click()

    await screen.getByRole('button', { name: /save/i }).click()
    const savedCouncil = onSave.mock.calls[0][0].council
    expect(savedCouncil.some((m: { label: string }) => m.label === 'NewAgent')).toBe(true)
  })
})
