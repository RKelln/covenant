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
