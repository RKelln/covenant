import type { Platform } from './platform'
import type { SectionMeta, ExecResult, TerminalConfig, CostEntry } from './types'

// Repo root path — used to resolve relative section paths.
// In development: the repo directory. In production: set via config.
const DEV_REPO_PATH = '/home/ryankelln/Documents/Projects/Art/100_Year_Decade/covenant/repo'

export class TauriPlatform implements Platform {
  // Cache to avoid repeated path resolution
  private _repoPath: string | null = null
  private _configLoaded = false
  private _config: TerminalConfig | null = null

  async readFile(path: string): Promise<string> {
    const { readTextFile } = await import('@tauri-apps/plugin-fs')
    if (path.startsWith('/')) {
      return readTextFile(path)
    }
    const repoPath = await this._getRepoPath()
    return readTextFile(`${repoPath}/${path}`)
  }

  async writeFile(path: string, content: string): Promise<void> {
    const { writeTextFile, mkdir } = await import('@tauri-apps/plugin-fs')
    // Ensure parent directory exists
    const dir = path.substring(0, path.lastIndexOf('/'))
    if (dir) {
      try {
        await mkdir(dir, { recursive: true })
      } catch {
        // Directory may already exist — ignore
      }
    }
    await writeTextFile(path, content)
  }

  async listSections(): Promise<SectionMeta[]> {
    const { readDir } = await import('@tauri-apps/plugin-fs')
    const repoPath = await this._getRepoPath()
    const sectionsPath = `${repoPath}/sections`
    // Enumerate top-level category directories
    const categories = await readDir(sectionsPath)
    const sections: SectionMeta[] = []
    for (const cat of categories) {
      if (!cat.name || cat.name.startsWith('.')) continue
      const catPath = `${sectionsPath}/${cat.name}`
      try {
        const files = await readDir(catPath)
        for (const file of files) {
          if (file.name?.endsWith('.md')) {
            sections.push({
              id: '', // filled by parser
              title: file.name.replace('.md', ''),
              path: `${catPath}/${file.name}`,
              category: cat.name,
              status: 'draft',
            })
          }
        }
      } catch {
        // Skip unreadable directories
      }
    }
    return sections
  }

  async exec(command: string, args: string[]): Promise<ExecResult> {
    const { Command } = await import('@tauri-apps/plugin-shell')
    const cmd = Command.create(command, args)
    const output = await cmd.execute()
    return {
      code: output.code ?? 0,
      stdout: output.stdout,
      stderr: output.stderr,
    }
  }

  async loadConfig(): Promise<TerminalConfig | null> {
    if (this._configLoaded) return this._config
    this._configLoaded = true
    try {
      const { appConfigDir } = await import('@tauri-apps/api/path')
      const dir = await appConfigDir()
      const { readTextFile } = await import('@tauri-apps/plugin-fs')
      const content = await readTextFile(`${dir}/terminal-config.json`)
      this._config = JSON.parse(content) as TerminalConfig
      if (this._config?.repoPath) this._repoPath = this._config.repoPath
      return this._config
    } catch {
      return null
    }
  }

  async saveConfig(config: TerminalConfig): Promise<void> {
    const { appConfigDir } = await import('@tauri-apps/api/path')
    const dir = await appConfigDir()
    await this.writeFile(`${dir}/terminal-config.json`, JSON.stringify(config, null, 2))
    // Invalidate cache
    this._config = config
    this._configLoaded = true
    if (config.repoPath) this._repoPath = config.repoPath
  }

  async logApiCall(entry: CostEntry): Promise<void> {
    console.log('[cost]', entry)
  }

  private async _getRepoPath(): Promise<string> {
    if (this._repoPath) return this._repoPath
    // Load config to check for explicit repoPath
    const config = await this.loadConfig()
    if (config?.repoPath) {
      this._repoPath = config.repoPath
      return this._repoPath
    }
    // Development fallback
    this._repoPath = DEV_REPO_PATH
    return this._repoPath
  }
}
