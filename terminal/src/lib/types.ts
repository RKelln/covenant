export interface SectionMeta {
  id: string
  title: string
  path: string
  category: string
  status: 'draft' | 'stable' | 'proposed'
}

export interface ExecResult {
  code: number
  stdout: string
  stderr: string
}

export interface TerminalConfig {
  mode: 'contributor' | 'kiosk'
  repoPath?: string
  defaultModel?: string
  providers: ProviderConfig[]
  council: CouncilMemberConfig[]
}

export interface ProviderConfig {
  type: 'openrouter' | 'copilot' | 'anthropic' | 'openai' | 'google'
  apiKey?: string
  baseUrl?: string
}

export interface CouncilMemberConfig {
  provider: string
  model: string
  label: string
  systemPrompt?: string
  tintColor?: string
}

export interface CostEntry {
  timestamp: number
  provider: string
  model: string
  tokens_in: number
  tokens_out: number
  estimated_kwh: number
  estimated_water_ml: number
}
