<script lang="ts">
  import type { Section } from '$lib/covenant/types'

  interface Props {
    sections: Section[]
    selected?: string
    onselect?: (id: string) => void
  }

  let { sections, selected, onselect }: Props = $props()

  let searchQuery = $state('')

  // Category display names derived from the NN-name prefix
  function categoryLabel(cat: string): string {
    const name = cat.replace(/^\d+-/, '')
    return name.charAt(0).toUpperCase() + name.slice(1).replace(/-/g, ' ')
  }

  // Group sections by category
  let grouped = $derived(() => {
    const filtered = sections.filter(s =>
      s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.id.toLowerCase().includes(searchQuery.toLowerCase())
    )
    const map: Record<string, Section[]> = {}
    for (const s of filtered) {
      if (!map[s.category]) map[s.category] = []
      map[s.category].push(s)
    }
    return map
  })

  function handleSelect(id: string) {
    onselect?.(id)
  }
</script>

<nav class="section-nav" aria-label="Section navigation">
  <div class="search-wrapper">
    <input
      type="search"
      placeholder="Search sections…"
      bind:value={searchQuery}
      aria-label="Search sections"
      class="search-input"
    />
  </div>

  <div class="nav-categories">
    {#each Object.entries(grouped()) as [category, categorySections]}
      <div class="nav-category">
        <div class="separator-section">
          <span class="section-mark">§</span>
          <span class="category-label">{categoryLabel(category)}</span>
        </div>
        <ul class="section-list" role="list">
          {#each categorySections as section}
            <li>
              <button
                class="section-item"
                class:selected={selected === section.id}
                onclick={() => handleSelect(section.id)}
                aria-current={selected === section.id ? 'page' : undefined}
              >
                <span class="section-title">{section.title}</span>
                {#if section.status}
                  <span
                    class="status-badge"
                    class:draft={section.status === 'draft'}
                    class:active={section.status === 'active'}
                    title={section.status}
                    aria-label={section.status}
                  >{section.status.charAt(0)}</span>
                {/if}
              </button>
            </li>
          {/each}
        </ul>
      </div>
    {/each}
  </div>
</nav>

<style>
  .section-nav {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
    border-right: var(--separator-weight) solid var(--color-rule);
  }

  .search-wrapper {
    padding: var(--space-md);
    border-bottom: var(--separator-weight) solid var(--color-rule);
  }

  .search-input {
    width: 100%;
    padding: var(--space-xs) var(--space-sm);
    font-size: var(--type-ui);
    font-family: var(--font-ui);
    background: transparent;
    border: var(--separator-weight) solid var(--color-rule-strong);
    color: var(--color-text);
    outline: none;
  }

  .search-input:focus {
    border-color: var(--color-text-mid);
  }

  .nav-categories {
    flex: 1;
    overflow-y: auto;
    padding: var(--space-sm) 0;
  }

  .separator-section {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-md);
    font-size: var(--type-meta);
    color: var(--color-text-muted);
    font-family: var(--font-document);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .section-mark {
    font-family: var(--font-document);
    font-size: var(--type-ui);
    opacity: 0.6;
  }

  .section-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .section-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: var(--space-xs) var(--space-md);
    background: none;
    border: none;
    cursor: pointer;
    text-align: left;
    font-family: var(--font-document);
    font-size: var(--type-body);
    color: var(--color-text-mid);
    transition: color 0.15s ease;
  }

  .section-item:hover {
    color: var(--color-text);
  }

  .section-item.selected {
    color: var(--color-text);
    font-style: italic;
  }

  .status-badge {
    font-family: var(--font-ui);
    font-size: var(--type-meta);
    padding: 1px 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text-muted);
    border: 1px dotted var(--color-rule-strong);
    cursor: default;
    flex-shrink: 0;
  }

  .status-badge.draft {
    color: var(--color-text-muted);
  }

  .status-badge.active {
    color: var(--color-text-mid);
    border-color: var(--color-text-mid);
  }
</style>
