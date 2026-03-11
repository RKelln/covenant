/**
 * Render Covenant section markdown to HTML.
 * Handles the subset of markdown used in section bundles + cross-reference syntax.
 */

const XREF_RE = /§\[([^\]]+)\]/g

/**
 * Minimal markdown to HTML converter for section content.
 * Handles: headings, bold, italic, lists, paragraphs, cross-references.
 */
export function renderMarkdown(md: string, onXref?: (id: string) => string): string {
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
    if (h3) { result.push(`<h3>${h3[1]}</h3>`); i++; continue }
    if (h2) { result.push(`<h2>${h2[1]}</h2>`); i++; continue }

    // Unordered list
    const ulItem = line.match(/^[-*] (.+)/)
    if (ulItem) {
      if (!inList) { result.push('<ul>'); inList = true }
      result.push(`<li>${ulItem[1]}</li>`)
      i++; continue
    } else if (inList) { result.push('</ul>'); inList = false }

    // Ordered list
    const olItem = line.match(/^\d+\. (.+)/)
    if (olItem) {
      if (!inOrderedList) { result.push('<ol>'); inOrderedList = true }
      result.push(`<li>${olItem[1]}</li>`)
      i++; continue
    } else if (inOrderedList) { result.push('</ol>'); inOrderedList = false }

    // Blank line
    if (line.trim() === '') {
      result.push('')
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
