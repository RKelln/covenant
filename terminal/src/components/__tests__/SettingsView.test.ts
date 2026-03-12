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

  test('add button is disabled when model is empty', async () => {
    const screen = render(SettingsView, { config: defaultConfig() })
    const addBtn = screen.getByRole('button', { name: /test & add/i })
    // No model entered — button should be disabled
    await expect.element(addBtn).toBeDisabled()
  })

  test('add button is enabled after typing a model ID and blurring', async () => {
    const screen = render(SettingsView, { config: defaultConfig() })
    const modelInput = screen.getByPlaceholder('Model ID (e.g. anthropic/claude-3-haiku)')
    await modelInput.fill('openai/gpt-4o-mini')
    // Blur triggers onselect in the combobox
    await modelInput.element().dispatchEvent(new Event('blur'))
    // Small wait for the blur timer (150 ms in combobox handleBlur)
    await new Promise(r => setTimeout(r, 200))
    const addBtn = screen.getByRole('button', { name: /test & add/i })
    await expect.element(addBtn).not.toBeDisabled()
  })
})
