export type SectionStatus = 'draft' | 'stable' | 'proposed'
export type Register = 'ritual' | 'spec' | 'digest' | 'log' | 'complete'

export interface SectionFrontmatter {
  id: string
  title: string
  status: SectionStatus
  since: string
  depends_on: string[]
  terms_introduced: string[]
  [key: string]: unknown
}

export interface Section {
  id: string
  title: string
  status: SectionStatus
  since: string
  category: string
  frontmatter: SectionFrontmatter
  ritual: string
  spec: string
  digest: string
  log: string
  rawPath?: string
}

export interface SectionCategory {
  id: string
  label: string
  sections: Section[]
}
