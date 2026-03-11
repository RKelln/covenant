import type { AgentProvider, ChatChunk, ChatParams, ModelInfo } from './provider'

/**
 * GitHub Copilot Chat API base URL.
 * The Copilot API uses the same OpenAI-compatible SSE format.
 */
const COPILOT_BASE = 'https://api.githubcopilot.com'

/**
 * Parse a Server-Sent Events stream into individual data lines.
 * Reusable utility shared with openrouter.ts.
 */
async function* parseSSE(
  reader: ReadableStreamDefaultReader<Uint8Array>
): AsyncIterable<string> {
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const parts = buffer.split('\n\n')
    buffer = parts.pop() ?? ''

    for (const part of parts) {
      for (const line of part.split('\n')) {
        if (line.startsWith('data: ')) {
          yield line.slice(6)
        }
      }
    }
  }

  if (buffer) {
    for (const line of buffer.split('\n')) {
      if (line.startsWith('data: ')) {
        yield line.slice(6)
      }
    }
  }
}

export class CopilotProvider implements AgentProvider {
  readonly name = 'copilot'

  constructor(private readonly token: string) {}

  async *chat(params: ChatParams): AsyncIterable<ChatChunk> {
    const messages = params.system
      ? [{ role: 'system' as const, content: params.system }, ...params.messages]
      : params.messages

    const response = await fetch(`${COPILOT_BASE}/chat/completions`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.token}`,
        'Content-Type': 'application/json',
        'Copilot-Integration-Id': 'vscode-chat',
        'Editor-Plugin-Version': 'covenant-terminal/0.1.0',
        'Editor-Version': 'covenant-terminal/0.1.0',
      },
      body: JSON.stringify({
        model: params.model,
        messages,
        stream: true,
        temperature: params.temperature ?? 0.7,
        max_tokens: params.max_tokens,
      }),
    })

    if (!response.ok) {
      const text = await response.text().catch(() => '')
      if (response.status === 401) {
        throw new Error(`Unauthorized: Invalid API key or expired token. ${text}`)
      }
      throw new Error(`Copilot API error ${response.status}: ${text}`)
    }

    if (!response.body) {
      throw new Error('Copilot: Response body is null')
    }

    const reader = response.body.getReader()

    for await (const data of parseSSE(reader)) {
      if (data === '[DONE]') {
        yield { content: '', done: true }
        return
      }

      try {
        const parsed = JSON.parse(data)
        const delta = parsed?.choices?.[0]?.delta?.content
        if (delta != null) {
          yield { content: delta, done: false }
        }
      } catch {
        // Skip malformed SSE lines
      }
    }

    yield { content: '', done: true }
  }

  async models(): Promise<ModelInfo[]> {
    const response = await fetch(`${COPILOT_BASE}/models`, {
      headers: {
        Authorization: `Bearer ${this.token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`Copilot models API error ${response.status}`)
    }

    const json = await response.json() as {
      data: Array<{ id: string; name: string; context_length?: number }>
    }
    return (json.data ?? []).map(m => ({
      id: m.id,
      name: m.name,
      provider: 'copilot',
      context_length: m.context_length,
    }))
  }
}
