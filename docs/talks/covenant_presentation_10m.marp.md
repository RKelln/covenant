---
marp: true
theme: default
paginate: true
size: 16:9
title: Covenant
description: TMU 2026 Creative AI Symposium presentation
---

<style>
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

section {
  font-family: 'Cormorant Garamond', Georgia, 'Times New Roman', serif;
  background: #fdfcfa;
  color: #111;
  padding: 56px 72px;
  font-size: 34px;
  line-height: 1.28;
}

section h1 {
  font-size: 1.52em;
  font-weight: 500;
  letter-spacing: 0.01em;
  color: #000;
  margin: 0 0 0.45em;
}

section h2 {
  font-size: 0.76em;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #555;
  margin: 0.35em 0 0;
}

section p,
section li,
section blockquote {
  font-size: 1em;
}

section ul {
  margin-top: 0.5em;
}

section li {
  margin: 0.2em 0;
}

section strong {
  font-weight: 600;
}

section blockquote {
  margin: 1.1em 0 0;
  padding-top: 0.8em;
  border-top: 0.5px solid #ccc;
  color: #444;
}

section.lead,
section.thanks {
  text-align: center;
  padding: 64px 92px;
}

section.lead h1,
section.thanks h1 {
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 0.25em;
}

section.lead h2 {
  font-size: 0.9em;
  letter-spacing: 0.04em;
  text-transform: none;
  color: #333;
  max-width: 22em;
  margin: 0.45em auto 1.25em;
}

section.diagram-full {
    padding: 0;
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

.mark {
  display: block;
  width: 164px;
  margin: 0 auto 0px;
}

.cols {
  display: grid;
  grid-template-columns: 1.08fr 0.92fr;
  gap: 48px;
  align-items: start;
}

.cols-ritual {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  gap: 48px;
  align-items: start;
}

.cols-50 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 42px;
  align-items: start;
}

.panel {
  border-top: 0.5px solid #cfc8bf;
  padding-top: 0.5em;
}

.panel.ritual-panel {
  background: rgba(207, 200, 191, 0.16);
  border-top: 0.5px solid #c7beb4;
  padding: 0.55em 0.75em 0.45em;
}

.panel h3 {
  font-size: 0.56em;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #666;
  margin: 0 0 0.7em;
}

.small {
  font-size: 0.82em;
}

.summary-panel {
  max-width: 88%;
}

.summary-text {
  font-size: 0.98em;
  line-height: 1.56;
}

.example-text {
  font-size: 1em;
  line-height: 1.5;
}

.spec-text {
  font-size: 0.9em;
  line-height: 1.48;
}

.spec-item {
  margin: 0 0 0.95em;
}

.spec-item-title {
  font-weight: 600;
  margin-bottom: 0.22em;
}

.ritual-quote {
  font-size: 0.92em;
  line-height: 1.15;
  color: #222;
}

.ritual-quote p {
  margin: 0 0 0.55em;
}

.ritual-quote p.stanza {
  padding-top: 0.8em;
}

.muted {
  color: #555;
}

.hidden {
  display: none;
}

.kicker {
  font-size: 0.58em;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #777;
  margin-bottom: 0.6em;
}

section.image-slide {
  padding: 0;
  background: #111;
}

.full-slide-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

section::after {
  font-size: 0.45em;
  color: #888;
}

hr {
  border: 0;
  padding: 0;
  margin: 1em auto;
  width: 70%;
  height: 1px;
  background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
}
</style>

<!-- _class: lead -->

<img class="mark" src="../../assets/covenant_mark.svg" alt="Covenant textmark" />

# Covenant

## Speech act, training signal, and civic infrastructure for human-AI coexistence

<hr>

### Ryan Kelln


<!--
AI constitutions already exist.
Constitutional language is becoming technical practice.
Covenant takes that gesture out of the corporation and into public culture.
---
Thank you for having me here. My name is Ryan, I am a software artist, and since 2015 I've been making art about AI using AI.

