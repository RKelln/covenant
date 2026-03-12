import { test, expect } from 'vitest'
import { mount } from 'svelte'

test('vitest is configured', () => {
  expect(1 + 1).toBe(2)
})

test('svelte mount API is available (Svelte 5)', () => {
  // Ensures we are using the Svelte 5 mount() API, not the legacy new Component() API
  expect(typeof mount).toBe('function')
})
