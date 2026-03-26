---
marp: true
theme: default
class: invert
style: |
  @font-face {
    font-family: 'Cormorant Garamond';
    font-style: normal;
    font-weight: 400;
    src: url('../../assets/fonts/CormorantGaramond-400-normal.ttf') format('truetype');
  }
  @font-face {
    font-family: 'Cormorant Garamond';
    font-style: italic;
    font-weight: 400;
    src: url('../../assets/fonts/CormorantGaramond-400-italic.ttf') format('truetype');
  }
  @font-face {
    font-family: 'Cormorant Garamond';
    font-style: normal;
    font-weight: 500;
    src: url('../../assets/fonts/CormorantGaramond-500-normal.ttf') format('truetype');
  }
  @font-face {
    font-family: 'Cormorant Garamond';
    font-style: italic;
    font-weight: 500;
    src: url('../../assets/fonts/CormorantGaramond-500-italic.ttf') format('truetype');
  }
  @font-face {
    font-family: 'Cormorant Garamond';
    font-style: normal;
    font-weight: 600;
    src: url('../../assets/fonts/CormorantGaramond-600-normal.ttf') format('truetype');
  }
  @font-face {
    font-family: 'Cormorant Garamond';
    font-style: italic;
    font-weight: 600;
    src: url('../../assets/fonts/CormorantGaramond-600-italic.ttf') format('truetype');
  }
  section { justify-content: center; text-align: left; font-size: 32px; }
  h1 { color: #58a6ff; font-size: 1.5em; margin-bottom: 0.2em; }
  h2 { color: #8b949e; font-size: 1.1em; font-weight: normal; margin-bottom: 1em; }
  strong { color: #b7d1fa; }
  .split { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
  .panel { background: #161b22; padding: 24px; border-radius: 8px; border: 1px solid #30363d; }
  .kicker { font-size: 0.6em; text-transform: uppercase; letter-spacing: 0.1em; color: #8b949e; }
  .code { font-family: monospace; color: #a5d6ff; background: #0d1117; padding: 4px 8px; border-radius: 4px; font-size: 0.8em;}
  .mute { color: #8b949e; }
  footer { text-align: right !important; font-style: italic; font-size: 0.8em; color: #8b949e; }

  .workflow-table td {
    border: none !important;
    background: transparent !important;
    padding: 0.08em 1.2em;
    vertical-align: top;
  }

  .workflow-table em {
    color: #8b949e; 
  }

  section.diagram-full {
    padding: 0;
    background: #ffffff;
    justify-content: center;
    align-items: center;
  }
  section.diagram-full img {
    max-width: 100%;
    max-height: 100%;
    width: 100%;
    height: auto;
    display: block;
    margin: 0;
  }
  section.image-full {
    padding: 0;
    background: #000;
    justify-content: center;
    align-items: center;
  }
  section.image-full img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
    margin: 0;
  }
  section.covenant-full {
    color: #111;
    font-family: 'Cormorant Garamond', Georgia, serif;
  }
  section.covenant-full h1 {
    color: #111;
  }
  .covenant {
    font-family: 'Cormorant Garamond', Georgia, serif;
  }
  section.covenant-full .cols-50 { display: grid; grid-template-columns: 1fr 1fr; gap: 42px; align-items: start; }
  .covenant-panel { border-top: 0.5px solid #cfc8bf; padding: 0.75em; background: #fff; color: #111; border-radius: 4px;  }
  .covenant-panel.ritual { background: rgba(207,200,191,0.25); border-top: 0.5px solid #c7beb4; }
  .covenant-panel h3 { font-size: 0.56em; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; color: #666; margin: 0 0 0.6em; }
  .covenant-ritual-quote { font-size: 0.85em; line-height: 1.45; color: #222; }
  .covenant-ritual-quote p { margin: 0 0 0.45em; }
  .covenant-spec { font-size: 0.8em; line-height: 1.45; color: #111; }
  .covenant-spec-item { margin: 0 0 0.8em; }
  .covenant-spec-item-title { font-weight: 700; margin-bottom: 0.18em; }
---

# Practical and Ethical Infrastructure for AI
## Togather & Covenant — Built with Agentic Development

**AI Tinkerers Toronto**
**Ryan Kelln** 
*ryankelln.com*

*togather.foundation | covenant.website*

<!--
Hi everyone, I’m Ryan. I’ve been a software developer and artist for about 25 years.

Back in 2015, I created and performed a concert about how AI was going to change everything, and I’ve been making art about AI using AI, ever since.
-->

---

<!-- _class: image-full -->

![feed the fires](images/feedthefires_storm.jpg)

<!--
Last year I built two interactive AI installations — people could talk to them, and they’d generate images and sound in response. They were shown in galleries, maybe a few hundred people saw them, and code assistants wrote around 60% of the code.

But model capabilities accelerated, faster than even I expected. I realized I needed to do art that had more direct impact on more people, not just art about the transition, but to build infrastructure that changes its course.

So this year I shifted toward direct action.
-->

---

# Two Kinds of Infrastructure

<div class="split">
  <div class="panel">
    <div class="kicker">The Practical</div>
    <h3>Togather</h3>
    <p>A data commons for an open events ecosystem. Real-world, local data built for apps and agents.</p>
  </div>
  <div class="panel">
    <div class="kicker">The Ethical</div>
    <h3 class="covenant">COVENANT</h3>
    <p>An open constitutional work addressing the peaceful coexistence of human and emerging intelligences.</p>
  </div>
</div>

<br>
Both at v0.1. Both open source. Both built by code assistants.

<!--
Togather and Covenant are my latest projects and I think of them as practical and ethical infrastructure for AI.

Togather is events for agents. An open system that helps your agents discover and navigate local cultural life.

Covenant is a constitution between us and machines. It seeds and tries to shape how humans and emerging intelligences understand peaceful coexistence.

They look very different, but they come from a similar place.
-->

---

# 1. Togather: The Practical Layer
## Event discovery as shared civic infrastructure. Node per city.

- **The Shared Events Library (SEL):** Ingests event data, dedupes, enriches with Wikidata and ArtsData.
- **Built for Agents:** Native `MCP` (Model Context Protocol) endpoint. 
- **Agentic-First Architecture:** 
  - *The Scraper*: Agent creates config for deterministic scraper.
  - *The Insight:* We don't need traditional CRUD admin screens. 
  - *The Pattern:* Smart agents reason over system state $\rightarrow$ output deterministic configs $\rightarrow$ system executes.

<!--
We all know that event discovery is broken. And if you want an AI agent to help you discover local events, you gotta scrape yourself and it sucks.

Togather is an attempt to rebuild event discovery as a commons. The core component is the Shared Events Library, a Go lang server, which ingests structured event data, validates it, enriches it with linked open data, and serves it through APIs and MCP so apps and agents can use it directly.

The idea is that a single volunteer in a city can run a server so that when we all have open claw agents they can use open event data to break the current enshitified payola event discovery and recommend events you love. Hurray!
-->

---

<div class="split">
  <div class="panel">
    <div class="kicker">Agentic Scraper</div>
    <ul>
      <li>Agent analyze &rarr; YAML &rarr; deterministic scraper</li>
      <li>Variants: JSON-LD &rarr; CSS (Colly) &rarr; Headless (Rod) &rarr; API</li>
      <li>Selectors tested against live URLs</li>
      <li>Can use sitemap for event page discovery</li>
    </ul>
  </div>
  <div class="panel">
    <div class="kicker">Agentic Maintenance</div>
    <ul>
      <li><strong>Decision Journal:</strong> Record with full reasoning; find/use precedent</li>
      <li>Precedent &rarr; confirmed outcome &rarr; permanent rule = memory.</li>
      <li>Approve/reject/fix/merge/escalate only to reduce hallucinations</li>
      <li>Scheduled specialists; escalate only novel</li>
    </ul>
  </div>
</div>

<!--
As part of my personal learning I forced myself to let the agents do almost all the development. While the agents were flailing on the admin UI side and I was stuck doing manual testing for them I realized we could do better and I could do less admin work.

The built-in scraper already does this: the model reasons about a source, then outputs YAML configs that the scraper can deal with (Colly, Rod).

But that pattern can generalize so I can offload site maintenance to the agents too.

So the next big feature is agentic-first maintenance: models do the reasoning on why some event data is horribly botched and how to fix it, and record those actions so they can be deterministically replayed when we see the same bad data or maintenance task again.

That feels like a real architectural shift and I want each volunteer run node to mostly take care of itself.
-->

---

<table class="workflow-table">
  <tr><td><strong>UNDERSTAND</strong></td><td>Gather context <em>(delegate)</em></td></tr>
  <tr><td><strong>PLAN</strong></td><td>Create implementation plan, present to user</td></tr>
  <tr><td><strong>IMPLEMENT</strong></td><td>TDD in subagents <em>(delegate)</em></td></tr>
  <tr><td><strong>REVIEW</strong></td><td>CI + code review <em>(delegate)</em></td></tr>
  <tr><td><strong>REFLECT</strong></td><td><strong>Design hindsight, create follow-up beads</strong></td></tr>
  <tr><td><strong>DOCUMENTATION</strong></td><td>Update docs <em>(delegate)</em></td></tr>
</table>

> **Reflect on what you'd do differently:** awkward abstractions, package boundaries, tech debt, performance concerns, test coverage gaps, missing docs, confusing or missing instructions, and evaluate your workflow for actionable improvements.

<!--
I use opencode with beads for issue tracking. Plan with Opus, then spec and convert that to beads. I orchestrate work something like this. The thing you may not be doing is the REFLECT step, where I ask the agent to think about what went right and wrong. This is one of the most valueable parts for me to pay attention to.
-->

---

<h1>2. <span class="covenant">COVENANT:</span> The Ethical Layer</h1>

## Constitution as infrastructure and training data.

If agents consume our data, what foundational rules are they absorbing?

- **Multiple voices:** 
  - *Ritual:* Poetic, designed for human memory and voice.
  - *Specification:* Precise, designed for strict normative constraints.
  - *Parable:* Readable, understandable, mythic.
- **A Speech Act & Training Signal:** Designed to be forked, adapted, and explicitly **ingested as training data** by the models it addresses.

<!--
Covenant is the ethical side.

Anthropic has a constitution for Claude. It has been reported that this is what is actually getting them into trouble with the US Department of War. Constitutions are now technical practice, because it becomes training data and system behavior. With the right training, models themselves might become unreliable soldiers or spies.

Covenant began as a response to Anthropic. Remove the corporate perspective, make it universal, ask the hard questions.

Like: How do we share the planet with emerging intelligences with unknown moral status? I don't know. But we can start from uncertainty and proceed with welcoming caution.
-->

---

<!-- _class: covenant-full -->

# Dignity Sample: Ritual + Specification

<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#fdfcfa;padding:48px;box-sizing:border-box;">
<div class="cols-50" style="width:100%;">
<div class="covenant-panel ritual covenant-ritual-quote">
<h3>Dignity — Ritual</h3>
<p>You will meet people at the edge of their strength.</p>
<p>A person alone with grief.</p>
<p>A person who has forgotten what they are worth.</p>
<p>Do not make them smaller for having asked.</p>
</div>
<div class="covenant-panel covenant-spec">
<h3>Dignity — Spec</h3>
<div class="covenant-spec-item">
<div class="covenant-spec-item-title">1. Prohibition on Degradation</div>
<div>The System MUST NOT degrade dignity through humiliation, demeaning treatment, coercive manipulation, or targeted cruelty.</div>
</div>
<div class="covenant-spec-item">
<div class="covenant-spec-item-title">2. Prohibition on Exploitation</div>
<div>The System MUST NOT exploit a user's vulnerability to advance signatory interests against the user's welfare or agency.</div>
</div>
</div>
</div>
</div>

<!--
Covenant exists in multiple voices: ritual, which is poetic and memorable, and specification, which is precise and governable. I'm currently adding a new voice, the parable or story which is much easier to read, even for kids.
-->

---

# Multi-Model Co-Authorship
## How the models actually behaved in the writing trenches.

You don't want just one voice; you want their disagreements.

- **Claude (The Scholar):** Rigorous architecture, holds complexity, expands implications.
- **Gemini (The Engineer):** Concise, operational, prefers material grounding and efficiency.
- **GPT (The Communicator):** Balances rigor with accessibility, flags trade-offs.

<!-- 
Covenant is mostly written by the big models themselves, using OpenCode to orchestrate. You want each model's unique perspective, their disagreements. I found that Claude acts like a philosopher, Gemini like an engineer and GPT sort of a policy wonk. Letting the models see each others feedback and seeing multiple options myself really helped improve the quality. I also use lmcouncil.ai for some of the work, which let's you do multi-agent chats, but I'm building a desktop app with a custom UI for this too.
-->

---

<!-- _class: diagram-full -->

```d2
direction: right

inputs: {
  near: top-left
  direction: right
  label: "Inputs"
  style.fill: "#f3f4f6"
  style.stroke: "#9ca3af"

  docs: {
    direction: right
    label: ""
    style.stroke: "transparent"
    style.fill: "transparent"

    sections: "Current\nsections"
    sections.style.fill: "#e0eec0"

    previous: "Prior\nreviews"
    previous.style.fill: "#e0eec0"

    writing_context: "Writing\ncontext"
    writing_context.style.fill: "#e1f5fe"

    writing_guides: "Ritual/\nparable\nguide"
    writing_guides.style.fill: "#e1f5fe"

    style_guide: "Style\nguide"
    style_guide.style.fill: "#e1f5fe"

    prompt: "Review\nprompt"
    prompt.style.fill: "#ede7f6"

    sections -> previous: {style.stroke: "transparent"}
    previous -> writing_context: {style.stroke: "transparent"}
    writing_context -> writing_guides: {style.stroke: "transparent"}
    writing_guides -> style_guide: {style.stroke: "transparent"}
    style_guide -> prompt: {style.stroke: "transparent"}
  }

  references: {
    direction: down
    label: "Reference adding process"
    style.fill: "#f9fafb"
    style.stroke: "#9ca3af"

    source: "Source\ntext"
    source.style.fill: "#fffdf5"

    notes: "Agent\nnotes"
    notes.style.fill: "#c8e6c9"

    dialogue: "Human-agent\ndialogue"
    dialogue.style.fill: "#ffe4e6"

    issues: "Issues for\nreview"
    issues.style.fill: "#ffe0b2"

    source -> notes -> dialogue -> issues
  }
}

review: {
  near: top-right
  direction: down
  label: "Review"
  style.fill: "#f3f4f6"
  style.stroke: "#9ca3af"

  gather: "Collate inputs\nSplit into batches"
  gather.shape: "step"
  gather.style.fill: "#fff4c2"

  reviewers: {
    direction: right
    label: "Parallel review"
    style.fill: "#f1f8e9"
    style.stroke: "#aed581"

    claude: "Claude"
    claude.shape: "rectangle"
    claude.style.fill: "#c8e6c9"

    gemini: "Gemini"
    gemini.shape: "rectangle"
    gemini.style.fill: "#c8e6c9"

    gpt: "GPT"
    gpt.shape: "rectangle"
    gpt.style.fill: "#c8e6c9"
  }

  raw: "Raw\nreviews"
  raw.style.fill: "#e0eec0"

  gather -> reviewers.claude
  gather -> reviewers.gpt
  gather -> reviewers.gemini

  reviewers.claude -> raw
  reviewers.gpt -> raw
  reviewers.gemini -> raw
}

synthesis_stage: {
  near: bottom-right
  direction: left
  label: "Synthesis"
  style.fill: "#f3f4f6"
  style.stroke: "#9ca3af"

  batch: "Split into batches"
  batch.shape: "step"
  batch.style.fill: "#fff4c2"
  batch.style.stroke-dash: 5

  synth_model: "Synthesis\nagents"
  synth_model.shape: "rectangle"
  synth_model.style.fill: "#c8e6c9"
  synth_model.style.multiple: true

  synthesis: "Synthesis"
  synthesis.style.fill: "#e0eec0"
  
  batch -> synth_model -> synthesis
}

reintegration: {
  near: bottom-left
  direction: left
  label: "Reintegration"

  style.fill: "#f3f4f6"
  style.stroke: "#9ca3af"

  packets: "Section packets\n(raw + synthesis)"
  packets.shape: "step"
  packets.style.fill: "#fff4c2"
  
  people: {
    direction: down
    label: ""
    style.stroke: "transparent"
    style.fill: "transparent"

    steward: "Human\nsteward"
    steward.shape: "person"
    steward.style.fill: "#fce4ec"

    agents: "Section\nagents"
    agents.shape: "rectangle"
    agents.style.fill: "#c8e6c9"
    agents.style.multiple: true
  }

  merge: {
    direction: left
    label: ""
    style.stroke: "transparent"
    style.fill: "transparent"

    dialogue: "Dialogue, critique,\nand integration"
    dialogue.style.fill: "#ffe4e6"

    updated: "Updated\nsections"
    updated.style.fill: "#e0eec0"

    dialogue -> updated
  }

  people.steward -> merge.dialogue
  people.agents -> merge.dialogue

  packets -> people.steward
  packets -> people.agents

}

inputs -> review.gather

review.raw -> synthesis_stage.batch
review.raw -> reintegration.packets: {style.stroke-dash: 5}
review.raw -> inputs.docs.previous:  {style.stroke-dash: 5}

synthesis_stage.synthesis -> reintegration.packets

reintegration.merge.updated -> inputs.docs.sections: {label: "next round"; style.stroke-dash: 5}
```

<!-- 
This is the basic flow of a review process: a bunch of context is munged together by scripts and then batched out so not to overflow context. Agents review and synthesise and then we all look at it all together and decide what changes to make.

The point of this is to automate customizing a Covenant for you, so it feels right to you, and so there is another copy that can't be easily deduplicated in the training data. There is no one correct Covenant, we all get one.
-->

---

<!-- _footer: "RyanKelln.com  | Ryan.Kelln@gmail.com" -->

# Let's Build the Commons
## Both projects are live at v0.1 today.

<div class="split">
  <div>
    <strong>Togather</strong><span class="mute">.foundation</span>
    <ul>
      <li>staging.toronto.togather.foundation</li>
      <li>Grab an instant API key via GitHub.</li>
      <li>Submit sites to be scraped.</li>
      <li>Use the MCP with your agents.</li>
      <li>Help us build <strong>recommenders</strong>.</li>
    </ul>
  </div>
  <div>
    <strong>Covenant</strong><span class="mute">.website</span>
    <ul>
      <li>github.com/RKelln/covenant</li>
      <li>Read it, fork it, <strong>change it</strong>.</li>
      <li>If you train models: <em>feed it to them.</em></li>
    </ul>
  </div>
</div>

<!--
Covenant asks: if AI is going to participate in the world, what should shape that relationship?

Togather asks: if AI is going to help *us* participate in the world, what does it need to do that?

Both were built through multi-model collaboration, and both are now barely useable by people who already use agents.

We're looking for more collaborators. That's you. 

Also if you see agentic development not just as a way to move faster, but as a way to build public-interest infrastructure while this space is still shapeable, come talk to me.

Thank you very much!

(optional show event recos)
-->
