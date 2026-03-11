import { describe, test, expect, vi } from 'vitest'
import { synthesize } from '../synthesis'
import type { AgentProvider, ChatChunk } from '$lib/agents/provider'

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

async function collectStream(iter: AsyncIterable<ChatChunk>): Promise<ChatChunk[]> {
  const chunks: ChatChunk[] = []
  for await (const chunk of iter) chunks.push(chunk)
  return chunks
}

async function collectStreamText(iter: AsyncIterable<ChatChunk>): Promise<string> {
  return (await collectStream(iter)).map(c => c.content).join('')
}

describe('synthesize', () => {
  test('synthesizes multiple responses and streams output', async () => {
    const mockProvider: AgentProvider = {
      name: 'synthesizer',
      chat: vi.fn().mockReturnValue(asyncIterableOf([
        { content: 'Both agree that dignity sets a minimum...', done: false },
        { content: '', done: true },
      ])),
      models: vi.fn().mockResolvedValue([]),
    }

    const responses = [
      { agent: 'Claude', text: 'Dignity is the floor — it constrains all other obligations.' },
      { agent: 'GPT', text: 'Dignity here means protection from degradation, not positive entitlement.' },
    ]

    const stream = synthesize(mockProvider, responses, { model: 'test-model' })
    const text = await collectStreamText(stream)
    expect(text).toContain('Both agree')
  })

  test('synthesis prompt includes all council responses', async () => {
    const chatSpy = vi.fn().mockReturnValue(asyncIterableOf([{ content: 'ok', done: true }]))
    const mockProvider: AgentProvider = { name: 'mock', chat: chatSpy, models: vi.fn().mockResolvedValue([]) }

    await collectStream(synthesize(mockProvider, [
      { agent: 'A', text: 'Response A' },
      { agent: 'B', text: 'Response B' },
    ], { model: 'test-model' }))

    const params = chatSpy.mock.calls[0][0]
    const allContent = params.messages.map((m: { content: string }) => m.content).join(' ')
    expect(allContent).toContain('Response A')
    expect(allContent).toContain('Response B')
  })

  test('synthesis prompt includes agent names', async () => {
    const chatSpy = vi.fn().mockReturnValue(asyncIterableOf([{ content: 'ok', done: true }]))
    const mockProvider: AgentProvider = { name: 'mock', chat: chatSpy, models: vi.fn().mockResolvedValue([]) }

    await collectStream(synthesize(mockProvider, [
      { agent: 'Claude', text: 'Some view' },
    ], { model: 'test-model' }))

    const params = chatSpy.mock.calls[0][0]
    const allContent = params.messages.map((m: { content: string }) => m.content).join(' ')
    expect(allContent).toContain('Claude')
  })

  test('uses the provided model', async () => {
    const chatSpy = vi.fn().mockReturnValue(asyncIterableOf([{ content: 'ok', done: true }]))
    const mockProvider: AgentProvider = { name: 'mock', chat: chatSpy, models: vi.fn().mockResolvedValue([]) }

    await collectStream(synthesize(mockProvider, [
      { agent: 'A', text: 'text' },
    ], { model: 'anthropic/claude-3-haiku' }))

    expect(chatSpy.mock.calls[0][0].model).toBe('anthropic/claude-3-haiku')
  })

  test('handles empty response list', async () => {
    const chatSpy = vi.fn().mockReturnValue(asyncIterableOf([{ content: 'Nothing to synthesize', done: true }]))
    const mockProvider: AgentProvider = { name: 'mock', chat: chatSpy, models: vi.fn().mockResolvedValue([]) }

    const text = await collectStreamText(synthesize(mockProvider, [], { model: 'test' }))
    expect(text).toBe('Nothing to synthesize')
  })

  test('passes system prompt to provider', async () => {
    const chatSpy = vi.fn().mockReturnValue(asyncIterableOf([{ content: 'ok', done: true }]))
    const mockProvider: AgentProvider = { name: 'mock', chat: chatSpy, models: vi.fn().mockResolvedValue([]) }

    await collectStream(synthesize(mockProvider, [{ agent: 'A', text: 'text' }], { model: 'test' }))

    const params = chatSpy.mock.calls[0][0]
    expect(params.system).toBeTruthy()
    expect(typeof params.system).toBe('string')
  })
})
