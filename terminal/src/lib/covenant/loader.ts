import type { Platform } from '../platform'
import type { Section } from './types'
import { parseSection } from './parser'

/**
 * Load and parse all sections from the platform.
 */
export async function loadAllSections(platform: Platform): Promise<Section[]> {
  const metas = await platform.listSections()
  const sections: Section[] = []
  for (const meta of metas) {
    try {
      const raw = await platform.readFile(meta.path)
      const section = parseSection(raw)
      section.rawPath = meta.path
      section.category = meta.category
      sections.push(section)
    } catch (err) {
      console.warn(`[loader] Failed to parse ${meta.path}:`, err)
    }
  }
  return sections
}

/**
 * Load a single section by ID.
 */
export async function loadSection(platform: Platform, id: string): Promise<Section | null> {
  const metas = await platform.listSections()
  const meta = metas.find(m => m.id === id)
  if (!meta) return null
  const raw = await platform.readFile(meta.path)
  return parseSection(raw)
}

/**
 * Load all sections grouped by category.
 */
export async function loadSectionsByCategory(
  platform: Platform
): Promise<Record<string, Section[]>> {
  const sections = await loadAllSections(platform)
  const grouped: Record<string, Section[]> = {}
  for (const section of sections) {
    const cat = section.category
    if (!grouped[cat]) grouped[cat] = []
    grouped[cat].push(section)
  }
  return grouped
}
