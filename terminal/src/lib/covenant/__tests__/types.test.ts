import { test, expectTypeOf } from 'vitest'
import type { Section } from '$lib/covenant/types'

test('Section type has required fields', () => {
  const s = {} as Section
  expectTypeOf(s.id).toBeString()
  expectTypeOf(s.title).toBeString()
  expectTypeOf(s.status).toMatchTypeOf<'draft' | 'stable' | 'proposed'>()
  expectTypeOf(s.ritual).toBeString()
  expectTypeOf(s.spec).toBeString()
  expectTypeOf(s.digest).toBeString()
  expectTypeOf(s.log).toBeString()
  expectTypeOf(s.frontmatter).toBeObject()
})
