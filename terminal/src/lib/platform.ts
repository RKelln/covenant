import { isTauri } from '@tauri-apps/api/core'
import type { SectionMeta, ExecResult, TerminalConfig, CostEntry } from './types'
import type { ModelInfo } from './agents/provider'

export interface Platform {
  readFile(path: string): Promise<string>
  writeFile(path: string, content: string): Promise<void>
  listSections(): Promise<SectionMeta[]>
  exec(command: string, args: string[]): Promise<ExecResult>
  loadConfig(): Promise<TerminalConfig | null>
  saveConfig(config: TerminalConfig): Promise<void>
  loadModelCache(): Promise<ModelInfo[] | null>
  saveModelCache(models: ModelInfo[]): Promise<void>
  logApiCall(entry: CostEntry): Promise<void>
}

let _platform: Platform | null = null

export async function initPlatform(): Promise<Platform> {
  if (_platform) return _platform
  if (isTauri()) {
    const { TauriPlatform } = await import('./platform-tauri')
    _platform = new TauriPlatform()
  } else {
    const { WebPlatform } = await import('./platform-web')
    _platform = new WebPlatform()
  }
  return _platform
}

export function getPlatform(): Platform {
  if (_platform) return _platform
  throw new Error('Platform not initialized. Call initPlatform() first.')
}
