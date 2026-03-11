import type { ChatChunk } from '$lib/agents/provider'

export interface AgentStreamState {
  name: string
  text: string
  chunks: ChatChunk[]
  streaming: boolean
  done: boolean
  error: string | undefined
  push(chunk: ChatChunk): void
  pushError(err: Error): void
  reset(): void
}

/**
 * Creates a mutable state object that accumulates chunks from a single agent stream.
 * Designed to be held in $state() in Svelte components.
 */
export function createAgentStreamState(name: string): AgentStreamState {
  let text = ''
  let chunks: ChatChunk[] = []
  let streaming = false
  let done = false
  let error: string | undefined

  const state: AgentStreamState = {
    get name() { return name },
    get text() { return text },
    get chunks() { return chunks },
    get streaming() { return streaming },
    get done() { return done },
    get error() { return error },

    push(chunk: ChatChunk) {
      chunks = [...chunks, chunk]
      if (chunk.content) text += chunk.content
      if (chunk.error) {
        error = chunk.error
        streaming = false
        done = true
      } else if (chunk.done) {
        streaming = false
        done = true
      } else {
        streaming = true
      }
    },

    pushError(err: Error) {
      error = err.message
      streaming = false
      done = true
    },

    reset() {
      text = ''
      chunks = []
      streaming = false
      done = false
      error = undefined
    },
  }

  return state
}