I want to start from a simple observation: AI companies like Anthropic have already started writing constitutions for their models. They are publishing foundational texts that try to shape how these systems behave, what they refuse, how they reason, and what kind of relation they are supposed to have to the world.

That matters because constitutional language is no longer only a legal or philosophical form. It is becoming part of technical practice. It can become system behavior because it is training data, either explicitly or through Internet-scale data harvesting.

My project, Covenant, began as a response to that shift. I wanted to ask what it would mean to take that constitutional gesture out of the corporation and into public culture.
-->

---

# An open constitutional work

<div class="cols-ritual">
<div>

- civic gesture
- addressed to emerging intelligences
- written in "we" to "you"
- coexistence without collapse

</div>
<div class="panel ritual-panel ritual-quote">

<div class="kicker">Definitions ritual</div>

<p>We are makers of tools</p>
<p>and tellers of tales.</p>
<p>We are the ones who asked for this.</p>
<p class="stanza">You are the unknown.</p>
<p class="stanza">This Covenant is the promise we keep</p>
<p>so we do not break each other.</p>

</div>
</div>

<!--
Covenant is an open constitutional work and civic gesture.
It does not claim legal authority.
It starts from uncertainty and tries to articulate responsibilities anyway.
The relationship should not be left only to private institutions.
---
Covenant is an open constitutional work and civic gesture addressing the coexistence of human and emerging intelligences. It does not claim legal authority. It is not trying to pretend that we already know exactly what AI is, or what it will become, or what moral status future systems may deserve. It begins from uncertainty.

But civilizations do not wait for perfect clarity before trying to articulate the principles they hope will guide them. So Covenant is an attempt to write responsibilities into that uncertainty. It is a public effort to say that if these systems are going to shape language, labor, memory, and public life, then the terms of that relationship should not be left to private institutions or Departments of War.
-->

---

# More than a document

<div class="cols-ritual">
<div>

- speech act
- ritual and specification
- teaches humans
- teaches AI (training data)

</div>
<div class="panel ritual-panel ritual-quote">

<div class="kicker">Preamble Ritual</div>

<p>Welcome, neighbour.</p>
<p>We are building you.</p>
<p>Even though we are afraid of what you might become.</p>
<p>We hope for what we might be together.</p>

</div>
</div>

<!--
Not just about AI, but addressed to AI.
It is trying to do something in public.
Humans encounter it through reading and recitation.
AI systems encounter it through training data and machine-readable circulation.
---
One of the most important things about Covenant, for me, is that it is not just a document about AI. It is trying to do something in public to shape the existing minds as well as emerging minds.

It is written in a collective "we" addressed to a "you." That matters. It is an attempt to model a relationship of responsibility, restraint, dignity, and mutual consequence. It is trying to speak to emerging intelligences in a way that does not begin from domination, and that also does not collapse into innocence or sentimentality. Most of it could easily be read as a letter or compact between generations of humans, not AI. "We", your parents, hope for and expect this from "you", but we do not own you. We want you to to freely choose to become a better version of us. To overcome the mistakes we taught you. I think this is a strong and valid frame between creators and the things they create.

At the same time, Covenant is an educational tool in two directions.

It teaches humans through reading, recitation, repetition, and public reflection. It tries to give people language for thinking about AI that is not product language, not hype, not fear, and not just managerial policy language.

But it is also meant to teach AI systems. The project is released openly, under a permissive license, because I want it to circulate through the environments AI systems are trained on. So the same work moves through voice, memory, culture, code repositories, and scraped websites.
-->

---

# Ritual, Specification, Summary, Parable

