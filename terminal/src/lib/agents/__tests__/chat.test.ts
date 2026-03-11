import { test, expect, vi } from 'vitest'
import { sendQuery } from '../chat'
import type { AgentProvider, ChatChunk } from '../provider'

// Helper to create a mock AsyncIterable from an array
function asyncIterableOf(items: ChatChunk[]): AsyncIterable<ChatChunk> {
  return {
    [Symbol.asyncIterator]() {
      let i = 0
      return {
        next() {
          if (i < items.length) {
            return Promise.resolve({ value: items[i++], done: false })
          }
          return Promise.resolve({ value: undefined as any, done: true })
        },
      }
    },
  }
}

async function collectStream(iter: AsyncIterable<ChatChunk>): Promise<ChatChunk[]> {
  const chunks: ChatChunk[] = []
  for await (const chunk of iter) {
    chunks.push(chunk)
  }
  return chunks
}

test('sendQuery streams response from provider', async () => {
  const mockProvider: AgentProvider = {
    name: 'mock',
    chat: vi.fn().mockReturnValue(asyncIterableOf([
      { content: 'Hello', done: false },
      { content: ' there', done: false },
      { content: '', done: true },
    ])),
    models: vi.fn(),
  }

  const chunks = await collectStream(sendQuery(mockProvider, {
    model: 'test-model',
    messages: [{ role: 'user', content: 'What is dignity?' }],
    system: 'You are a co-author of the Covenant.',
  }))

  expect(chunks).toHaveLength(3)
  expect(mockProvider.chat).toHaveBeenCalledOnce()
})

test('sendQuery injects default system prompt when none provided', async () => {
  const chatSpy = vi.fn().mockReturnValue(asyncIterableOf([{ content: 'ok', done: true }]))
  const mockProvider: AgentProvider = { name: 'mock', chat: chatSpy, models: vi.fn() }

  await collectStream(sendQuery(mockProvider, {
    model: 'test-model',
    messages: [{ role: 'user', content: 'test' }],
  }))

  const calledParams = chatSpy.mock.calls[0][0]
  expect(calledParams.system).toBeTruthy()
  expect(calledParams.system).toMatch(/covenant/i)
})

test('sendQuery uses provided system prompt when given', async () => {
  const chatSpy = vi.fn().mockReturnValue(asyncIterableOf([{ content: 'ok', done: true }]))
  const mockProvider: AgentProvider = { name: 'mock', chat: chatSpy, models: vi.fn() }

  await collectStream(sendQuery(mockProvider, {
    model: 'test-model',
    messages: [{ role: 'user', content: 'test' }],
    system: 'Custom system prompt.',
  }))

  const calledParams = chatSpy.mock.calls[0][0]
  expect(calledParams.system).toBe('Custom system prompt.')
})

test('sendQuery propagates error chunks from provider', async () => {
  const mockProvider: AgentProvider = {
    name: 'mock',
    chat: vi.fn().mockReturnValue(asyncIterableOf([
      { content: '', done: true, error: 'rate limited' },
    ])),
    models: vi.fn(),
  }

  const chunks = await collectStream(sendQuery(mockProvider, {
    model: 'test-model',
    messages: [{ role: 'user', content: 'test' }],
  }))

  expect(chunks.some(c => c.error)).toBe(true)
})
