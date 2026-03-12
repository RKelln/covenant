/**
 * Render Covenant section markdown to HTML.
 * Handles the subset of markdown used in section bundles + cross-reference syntax.
 */

const XREF_RE = /§\[([^\]]+)\]/g

export interface RenderOptions {
  /** Poetic mode: group consecutive non-blank lines into a single <p> joined with <br>.
   *  Blank lines separate stanzas. Used for the Ritual register. */
  poetic?: boolean
}

/**
 * Minimal markdown to HTML converter for section content.
 * Handles: headings, bold, italic, lists, paragraphs, cross-references.
 */
export function renderMarkdown(md: string, onXref?: (id: string) => string, options?: RenderOptions): string {
  if (!md) return ''

  let html = md
    // Escape HTML entities
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  // Cross-references: §[section.id]
  html = html.replace(XREF_RE, (_, id) => {
    const display = onXref ? onXref(id) : `§${id}`
    return `<span class="xref" data-section-id="${id}">${display}</span>`
  })

  // Bold **text**
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')

  // Italic *text* (but not **)
  html = html.replace(/(?<!\*)\*(?!\*)([^*]+)(?<!\*)\*(?!\*)/g, '<em>$1</em>')

  if (options?.poetic) {
    return renderPoetic(html)
  }

  // Process line by line for blocks
  const lines = html.split('\n')
  const result: string[] = []
  let inList = false
  let inOrderedList = false
  let i = 0

  while (i < lines.length) {
    const line = lines[i]

    // Headings
    const h3 = line.match(/^### (.+)/)
    const h2 = line.match(/^## (.+)/)
    if (h3) {
      if (inList) { result.push('</ul>'); inList = false }
      if (inOrderedList) { result.push('</ol>'); inOrderedList = false }
      result.push(`<h3>${h3[1]}</h3>`)
      i++; continue
    }
    if (h2) {
      if (inList) { result.push('</ul>'); inList = false }
      if (inOrderedList) { result.push('</ol>'); inOrderedList = false }
      result.push(`<h2>${h2[1]}</h2>`)
      i++; continue
    }

    // Unordered list item
    const ulItem = line.match(/^[-*] (.+)/)
    if (ulItem) {
      if (inOrderedList) { result.push('</ol>'); inOrderedList = false }
      if (!inList) { result.push('<ul>'); inList = true }
      result.push(`<li>${ulItem[1]}</li>`)
      i++; continue
    }

    // Ordered list item (with optional indented continuation lines)
    const olItem = line.match(/^(\d+)\. (.+)/)
    if (olItem) {
      if (inList) { result.push('</ul>'); inList = false }
      if (!inOrderedList) { result.push('<ol>'); inOrderedList = true }
      // Collect indented continuation lines (blank lines between items are allowed)
      const itemLines: string[] = [olItem[2]]
      let j = i + 1
      while (j < lines.length) {
        const next = lines[j]
        if (next.match(/^(\d+)\. /)) break            // next numbered item — stop
        if (next.match(/^[-*] /)) break               // unordered item — stop
        if (next.match(/^##/)) break                  // heading — stop
        if (next.trim() !== '') {
          // Non-blank, non-list line — treat as continuation if indented OR immediately follows
          itemLines.push(next.trim())
        }
        // blank lines between item and continuation, or between items: skip but stay in list
        j++
      }
      result.push(`<li>${itemLines.join(' ')}</li>`)
      i = j
      continue
    }

    // If we reach here, we're out of list context
    if (inList) { result.push('</ul>'); inList = false }
    if (inOrderedList) { result.push('</ol>'); inOrderedList = false }

    // Blank line — skip
    if (line.trim() === '') {
      i++; continue
    }

    // Paragraph
    result.push(`<p>${line}</p>`)
    i++
  }

  if (inList) result.push('</ul>')
  if (inOrderedList) result.push('</ol>')

  return result.join('\n')
}

/**
 * Render poetic/ritual text: consecutive non-blank lines become one <p> joined with <br>.
 * Blank lines separate stanzas.
 */
function renderPoetic(html: string): string {
  const lines = html.split('\n')
  const result: string[] = []
  let stanza: string[] = []

  function flushStanza() {
    if (stanza.length === 0) return
    result.push(`<p>${stanza.join('<br>\n')}</p>`)
    stanza = []
  }

  for (const line of lines) {
    if (line.trim() === '') {
      flushStanza()
    } else {
      stanza.push(line)
    }
  }
  flushStanza()

  return result.join('\n')
}