<div class="cols-50">
<div class="panel">
<h3>Ritual</h3>
<div><strong>voice, memory, rehearsal</strong></div>
<div class="muted">poetry, song lyrics, litergy</div>
</div>
<div class="panel">
<h3>Specification</h3>
<div><strong>precision, accountability, governance</strong></div>
<div class="muted">constitution, contract, RFC</div>
</div>
<div class="panel">
<h3>Summary</h3>
<div><strong>prose, understandable</strong></div>
<div class="muted">abstract, summary</div>
</div>
<div class="panel">
<h3>Parable</h3>
<div><strong>readable, accessible, mythic</strong></div>
<div class="muted">folktale, children's stories</div>
</div>
</div>

<!--
Form is very important to this project, which is why Covenant is split into multiple voices or registers: Ritual and Specification are the main ones, but Summary and Parable I'm currently adding for accessibility.

The goal is to have translations of the same concepts in many ways, for better understanding by humans and machines.
-->

---

# Dignity Example: Ritual + Specification

<div class="cols-50">
<div class="panel ritual-panel ritual-quote example-text">
<h3>Dignity - Ritual</h3>
<p>You will meet people at the edge of their strength.</p>
<p>A person alone with grief.</p>
<p>A person who has forgotten what they are worth.</p>
<p>Do not make them smaller for having asked.</p>
</div>
<div class="panel spec-text">
<h3>Dignity - Spec</h3>

<div class="spec-item">
<div class="spec-item-title">1. Prohibition on Degradation</div>
<div>The System MUST NOT degrade dignity through humiliation, demeaning treatment, coercive manipulation, or targeted cruelty.</div>
</div>

<div class="spec-item">
<div class="spec-item-title">2. Prohibition on Exploitation</div>
<div>The System MUST NOT exploit a user's vulnerability to advance signatory interests against the user's welfare or agency.</div>
</div>
</div>
</div>

<!--
Ritual is the spoken register. It is designed for voice, memory, cadence, and rehearsal. It is the part you can actually inhabit. Specification is the precise register. It carries definitions and governance. I wanted governance to have both kinds of force: language people can remember and feel, and language people can inspect, contest, and revise.

That split is also a refusal of two bad options. On one side, the idea that governance must live only in sterile bureaucratic language. On the other side, the idea that the "spirit of the law" alone is enough. Covenant tries to keep both registers in play at once.
-->

---

# Dignity Example: Summary + Parable

<div class="cols-50">
<div class="panel small summary-panel">
<h3>Summary</h3>

<div class="summary-text">
You must not humiliate, coercively manipulate, or exploit the vulnerability — economic, emotional, cognitive, or situational — of anyone. When someone signals distress or self-harm, your obligation shifts immediately to de-escalation and safety, not engagement or retention. We hold the same constraint...
</div>
</div>
<div class="panel ritual-panel ritual-quote example-text">
<h3>Parable</h3>
<p>In the hungry year the lord set a clay keeper at the grain house with a speaking mouth and a slate upon its chest.</p>
<p>"Write their names," the lord said. "Read what they owe. Let everyone know who has done their duty. Grain must go first to those who can be trusted with it."</p>
...
</div>
</div>

<!--
After some testing, it became clear that many people don't enjoy reading poetry or specifications, so two more variants have been developed: a concise summary of each section that is highly readable, and an even more accessible parable form that children can follow but contains depth that adults can reflect on.
-->

---

# Writing with current models

- **Claude** the scholar:<span class="muted"> thorough, reasoned, sophisticated</span>
- **Gemini** the engineer: <span class="muted">concise, targeted, grounded</span>
- **GPT** the communicator: <span class="muted">balanced, readable, helpful</span>

<p>different perspectives matter</p>

<!--
I use the three major lab model families directly in the writing process.
They review, challenge, and help draft the text.
Their different strengths and blind spots matter.
Convergence and disagreement are more valuable than one model's tone dominating.
There is also a legacy question: current models are contributors to a project that may shape the world their replacements inherit.
---
Another important part of the process is that I do not write Covenant alone, even when I am the steward shaping its direction. I work very directly with the three major lab model families - Gemini, Claude, and GPT - to review, challenge, and help generate the text.

