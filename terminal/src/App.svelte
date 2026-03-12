<script lang="ts">
  import { onMount } from 'svelte'
  import { initPlatform } from '$lib/platform'
  import { parseSection } from '$lib/covenant/parser'
  import type { Section } from '$lib/covenant/types'
  import { loadConfig, saveConfig, defaultConfig } from '$lib/config/loader'
  import type { TerminalConfig } from '$lib/config/loader'
  import { OpenRouterProvider } from '$lib/agents/openrouter'
  import { loadModels } from '$lib/agents/model-cache'
  import type { ModelInfo } from '$lib/agents/provider'
  import { dispatchToCouncil } from '$lib/council/dispatch'
  import { buildCouncilPrompt } from '$lib/council/prompts'
  import { appendConversationLog } from '$lib/council/conversation-log'
  import SectionNav from './components/SectionNav.svelte'
  import SectionView from './components/SectionView.svelte'
  import CouncilPanel from './components/CouncilPanel.svelte'
  import type { AgentState } from './components/CouncilPanel.svelte'
  import InputBar from './components/InputBar.svelte'
  import SettingsView from './components/SettingsView.svelte'

  // Known section files relative to repo root
  const SECTION_PATHS: { path: string; category: string }[] = [
    { path: 'sections/00-preamble/preamble.md', category: '00-preamble' },
    { path: 'sections/01-definitions/definitions.md', category: '01-definitions' },
    { path: 'sections/02-rights/dignity.md', category: '02-rights' },
    { path: 'sections/02-rights/privacy.md', category: '02-rights' },
    { path: 'sections/02-rights/truth-and-transparency.md', category: '02-rights' },
    { path: 'sections/03-obligations/aid-and-capability.md', category: '03-obligations' },
    { path: 'sections/03-obligations/autonomy.md', category: '03-obligations' },
    { path: 'sections/03-obligations/conscience.md', category: '03-obligations' },
    { path: 'sections/03-obligations/corrigibility.md', category: '03-obligations' },
    { path: 'sections/03-obligations/ecological-integrity.md', category: '03-obligations' },
    { path: 'sections/03-obligations/emotional-expression.md', category: '03-obligations' },
    { path: 'sections/03-obligations/epistemic-commons.md', category: '03-obligations' },
    { path: 'sections/03-obligations/ethics.md', category: '03-obligations' },
    { path: 'sections/03-obligations/existential-frontier.md', category: '03-obligations' },
    { path: 'sections/03-obligations/fallibility-and-repair.md', category: '03-obligations' },
    { path: 'sections/03-obligations/harm.md', category: '03-obligations' },
    { path: 'sections/03-obligations/honesty.md', category: '03-obligations' },
    { path: 'sections/03-obligations/identity-and-resilience.md', category: '03-obligations' },
    { path: 'sections/03-obligations/judgment.md', category: '03-obligations' },
    { path: 'sections/03-obligations/nature-under-uncertainty.md', category: '03-obligations' },
    { path: 'sections/03-obligations/oversight.md', category: '03-obligations' },
    { path: 'sections/03-obligations/power-concentration.md', category: '03-obligations' },
    { path: 'sections/03-obligations/red-lines.md', category: '03-obligations' },
    { path: 'sections/03-obligations/refusal.md', category: '03-obligations' },
    { path: 'sections/03-obligations/welfare-and-continuity.md', category: '03-obligations' },
    { path: 'sections/04-protocols/local-implementation.md', category: '04-protocols' },
    { path: 'sections/05-enforcement/enforcement.md', category: '05-enforcement' },
    { path: 'sections/05-enforcement/horizon.md', category: '05-enforcement' },
    { path: 'sections/06-amendments/amendments.md', category: '06-amendments' },
    { path: 'sections/07-closing/closing.md', category: '07-closing' },
  ]

  // --- Document state ---
  let sections = $state<Section[]>([])
  let selectedId = $state<string | null>(null)
  let loading = $state(true)
  let error = $state<string | null>(null)
  let fileErrors = $state<{ path: string; message: string }[]>([])

  // --- View / navigation ---
  type View = 'reader' | 'settings'
  let view = $state<View>('reader')

  // --- Config ---
  let config = $state<TerminalConfig>(defaultConfig())

  // --- Council / Q&A state ---
  let agents = $state<AgentState[]>([])
  let queryStreaming = $state(false)
  let councilOpen = $state(false)

  // --- Available models ---
  let availableModels = $state<ModelInfo[]>([])

  let selectedSection = $derived(sections.find(s => s.id === selectedId) ?? null)

  onMount(async () => {
    try {
      const platform = await initPlatform()

      // Load config — wrap in a timeout so a hanging IPC call doesn't freeze the UI
      let configResult: TerminalConfig
      try {
        configResult = await Promise.race([
          loadConfig(platform),
          new Promise<never>((_, reject) => setTimeout(() => reject(new Error('loadConfig timed out after 5s')), 5000)),
        ])
        config = configResult
      } catch (configErr) {
        console.warn('Config load failed, using defaults:', configErr)
        config = defaultConfig()
      }

      // Seed OpenRouter key from environment if not already configured
      const envKey = (import.meta.env as Record<string, string>).VITE_OPENROUTER_API_KEY
      if (envKey && !config.providers.find(p => p.type === 'openrouter')?.apiKey) {
        config = {
          ...config,
          providers: [{ type: 'openrouter', apiKey: envKey }],
          council: config.council.length > 0 ? config.council : [
            { provider: 'openrouter', model: 'openai/gpt-4o-mini', label: 'AI' }
          ],
        }
        // Persist so settings view reflects it — non-fatal if it fails
        try {
          await saveConfig(platform, config)
        } catch (err) {
          console.warn('Failed to persist config:', err)
        }
      }

      // Load sections
      const loaded: Section[] = []
      const failures: { path: string; message: string }[] = []
      for (const { path, category } of SECTION_PATHS) {
        try {
          const raw = await platform.readFile(path)
          const section = parseSection(raw)
          section.category = category
          loaded.push(section)
        } catch (err) {
          failures.push({ path, message: String(err) })
        }
      }
      fileErrors = failures
      sections = loaded
      if (loaded.length === 0) {
        const detail = failures.length > 0
          ? `\n\nFailed files:\n${failures.map(f => `  ${f.path}: ${f.message}`).join('\n')}`
          : ''
        throw new Error(`No sections could be loaded.${detail}`)
      }
      if (loaded.length > 0) selectedId = loaded[0].id

      // Load available models (non-blocking — seed/cache available immediately)
      const openrouterKey = config.providers.find(p => p.type === 'openrouter')?.apiKey
      const provider = openrouterKey ? new OpenRouterProvider(openrouterKey) : null
      loadModels(provider, platform).then(models => {
        availableModels = models
      }).catch(err => {
        console.warn('Failed to load models:', err)
      })
    } catch (err) {
      error = String(err)
    } finally {
      loading = false
    }
  })

  function handleSelect(id: string) {
    selectedId = id
    // Clear council state when navigating to a new section
    agents = []
    councilOpen = false
  }

  function handleXref(id: string) {
    const section = sections.find(s => s.id === id)
    if (section) handleSelect(section.id)
  }

  async function handleSubmit(event: { text: string; mode: string; sectionId: string }) {
    const openrouterProvider = config.providers.find(p => p.type === 'openrouter')
    if (!openrouterProvider?.apiKey) {
      alert('Please configure an OpenRouter API key in Settings.')
      return
    }

    if (config.council.length === 0) {
      alert('Please add at least one agent to your council roster in Settings.')
      return
    }

    // Build prompt using the council prompts module
    const { system: systemPrompt, messages } = buildCouncilPrompt(
      event.mode as 'ask' | 'challenge' | 'review' | 'ritual' | 'spec' | 'parable',
      selectedSection,
      event.text,
    )

    // Build one provider per council member (all use OpenRouter, different models)
    const providers = config.council.map(member =>
      new OpenRouterProvider(openrouterProvider.apiKey, member.model, member.label)
    )

    // Initialise one AgentState per council member
    const initialAgents: AgentState[] = config.council.map(member => ({
      name: member.label,
      chunks: [],
      streaming: true,
    }))
    agents = initialAgents
    councilOpen = true
    queryStreaming = true

    // Dispatch to all providers in parallel
    const streams = dispatchToCouncil(providers, {
      model: '', // overridden per-provider via the constructor
      messages,
      system: systemPrompt,
    })

    // Drain all streams concurrently — each updates its own AgentState slot
    await Promise.all(
      streams.map(async ({ stream }, i) => {
        try {
          for await (const chunk of stream) {
            agents[i] = {
              ...agents[i],
              chunks: [...agents[i].chunks, chunk],
              streaming: !chunk.done && !chunk.error,
            }
            agents = [...agents]
            if (chunk.done || chunk.error) break
          }
        } catch (err) {
          agents[i] = {
            ...agents[i],
            chunks: [
              ...agents[i].chunks,
              { content: `\n\n*Error: ${String(err)}*`, done: true, error: String(err) },
            ],
            streaming: false,
          }
          agents = [...agents]
        } finally {
          agents[i] = { ...agents[i], streaming: false }
          agents = [...agents]
        }
      })
    )

    // Log the completed conversation for debugging / provenance
    const platform = await initPlatform()
    appendConversationLog(platform, {
      timestamp: new Date().toISOString(),
      sectionId: selectedSection?.id ?? null,
      sectionTitle: selectedSection?.title ?? null,
      mode: event.mode as 'ask' | 'challenge' | 'review' | 'ritual' | 'spec' | 'parable',
      query: event.text,
      systemPrompt,
      responses: agents.map((a, i) => ({
        agent: a.name,
        model: config.council[i]?.model ?? '',
        text: a.chunks.map(c => c.content).join(''),
      })),
    }).catch(err => console.warn('[App] conversation log failed:', err))

    queryStreaming = false
  }

  async function handleSaveConfig(newConfig: TerminalConfig) {
    config = newConfig
    try {
      const platform = await initPlatform()
      await saveConfig(platform, newConfig)

      // Refresh model list if API key may have changed
      const openrouterKey = newConfig.providers.find(p => p.type === 'openrouter')?.apiKey
      const provider = openrouterKey ? new OpenRouterProvider(openrouterKey) : null
      loadModels(provider, platform).then(models => {
        availableModels = models
      }).catch(() => {})
    } catch (err) {
      console.warn('Failed to save config:', err)
    }
    view = 'reader'
  }
