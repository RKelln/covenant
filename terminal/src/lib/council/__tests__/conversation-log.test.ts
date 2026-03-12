import { describe, test, expect, vi, beforeEach } from 'vitest'
import { appendConversationLog } from '../conversation-log'
import type { ConversationEntry } from '../conversation-log'
import type { Platform } from '$lib/platform'

function mockPlatform(overrides: Partial<Platform> = {}): Platform {
  return {
    readFile: vi.fn(),
    writeFile: vi.fn().mockResolvedValue(undefined),
    listSections: vi.fn(),
    exec: vi.fn(),
    loadConfig: vi.fn(),
    saveConfig: vi.fn(),
    loadModelCache: vi.fn(),
    saveModelCache: vi.fn(),
    logApiCall: vi.fn(),
    ...overrides,
  }
}

const entry: ConversationEntry = {
  timestamp: '2026-03-12T12:00:00.000Z',
  sectionId: 'rights.dignity',
  sectionTitle: 'Dignity',
  mode: 'ask',
  query: 'What does dignity mean here?',
  systemPrompt: 'You are deeply familiar with the Covenant...',
  responses: [
    { agent: 'GPT-4o', model: 'openai/gpt-4o', text: 'Dignity here means...' },
    { agent: 'Claude', model: 'anthropic/claude-opus', text: 'The section grounds dignity in...' },
  ],
}

describe('appendConversationLog', () => {
  test('calls platform.writeFile with a JSONL path', async () => {
    const platform = mockPlatform()
    await appendConversationLog(platform, entry)
    expect(platform.writeFile).toHaveBeenCalledOnce()
    const [path] = (platform.writeFile as ReturnType<typeof vi.fn>).mock.calls[0]
    expect(path).toMatch(/conversation-log/)
    expect(path).toMatch(/\.jsonl$/)
  })

  test('writes the entry as valid JSON on a single line', async () => {
    const platform = mockPlatform()
    await appendConversationLog(platform, entry)
    const [, content] = (platform.writeFile as ReturnType<typeof vi.fn>).mock.calls[0]
    // Content must be valid JSON (one or more lines; entry line must parse)
    const lines = (content as string).trim().split('\n').filter(Boolean)
    expect(lines.length).toBeGreaterThanOrEqual(1)
    const lastLine = lines[lines.length - 1]
    expect(() => JSON.parse(lastLine)).not.toThrow()
  })

  test('written entry contains timestamp, sectionId, mode, and query', async () => {
    const platform = mockPlatform()
    await appendConversationLog(platform, entry)
    const [, content] = (platform.writeFile as ReturnType<typeof vi.fn>).mock.calls[0]
    const lines = (content as string).trim().split('\n').filter(Boolean)
    const parsed = JSON.parse(lines[lines.length - 1])
    expect(parsed.timestamp).toBe(entry.timestamp)
    expect(parsed.sectionId).toBe(entry.sectionId)
    expect(parsed.mode).toBe(entry.mode)
    expect(parsed.query).toBe(entry.query)
  })

  test('written entry contains responses array', async () => {
    const platform = mockPlatform()
    await appendConversationLog(platform, entry)
    const [, content] = (platform.writeFile as ReturnType<typeof vi.fn>).mock.calls[0]
    const lines = (content as string).trim().split('\n').filter(Boolean)
    const parsed = JSON.parse(lines[lines.length - 1])
    expect(Array.isArray(parsed.responses)).toBe(true)
    expect(parsed.responses).toHaveLength(2)
    expect(parsed.responses[0].agent).toBe('GPT-4o')
  })

  test('appends to existing content by reading first', async () => {
    const existingLine = JSON.stringify({ timestamp: '2026-03-11T00:00:00.000Z', query: 'old' })
    const platform = mockPlatform({
      readFile: vi.fn().mockResolvedValue(existingLine + '\n'),
    })
    await appendConversationLog(platform, entry)
    const [, content] = (platform.writeFile as ReturnType<typeof vi.fn>).mock.calls[0]
    const lines = (content as string).trim().split('\n').filter(Boolean)
    // Should have both lines
    expect(lines.length).toBe(2)
    expect(JSON.parse(lines[0]).query).toBe('old')
    expect(JSON.parse(lines[1]).query).toBe('What does dignity mean here?')
  })

  test('does not throw if readFile fails (treats as empty log)', async () => {
    const platform = mockPlatform({
      readFile: vi.fn().mockRejectedValue(new Error('file not found')),
    })
    await expect(appendConversationLog(platform, entry)).resolves.not.toThrow()
    expect(platform.writeFile).toHaveBeenCalledOnce()
  })

  test('does not throw if platform.writeFile fails', async () => {
    const platform = mockPlatform({
      writeFile: vi.fn().mockRejectedValue(new Error('disk full')),
    })
    await expect(appendConversationLog(platform, entry)).resolves.not.toThrow()
  })
})
