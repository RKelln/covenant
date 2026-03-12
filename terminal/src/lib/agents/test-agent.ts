import type { AgentProvider } from './provider'

export interface AgentTestResult {
  ok: boolean
  /** First token received from the model, confirming it's live */
  preview?: string
  error?: string
}

/**
 * Sends a minimal one-token probe to the given provider and resolves with
 * whether it succeeded. Designed to be called before adding an agent to the
 * council roster so bad model IDs or auth failures surface immediately.
 *
 * Times out after `timeoutMs` (default 15 s) — enough for cold-start latency
 * on cheaper models without hanging the UI indefinitely.
 */
export async function testAgent(
  provider: AgentProvider,
  timeoutMs = 15_000,
): Promise<AgentTestResult> {
  const probe = async (): Promise<AgentTestResult> => {
    let preview = ''
    for await (const chunk of provider.chat({
      model: '', // overridden by per-instance model in the provider
      messages: [{ role: 'user', content: 'Reply with one word: ready' }],
      max_tokens: 8,
    })) {
      if (chunk.error) {
        return { ok: false, error: chunk.error }
      }
      if (chunk.content) preview += chunk.content
      if (chunk.done) break
    }
    return { ok: true, preview: preview.trim() }
  }

  const timeout = new Promise<AgentTestResult>(resolve =>
    setTimeout(() => resolve({ ok: false, error: 'Timed out — no response after 15 s' }), timeoutMs)
  )

  try {
    return await Promise.race([probe(), timeout])
  } catch (err) {
    return { ok: false, error: err instanceof Error ? err.message : String(err) }
  }
}
