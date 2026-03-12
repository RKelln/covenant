import type { AgentProvider, ChatChunk, ChatParams, ModelInfo } from './provider'

const OPENROUTER_BASE = 'https://openrouter.ai/api/v1'

/**
 * Parse a Server-Sent Events stream into individual data lines.
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
    // All complete events except the last partial one
    buffer = parts.pop() ?? ''

    for (const part of parts) {
      for (const line of part.split('\n')) {
        if (line.startsWith('data: ')) {
          yield line.slice(6)
        }
      }
    }
  }

  // Flush any remaining buffer
  if (buffer) {
    for (const line of buffer.split('\n')) {
      if (line.startsWith('data: ')) {
        yield line.slice(6)
      }
    }
  }
}

export class OpenRouterProvider implements AgentProvider {
  readonly name: string

  /**
   * @param apiKey  OpenRouter API key
   * @param model   Optional default model — overrides params.model when set.
   *                Used so each council member can have its own model baked in.
   * @param label   Optional display label — sets `name`. Defaults to 'openrouter'.
   */
  constructor(
    private readonly apiKey: string,
    private readonly model?: string,
    label?: string,
  ) {
    this.name = label ?? 'openrouter'
  }

  async *chat(params: ChatParams): AsyncIterable<ChatChunk> {
    const messages = params.system
      ? [{ role: 'system' as const, content: params.system }, ...params.messages]
      : params.messages

    // Per-instance model takes precedence over params.model
    const model = this.model ?? params.model

    const response = await fetch(`${OPENROUTER_BASE}/chat/completions`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com/covenant-terminal',
        'X-Title': 'Covenant Terminal',
      },
      body: JSON.stringify({
        model,
        messages,
        stream: true,
        temperature: params.temperature ?? 0.7,
        max_tokens: params.max_tokens,
      }),
    })

    if (!response.ok) {
      const text = await response.text().catch(() => '')
      if (response.status === 401) {
        throw new Error(`Unauthorized: Invalid API key. ${text}`)
      }
      throw new Error(`OpenRouter API error ${response.status}: ${text}`)
    }

    if (!response.body) {
      throw new Error('OpenRouter: Response body is null')
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

    // Stream ended without [DONE]
    yield { content: '', done: true }
  }

  async models(): Promise<ModelInfo[]> {
    const response = await fetch(`${OPENROUTER_BASE}/models`, {
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
      },
    })

    if (!response.ok) {
      throw new Error(`OpenRouter models API error ${response.status}`)
    }

    const json = await response.json() as { data: Array<{ id: string; name: string; context_length?: number }> }
    return json.data.map(m => ({
      id: m.id,
      name: m.name,
      provider: 'openrouter',
      context_length: m.context_length,
    }))
  }
}
