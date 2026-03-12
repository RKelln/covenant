<script lang="ts">
  import type { ChatChunk } from '$lib/agents/provider'
  import { renderMarkdown } from '$lib/covenant/render'

  interface Props {
    agentName: string
    chunks: ChatChunk[]
    streaming: boolean
    tintColor?: string
  }

  let { agentName: _agentName, chunks, streaming, tintColor = '#b0a090' }: Props = $props()

  let text = $derived(chunks.map(c => c.content).join(''))
  let html = $derived(renderMarkdown(text))
</script>

<div class="agent-column" data-agent-column data-tint={tintColor} style="--tint: {tintColor}; --column-tint: {tintColor}">
  <div class="agent-response">
    {#if html}
      <!-- eslint-disable-next-line svelte/no-at-html-tags -->
      {@html html}
    {:else if !streaming}
      <p class="empty-state">—</p>
    {/if}
  </div>
</div>

<style>
  .agent-column {
    border-left: 3px solid var(--tint, #b0a090);
    padding: 0 var(--space-md);
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
  }

  .agent-response {
    font-family: var(--font-document, 'Cormorant Garamond', serif);
    font-size: 1.1rem;
    line-height: 1.65;
    color: var(--color-text, #2a2a2a);
  }

  .empty-state {
    color: var(--color-muted, #7a7570);
    font-style: italic;
  }
</style>
