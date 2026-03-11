import { describe, test, expect } from 'vitest'
import { createAgentStreamState } from '../stream'
import type { ChatChunk } from '$lib/agents/provider'

describe('AgentStreamState', () => {
  test('starts with empty text and streaming=false', () => {
    const state = createAgentStreamState('Claude')
    expect(state.name).toBe('Claude')
    expect(state.text).toBe('')
    expect(state.streaming).toBe(false)
    expect(state.error).toBeUndefined()
    expect(state.done).toBe(false)
  })

  test('accumulates chunks into text', () => {
    const state = createAgentStreamState('Claude')
    state.push({ content: 'Hello ', done: false })
    state.push({ content: 'world', done: false })
    expect(state.text).toBe('Hello world')
    expect(state.streaming).toBe(true)
    expect(state.done).toBe(false)
  })

  test('marks streaming=true when first chunk arrives (non-done)', () => {
    const state = createAgentStreamState('Claude')
    state.push({ content: 'hi', done: false })
    expect(state.streaming).toBe(true)
  })

  test('marks done=true and streaming=false when final chunk received', () => {
    const state = createAgentStreamState('Claude')
    state.push({ content: 'Done', done: false })
    state.push({ content: '', done: true })
    expect(state.streaming).toBe(false)
    expect(state.done).toBe(true)
    expect(state.text).toBe('Done')
  })

  test('done chunk with content appends it', () => {
    const state = createAgentStreamState('Claude')
    state.push({ content: 'Final.', done: true })
    expect(state.text).toBe('Final.')
    expect(state.done).toBe(true)
  })

  test('captures error state from pushError', () => {
    const state = createAgentStreamState('GPT')
    state.pushError(new Error('rate limited'))
    expect(state.error).toBe('rate limited')
    expect(state.streaming).toBe(false)
    expect(state.done).toBe(true)
  })

  test('captures error state from error chunk', () => {
    const state = createAgentStreamState('GPT')
    state.push({ content: '', done: true, error: 'network failure' })
    expect(state.error).toBe('network failure')
    expect(state.streaming).toBe(false)
    expect(state.done).toBe(true)
  })

  test('reset() clears all state', () => {
    const state = createAgentStreamState('Claude')
    state.push({ content: 'Some text', done: false })
    state.reset()
    expect(state.text).toBe('')
    expect(state.streaming).toBe(false)
    expect(state.done).toBe(false)
    expect(state.error).toBeUndefined()
  })

  test('chunks array accumulates all received chunks', () => {
    const state = createAgentStreamState('Claude')
    const c1: ChatChunk = { content: 'A', done: false }
    const c2: ChatChunk = { content: 'B', done: false }
    state.push(c1)
    state.push(c2)
    expect(state.chunks).toHaveLength(2)
    expect(state.chunks[0]).toEqual(c1)
    expect(state.chunks[1]).toEqual(c2)
  })
})
