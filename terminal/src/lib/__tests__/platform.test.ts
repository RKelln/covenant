import { test, expectTypeOf } from 'vitest'
import type { Platform } from '$lib/platform'

test('Platform interface has required methods', () => {
  const p = {} as Platform
  expectTypeOf(p.readFile).toBeFunction()
  expectTypeOf(p.listSections).toBeFunction()
  expectTypeOf(p.exec).toBeFunction()
  expectTypeOf(p.loadConfig).toBeFunction()
  expectTypeOf(p.saveConfig).toBeFunction()
  expectTypeOf(p.logApiCall).toBeFunction()
})
