import { describe, test, expect, vi } from 'vitest'
import { dispatchToCouncil } from '../dispatch'
import type { AgentProvider, ChatChunk, ChatParams } from '$lib/agents/provider'

function asyncIterableOf(items: ChatChunk[]): AsyncIterable<ChatChunk> {
  return {
    [Symbol.asyncIterator]() {
      let i = 0
      return {
        async next() {
          if (i < items.length) return { value: items[i++], done: false }
          return { value: undefined as unknown as ChatChunk, done: true }
        }
      }
    }
  }
}

async function collectStream(iterable: AsyncIterable<ChatChunk>): Promise<ChatChunk[]> {
  const chunks: ChatChunk[] = []
  for await (const chunk of iterable) chunks.push(chunk)
  return chunks
}

async function collectStreamText(iterable: AsyncIterable<ChatChunk>): Promise<string> {
  const chunks = await collectStream(iterable)
  return chunks.map(c => c.content).join('')
}

function mockProvider(name: string, items: ChatChunk[]): AgentProvider {
  return {
    name,
    chat: vi.fn().mockReturnValue(asyncIterableOf(items)),
    models: vi.fn().mockResolvedValue([]),
  }
}

function mockErrorProvider(name: string, error: Error): AgentProvider {
  async function* errorGen(): AsyncIterable<ChatChunk> {
    throw error
  }
  return {
    name,
    chat: vi.fn().mockReturnValue(errorGen()),
    models: vi.fn().mockResolvedValue([]),
  }
}

const baseParams: ChatParams = {
  model: 'test-model',
  messages: [{ role: 'user', content: 'test question' }],
}

describe('dispatchToCouncil', () => {
  test('dispatches to multiple providers in parallel', async () => {
    const provider1 = mockProvider('Claude', [
      { content: 'Response 1', done: false },
      { content: '', done: true },
    ])
    const provider2 = mockProvider('GPT', [
      { content: 'Response 2', done: false },
      { content: '', done: true },
    ])

    const results = dispatchToCouncil([provider1, provider2], baseParams)

    expect(results).toHaveLength(2)
    const text1 = await collectStreamText(results[0].stream)
    const text2 = await collectStreamText(results[1].stream)
    expect(text1).toContain('Response 1')
    expect(text2).toContain('Response 2')
  })

  test('one provider failure does not block others', async () => {
    const provider1 = mockProvider('Claude', [
      { content: 'OK', done: false },
      { content: '', done: true },
    ])
    const provider2 = mockErrorProvider('GPT', new Error('rate limited'))

    const results = dispatchToCouncil([provider1, provider2], baseParams)

    // Provider 1 stream succeeds
    const chunks1 = await collectStream(results[0].stream)
    expect(chunks1.some(c => c.content === 'OK')).toBe(true)

    // Provider 2 yields an error chunk, not a thrown exception
    const chunks2 = await collectStream(results[1].stream)
    expect(chunks2.some(c => c.error != null)).toBe(true)
  })

  test('returns provider names with streams', () => {
    const provider1 = mockProvider('Claude', [])
    const provider2 = mockProvider('GPT', [])

    const results = dispatchToCouncil([provider1, provider2], baseParams)
    expect(results[0].providerName).toBe('Claude')
    expect(results[1].providerName).toBe('GPT')
  })

  test('handles empty provider list', () => {
    const results = dispatchToCouncil([], baseParams)
    expect(results).toHaveLength(0)
  })

  test('passes params to each provider', async () => {
    const provider = mockProvider('Claude', [{ content: 'hi', done: true }])
    dispatchToCouncil([provider], baseParams)
    expect(provider.chat).toHaveBeenCalledWith(baseParams)
  })

  test('each provider is called independently and simultaneously', () => {
    const provider1 = mockProvider('A', [])
    const provider2 = mockProvider('B', [])

    dispatchToCouncil([provider1, provider2], baseParams)

    // Both called at dispatch time, not lazily
    expect(provider1.chat).toHaveBeenCalledOnce()
    expect(provider2.chat).toHaveBeenCalledOnce()
  })
})
