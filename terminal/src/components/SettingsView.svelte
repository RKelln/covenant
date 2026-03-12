<script lang="ts">
  import { untrack } from 'svelte'
  import type { TerminalConfig, ProviderConfig, CouncilMemberConfig } from '$lib/config/loader'
  import type { ModelInfo } from '$lib/agents/provider'
  import ModelCombobox from './ModelCombobox.svelte'

  interface Props {
    config: TerminalConfig
    availableModels?: ModelInfo[]
    onsave?: (config: TerminalConfig) => void
    onback?: () => void
  }

  let { config, availableModels = [], onsave, onback }: Props = $props()

  // Intentional: local state is seeded from initial prop values — not reactively bound
  let apiKey = $state(untrack(() => config.providers.find(p => p.type === 'openrouter')?.apiKey ?? ''))
  let selectedModel = $state(untrack(() => config.defaultModel ?? ''))
  let councilMembers = $state<CouncilMemberConfig[]>(untrack(() => [...config.council]))

  // Add-agent form state
  let newAgentLabel = $state('')
  let newAgentModel = $state('')
  let newAgentProvider = $state<string>('openrouter')

  function handleSave() {
    const providers: ProviderConfig[] = apiKey
      ? [{ type: 'openrouter', apiKey }]
      : config.providers.filter(p => p.type !== 'openrouter')

    const newConfig: TerminalConfig = {
      ...config,
      defaultModel: selectedModel || undefined,
      providers,
      council: councilMembers,
    }
    onsave?.(newConfig)
  }

  function removeAgent(index: number) {
    councilMembers = councilMembers.filter((_, i) => i !== index)
  }

  function addAgent() {
    if (!newAgentModel.trim()) return
    const label = newAgentLabel.trim() || newAgentModel.trim()
    councilMembers = [
      ...councilMembers,
      { provider: newAgentProvider, model: newAgentModel.trim(), label },
    ]
    newAgentLabel = ''
    newAgentModel = ''
  }
</script>

