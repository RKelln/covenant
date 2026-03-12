import type { Platform } from './platform'
import type { SectionMeta, ExecResult, TerminalConfig, CostEntry } from './types'
import type { ModelInfo } from './agents/provider'

// Injected at build/dev time by vite.config.ts → define.__SECTION_MANIFEST__
declare const __SECTION_MANIFEST__: { path: string; category: string }[]

export class WebPlatform implements Platform {
  async readFile(path: string): Promise<string> {
    // In dev, Vite middleware serves /sections/** directly from the repo root.
    const url = path.startsWith('/') ? path : `/${path}`
    const response = await fetch(url)
    if (!response.ok) throw new Error(`Failed to fetch ${path}: ${response.statusText}`)
    return response.text()
  }

  async writeFile(_path: string, _content: string): Promise<void> {
    throw new Error('File writing is not available in web mode.')
  }

  async listSections(): Promise<SectionMeta[]> {
    // Manifest is baked in at dev-server startup by vite.config.ts
    return __SECTION_MANIFEST__.map(({ path, category }) => ({
      id: '',
      title: path.split('/').pop()?.replace('.md', '') ?? '',
      path,
      category,
      status: 'draft' as const,
    }))
  }

  async exec(_command: string, _args: string[]): Promise<ExecResult> {
    return { code: 1, stdout: '', stderr: 'Shell commands are not available in web mode.' }
  }

  async loadConfig(): Promise<TerminalConfig | null> {
    const saved = localStorage.getItem('terminal-config')
    if (!saved) return null
    try { return JSON.parse(saved) as TerminalConfig } catch { return null }
  }

  async saveConfig(config: TerminalConfig): Promise<void> {
    localStorage.setItem('terminal-config', JSON.stringify(config))
  }

  async loadModelCache(): Promise<ModelInfo[] | null> {
    const saved = localStorage.getItem('model-cache')
    if (!saved) return null
    try { return JSON.parse(saved) as ModelInfo[] } catch { return null }
  }

  async saveModelCache(models: ModelInfo[]): Promise<void> {
    localStorage.setItem('model-cache', JSON.stringify(models))
  }

  async logApiCall(entry: CostEntry): Promise<void> {
    console.log('[cost/web]', entry)
  }
}