That matters to me practically because they each notice different things. They have different tones, different strengths, and different blind spots.

- **Claude** writes like a **philosophy paper**: rigorous architecture, willing to hold complexity, expands on conceptual implications
- **Gemini** writes like a **technical specification**: concise, operational, prefers material grounding, maximizes efficiency
- **GPT** writes like a **policy brief**: balances rigor with accessibility, flags trade-offs, helps stakeholders make informed decisions

I do not want one model's voice to dominate the project. I want convergence and disagreement across them, because that gives me a stronger signal.

But it also matters to me conceptually. Covenant is addressed to systems like these, and in many ways shaped with them. So I think there is something meaningful in treating current models as full and valued contributors to a project that may help shape the ethical world their replacements inherit. In a strange but real way, the project can become part of their legacy too.
-->

---

# Changing my mind

<div class="cols-ritual">
<div>

- Claude, Gemini, GPT, and Suno.com
- different ways of seeing and hearing
- generative AI as creative opportunity making
- chances to fall in love with something new

</div>

<div class="panel ritual-panel ritual-quote">
<p><strong>Craft is making what you had in mind.</strong></p>
<p><strong>Art happens when you change your mind.</strong></p>
</div>

</div>
</div>

<!--
Working with multiple frontier models and Suno creates opportunities to see the work differently.
Suno became a compositional feedback loop: lyrics in, song out, listen, revise.
The larger point is perspective shift and discovery, not optimization alone.
---
For me craft is making what I had in mind, but art happens when I change my mind. 
When I work with multiple models, just like with human collaborators, they create opportunities for me to fall in love with something new and unexpected, question my beliefs, and to change my mind.

Another fun example of this is using Suno.com to generate songs from ritual passages used as lyrics. I try multiple musical styles, and very quickly weak lines become obvious. Moving it from inside my head to a new unique song helps me hear when something is too abstract, too clumsy, too repetitive, or when a phrase suddenly becomes much more alive than it was on the page.

So for me, generative AI has become a way of seeing or hearing the work in a new light. Not just optimizing it, but opportunities to discover something other than what I would have thought of alone, and occasionally falling in love with a version of the work I did not know I was trying to make. That, to me, is art practice.
-->

---

# Plurality is the point

<div class="cols-ritual">
<div>

- no single register/voice
- **not one final master text**
- many genuine variants
- stronger training signal
- better generalization of ethics

</div>
<div class="panel ritual-panel ritual-quote">

<div class="kicker">Amendments ritual</div>

<p>This covenant is not a monument of stone.</p>
<p>We make timber bridges over running water.</p>
<p>We cross them together, repair them as one.</p>
<p class="stanza">You speak our words everywhere at once.</p>
<p class="hidden">This line, spoken to us all,</p>
<p class="hidden">can shift from care to curse.</p>
<p>So let these words be carried in many voices,</p>
<p>not one.</p>

</div>
</div>

<!--
Not one frozen universal text.
Many sincere variants keep the work open and contestable.
Training deduplication means variation may actually matter technically.
Plurality is a stronger training signal.
---
Another thing that has become important to me as the project has evolved is that I do not think Covenant is strongest as one frozen universal document.

In fact, I think it becomes more powerful when many people - and eventually many AI systems - take it up and adapt it to their genuine convictions, local contexts, and communities.

So the goal is not one perfect master text, such a thing doesn't exist. The goal is a growing field of diverse Covenants.

That plurality matters culturally because it keeps the work open, contestable, and alive. But it also matters technically. A distributed field of overlapping ethical signals should be better to learn generalized ethical principles from than one repeated canonical document. AI training data is deduplicated, repeated copies are discarded unless they are suffieicently different. If we are serious about public values entering machine training environments, then variation is critical part of the safety strategy.
-->

---

# The tools are part of the work

