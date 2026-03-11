import { test, expect, expectTypeOf } from 'vitest'
import type { AgentProvider, ChatChunk, ChatParams, Message, ModelInfo } from '../provider'

test('AgentProvider interface shape', () => {
  const p: AgentProvider = {} as AgentProvider
  expectTypeOf(p.name).toBeString()
  expectTypeOf(p.chat).toBeFunction()
  expectTypeOf(p.models).toBeFunction()
})

test('ChatChunk type has content and done fields', () => {
  const chunk: ChatChunk = { content: 'hello', done: false }
  expect(chunk.content).toBe('hello')
  expect(chunk.done).toBe(false)
})

test('ChatChunk can carry an optional error', () => {
  const chunk: ChatChunk = { content: '', done: true, error: 'rate limited' }
  expect(chunk.error).toBe('rate limited')
})

test('Message type has role and content', () => {
  const msg: Message = { role: 'user', content: 'Hello' }
  expectTypeOf(msg.role).toMatchTypeOf<'user' | 'assistant' | 'system'>()
  expectTypeOf(msg.content).toBeString()
})

test('ChatParams type has required model and messages fields', () => {
  const params: ChatParams = {
    model: 'openai/gpt-4o-mini',
    messages: [{ role: 'user', content: 'test' }],
  }
  expectTypeOf(params.model).toBeString()
  expectTypeOf(params.messages).toBeArray()
})

test('ModelInfo type has id, name, provider fields', () => {
  const model: ModelInfo = {
    id: 'openai/gpt-4o-mini',
    name: 'GPT-4o mini',
    provider: 'openrouter',
    context_length: 128000,
  }
  expectTypeOf(model.id).toBeString()
  expectTypeOf(model.name).toBeString()
  expectTypeOf(model.provider).toBeString()
})
