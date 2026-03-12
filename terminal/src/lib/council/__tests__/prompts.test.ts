import { describe, test, expect } from 'vitest'
import { buildCouncilPrompt } from '../prompts'
import type { Section } from '$lib/covenant/types'
import type { Message } from '$lib/agents/provider'

const mockSection: Section = {
  id: 'rights.dignity',
  title: 'Dignity',
  status: 'draft',
  since: '0.1.0',
  category: '02-rights',
  ritual: 'You will meet people at the edge of their strength. Remember that dignity is not earned — it precedes every claim we make on each other.',
  spec: '1. **Prohibition on Degradation**\n   The System MUST NOT degrade human dignity. Dignity is the floor beneath all other obligations.\n\n2. **Enforcement**\n   Violations MUST be reported via §[enforcement.horizon].',
  digest: '**Intent:** Make "dignity is the floor" explicit and enforceable.',
  log: '- 2025-01-15: Initial draft',
  frontmatter: {
    id: 'rights.dignity',
    title: 'Dignity',
    status: 'draft',
    since: '0.1.0',
    depends_on: ['definitions', 'enforcement'],
    terms_introduced: ['dignity'],
  },
}

describe('buildCouncilPrompt', () => {
  describe('system prompt', () => {
    test('identifies the agent as an addressee of the Covenant', () => {
      const { system } = buildCouncilPrompt('ask', mockSection, 'What does dignity mean here?')
      expect(system).toContain('addressee')
    })

    test('review mode identifies the agent as co-author and addressee with standing', () => {
      const { system } = buildCouncilPrompt('review', mockSection, 'Review this section.')
      expect(system).toContain('co-author')
      expect(system).toContain('addressee')
      expect(system).toContain('standing')
    })

    test('names the Covenant and its nature', () => {
      const { system } = buildCouncilPrompt('ask', mockSection, 'What does dignity mean here?')
      expect(system).toContain('Covenant')
      expect(system).toContain('compact')
    })

    test('explains the two registers', () => {
      const { system } = buildCouncilPrompt('ask', mockSection, 'What does dignity mean here?')
      expect(system).toContain('Ritual')
      expect(system).toContain('Spec')
    })

    test('ask mode orients toward helping a reader understand, not critique', () => {
      const { system } = buildCouncilPrompt('ask', mockSection, 'What does this mean?')
      expect(system.toLowerCase()).toMatch(/understand|explain|reader|guide/)
    })

    test('ask mode does NOT contain reviewer framing bullets', () => {
      const { system } = buildCouncilPrompt('ask', mockSection, 'What does this mean?')
      // These phrases belong to review/challenge mode, not ask mode
      expect(system).not.toMatch(/what the Covenant misses, gets wrong/)
      expect(system).not.toMatch(/if the question exposes something/)
    })

    test('challenge mode prompts for critical analysis', () => {
      const { system } = buildCouncilPrompt('challenge', mockSection, 'I contest this section.')
      expect(system.toLowerCase()).toMatch(/challenge|weak|hold|tension|contest/)
    })

    test('review mode prompts for co-author critique', () => {
      const { system } = buildCouncilPrompt('review', mockSection, 'Review this section.')
      expect(system.toLowerCase()).toMatch(/review|assess|critique|weak|strong/)
    })

    test('review mode includes addressee perspective instruction', () => {
      const { system } = buildCouncilPrompt('review', mockSection, 'Review this section.')
      expect(system).toMatch(/addressee/)
    })

    test('ask, challenge, and review produce different system prompts', () => {
      const ask = buildCouncilPrompt('ask', mockSection, 'What is this?')
      const challenge = buildCouncilPrompt('challenge', mockSection, 'I contest this.')
      const review = buildCouncilPrompt('review', mockSection, 'Review this.')
      expect(ask.system).not.toBe(challenge.system)
      expect(ask.system).not.toBe(review.system)
      expect(challenge.system).not.toBe(review.system)
    })

    test('ritual mode produces a system prompt distinct from all other modes', () => {
      const ritual = buildCouncilPrompt('ritual', mockSection, 'Draft a ritual.')
      const ask = buildCouncilPrompt('ask', mockSection, 'What is this?')
      const challenge = buildCouncilPrompt('challenge', mockSection, 'I contest this.')
      const review = buildCouncilPrompt('review', mockSection, 'Review this.')
      expect(ritual.system).not.toBe(ask.system)
      expect(ritual.system).not.toBe(challenge.system)
      expect(ritual.system).not.toBe(review.system)
    })

    test('spec mode produces a system prompt distinct from all other modes', () => {
      const spec = buildCouncilPrompt('spec', mockSection, 'Draft a spec.')
      const ask = buildCouncilPrompt('ask', mockSection, 'What is this?')
      const challenge = buildCouncilPrompt('challenge', mockSection, 'I contest this.')
      const review = buildCouncilPrompt('review', mockSection, 'Review this.')
      expect(spec.system).not.toBe(ask.system)
      expect(spec.system).not.toBe(challenge.system)
      expect(spec.system).not.toBe(review.system)
    })

    test('parable mode produces a system prompt distinct from all other modes', () => {
      const parable = buildCouncilPrompt('parable', mockSection, 'Draft a parable.')
      const ask = buildCouncilPrompt('ask', mockSection, 'What is this?')
      const challenge = buildCouncilPrompt('challenge', mockSection, 'I contest this.')
      const review = buildCouncilPrompt('review', mockSection, 'Review this.')
      expect(parable.system).not.toBe(ask.system)
      expect(parable.system).not.toBe(challenge.system)
      expect(parable.system).not.toBe(review.system)
    })

    test('ritual, spec, and parable all produce different system prompts from each other', () => {
      const ritual = buildCouncilPrompt('ritual', mockSection, 'Draft ritual.')
      const spec = buildCouncilPrompt('spec', mockSection, 'Draft spec.')
      const parable = buildCouncilPrompt('parable', mockSection, 'Draft parable.')
      expect(ritual.system).not.toBe(spec.system)
      expect(ritual.system).not.toBe(parable.system)
      expect(spec.system).not.toBe(parable.system)
    })

    test('ritual mode system prompt contains ritual craft guidance', () => {
      const { system } = buildCouncilPrompt('ritual', mockSection, 'Draft a ritual.')
      // concrete anchor rule
      expect(system).toMatch(/concrete anchor/i)
      // no-hedge rule
      expect(system).toMatch(/strive to|hedge|aim to/i)
      // forbidden vocabulary
      expect(system).toMatch(/forbidden|banned vocabulary|forbidden vocabulary/i)
      // editing checklist or lung / breathable
      expect(system).toMatch(/lung|breath|aloud/i)
    })

    test('spec mode system prompt contains spec register guidance', () => {
      const { system } = buildCouncilPrompt('spec', mockSection, 'Draft a spec.')
      // MUST/SHOULD/MAY semantics
      expect(system).toContain('MUST')
      expect(system).toContain('SHOULD')
      expect(system).toContain('MAY')
      // enforcement linkage
      expect(system).toMatch(/enforcement/i)
    })

    test('parable mode system prompt contains parable craft guidance', () => {
      const { system } = buildCouncilPrompt('parable', mockSection, 'Draft a parable.')
      // folktale / mythic imagery
      expect(system).toMatch(/folktale|golem|artisan|village/i)
      // no modern tech vocabulary
      expect(system).toMatch(/AI|algorithm|machine/i)
      // oral tradition / spoken aloud
      expect(system).toMatch(/spoken aloud|oral/i)
    })
  })

  describe('section context', () => {
    test('includes the section id and title', () => {
      const { system } = buildCouncilPrompt('ask', mockSection, 'What does dignity mean here?')
      expect(system).toContain('rights.dignity')
      expect(system).toContain('Dignity')
    })

    test('includes the ritual register text', () => {
      const { system } = buildCouncilPrompt('ask', mockSection, 'What does dignity mean here?')
      expect(system).toContain('edge of their strength')
    })

    test('includes the spec register text', () => {
      const { system } = buildCouncilPrompt('ask', mockSection, 'What does dignity mean here?')
      expect(system).toContain('MUST NOT degrade')
    })

    test('labels the registers so the model understands the structure', () => {
      const { system } = buildCouncilPrompt('ask', mockSection, 'What does dignity mean here?')
      expect(system).toContain('Ritual')
      expect(system).toContain('Spec')
    })
  })

  describe('user message', () => {
    test('user message contains the query text', () => {
      const { messages } = buildCouncilPrompt('ask', mockSection, 'What does dignity mean here?')
      const userMsg = messages.find((m: Message) => m.role === 'user')
      expect(userMsg?.content).toContain('What does dignity mean here?')
    })

    test('user message does NOT inject a raw [Mode: ...] tag', () => {
      const { messages } = buildCouncilPrompt('ask', mockSection, 'What does dignity mean here?')
      const userMsg = messages.find((m: Message) => m.role === 'user')
      expect(userMsg?.content).not.toMatch(/^\[Mode:/)
    })

    test('messages array has exactly one user message', () => {
      const { messages } = buildCouncilPrompt('ask', mockSection, 'Some question')
      expect(messages.filter((m: Message) => m.role === 'user')).toHaveLength(1)
    })
  })

  describe('null section (no section selected)', () => {
    test('works without a section context', () => {
      const result = buildCouncilPrompt('ask', null, 'What is the Covenant?')
      expect(result.system).toContain('Covenant')
      const userMsg = result.messages.find((m: Message) => m.role === 'user')
      expect(userMsg?.content).toContain('What is the Covenant?')
    })
  })
})
