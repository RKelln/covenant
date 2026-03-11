/**
 * Core provider interface and types for AI model integrations.
 */

export interface Message {
  role: 'user' | 'assistant' | 'system'
  content: string
}

export interface ChatChunk {
  content: string
  done: boolean
  error?: string
  /** Optional metadata (token counts, cost estimates, etc.) */
  metadata?: Record<string, unknown>
}

export interface ChatParams {
  model: string
  messages: Message[]
  system?: string
  temperature?: number
  max_tokens?: number
}

export interface ModelInfo {
  id: string
  name: string
  provider: string
  context_length?: number
}

/**
 * Common interface all AI provider adapters must implement.
 */
export interface AgentProvider {
  /** Provider identifier (e.g. 'openrouter', 'copilot') */
  name: string
  /** Stream a chat completion as an async iterable of chunks */
  chat(params: ChatParams): AsyncIterable<ChatChunk>
  /** Fetch available models from this provider */
  models(): Promise<ModelInfo[]>
}
