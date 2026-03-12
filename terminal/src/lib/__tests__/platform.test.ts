import { test, expect, expectTypeOf } from 'vitest'
import type { Platform } from '$lib/platform'
import { isTauri } from '@tauri-apps/api/core'

test('Platform interface has required methods', () => {
  const p = {} as Platform
  expectTypeOf(p.readFile).toBeFunction()
  expectTypeOf(p.listSections).toBeFunction()
  expectTypeOf(p.exec).toBeFunction()
  expectTypeOf(p.loadConfig).toBeFunction()
  expectTypeOf(p.saveConfig).toBeFunction()
  expectTypeOf(p.logApiCall).toBeFunction()
})

test('isTauri() is used for environment detection (not window.__TAURI_INTERNALS__)', () => {
  // In the test environment (browser via Playwright, no Tauri), isTauri() should be false
  expect(isTauri()).toBe(false)
})
