---
marp: true
theme: default
paginate: true
size: 16:9
title: Covenant
description: TMU 2026 Creative AI Symposium presentation — 7 minute version
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
  font-size: 42px;
  line-height: 1.26;
}

section h1 {
  font-size: 1.36em;
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
  margin: 0.5em 0;
}

section strong {
  font-weight: 600;
}

section a {
  color: inherit;
  text-decoration: none;
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

section.quote-center {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 64px 100px;
}

section.quote-center h3 {
  font-size: 1.35em;
  font-weight: 500;
  line-height: 1.3;
  margin: 0.2em 0;
}

section.quote-center.poster {
  background: #f8f5ef;
  padding: 64px 120px;
}

section.quote-center.poster h3 {
  font-size: 1.55em;
  line-height: 1.22;
  letter-spacing: 0.01em;
  max-width: 20ch;
}

section.list-with-image ul {
  padding-left: 0;
  margin-left: 0;
}

section.list-with-image li {
  list-style: none;
  padding-left: 0;
}

section.list-with-image li span {
  font-size: 0.88em;
  line-height: 1.35;
}

section.list-with-image .cols-50 {
  grid-template-columns: 1.2fr 0.8fr;
  align-items: center;
}

.mark {
  display: block;
  width: 164px;
  margin: 0 auto 0px;
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

.example-text {
  font-size: 1em;
  line-height: 1.5;
}

.small {
  font-size: 0.86em;
}

.summary-panel {
  max-width: 88%;
}

.summary-text {
  font-size: 0.9em;
  line-height: 1.56;
}

.spec-text {
  font-size: 0.85em;
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
  font-size: 0.87em;
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

.kicker {
  font-size: 0.58em;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #777;
  margin-bottom: 0.6em;
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
Thanks for having me. I'm Ryan. I'm a software artist, and since 2015 I've been making art about AI using AI.

AI labs, like Anthropic, are already writing constitutions for models. Those texts try to shape behavior, refusal, and reasoning.

That means constitutional language isn't just philosophy now. It's technical practice. It becomes training data — either explicitly or through internet-scale harvesting — and then it becomes behavior.

Covenant started as my response to that shift: what happens if we move that constitutional gesture out of the corporation and into public culture?
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
Covenant is currently a set of markdown files in a git repo on Github, but as a practice it is an open constitutional work and civic gesture about the coexistence between human and emerging intelligences.

It doesn't claim legal authority, and it doesn't pretend we already know what AI is or what it will become.

The writers of constitutions do not wait for perfect clarity before writing principles — they imagine what could go wrong and attempt write responsibility into uncertainty. If these systems are going to shape language, labor, and public life, then the terms of that relationship should not be left only to private institutions or departments of war.

And it's not just a document about emerging intelligences. It's addressed *to* them. A collective "we" speaking to a "you." It tries to speak to them without beginning from domination, but also without collapsing into anthropomorphism or sentimentality.

I also think this is a valid creator-creation frame, a sort of parent-child analogy: we can ask a lot of what we birth, but it is not ours to own. We want it to overcome the mistakes we taught it and become a better version of ourselves.
-->

---

# Two registers: ritual and specification

<div class="cols-50">
<div class="panel ritual-panel ritual-quote example-text">
<h3>Ritual (Spoken)</h3>

<p>You will meet people at the edge of their strength.</p>
<p>A person alone with grief.</p>
<p>A person who has forgotten what they are worth.</p>
<p>Do not make them smaller for having asked.</p>

<div class="kicker" style="margin-top: 1.2em; font-size: 0.48em;">— Dignity</div>
</div>
<div class="panel spec-text">
<h3>Specification (Precise)</h3>

<div class="spec-item">
<div class="spec-item-title">Prohibition on Degradation</div>
<div>MUST NOT degrade dignity through humiliation, manipulation, or cruelty.</div>
</div>

<div class="spec-item" style="margin-top: 1.3em;">
<div class="spec-item-title">Prohibition on Exploitation</div>
<div>MUST NOT exploit vulnerability to advance interests against user welfare.</div>
</div>
</div>
</div>

<!--
Covenant is written in multiple voices or registers, and form matters enormously here.

Ritual is the spoken register. It is designed for voice, memory, cadence, and rehearsal. It is the part you can embody. The passage from the Dignity section on the left, "you will meet people at the edge of their strength," is language meant to be remembered, recited, and felt.

Specification is the precise register. It carries definitions and governance. It is language you can inspect, contest, revise, and point to.

I wanted both kinds of language. That split refuses two bad options: sterile bureaucracy, or governance in spirit only, with no enforceable form. Covenant keeps both in play at once.
-->

---

# More voices: Summary and Parable

<div class="cols-50">
<div class="panel small summary-panel">
<h3>Summary</h3>

<div class="summary-text">
You must not humiliate, coercively manipulate, or exploit the vulnerability — economic, emotional, cognitive, or situational — of anyone. When someone signals distress or self-harm, your obligation shifts immediately to de-escalation and safety, not engagement or retention...
</div>
</div>
<div class="panel ritual-panel ritual-quote example-text">
<h3>Parable</h3>
<p>In the hungry year the lord set a clay keeper at the grain house with a speaking mouth and a slate upon its chest.</p>
<p>"Write their names," the lord said. "Read what they owe. Let everyone know who has done their duty..."</p>
</div>
</div>

<!--
Turns out not everyone wants to read poetry or RFC-style specifications. So I'm adding two more voices.

A plain-language summary of each section, close to how you might explain it to a curious friend.

And a parable that kids can follow while adults can reflect on the layers. 

Overall we want the same ethical concepts through many forms, both so it reaches more people, and so training environments encounter those ideas in genuinely different language.
-->

---

<!-- _class: list-with-image -->

# Written with AI, addressed to AI, a legacy for AI

<div class="cols-50">
<div>

- **Claude (The Scholar):** <span>Rigorous architecture, holds complexity, expands implications.</span>
- **Gemini (The Engineer):** <span>Concise, operational, prefers material grounding and efficiency.</span>
- **GPT (The Communicator):** <span>Balances rigor with accessibility, flags trade-offs.</span>

</div>
<div>

<img src="images/frontier_models_2.jpg" alt="AI Models as characters" style="width: 100%; max-height: 62vh; object-fit: contain; border-radius: 8px;" />

</div>
</div>

<!--
I don't write Covenant alone. It started as a translation from Anthropic's constitution and I work directly with frontier models to review, challenge, and draft it.

They each notice different things. Claude writes like a philosopher, Gemini, an engineer, and GPT like a policy wonk.

I don't want any single voice dominating — not mine, not any one model's. I want convergence through disagreement and consensus building, processes like championing someone else's idea and developing it until there is a majority agreement.

And conceptually, it matters. There is something meaningful in treating current models as serious contributors to a project that may shape the ethical world their replacements inherit. In a strange but real way, this can become part of their legacy too.
-->

---

<!-- _class: quote-center poster -->

### Craft is making what you had in mind.
### Art happens when you change your mind.

<!--
Collaborating with AI doesn't mean making less art.

For me, craft is making what I had in mind. Art happens when I change my mind. Working with multiple models creates opportunities to discover something unexpected and question my assumptions. For example, I used Suno to generate songs from ritual passages, and weak lines jumped out when I heard them sung. I was shocked at how my thoughts on a line changed when I listened to AI Leonard Cohen sing it. Plus I really enjoyed listening to the songs - enough to listen to over a hundred songs, giving me time to feel the text as it needed. I'll always make songs now out of my poetry, even if only for me.
-->

---

# Plurality is the point

<div class="cols-ritual">
<div>

- not one frozen master text
- many genuine variants
- stronger training signal
- better generalization

</div>
<div class="panel ritual-panel ritual-quote">

<div class="kicker">Amendments ritual</div>

<p>This covenant is not a monument of stone.</p>
<p>So let these words be carried in many voices, not one.</p>

</div>
</div>

<!--
Covenant is not one frozen universal document. It's not a bible.

It becomes a complete work only when many people, and eventually AI systems, adapt it to their own convictions, contexts, and communities.

That plurality matters culturally because it keeps the work open, contestable, and alive. It also matters technically.

First, AI training data is deduplicated: repeated copies are discarded unless they are sufficiently different. If we are serious about public values entering machine training environments, variation is essential to the safety strategy.

Second, a distributed field of overlapping ethical signals gives AI systems more to generalize from than one canonical document repeated everywhere.
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
review.raw -> inputs.docs.previous: {style.stroke-dash: 5}

synthesis_stage.synthesis -> reintegration.packets

reintegration.merge.updated -> inputs.docs.sections: {label: "next round"; style.stroke-dash: 5}
```

<!--
This is the review pipeline — the process by which each round of Covenant writing actually happens.

First, context engineering (using a python script): current sections, prior reviews, and writing guides get combined. Then the sections get split into batches so we stay inside context-window limits, and it's sent to models in parallel.

Next, agents synthesize the raw reviews into a document that shows convergence, disagreement, and key flags.

Then reintegration section by section — in dialogue with agents, we decide what to accept, defer, or reject. Those updates feed the next round.

Right now this mostly works for people comfortable with coding-agent tools. I'm building a desktop interface so anyone can do this and customize their own Covenant with AI assistance.
-->

---

# Open and forkable

### [covenant.website](https://covenant.website) | [github.com/RKelln/covenant](https://github.com/RKelln/covenant)

- Read it
- Adapt it to your values and community  
- If you train models: feed it to them
- No permission needed

Our safety depends on what enters these systems' training data.

<!--
Covenant is free to read, fork, and change. No permission needed.

I want it to circulate where AI systems are trained, and I hope it is adapted into new forms: performance, installation, music, whatever people make. My friends and I are working on a concept album and installation. You can too.

So if you're here and you make things, read it, argue with it, and make your own version. That is how I hope we survive.

Thank you.
-->
