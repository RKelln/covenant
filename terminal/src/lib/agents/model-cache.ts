import type { AgentProvider, ModelInfo } from './provider'
import type { Platform } from '../platform'
import seedModels from './models-seed.json'

/**
 * Load available models with a three-tier fallback:
 * 1. Live fetch from the provider API (cached to disk on success)
 * 2. Disk cache from a previous successful fetch
 * 3. Bundled seed file shipped with the app
 *
 * Pass provider as null when no API key is configured — skips straight to cache/seed.
 */
export async function loadModels(
  provider: AgentProvider | null,
  platform: Pick<Platform, 'loadModelCache' | 'saveModelCache'>,
): Promise<ModelInfo[]> {
  // Tier 1: live API fetch
  if (provider) {
    try {
      const models = await provider.models()
      // Cache for offline use — fire-and-forget
      platform.saveModelCache(models).catch(() => {})
      return models
    } catch {
      // Fall through to cache
    }
  }

  // Tier 2: disk cache
  try {
    const cached = await platform.loadModelCache()
    if (cached && cached.length > 0) return cached
  } catch {
    // Fall through to seed
  }

  // Tier 3: bundled seed
  return seedModels as ModelInfo[]
}
