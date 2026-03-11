<script lang="ts">
  import type { ChatChunk } from '$lib/agents/provider'
  import { renderMarkdown } from '$lib/covenant/render'

  interface Props {
    agentName: string
    chunks: ChatChunk[]
    streaming: boolean
    tintColor?: string
  }

  let { agentName, chunks, streaming, tintColor = '#b0a090' }: Props = $props()

  let text = $derived(chunks.map(c => c.content).join(''))
  let html = $derived(renderMarkdown(text))
</script>

<div class="agent-column" data-agent-column data-tint={tintColor} style="--tint: {tintColor}; --column-tint: {tintColor}">
  <div class="agent-header">
    <span class="agent-name">{agentName}</span>
    {#if streaming}
      <span class="streaming-indicator" data-streaming aria-label="Streaming">§</span>
    {/if}
  </div>
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

  .agent-header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding-bottom: var(--space-xs);
    border-bottom: 1px solid var(--color-border, #e0ddd8);
  }

  .agent-name {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--color-muted, #7a7570);
  }

  .streaming-indicator {
    font-family: var(--font-document, 'Cormorant Garamond', serif);
    font-size: 1.1rem;
    color: var(--tint, #b0a090);
    animation: pulse 1.2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
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
