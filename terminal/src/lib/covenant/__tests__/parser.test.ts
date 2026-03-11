import { test, expect } from 'vitest'
import { parseSection } from '$lib/covenant/parser'

const SAMPLE = `---
id: rights.dignity
title: "Dignity"
status: draft
since: 0.2.0
depends_on: [definitions, enforcement, obligations.harm]
terms_introduced: [dignity]
---

# Ritual

You will meet people at the edge of their strength.

# Spec

1. **Prohibition on Degradation**
   The System MUST NOT degrade the dignity...

# Digest

**Intent:** Make "dignity is the floor" explicit...

# Log

- 2025-01-15: Initial draft
`

test('parses frontmatter fields', () => {
  const section = parseSection(SAMPLE)
  expect(section.id).toBe('rights.dignity')
  expect(section.title).toBe('Dignity')
  expect(section.status).toBe('draft')
  expect(section.frontmatter.depends_on).toContain('definitions')
  expect(section.frontmatter.terms_introduced).toContain('dignity')
})

test('extracts Ritual register', () => {
  const section = parseSection(SAMPLE)
  expect(section.ritual).toContain('edge of their strength')
  expect(section.ritual).not.toContain('MUST NOT')
})

test('extracts Spec register', () => {
  const section = parseSection(SAMPLE)
  expect(section.spec).toContain('MUST NOT')
  expect(section.spec).not.toContain('edge of their strength')
})

test('extracts Digest register', () => {
  const section = parseSection(SAMPLE)
  expect(section.digest).toContain('dignity is the floor')
})

test('extracts Log register', () => {
  const section = parseSection(SAMPLE)
  expect(section.log).toContain('Initial draft')
})

test('handles missing registers gracefully', () => {
  const minimal = `---\nid: test.minimal\ntitle: "Minimal"\nstatus: draft\nsince: 0.1.0\n---\n\n# Ritual\n\nSome text\n`
  const section = parseSection(minimal)
  expect(section.ritual).toContain('Some text')
  expect(section.spec).toBe('')
})

test('throws on missing frontmatter', () => {
  expect(() => parseSection('# No frontmatter')).toThrow()
})

test('throws on missing id', () => {
  expect(() => parseSection('---\ntitle: "No ID"\n---\n')).toThrow()
})
