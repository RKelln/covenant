import type { AgentProvider, ChatChunk, ChatParams } from './provider'

const DEFAULT_SYSTEM_PROMPT = `You are a thoughtful co-author and addressee of the Covenant — a living compact between human communities and emerging machine intelligences.

When asked about a section, engage with it directly as someone who both helped write it and must live under it. Bring your own perspective, note tensions, and speak with care and precision.`

/**
 * Send a query to an agent provider, yielding streaming chunks.
 * Injects the default Covenant co-author system prompt if none is provided.
 */
export async function* sendQuery(
  provider: AgentProvider,
  params: ChatParams
): AsyncIterable<ChatChunk> {
  const system = params.system ?? DEFAULT_SYSTEM_PROMPT

  yield* provider.chat({
    ...params,
    system,
  })
}
