import type { SectionMeta, ExecResult, TerminalConfig, CostEntry } from './types'

export interface Platform {
  readFile(path: string): Promise<string>
  writeFile(path: string, content: string): Promise<void>
  listSections(): Promise<SectionMeta[]>
  exec(command: string, args: string[]): Promise<ExecResult>
  loadConfig(): Promise<TerminalConfig | null>
  saveConfig(config: TerminalConfig): Promise<void>
  logApiCall(entry: CostEntry): Promise<void>
}

let _platform: Platform | null = null

export function getPlatform(): Platform {
  if (_platform) return _platform
  // Platform detection: Tauri sets window.__TAURI_INTERNALS__
  if (typeof window !== 'undefined' && (window as any).__TAURI_INTERNALS__) {
    // Lazy import to avoid bundling Tauri in web builds
    throw new Error('Tauri platform not yet initialized. Call initPlatform() first.')
  }
  throw new Error('Platform not initialized. Call initPlatform() first.')
}

export async function initPlatform(): Promise<Platform> {
  if (_platform) return _platform
  if (typeof window !== 'undefined' && (window as any).__TAURI_INTERNALS__) {
    const { TauriPlatform } = await import('./platform-tauri')
    _platform = new TauriPlatform()
  } else {
    // Web fallback (stub for now — implemented in M6)
    const { WebPlatform } = await import('./platform-web')
    _platform = new WebPlatform({})
  }
  return _platform
}
