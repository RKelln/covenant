import { test, expect, vi } from 'vitest'
import { defaultConfig, loadConfig, saveConfig } from '../loader'
import type { TerminalConfig } from '../types'

test('default config has sensible values', () => {
  const config = defaultConfig()
  expect(config.mode).toBe('contributor')
  expect(config.providers).toEqual([])
  expect(config.council).toEqual([])
})

test('loadConfig returns defaults when no saved config', async () => {
  const mockPlatform = { loadConfig: vi.fn().mockResolvedValue(null) }
  const config = await loadConfig(mockPlatform as any)
  expect(config.mode).toBe('contributor')
  expect(config.providers).toEqual([])
})

test('loadConfig merges saved config with defaults', async () => {
  const saved = { providers: [{ type: 'openrouter', apiKey: 'key-123' }] }
  const mockPlatform = { loadConfig: vi.fn().mockResolvedValue(saved) }
  const config = await loadConfig(mockPlatform as any)
  expect(config.providers[0].apiKey).toBe('key-123')
  expect(config.mode).toBe('contributor') // default filled in
  expect(config.council).toEqual([])      // default filled in
})

test('saveConfig persists via platform', async () => {
  const mockPlatform = { saveConfig: vi.fn().mockResolvedValue(undefined) }
  const config: TerminalConfig = {
    ...defaultConfig(),
    providers: [{ type: 'openrouter', apiKey: 'x' }],
  }
  await saveConfig(mockPlatform as any, config)
  expect(mockPlatform.saveConfig).toHaveBeenCalledWith(config)
})

test('loadConfig handles platform errors gracefully', async () => {
  const mockPlatform = { loadConfig: vi.fn().mockRejectedValue(new Error('io error')) }
  // Should return defaults rather than throw
  const config = await loadConfig(mockPlatform as any)
  expect(config.mode).toBe('contributor')
})
