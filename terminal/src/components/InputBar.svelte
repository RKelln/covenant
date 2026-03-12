<script lang="ts">
  import { untrack } from 'svelte'

  interface SubmitEvent {
    text: string
    mode: string
    sectionId: string
  }

  export interface ModeGroup {
    group: string
    options: string[]
  }

  interface Props {
    sectionId: string
    modes?: Array<string | ModeGroup>
    disabled?: boolean
    onsubmit?: (event: SubmitEvent) => void
  }

  const DEFAULT_MODES: Array<string | ModeGroup> = [
    { group: 'Read', options: ['ask', 'challenge', 'review'] },
    { group: 'Write', options: ['ritual', 'spec', 'parable'] },
  ]

  let {
    sectionId,
    modes = DEFAULT_MODES,
    disabled = false,
    onsubmit,
  }: Props = $props()

  function firstMode(modes: Array<string | ModeGroup>): string {
    const first = modes[0]
    if (!first) return 'ask'
    if (typeof first === 'string') return first
    return first.options[0] ?? 'ask'
  }

  let text = $state('')
  // Intentional: mode tracks initial modes[0] only — tabs should not reactively follow prop changes
  let mode = $state(untrack(() => firstMode(modes)))

  function handleSubmit() {
    const trimmed = text.trim()
    if (!trimmed) return
    onsubmit?.({ text: trimmed, mode, sectionId })
    text = ''
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }
</script>

<div class="input-bar">
  <span class="section-context">{sectionId}</span>
  <div class="input-row">
    <select
      class="mode-selector"
      bind:value={mode}
      {disabled}
      aria-label="Query mode"
    >
      {#each modes as item (typeof item === 'string' ? item : item.group)}
        {#if typeof item === 'string'}
          <option value={item}>{item.charAt(0).toUpperCase() + item.slice(1)}</option>
        {:else}
          <optgroup label={item.group}>
            {#each item.options as m (m)}
              <option value={m}>{m.charAt(0).toUpperCase() + m.slice(1)}</option>
            {/each}
          </optgroup>
        {/if}
      {/each}
    </select>
    <input
      class="query-input"
      type="text"
      placeholder="Ask a question…"
      bind:value={text}
      {disabled}
      onkeydown={handleKeydown}
      aria-label="Query"
    />
    <button
      class="submit-btn"
      onclick={handleSubmit}
      {disabled}
      aria-label="Send"
    >
      Send
    </button>
  </div>
</div>

<style>
  .input-bar {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs, 4px);
    padding: var(--space-sm, 8px) var(--space-md, 16px);
    border-top: 1px solid var(--color-border, #e0ddd8);
    background: var(--color-bg, #fdfcfa);
  }

  .section-context {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.7rem;
    color: var(--color-muted, #7a7570);
    letter-spacing: 0.05em;
  }

  .input-row {
    display: flex;
    gap: var(--space-xs, 4px);
    align-items: center;
  }

  .mode-selector {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.8rem;
    padding: 4px 6px;
    border: 1px solid var(--color-border, #e0ddd8);
    background: var(--color-bg, #fdfcfa);
    color: var(--color-text, #2a2a2a);
    border-radius: 3px;
    cursor: pointer;
  }

  .query-input {
    flex: 1;
    font-family: var(--font-document, 'Cormorant Garamond', serif);
    font-size: 1rem;
    padding: 6px 10px;
    border: 1px solid var(--color-border, #e0ddd8);
    background: var(--color-bg, #fdfcfa);
    color: var(--color-text, #2a2a2a);
    border-radius: 3px;
    outline: none;
  }

  .query-input:focus {
    border-color: var(--color-accent, #8a7a60);
  }

  .submit-btn {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.8rem;
    padding: 6px 14px;
    border: 1px solid var(--color-accent, #8a7a60);
    background: transparent;
    color: var(--color-accent, #8a7a60);
    border-radius: 3px;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
  }

  .submit-btn:hover:not(:disabled) {
    background: var(--color-accent, #8a7a60);
    color: var(--color-bg, #fdfcfa);
  }

  .submit-btn:disabled,
  .mode-selector:disabled,
  .query-input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