<div class="settings-view">
  <div class="settings-header">
    <h2 class="settings-title">Settings</h2>
    {#if onback}
      <button class="back-btn" onclick={onback}>← Back</button>
    {/if}
  </div>

  <div class="settings-body">
    <section class="settings-section">
      <h3 class="section-heading">Providers</h3>

      <div class="field">
        <label class="field-label" for="openrouter-key">OpenRouter API Key</label>
        <input
          id="openrouter-key"
          type="password"
          class="field-input"
          bind:value={apiKey}
          placeholder="sk-or-…"
          autocomplete="off"
        />
      </div>
    </section>

    {#if availableModels.length > 0}
      <section class="settings-section">
        <h3 class="section-heading">Default Model</h3>
        <p class="section-desc">Used for all tasks outside the council: applying edits, answering questions, running commands.</p>
        <div class="field">
          <ModelCombobox
            models={availableModels}
            value={selectedModel}
            placeholder="Search models…"
            onselect={(id) => { selectedModel = id }}
          />
        </div>
      </section>
    {/if}

    <section class="settings-section">
      <h3 class="section-heading">Council Roster</h3>

      {#if councilMembers.length > 0}
        <div class="roster-list">
          {#each councilMembers as member, i (i)}
            <div class="roster-item">
              <span class="roster-label" data-council-label>{member.label}</span>
              <span class="roster-model">{member.model}</span>
              <button
                class="remove-btn"
                data-remove-agent
                onclick={() => removeAgent(i)}
                aria-label="Remove {member.label}"
              >×</button>
            </div>
          {/each}
        </div>
      {:else}
        <p class="roster-empty">No council members configured.</p>
      {/if}

      <div class="add-agent-form">
        <h4 class="add-heading">Add agent</h4>
        <div class="add-row">
          <input
            class="field-input add-input"
            type="text"
            placeholder="Label (e.g. Claude)"
            data-add-label
            bind:value={newAgentLabel}
          />
          <div class="add-input">
            <ModelCombobox
              models={availableModels}
              value={newAgentModel}
              placeholder="Model ID (e.g. anthropic/claude-3-haiku)"
              onselect={(id) => { newAgentModel = id }}
            />
          </div>
          <select class="field-select add-provider" bind:value={newAgentProvider}>
            <option value="openrouter">OpenRouter</option>
            <option value="copilot">Copilot</option>
          </select>
          <button
            class="add-btn"
            data-add-agent-btn
            onclick={addAgent}
            disabled={!newAgentModel.trim()}
          >Add</button>
        </div>
      </div>
    </section>
  </div>

  <div class="settings-footer">
    <button class="save-btn" onclick={handleSave}>Save</button>
  </div>
</div>

<style>
  .settings-view {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: var(--space-lg, 24px);
    background: var(--color-bg, #fdfcfa);
    color: var(--color-text, #2a2a2a);
  }

  .settings-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-lg, 24px);
  }

  .settings-title {
    font-family: var(--font-document, 'Cormorant Garamond', serif);
    font-size: 1.6rem;
    font-weight: 600;
    margin: 0;
  }

  .back-btn {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.85rem;
    background: none;
    border: none;
    color: var(--color-accent, #8a7a60);
    cursor: pointer;
  }

  .settings-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: var(--space-lg, 24px);
    overflow-y: auto;
  }

  .settings-section {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm, 8px);
  }

  .section-heading {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--color-muted, #7a7570);
    margin: 0 0 var(--space-xs, 4px) 0;
  }

  .section-desc {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.8rem;
    color: var(--color-muted, #7a7570);
    margin: 0 0 var(--space-xs, 4px) 0;
    line-height: 1.4;
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .field-label {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.85rem;
    color: var(--color-text, #2a2a2a);
  }

  .field-input,
  .field-select {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.9rem;
    padding: 6px 10px;
    border: 1px solid var(--color-border, #e0ddd8);
    background: var(--color-bg, #fdfcfa);
    color: var(--color-text, #2a2a2a);
    border-radius: 3px;
    outline: none;
    max-width: 360px;
  }

  .field-input:focus,
  .field-select:focus {
    border-color: var(--color-accent, #8a7a60);
  }

  /* Roster */
  .roster-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .roster-item {
    display: flex;
    align-items: center;
    gap: var(--space-sm, 8px);
    padding: 6px 10px;
    background: var(--color-bg-alt, #f5f3f0);
    border-radius: 3px;
    border: 1px solid var(--color-border, #e0ddd8);
  }

  .roster-label {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--color-text, #2a2a2a);
    min-width: 80px;
  }

  .roster-model {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.8rem;
    color: var(--color-muted, #7a7570);
    flex: 1;
  }

  .remove-btn {
    font-size: 1rem;
    background: none;
    border: none;
    color: var(--color-muted, #7a7570);
    cursor: pointer;
    padding: 0 4px;
    line-height: 1;
  }

  .remove-btn:hover {
    color: var(--color-text, #2a2a2a);
  }

  .roster-empty {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.85rem;
    color: var(--color-muted, #7a7570);
    font-style: italic;
    margin: 0;
  }

  .add-agent-form {
    margin-top: var(--space-sm, 8px);
    padding-top: var(--space-sm, 8px);
    border-top: 1px solid var(--color-border, #e0ddd8);
  }

  .add-heading {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.75rem;
    color: var(--color-muted, #7a7570);
    margin: 0 0 6px 0;
    font-weight: 400;
  }

  .add-row {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    align-items: center;
  }

  .add-input {
    max-width: none;
    flex: 1;
    min-width: 120px;
  }

  .add-provider {
    max-width: none;
    flex: 0 0 auto;
  }

  .add-btn {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.85rem;
    padding: 6px 14px;
    border: 1px solid var(--color-accent, #8a7a60);
    background: transparent;
    color: var(--color-accent, #8a7a60);
    border-radius: 3px;
    cursor: pointer;
  }

  .add-btn:hover:not(:disabled) {
    background: var(--color-accent, #8a7a60);
    color: var(--color-bg, #fdfcfa);
  }

  .add-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  /* Footer */
  .settings-footer {
    padding-top: var(--space-md, 16px);
    border-top: 1px solid var(--color-border, #e0ddd8);
  }

  .save-btn {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.85rem;
    padding: 8px 20px;
    border: 1px solid var(--color-accent, #8a7a60);
    background: var(--color-accent, #8a7a60);
    color: var(--color-bg, #fdfcfa);
    border-radius: 3px;
    cursor: pointer;
    transition: opacity 0.15s;
  }

  .save-btn:hover {
    opacity: 0.85;
  }
</style>
