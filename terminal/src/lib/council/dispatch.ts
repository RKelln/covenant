import type { AgentProvider, ChatChunk, ChatParams } from '$lib/agents/provider'

export interface CouncilStream {
  providerName: string
  stream: AsyncIterable<ChatChunk>
}

/**
 * Dispatches a query to all providers simultaneously and returns an array of
 * named async iterables — one per provider. Provider errors are caught and
 * surfaced as error chunks so they cannot block other streams.
 */
export function dispatchToCouncil(
  providers: AgentProvider[],
  params: ChatParams,
): CouncilStream[] {
  return providers.map(provider => {
    // Start the chat immediately (parallel kick-off)
    const rawStream = provider.chat(params)

    // Wrap in an error-safe async generator
    async function* safeStream(): AsyncIterable<ChatChunk> {
      try {
        for await (const chunk of rawStream) {
          yield chunk
        }
      } catch (err) {
        yield {
          content: '',
          done: true,
          error: err instanceof Error ? err.message : String(err),
        }
      }
    }

    return {
      providerName: provider.name,
      stream: safeStream(),
    }
  })
}
