import type { Section, SectionFrontmatter, SectionStatus } from './types'

/**
 * Parse YAML frontmatter from a markdown string.
 * Returns the parsed object and the remaining content after the frontmatter block.
 */
function parseFrontmatter(raw: string): { frontmatter: SectionFrontmatter; body: string } {
  if (!raw.startsWith('---')) {
    throw new Error('Section must begin with YAML frontmatter (---)')
  }
  const end = raw.indexOf('\n---', 3)
  if (end === -1) {
    throw new Error('Frontmatter block not closed (missing closing ---)')
  }
  const yamlBlock = raw.slice(4, end).trim()
  const body = raw.slice(end + 4).trim()
  const frontmatter = parseYaml(yamlBlock) as SectionFrontmatter
  return { frontmatter, body }
}

/**
 * Minimal YAML parser for the Covenant section frontmatter schema.
 * Handles: string values, quoted strings, arrays (block and inline), booleans.
 * Not a general YAML parser — only covers what the section bundle uses.
 */
function parseYaml(yaml: string): Record<string, unknown> {
  const result: Record<string, unknown> = {}
  const lines = yaml.split('\n')
  let i = 0
  while (i < lines.length) {
    const line = lines[i]
    const colonIdx = line.indexOf(':')
    if (colonIdx === -1) { i++; continue }
    const key = line.slice(0, colonIdx).trim()
    let value = line.slice(colonIdx + 1).trim()

    if (value === '' || value === '[]') {
      // Could be a block list or empty
      if (i + 1 < lines.length && lines[i + 1].trimStart().startsWith('-')) {
        const items: string[] = []
        i++
        while (i < lines.length && lines[i].trimStart().startsWith('-')) {
          items.push(lines[i].replace(/^\s*-\s*/, '').trim().replace(/^["']|["']$/g, ''))
          i++
        }
        result[key] = value === '[]' ? [] : items
        continue
      } else {
        result[key] = value === '[]' ? [] : ''
      }
    } else if (value.startsWith('[')) {
      // Inline array
      const inner = value.slice(1, value.lastIndexOf(']'))
      result[key] = inner
        ? inner.split(',').map(s => s.trim().replace(/^["']|["']$/g, ''))
        : []
    } else if (value.startsWith('"') || value.startsWith("'")) {
      result[key] = value.slice(1, value.length - 1)
    } else if (value === 'true') {
      result[key] = true
    } else if (value === 'false') {
      result[key] = false
    } else {
      result[key] = value
    }
    i++
  }
  return result
}

/**
 * Extract a named register section (# Ritual, # Spec, # Digest, # Log) from the body.
 * Returns the content between this heading and the next same-level heading (or end of string).
 */
function extractRegister(body: string, name: string): string {
  const headingPattern = new RegExp(`^# ${name}\\s*$`, 'mi')
  const match = headingPattern.exec(body)
  if (!match) return ''

  const start = match.index + match[0].length
  // Find the next # heading at the same level
  const remaining = body.slice(start)
  const nextHeading = /^# \w/m.exec(remaining)
  const end = nextHeading ? nextHeading.index : remaining.length
  return remaining.slice(0, end).trim()
}

/**
 * Parse a Covenant section bundle markdown string into a Section object.
 */
export function parseSection(raw: string): Section {
  const { frontmatter, body } = parseFrontmatter(raw)

  if (!frontmatter.id || typeof frontmatter.id !== 'string') {
    throw new Error('Section frontmatter must have a non-empty "id" field')
  }
  if (!frontmatter.title || typeof frontmatter.title !== 'string') {
    throw new Error('Section frontmatter must have a non-empty "title" field')
  }
  if (!frontmatter.status) {
    throw new Error('Section frontmatter must have a "status" field')
  }

  return {
    id: frontmatter.id,
    title: frontmatter.title,
    status: frontmatter.status as SectionStatus,
    since: (frontmatter.since as string) ?? '',
    category: frontmatter.id.split('.')[0] ?? frontmatter.id,
    frontmatter: {
      ...frontmatter,
      depends_on: Array.isArray(frontmatter.depends_on) ? frontmatter.depends_on : [],
      terms_introduced: Array.isArray(frontmatter.terms_introduced) ? frontmatter.terms_introduced : [],
    },
    ritual: extractRegister(body, 'Ritual'),
    spec: extractRegister(body, 'Spec'),
    digest: extractRegister(body, 'Digest'),
    log: extractRegister(body, 'Log'),
  }
}
