/**
 * Conversation logging for debugging and provenance.
 *
 * Each call to appendConversationLog appends one JSONL line to
 * `conversation-log.jsonl` in the platform's writable location.
 *
 * In web mode, platform.writeFile throws — errors are swallowed silently
 * so logging never breaks the query flow.
 */

import type { Platform } from '$lib/platform'
import type { CouncilMode } from './prompts'

export interface ConversationResponse {
  agent: string
  model: string
  text: string
}

export interface ConversationEntry {
  timestamp: string
  sectionId: string | null
  sectionTitle: string | null
  mode: CouncilMode
  query: string
  systemPrompt: string
  responses: ConversationResponse[]
}

const LOG_PATH = 'conversation-log.jsonl'

/**
 * Append a conversation entry to the log file.
 * Reads the existing file first (to preserve prior entries), then writes
 * the full content back with the new entry appended.
 *
 * Errors (file not found, write failure) are caught and logged to console —
 * they must never propagate to the caller.
 */
export async function appendConversationLog(
  platform: Platform,
  entry: ConversationEntry,
): Promise<void> {
  try {
    let existing = ''
    try {
      existing = await platform.readFile(LOG_PATH)
    } catch {
      // File doesn't exist yet — start fresh
    }

    const line = JSON.stringify(entry)
    const content = existing
      ? existing.trimEnd() + '\n' + line + '\n'
      : line + '\n'

    await platform.writeFile(LOG_PATH, content)
  } catch (err) {
    console.warn('[conversation-log] Failed to write log entry:', err)
  }
}
