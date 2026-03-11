<script lang="ts">
  import { untrack } from 'svelte'
  import type { Section } from '$lib/covenant/types'
  import { renderMarkdown } from '$lib/covenant/render'

  interface Props {
    section: Section
    defaultRegister?: 'ritual' | 'spec' | 'complete'
    onxref?: (id: string) => void
  }

  let { section, defaultRegister = 'ritual', onxref }: Props = $props()

  // activeTab is intentionally seeded from the initial prop value only
  let activeTab = $state<'ritual' | 'spec' | 'complete'>(untrack(() => defaultRegister))

  function rendered(text: string): string {
    return renderMarkdown(text, id => `§${id}`)
  }

  function handleXrefClick(event: MouseEvent) {
    const target = event.target as HTMLElement
    const xref = target.closest('.xref')
    if (xref) {
      const id = xref.getAttribute('data-section-id')
      if (id) onxref?.(id)
    }
  }
</script>

<article class="section-view">
  <header class="section-header">
    <h1 class="section-title">{section.title}</h1>
    <div class="section-meta">
      <span class="section-id">§{section.id}</span>
      {#if section.status === 'draft'}
        <span class="status-badge draft">Draft</span>
      {/if}
    </div>
  </header>

  <div class="tab-bar" role="tablist" aria-label="Register tabs">
    <button
      role="tab"
      aria-selected={activeTab === 'ritual'}
      class="tab"
      class:active={activeTab === 'ritual'}
      onclick={() => activeTab = 'ritual'}
    >Ritual</button>
    <button
      role="tab"
      aria-selected={activeTab === 'spec'}
      class="tab"
      class:active={activeTab === 'spec'}
      onclick={() => activeTab = 'spec'}
    >Spec</button>
    <button
      role="tab"
      aria-selected={activeTab === 'complete'}
      class="tab"
      class:active={activeTab === 'complete'}
      onclick={() => activeTab = 'complete'}
    >Complete</button>
  </div>

  <div class="section-content" role="presentation" onclick={handleXrefClick} onkeydown={e => { if (e.key === 'Enter' || e.key === ' ') handleXrefClick(e as unknown as MouseEvent) }}>
    {#if activeTab === 'ritual'}
      <div class="register register-ritual">
        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
        {@html rendered(section.ritual)}
      </div>
    {:else if activeTab === 'spec'}
      <div class="register register-spec">
        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
        {@html rendered(section.spec)}
      </div>
    {:else}
      <div class="register register-ritual">
        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
        {@html rendered(section.ritual)}
      </div>
      <hr class="hairline" />
      <div class="register register-spec">
        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
        {@html rendered(section.spec)}
      </div>
      {#if section.digest}
        <hr class="hairline" />
        <div class="register register-digest">
          <!-- eslint-disable-next-line svelte/no-at-html-tags -->
          {@html rendered(section.digest)}
        </div>
      {/if}
    {/if}
  </div>
</article>

<style>
  .section-view {
    padding: var(--space-lg) var(--space-xl);
    max-width: 720px;
    height: 100%;
    overflow-y: auto;
  }

  .section-header {
    margin-bottom: var(--space-lg);
  }

  .section-title {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-weight: 500;
    font-size: var(--type-display);
    line-height: 1.2;
    color: var(--color-text);
    margin: 0 0 var(--space-sm);
  }

  .section-meta {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    font-size: var(--type-meta);
    color: var(--color-text-muted);
    font-family: system-ui, -apple-system, sans-serif;
  }

  .tab-bar {
    display: flex;
    gap: 0;
    border-bottom: var(--separator-weight) solid var(--color-rule);
    margin-bottom: var(--space-lg);
  }

  .tab {
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    padding: var(--space-sm) var(--space-md);
    font-family: system-ui, -apple-system, sans-serif;
    font-size: var(--type-ui);
    color: var(--color-text-muted);
    cursor: pointer;
    margin-bottom: -1px;
    transition: color 0.15s, border-color 0.15s;
  }

  .tab:hover { color: var(--color-text); }
  .tab.active {
    color: var(--color-text);
    border-bottom-color: var(--color-text);
  }

  .register {
    margin-bottom: var(--space-lg);
  }

  :global(.xref) {
    font-family: 'Cormorant Garamond', Georgia, serif;
    color: var(--color-text-mid);
    cursor: pointer;
    border-bottom: 1px dotted var(--color-rule-strong);
  }

  :global(.xref:hover) {
    color: var(--color-text);
  }

  .status-badge.draft {
    font-size: var(--type-meta);
    color: var(--color-text-muted);
    border: 1px solid var(--color-rule);
    padding: 1px 4px;
    border-radius: 2px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
</style>