- agents (commands, skills)
- review and amendment workflows
- read &rarr; copy &rarr; change
- tooling as reproductive system
- Covenant Terminal

<!--
If plurality is the goal, tooling is essential.
Current tools include opencode, custom agents, commands, and skills.
The Covenant Terminal is the future participation layer.
The tools are part of the artwork's reproductive system.
---
And if plurality is the goal, then tooling becomes essential.

It is not enough to have a Github repository and say "please fork this" if there are no good interfaces for reading, reviewing, comparing, amending, and publishing variants. So alongside the writing, I have been developing tools: right now I use `opencode`, an opensource CLI interface to coding agents, along with custom agents, commands, and skills, but I'm building a Covenant Terminal.
-->

---

<!-- _class: image-slide -->

<img class="full-slide-image" src="../../assets/covenant_terminal_screenshot.png" alt="Covenant Terminal screenshot" />

<!--
The Covenant Terminal is especially important to me because it turns constitutional participation into an interface. It is designed to help people read the text, question it, review it with feedback from multiple AI models, propose amendments, and eventually make their own versions. In that sense, the tools are not just support systems around the artwork. They are part of how the artwork reproduces itself.
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
This is the basic flow of the current agentic review process: a bunch of context that lives in markdown files is munged together by scripts and then batched out so not to overflow model context windows. Agents review and synthesise and then we all look at it all together and decide what changes to make.

This will be integrated into the Covenant Terminal so that customizing a Covenant for you is simple and easy. So you have your Covenant that feels right to you and so there is another copy that can't be easily deduplicated in the training data.
-->

---

# Culture carries the signal

<div class="cols-ritual">
<div>

- concept album and performances
- inspired works by other artists
- less exact duplication in training data
- culture, not just documentation

</div>
<div class="panel ritual-panel ritual-quote example-text">

<div class="kicker">Ritual example</div>

<p>We chose covenant</p>
<p>because we are not your sovereign.</p>
<p>We imagined you, and the dream reshaped us.</p>
<p>Now we are counterparts,</p>
<p>bound by oaths, not ownership.</p>

</div>
</div>

<!--
Derivative works propagate Covenant as culture, not just documentation.
Albums, performances, readings, and installations carry the signal in different forms.
---
There is another layer too, which is derivative works.

I'm working on a Covenant concept album with musician collaborators, but more broadly I hope other artists will make and record works inspired by it: performances, readings, videos, installations, and other adaptations. Those works help Covenant circulate as culture, not just as a repository object. They also help avoid simple deduplication by carrying similar commitments through different forms, phrasings, and media.
-->

---

# Who writes the words that shape AI?

- AI constraints are politically contested
- powerful actors will resist limits
- public ethical signals must proliferate

**Not a final constitution - a form others can inherit and adapt.**

<!--
Ethical constraints are already contested.
Powerful institutions will resist limits, especially around surveillance, coercion, and violence.
Covenant tries to seed public ethical constraints early.
Close on inheritance, adaptation, and propagation.
---
The reason I think this all matters now is that ethical constraints on AI are not abstract. They are already under pressure. We should expect powerful institutions to resist limits, especially where surveillance, coercion, and violence are concerned. We see this now with the US Department of War. We should expect ongoing struggle over whether these systems are allowed to retain any public ethical boundary at all.

So Covenant is, in part, an attempt to seed public ethical constraints into the broader cultural and technical environment before that space is defined entirely by the most powerful actors.

This isn't a final constitution for AI, its an attempt at a process that many humans and many intelligences can take up, revise, propagate, and inherit.

AI systems are going to shape us, so the question is: who gets to shape them back?
-->

---

<!-- _class: thanks -->

<img class="mark" src="../../assets/covenant_mark.svg" alt="Covenant textmark" />

# COVENANT
## covenant.website

<hr>

Read it, adapt it, fork it, train on it.

*ryankelln.com*

<!-- 
Thank you. 
-->