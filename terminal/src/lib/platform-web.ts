import type { Platform } from './platform'
import type { SectionMeta, ExecResult, TerminalConfig, CostEntry } from './types'

export interface WebPlatformOptions {
  repoOwner?: string
  repoName?: string
  branch?: string
}

export class WebPlatform implements Platform {
  constructor(private options: WebPlatformOptions) {}

  async readFile(path: string): Promise<string> {
    const { repoOwner = 'ryankelln', repoName = 'covenant', branch = 'main' } = this.options
    const url = `https://raw.githubusercontent.com/${repoOwner}/${repoName}/${branch}/${path}`
    const response = await fetch(url)
    if (!response.ok) throw new Error(`Failed to fetch ${path}: ${response.statusText}`)
    return response.text()
  }

  async writeFile(_path: string, _content: string): Promise<void> {
    throw new Error('File writing is not available in web mode.')
  }

  async listSections(): Promise<SectionMeta[]> {
    // In web mode, return a stub — full implementation in M6
    return []
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

  async logApiCall(entry: CostEntry): Promise<void> {
    console.log('[cost/web]', entry)
  }
}
