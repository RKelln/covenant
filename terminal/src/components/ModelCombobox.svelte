<script lang="ts">
  import { untrack } from 'svelte'
  import type { ModelInfo } from '$lib/agents/provider'

  interface SeedModel extends ModelInfo {
    recommended?: boolean
  }

  interface Props {
    models: SeedModel[]
    value: string
    placeholder?: string
    onselect?: (modelId: string) => void
  }

  let { models, value = '', placeholder = 'Search models…', onselect }: Props = $props()

  let query = $state(untrack(() => value))
  let open = $state(false)
  let focusedIndex = $state(-1)

  // Sync query when parent resets value (e.g. after adding an agent)
  $effect(() => {
    query = value
  })

  const listId = 'model-list-' + Math.random().toString(36).slice(2, 8)

  // Split into recommended and rest, then filter by query
  let filtered = $derived.by(() => {
    const q = query.toLowerCase().trim()
    const match = (m: SeedModel) =>
      !q || m.id.toLowerCase().includes(q) || m.name.toLowerCase().includes(q)
    const rec = models.filter(m => m.recommended && match(m))
    const rest = models.filter(m => !m.recommended && match(m))
    return { recommended: rec, others: rest }
  })

  let allFiltered = $derived([...filtered.recommended, ...filtered.others])

  function select(modelId: string) {
    query = modelId
    open = false
    focusedIndex = -1
    onselect?.(modelId)
  }

  function handleBlur() {
    // Delay to allow click on dropdown item to fire first
    setTimeout(() => {
      if (!open) return
      open = false
      if (query.trim() && query !== value) {
        onselect?.(query.trim())
      }
    }, 150)
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'ArrowDown') {
      e.preventDefault()
      open = true
      focusedIndex = Math.min(focusedIndex + 1, allFiltered.length - 1)
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      focusedIndex = Math.max(focusedIndex - 1, 0)
    } else if (e.key === 'Enter') {
      e.preventDefault()
      if (focusedIndex >= 0 && focusedIndex < allFiltered.length) {
        select(allFiltered[focusedIndex].id)
      } else if (query.trim()) {
        select(query.trim())
      }
    } else if (e.key === 'Escape') {
      open = false
      focusedIndex = -1
    }
  }

  function handleInput() {
    open = true
    focusedIndex = -1
  }
</script>

<div class="combobox">
  <input
    type="text"
    class="combobox-input"
    {placeholder}
    bind:value={query}
    onfocus={() => { open = true }}
    onblur={handleBlur}
    oninput={handleInput}
    onkeydown={handleKeydown}
    role="combobox"
    aria-expanded={open}
    aria-haspopup="listbox"
    aria-controls={listId}
    aria-autocomplete="list"
    autocomplete="off"
  />

  {#if open && (filtered.recommended.length > 0 || filtered.others.length > 0)}
    <ul class="combobox-list" id={listId} role="listbox">
      {#if filtered.recommended.length > 0}
        <li class="group-header" data-recommended-header aria-hidden="true">Recommended</li>
        {#each filtered.recommended as model, i (model.id)}
          <li
            class="combobox-option"
            class:focused={focusedIndex === i}
            role="option"
            aria-selected={focusedIndex === i}
            onmousedown={() => select(model.id)}
          >
            <span class="option-name">{model.name}</span>
            <span class="option-id">{model.id}</span>
          </li>
        {/each}
      {/if}

      {#if filtered.others.length > 0}
        {#if filtered.recommended.length > 0}
          <li class="group-divider" aria-hidden="true"></li>
        {/if}
        {#each filtered.others as model, i (model.id)}
          {@const idx = filtered.recommended.length + i}
          <li
            class="combobox-option"
            class:focused={focusedIndex === idx}
            role="option"
            aria-selected={focusedIndex === idx}
            onmousedown={() => select(model.id)}
          >
            <span class="option-name">{model.name}</span>
            <span class="option-id">{model.id}</span>
          </li>
        {/each}
      {/if}
    </ul>
  {/if}
</div>

<style>
  .combobox {
    position: relative;
    width: 100%;
  }

  .combobox-input {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.9rem;
    padding: 6px 10px;
    border: 1px solid var(--color-border, #e0ddd8);
    background: var(--color-bg, #fdfcfa);
    color: var(--color-text, #2a2a2a);
    border-radius: 3px;
    outline: none;
    width: 100%;
    box-sizing: border-box;
  }

  .combobox-input:focus {
    border-color: var(--color-accent, #8a7a60);
  }

  .combobox-list {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    max-height: 280px;
    overflow-y: auto;
    margin: 2px 0 0 0;
    padding: 0;
    list-style: none;
    background: var(--color-bg, #fdfcfa);
    border: 1px solid var(--color-border, #e0ddd8);
    border-radius: 3px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    z-index: 100;
  }

  .group-header {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--color-muted, #7a7570);
    padding: 6px 10px 2px;
    user-select: none;
  }

  .group-divider {
    height: 1px;
    background: var(--color-border, #e0ddd8);
    margin: 4px 8px;
  }

  .combobox-option {
    display: flex;
    flex-direction: column;
    gap: 1px;
    padding: 5px 10px;
    cursor: pointer;
    transition: background 0.1s;
  }

  .combobox-option:hover,
  .combobox-option.focused {
    background: var(--color-bg-alt, #f5f3f0);
  }

  .option-name {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.85rem;
    color: var(--color-text, #2a2a2a);
  }

  .option-id {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.72rem;
    color: var(--color-muted, #7a7570);
  }
</style>
