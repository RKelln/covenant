import type { Platform } from '../platform'
import type { TerminalConfig } from '../types'

export type { TerminalConfig, ProviderConfig, CouncilMemberConfig } from '../types'

/**
 * Returns a safe default configuration.
 */
export function defaultConfig(): TerminalConfig {
  return {
    mode: 'contributor',
    defaultModel: '',
    providers: [],
    council: [],
  }
}

/**
 * Load configuration from the platform, merging with defaults.
 * Returns defaults if no config is saved or on any error.
 */
export async function loadConfig(platform: Pick<Platform, 'loadConfig'>): Promise<TerminalConfig> {
  try {
    const saved = await platform.loadConfig()
    if (!saved) return defaultConfig()
    return { ...defaultConfig(), ...saved }
  } catch {
    return defaultConfig()
  }
}

/**
 * Persist configuration through the platform.
 */
export async function saveConfig(
  platform: Pick<Platform, 'saveConfig'>,
  config: TerminalConfig
): Promise<void> {
  await platform.saveConfig(config)
}
