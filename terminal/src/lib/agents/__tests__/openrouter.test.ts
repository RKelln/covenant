import { test, expect, vi, beforeEach, afterEach } from 'vitest'
import { OpenRouterProvider } from '../openrouter'
import type { ChatChunk } from '../provider'

// Helper to create a mock SSE ReadableStream response
function mockSSEResponse(lines: string[]): Response {
  const body = lines.map(l => `${l}\n\n`).join('')
  return new Response(body, {
    status: 200,
    headers: { 'content-type': 'text/event-stream' },
  })
}

// Collect all chunks from an AsyncIterable
async function collectStream(iter: AsyncIterable<ChatChunk>): Promise<ChatChunk[]> {
  const chunks: ChatChunk[] = []
  for await (const chunk of iter) {
    chunks.push(chunk)
  }
  return chunks
}

beforeEach(() => {
  vi.restoreAllMocks()
})

afterEach(() => {
  vi.restoreAllMocks()
})

test('OpenRouter adapter has correct name', () => {
  const adapter = new OpenRouterProvider('test-key')
  expect(adapter.name).toBe('openrouter')
})

test('chat() streams chunks from SSE response', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(mockSSEResponse([
    'data: {"choices":[{"delta":{"content":"Hello"}}]}',
    'data: {"choices":[{"delta":{"content":" world"}}]}',
    'data: [DONE]',
  ])))

  const adapter = new OpenRouterProvider('test-key')
  const chunks = await collectStream(adapter.chat({
    model: 'openai/gpt-4o-mini',
    messages: [{ role: 'user', content: 'hi' }],
  }))

  // Two content chunks + one done chunk
  expect(chunks.length).toBeGreaterThanOrEqual(2)
  const contentChunks = chunks.filter(c => c.content)
  expect(contentChunks[0].content).toBe('Hello')
  expect(contentChunks[1].content).toBe(' world')
  const doneChunk = chunks.find(c => c.done)
  expect(doneChunk).toBeDefined()
})

test('chat() sends correct Authorization header', async () => {
  const fetchMock = vi.fn().mockResolvedValue(mockSSEResponse(['data: [DONE]']))
  vi.stubGlobal('fetch', fetchMock)

  const adapter = new OpenRouterProvider('sk-or-test-key')
  await collectStream(adapter.chat({
    model: 'openai/gpt-4o-mini',
    messages: [{ role: 'user', content: 'hi' }],
  }))

  expect(fetchMock).toHaveBeenCalledWith(
    expect.stringContaining('openrouter'),
    expect.objectContaining({
      headers: expect.objectContaining({
        Authorization: 'Bearer sk-or-test-key',
      }),
    })
  )
})

test('chat() throws on 401 (bad API key)', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(
    new Response('Unauthorized', { status: 401 })
  ))
  const adapter = new OpenRouterProvider('bad-key')
  await expect(
    collectStream(adapter.chat({
      model: 'openai/gpt-4o-mini',
      messages: [{ role: 'user', content: 'hi' }],
    }))
  ).rejects.toThrow(/unauthorized|api key|401/i)
})

test('models() returns available model list', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(
    new Response(JSON.stringify({ data: [
      { id: 'openai/gpt-4o-mini', name: 'GPT-4o mini', context_length: 128000 },
      { id: 'anthropic/claude-3-haiku', name: 'Claude 3 Haiku', context_length: 200000 },
    ] }), { status: 200 })
  ))
  const adapter = new OpenRouterProvider('test-key')
  const models = await adapter.models()
  expect(models).toHaveLength(2)
  expect(models[0].id).toBe('openai/gpt-4o-mini')
  expect(models[0].provider).toBe('openrouter')
})

test('models() throws on network error', async () => {
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Network error')))
  const adapter = new OpenRouterProvider('test-key')
  await expect(adapter.models()).rejects.toThrow(/network error/i)
})