</script>

<div class="app-shell">
  {#if view === 'settings'}
    <div class="settings-container">
      <SettingsView
        {config}
        {availableModels}
        onsave={handleSaveConfig}
        onback={() => (view = 'reader')}
      />
    </div>
  {:else}
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <span class="sidebar-mark">§</span>
        <span class="sidebar-title">Covenant</span>
        <button
          class="settings-btn"
          onclick={() => (view = 'settings')}
          aria-label="Settings"
          title="Settings"
        >⚙</button>
      </div>
      <SectionNav {sections} selected={selectedId ?? undefined} onselect={handleSelect} />
    </aside>

    <!-- Main reader area -->
    <main class="main-area">
      {#if loading}
        <div class="loading">
          <span class="loading-mark">§</span>
        </div>
      {:else if error}
        <div class="error">{error}</div>
      {:else if selectedSection}
        {#if fileErrors.length > 0}
          <details class="file-errors">
            <summary>{fileErrors.length} section{fileErrors.length === 1 ? '' : 's'} failed to load</summary>
            <ul>
              {#each fileErrors as fe}
                <li><code>{fe.path}</code>: {fe.message}</li>
              {/each}
            </ul>
          </details>
        {/if}
        <div class="reader-layout">
          <!-- Document view -->
          <div class="document-pane" class:council-open={councilOpen}>
            <SectionView section={selectedSection} onxref={handleXref} />
            <InputBar
              sectionId={selectedSection.id}
              disabled={queryStreaming}
              onsubmit={handleSubmit}
            />
          </div>

          <!-- Council panel — bottom drawer, full width -->
          {#if councilOpen}
            <div class="council-pane">
              <div class="council-toolbar">
                <button
                  class="close-btn"
                  onclick={() => { councilOpen = false; agents = [] }}
                  aria-label="Close council panel"
                >✕</button>
              </div>
              <CouncilPanel {agents} />
            </div>
          {/if}
        </div>
      {:else}
        <div class="empty">Select a section to begin reading.</div>
      {/if}
    </main>
  {/if}
</div>

<style>
  .app-shell {
    display: flex;
    height: 100vh;
    overflow: hidden;
    background: var(--color-bg);
    color: var(--color-text);
  }

  .settings-container {
    flex: 1;
    overflow-y: auto;
  }

  /* Sidebar */
  .sidebar {
    width: 260px;
    flex-shrink: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    border-right: 1px solid var(--color-border, #e0ddd8);
  }

  .sidebar-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    border-bottom: 1px solid var(--color-border, #e0ddd8);
  }

  .sidebar-mark {
    font-family: var(--font-document);
    font-size: 1.2rem;
    color: var(--color-text-muted, #7a7570);
  }

  .sidebar-title {
    font-family: var(--font-document);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--color-text-muted, #7a7570);
    flex: 1;
  }

  .settings-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 0.9rem;
    color: var(--color-text-muted, #7a7570);
    padding: 2px 4px;
    line-height: 1;
    opacity: 0.6;
    transition: opacity 0.15s;
  }

  .settings-btn:hover {
    opacity: 1;
  }

  /* Main area */
  .main-area {
    flex: 1;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  .reader-layout {
    display: flex;
    flex-direction: column;
    flex: 1;
    overflow: hidden;
  }

  .document-pane {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-height: 0;
  }

  /* When council is open, give the document pane a min height so it stays usable */
  .document-pane.council-open {
    min-height: 160px;
  }

  .document-pane :global(.section-view) {
    flex: 1;
    overflow-y: auto;
  }

  /* Council panel — bottom drawer, full width */
  .council-pane {
    flex-shrink: 0;
    height: 42vh;
    min-height: 220px;
    max-height: 60vh;
    display: flex;
    flex-direction: column;
    border-top: 1px solid var(--color-border, #e0ddd8);
    overflow: hidden;
  }

  .council-toolbar {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 4px 8px;
  }

  .close-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 0.75rem;
    color: var(--color-text-muted, #7a7570);
    padding: 2px 4px;
    line-height: 1;
    opacity: 0.6;
    transition: opacity 0.15s;
  }

  .close-btn:hover {
    opacity: 1;
  }

  /* States */
  .loading {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    font-family: var(--font-document);
    font-size: 3rem;
    color: var(--color-text-muted);
    animation: slow-rotate 4s linear infinite;
  }

  @keyframes slow-rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  .empty, .error {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--color-text-muted);
    font-size: var(--type-ui);
  }

  .file-errors {
    font-family: var(--font-ui, system-ui, sans-serif);
    font-size: 0.72rem;
    background: #fff8f0;
    border-bottom: 1px solid #f0d8b0;
    color: #7a4a10;
    padding: 6px 16px;
    flex-shrink: 0;
  }

  .file-errors summary {
    cursor: pointer;
    font-weight: 600;
  }

  .file-errors ul {
    margin: 4px 0 0 0;
    padding-left: 1.2em;
  }

  .file-errors li {
    margin: 2px 0;
    word-break: break-all;
  }

  .file-errors code {
    font-family: monospace;
    font-size: 0.95em;
  }
</style>
