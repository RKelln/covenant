import { test, expect } from 'vitest'
import { renderMarkdown } from '../render'

test('returns empty string for empty input', () => {
  expect(renderMarkdown('')).toBe('')
})

test('renders bold text as <strong>', () => {
  const html = renderMarkdown('**bold word**')
  expect(html).toContain('<strong>bold word</strong>')
})

test('renders italic text as <em>', () => {
  const html = renderMarkdown('*italic word*')
  expect(html).toContain('<em>italic word</em>')
})

test('does not render ** as italic', () => {
  const html = renderMarkdown('**not italic**')
  expect(html).not.toContain('<em>')
  expect(html).toContain('<strong>')
})

test('renders unordered list items', () => {
  const html = renderMarkdown('- item one\n- item two')
  expect(html).toContain('<ul>')
  expect(html).toContain('<li>item one</li>')
  expect(html).toContain('<li>item two</li>')
  expect(html).toContain('</ul>')
})

test('renders ordered list items', () => {
  const html = renderMarkdown('1. first\n2. second')
  expect(html).toContain('<ol>')
  expect(html).toContain('<li>first</li>')
  expect(html).toContain('<li>second</li>')
  expect(html).toContain('</ol>')
})

test('renders h2 heading', () => {
  const html = renderMarkdown('## Section Heading')
  expect(html).toContain('<h2>Section Heading</h2>')
})

test('renders h3 heading', () => {
  const html = renderMarkdown('### Sub Heading')
  expect(html).toContain('<h3>Sub Heading</h3>')
})

test('wraps plain text in <p> tags', () => {
  const html = renderMarkdown('Just a paragraph.')
  expect(html).toContain('<p>Just a paragraph.</p>')
})

test('renders cross-reference with default display', () => {
  const html = renderMarkdown('See §[rights.dignity] for details.')
  expect(html).toContain('class="xref"')
  expect(html).toContain('data-section-id="rights.dignity"')
  expect(html).toContain('§rights.dignity')
})

test('renders cross-reference with custom display callback', () => {
  const html = renderMarkdown('See §[rights.dignity].', id => `[${id}]`)
  expect(html).toContain('[rights.dignity]')
})

test('escapes HTML entities in content', () => {
  const html = renderMarkdown('5 < 10 & 10 > 5')
  expect(html).toContain('&lt;')
  expect(html).toContain('&gt;')
  expect(html).toContain('&amp;')
  expect(html).not.toContain('<10')
})

// Poetic mode (ritual register)
test('poetic mode: adjacent lines joined with <br> into one <p>', () => {
  const html = renderMarkdown('Line one.\nLine two.\nLine three.', undefined, { poetic: true })
  expect(html).toContain('<p>Line one.<br>\nLine two.<br>\nLine three.</p>')
})

test('poetic mode: blank line starts a new stanza <p>', () => {
  const html = renderMarkdown('Stanza one.\nLine two.\n\nStanza two.\nLine four.', undefined, { poetic: true })
  expect(html).toContain('<p>Stanza one.<br>\nLine two.</p>')
  expect(html).toContain('<p>Stanza two.<br>\nLine four.</p>')
})

test('poetic mode: single line stanza is still a <p>', () => {
  const html = renderMarkdown('Alone.\n\nAlso alone.', undefined, { poetic: true })
  expect(html).toContain('<p>Alone.</p>')
  expect(html).toContain('<p>Also alone.</p>')
})

test('non-poetic mode still wraps each line in its own <p>', () => {
  const html = renderMarkdown('Line one.\nLine two.')
  // Each line is its own paragraph in default mode
  const matches = html.match(/<p>/g)
  expect(matches).toHaveLength(2)
})

// Ordered list with indented continuation (Spec format)
test('ordered list: indented continuation line folds into the preceding <li>', () => {
  const md = '1. **Heading**\n   Body text here.'
  const html = renderMarkdown(md)
  expect(html).toContain('<ol>')
  expect(html).toContain('<li>')
  expect(html).toContain('<strong>Heading</strong>')
  expect(html).toContain('Body text here.')
  // Body text must be inside the <li>, not a separate <p>
  expect(html).not.toMatch(/<\/li>\s*<p>Body/)
  expect(html).not.toMatch(/<\/ol>\s*<p>Body/)
})

test('ordered list with continuation: multiple items each with body', () => {
  const md = '1. **First**\n   First body.\n\n2. **Second**\n   Second body.'
  const html = renderMarkdown(md)
  // Both items should be in a single <ol>
  const olMatches = html.match(/<ol>/g)
  expect(olMatches).toHaveLength(1)
  // Both li elements present
  const liMatches = html.match(/<li>/g)
  expect(liMatches).toHaveLength(2)
})
