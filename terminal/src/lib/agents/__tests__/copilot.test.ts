import { describe, test, expect, vi } from 'vitest'
import { CopilotProvider } from '../copilot'
import type { ChatChunk } from '$lib/agents/provider'

function makeSSEResponse(lines: string[]): Response {
  const body = lines.join('\n\n') + '\n\n'
  const encoder = new TextEncoder()
  const stream = new ReadableStream({
    start(controller) {
      controller.enqueue(encoder.encode(body))
      controller.close()
    }
  })
  return new Response(stream, { status: 200 })
}

async function collectStream(iter: AsyncIterable<ChatChunk>): Promise<ChatChunk[]> {
  const chunks: ChatChunk[] = []
  for await (const chunk of iter) chunks.push(chunk)
  return chunks
}

describe('CopilotProvider', () => {
  test('has correct name', () => {
    const adapter = new CopilotProvider('ghp_test')
    expect(adapter.name).toBe('copilot')
  })

  test('chat() streams chunks from SSE response', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(makeSSEResponse([
      'data: {"choices":[{"delta":{"content":"Hello"}}]}',
      'data: {"choices":[{"delta":{"content":" world"}}]}',
      'data: [DONE]',
    ])))

    const adapter = new CopilotProvider('ghp_test')
    const chunks = await collectStream(adapter.chat({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: 'hi' }],
    }))

    const content = chunks.map(c => c.content).join('')
    expect(content).toContain('Hello')
    expect(content).toContain(' world')
    expect(chunks.some(c => c.done)).toBe(true)
  })

  test('chat() uses Copilot API endpoint', async () => {
    const fetchSpy = vi.fn().mockResolvedValue(makeSSEResponse(['data: [DONE]']))
    vi.stubGlobal('fetch', fetchSpy)

    const adapter = new CopilotProvider('ghp_test')
    await collectStream(adapter.chat({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: 'hi' }],
    }))

    expect(fetchSpy).toHaveBeenCalledWith(
      expect.stringContaining('copilot'),
      expect.anything()
    )
  })

  test('chat() sends Authorization header with bearer token', async () => {
    const fetchSpy = vi.fn().mockResolvedValue(makeSSEResponse(['data: [DONE]']))
    vi.stubGlobal('fetch', fetchSpy)

    const adapter = new CopilotProvider('ghp_test_key')
    await collectStream(adapter.chat({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: 'hi' }],
    }))

    const [, init] = fetchSpy.mock.calls[0]
    expect(init.headers['Authorization']).toMatch(/bearer ghp_test_key/i)
  })

  test('chat() throws on 401 (bad API key)', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(
      new Response('Unauthorized', { status: 401 })
    ))
    const adapter = new CopilotProvider('bad-key')
    await expect(
      collectStream(adapter.chat({ model: 'gpt-4o', messages: [{ role: 'user', content: 'hi' }] }))
    ).rejects.toThrow(/unauthorized|api key/i)
  })

  test('models() returns available model list', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(
      new Response(JSON.stringify({
        data: [
          { id: 'gpt-4o', name: 'GPT-4o', context_length: 128000 },
          { id: 'gpt-4o-mini', name: 'GPT-4o mini', context_length: 128000 },
        ]
      }))
    ))

    const adapter = new CopilotProvider('ghp_test')
    const models = await adapter.models()
    expect(models[0].id).toBe('gpt-4o')
    expect(models[0].provider).toBe('copilot')
  })
})
