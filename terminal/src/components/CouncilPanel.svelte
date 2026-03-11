<script lang="ts">
  import type { ChatChunk } from '$lib/agents/provider'
  import AgentColumn from './AgentColumn.svelte'

  export interface AgentState {
    name: string
    chunks: ChatChunk[]
    streaming: boolean
    tint?: string
  }

  export interface SynthesisState {
    chunks: ChatChunk[]
    streaming: boolean
  }

  interface Props {
    agents: AgentState[]
    synthesis?: SynthesisState
  }

  // Default tint palette — warm and cool alternating
  const TINT_PALETTE = [
    '#c8b89a',  // warm tan (Claude)
    '#8ab4c8',  // cool blue (GPT)
    '#98c8a0',  // sage (Gemini)
    '#c8a0b8',  // muted rose (fourth)
    '#a8a8c8',  // slate (fifth)
  ]

  let { agents, synthesis }: Props = $props()

  let agentsWithTints = $derived(agents.map((agent, i) => ({
    ...agent,
    resolvedTint: agent.tint ?? TINT_PALETTE[i % TINT_PALETTE.length],
  })))

  let synthesisText = $derived(synthesis?.chunks.map(c => c.content).join('') ?? '')
</script>

<div class="council-panel">
  {#if agents.length === 0}
    <div class="empty-state">
      <span class="empty-prompt">Ask a question about this section</span>
    </div>
  {:else}
    <div class="agent-columns">
      {#each agentsWithTints as agent (agent.name)}
        <AgentColumn
          agentName={agent.name}
          chunks={agent.chunks}
          streaming={agent.streaming}
          tintColor={agent.resolvedTint}
        />
      {/each}
    </div>

    {#if synthesis}
      <div class="synthesis-section">
        <div class="synthesis-heading">Synthesis</div>
        <div class="synthesis-body">
          {#if synthesisText}
            <!-- eslint-disable-next-line svelte/no-at-html-tags -->
            {@html synthesisText}
          {:else if synthesis.streaming}
            <span class="synthesis-pending">§</span>
          {/if}
        </div>
      </div>
    {/if}
  {/if}
</div>

<style>
  .council-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow-y: auto;
    padding: var(--space-md);
    gap: var(--space-lg);
  }

  .empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    min-height: 6rem;
  }

  .empty-prompt {
    font-family: var(--font-document, 'Cormorant Garamond', serif);
    font-style: italic;
    color: var(--color-muted, #7a7570);
    font-size: 1.1rem;
  }

  .agent-columns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--space-lg);
  }

  .synthesis-section {
    border-top: 1px solid var(--color-border, #e0ddd8);
    padding-top: var(--space-md);
  }

  .synthesis-heading {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--color-muted, #7a7570);
    margin-bottom: var(--space-sm);
  }

  .synthesis-body {
    font-family: var(--font-document, 'Cormorant Garamond', serif);
    font-size: 1.1rem;
    line-height: 1.65;
    color: var(--color-text, #2a2a2a);
  }

  .synthesis-pending {
    font-family: var(--font-document, 'Cormorant Garamond', serif);
    color: var(--color-muted, #7a7570);
    animation: pulse 1.2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }
</style>
