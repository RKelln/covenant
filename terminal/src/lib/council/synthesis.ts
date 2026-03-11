import type { AgentProvider, ChatChunk } from '$lib/agents/provider'

export interface CouncilResponse {
  agent: string
  text: string
}

export interface SynthesisParams {
  model: string
  temperature?: number
}

const SYNTHESIS_SYSTEM_PROMPT = `You are a synthesis reader of the Covenant — a living compact between human communities and emerging machine intelligences.

You have received responses from multiple AI council members on a question about the Covenant. Your task is to synthesize their perspectives into a coherent summary that:

1. Identifies points of convergence across the responses
2. Notes meaningful divergences or tensions
3. Highlights any implied decisions or editorial choices facing the steward
4. Remains faithful to each voice without flattening differences

Write in a calm, precise register. Use the § symbol when referring to specific sections. Do not declare winners or make your own editorial judgment — illuminate the space of views.`

/**
 * Synthesizes multiple council responses into a single streaming response.
 * The synthesis prompt includes all agent responses and asks the provider
 * to identify convergence, divergence, and implied decisions.
 */
export function synthesize(
  provider: AgentProvider,
  responses: CouncilResponse[],
  params: SynthesisParams,
): AsyncIterable<ChatChunk> {
  const responseBlock = responses.length === 0
    ? 'No council responses were provided.'
    : responses.map(r => `## ${r.agent}\n\n${r.text}`).join('\n\n---\n\n')

  const userMessage = `Here are the council responses:\n\n${responseBlock}\n\nPlease synthesize these perspectives.`

  return provider.chat({
    model: params.model,
    temperature: params.temperature,
    system: SYNTHESIS_SYSTEM_PROMPT,
    messages: [
      { role: 'user', content: userMessage },
    ],
  })
}
