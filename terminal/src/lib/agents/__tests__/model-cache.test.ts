import { test, expect, vi, describe, beforeEach } from 'vitest'
import { loadModels } from '../model-cache'
import type { ModelInfo, AgentProvider, ChatChunk, ChatParams } from '../provider'
import type { Platform } from '../../platform'

// Minimal mock provider
function mockProvider(models: ModelInfo[] | Error): AgentProvider {
  return {
    name: 'test',
    async *chat(_params: ChatParams): AsyncIterable<ChatChunk> {},
    models: models instanceof Error
      ? vi.fn().mockRejectedValue(models)
      : vi.fn().mockResolvedValue(models),
  }
}

// Minimal mock platform (only cache methods needed)
function mockPlatform(cached: ModelInfo[] | null = null) {
  return {
    loadModelCache: vi.fn().mockResolvedValue(cached),
    saveModelCache: vi.fn().mockResolvedValue(undefined),
  } as Pick<Platform, 'loadModelCache' | 'saveModelCache'>
}

const LIVE_MODELS: ModelInfo[] = [
  { id: 'openai/gpt-4o', name: 'GPT-4o', provider: 'openrouter', context_length: 128000 },
  { id: 'anthropic/claude-sonnet-4', name: 'Claude Sonnet 4', provider: 'openrouter', context_length: 200000 },
]

const CACHED_MODELS: ModelInfo[] = [
  { id: 'openai/gpt-4o-mini', name: 'GPT-4o mini', provider: 'openrouter', context_length: 128000 },
]

describe('loadModels', () => {
  test('returns live models from provider on success', async () => {
    const provider = mockProvider(LIVE_MODELS)
    const platform = mockPlatform()
    const result = await loadModels(provider, platform)
    expect(result).toEqual(LIVE_MODELS)
  })

  test('caches live models to disk on success', async () => {
    const provider = mockProvider(LIVE_MODELS)
    const platform = mockPlatform()
    await loadModels(provider, platform)
    expect(platform.saveModelCache).toHaveBeenCalledWith(LIVE_MODELS)
  })

  test('falls back to disk cache when provider fails', async () => {
    const provider = mockProvider(new Error('Network error'))
    const platform = mockPlatform(CACHED_MODELS)
    const result = await loadModels(provider, platform)
    expect(result).toEqual(CACHED_MODELS)
  })

  test('falls back to bundled seed when both provider and disk cache fail', async () => {
    const provider = mockProvider(new Error('Network error'))
    const platform = mockPlatform(null)
    const result = await loadModels(provider, platform)
    // Should return the seed models (non-empty array)
    expect(result.length).toBeGreaterThan(0)
    // First entry should be from the seed file
    expect(result[0].provider).toBe('openrouter')
  })

  test('does not write to cache when falling back', async () => {
    const provider = mockProvider(new Error('Network error'))
    const platform = mockPlatform(CACHED_MODELS)
    await loadModels(provider, platform)
    expect(platform.saveModelCache).not.toHaveBeenCalled()
  })

  test('returns seed when provider is null (no API key configured)', async () => {
    const platform = mockPlatform(null)
    const result = await loadModels(null, platform)
    expect(result.length).toBeGreaterThan(0)
  })

  test('returns disk cache over seed when provider is null', async () => {
    const platform = mockPlatform(CACHED_MODELS)
    const result = await loadModels(null, platform)
    expect(result).toEqual(CACHED_MODELS)
  })
})
