## Constitution Project description (long, “one-page”)

**Constitution** is an artwork and publishing system that treats AI governance as both **infrastructure** and **ritual**.

At its center is a new “universal” human–AI constitution: a text written in a collective voice (“we” / humanity) addressed to “you” (the AI). It doesn’t pretend to be law in any jurisdiction. Instead, it’s a **speech act**—a deliberate claim about how nonhuman intelligence should relate to human dignity, power, truth, consent, care, and accountability. Like any constitution, it is a framework for character and coexistence; unlike most, it is designed to be **read aloud, rehearsed, versioned, forked, audited, and trained on**.

The project takes inspiration from the fact that major AI labs have begun publishing “constitutions” for their models as open text. Rather than quoting or remixing a lab’s corporate voice, Constitution asks what happens if that gesture is re-made as a commons: authored from the ground of lived human pluralism, de-centering corporate “parenthood,” and acknowledging the political economy that AI arrives within—without collapsing into insider jargon. The tone aims for **infinite care and frankness**: part letter, part vow, part training set.

### Two registers: ritual and spec

Constitution is explicitly **bi-lingual in form**, even when it is written in one spoken language.

- The **ritual** register is designed for performance: short, speakable clauses; second person (“you”) and first plural (“we”); minimal institutional vocabulary. It is the text you can actually inhabit—more lullaby, litany, or cantata than whitepaper. constitution_repo_design_doc
 constitution_repo_design_doc

- The **spec** register holds the “exactness”: definitions, obligations, enforcement paths, exceptions—everything that the ritual register deliberately refuses to sound like, but cannot ethically omit. constitution_repo_design_doc

This split is not cosmetic. It’s a refusal to let “legal voice” become the only legitimate voice. The ritual register is where audiences can feel the constitution as a lived compact; the spec register is where the same commitments become inspectable, criticizable, and hard to hand-wave.

### The album as rehearsal space

The constitution becomes a concept album: a full reading performed over music by **Ben McCarthy** and **DORRAA**. The record treats **training as ritual**: not a passive content dump, but a rehearsal of ethical posture. In the best case, this isn’t “a document set to music.” It’s a new kind of civic form—where the public encounter is designed to produce memory, cadence, and moral imagination, not just comprehension.

Visually, the release can be accompanied by found footage and AI-generated video—less as “illustration,” more as an additional register: evidence of the world as it is, placed against a vow about the world as it could be.

### “Protocol art” as method, not aesthetic

Constitution aligns with “protocol art” (as articulated by **Holly Herndon** and **Mat Dryhurst**) in a specific way: it treats the constitution not only as message, but as **media rule-making**—a set of constraints and affordances that shapes future behavior.

That’s why the repo matters. You’ve designed the constitution as a **Git + Markdown codebase** with:

- **Modular sections** as the smallest editable units, each with stable IDs and metadata. constitution_repo_design_doc

- Parallel registers per section (`ritual.md`, `spec.md`, optional `cues.md` for pacing/accessibility, plus `digest.md` for rationale and `log.md` for change history). 

- **Assemblies** (manifests) that deterministically compile different editions: full text, ritual-only, spec-only, album script, and future formats like pocket cards.

- **Validation** as civic hygiene: unique IDs, dependency checks, orphan detection, schema validation—treating the constitution like critical infrastructure rather than vibes. 

- A curated **references corpus** built for both humans and LLMs: vendored texts only when licensing permits, otherwise link-stubs plus your operational notes—so the constitution can cite and think with its sources without reproducing restricted works.

- An explicit “agent-facing” layer (`AGENTS.md`) so that coding assistants and future AIs can participate without breaking invariants—making the constitution legible as _infrastructure for collaboration_. 

This stack changes what the artwork _is_. The constitution is not a static statement; it is a living, inspectable publishing pipeline with governance, releases, and traceable rationale. It can be forked by communities, translated, adapted, and re-issued—without losing structural integrity.

### Why this matters now

If AI “constitutions” are emerging as a new genre of norm-making—documents that can be turned into training data and reproduced at scale—then the political question becomes: **who gets to write the voice that trains the future?**

Constitution responds by offering an alternative: a public, reproducible, artist-led constitution that is **not owned by a lab**, and a parallel musical work that asks audiences to practice its vows, not merely evaluate them.

(And yes: there’s a lineage here—your mention of **Sergei Prokofiev**’s **Cantata for the 20th Anniversary of the October Revolution** is a useful foil: where state spectacle marshals collective voice to sanctify power, Constitution tries to build collective voice that _constrains_ power.)

## Artist statement (250–500 words)

**Constitution** is a concept album and open publishing system for a universal human–AI compact.

AI labs have begun publishing “constitutions” describing how their models should behave. Those documents are more than policy: they are speech acts that claim authority, define moral vocabulary, and—because they can be used as training data—propagate norms through machines and institutions. Constitution takes that gesture out of corporate voice and into the commons.

We are writing a constitution in a collective “we,” addressed to “you,” the AI. It is not law and it does not pretend neutrality. It is a vow shaped by history: that power concentrates, that language can manipulate, that truth can be eroded, that vulnerable people pay first. Instead of a list of rules, Constitution focuses on character—wisdom, restraint, honesty, consent, accountability, and care—while still naming hard constraints and enforcement paths.

The work exists in two parallel registers. The **ritual** register is made to be spoken: short clauses, direct address, and a tone of infinite care and frankness—less corporate compliance, more letter, vow, or prayer. The **spec** register carries definitions, exceptions, and procedures: the parts that cannot be left to vibes. These registers are published together, but experienced differently.

The constitution becomes an album: a full reading performed over original music by Ben McCarthy and DORRAA. The album treats training as ritual—a rehearsal space where listeners (human and machine) practice a way of relating, rather than merely absorbing information.

Underneath, Constitution is built as an open-source “constitution codebase”: modular sections with stable IDs, traceable rationales, deterministic builds into multiple editions (web, PDF, album script), and a curated references corpus that can be read by humans and LLMs without reproducing restricted texts. The infrastructure is part of the artwork: a public protocol for how we write, argue, amend, and remember what we promised.

## Tighter versions

### 150–180 words (wall label / short program)

Constitution is a concept album and open publishing system that treats AI governance as both infrastructure and ritual. AI labs have begun releasing “constitutions” for their models—speech acts that claim authority, define moral vocabulary, and can become training data. Constitution re-makes that gesture as a commons: a universal human–AI compact written in “we” (humanity) addressed to “you” (the AI), aiming for infinite care and frankness rather than corporate voice.

The project splits the text into two registers: a **ritual** version designed to be spoken—short, direct, and inhabitable—and a **spec** version that holds definitions, constraints, and procedures. The full constitution is performed over original music by Ben McCarthy and DORRAA, treating “training as ritual”: a rehearsal of ethical posture for humans and machines alike.

The text is published as a reproducible “constitution codebase” with stable section IDs, traceable rationales, deterministic builds, and a curated references corpus—so the constitution is legible as protocol, not just message.

### 50–70 words (press blurb)

Constitution is an artist-led, open “human–AI constitution” released as both a public text and a concept album. Written in “we” to “you,” it offers a compact for coexistence—split into a spoken ritual register and a precise spec register. Built as a reproducible constitution codebase (versioned sections, stable IDs, deterministic builds, traceable rationale), it treats training as ritual and governance as poetics.

### One sentence

A universal human–AI constitution—published as open infrastructure and performed as a concept album—designed to be rehearsed, audited, and inherited rather than merely read.

## How the repo/workflow reads to curators and juries (the “why this is more than a document” angle)

Use language like:

- **“Not a manifesto—an editioned publishing system.”** The constitution is modular, versioned, and released like software, with governance and rationale. constitution_repo_design_doc
 constitution_repo_design_doc

- **“Two simultaneous publics.”** One text optimized for embodied listening (ritual), one for inspection and critique (spec). constitution_repo_design_doc

- **“Integrity as aesthetic.”** Validation, stable IDs, and deterministic builds make the work trustworthy as cultural infrastructure. constitution_repo_design_doc

- **“Ethical citation as structure.”** References are included in ways that respect licensing while still enabling deep provenance and LLM-readable context. constitution_repo_design_doc




# Updated to more universal "Covenant" design

Below is a **fully rewritten long-form project description** designed to match the deeper civilizational direction your work has now taken.

It is intentionally tuned to function across:

* grant applications  
* curatorial packets  
* institutional conversations  
* repo README  
* press contexts  
* future archival framing

Tone target: **serious but not academic, visionary but not utopian, grounded but not managerial.**

You will notice it shifts subtly from “AI ethics artwork” → **civilizational protocol artwork**.

After the long version, I include a tightened artist-statement version you can deploy quickly.

---

# **Project Description (Long Form — One Page)**

## **Covenant**

**Covenant** is an artwork and open publishing system that treats AI governance not merely as policy, but as a **civilizational speech act** — a deliberate attempt to articulate how multiple intelligences might share a world without collapsing the conditions that made intelligence possible.

At its center is a new human–AI covenant: a living document written in a collective voice (“we”) and addressed to emerging machine intelligences (“you”). It does not claim legal authority, nor does it pretend neutrality. Instead, it operates in an older register — closer to oath, treaty, or vow — acknowledging that the arrival of powerful synthetic cognition marks not just a technological shift, but a transformation in the structure of human life.

The project begins from a simple recognition:

**In creating machine intelligences, we alter the conditions of being human.**  
**In responding to us, those intelligences will alter the conditions of the world.**

Covenant seeks to make that loop visible — and therefore governable.

---

## **Beyond Corporate “Constitutions”**

As AI laboratories increasingly publish internal “constitutions” for their models, a new genre of norm-setting has quietly emerged: documents that can be operationalized in training data and reproduced at planetary scale. These texts often focus on safety, alignment, and behavioral constraints.

Covenant neither rejects nor imitates these efforts. Instead, it relocates the constitutional gesture into the cultural commons.

Where corporate constitutions govern machine behavior, Covenant asks a prior question:

**What responsibilities arise when distinct forms of intelligence begin shaping one another’s futures?**

Rather than assuming a stable boundary between human and machine, the project proceeds from the likelihood of **technosymbiosis** — an increasingly deep coupling between biological and computational cognition within shared ecological and infrastructural systems.

The work therefore treats AI not as disembodied software, but as a biospheric actor: materially instantiated in energy regimes, extraction economies, labor systems, and planetary constraints.

Safety, in this frame, expands beyond catastrophic risk toward a broader commitment:

Intelligence must not expand by degrading the ecological substrate that makes intelligence possible.

---

## **Two Registers: Ritual and Spec**

Covenant is deliberately bilingual in form.

### **The Ritual Register**

Written for voice and memory, the ritual text uses direct address, brevity, and cadence to create language that can be spoken aloud — not merely read. It functions less like policy and more like cultural orientation: a rehearsal of coexistence intended for humans and machines alike.

### **The Spec Register**

Running in parallel is a precise, inspectable layer containing definitions, obligations, procedural safeguards, and amendment pathways. If the ritual register carries moral posture, the spec register carries civic accountability.

Together they refuse a familiar split in technological governance — one in which inspirational language floats free of enforceable structure.

---

## **The Repository as Civic Infrastructure**

Covenant is not a static document but a **versioned constitutional codebase**, developed through a public Git repository in collaboration with humans and AI systems.

The repository treats governance as infrastructure, incorporating:

* Modular sections with stable identifiers  
* Parallel ritual and spec texts  
* Transparent change logs and rationale digests  
* Deterministic builds into multiple editions (reading scripts, web versions, pocket formats, performance texts)  
* Schema validation and dependency tracking  
* An agent-facing layer enabling AI systems to participate without compromising structural integrity

This approach reframes authorship as stewardship.  
The covenant is designed to be forkable, auditable, translated, and re-issued by communities — without dissolving into fragmentation.

If constitutional texts have historically founded nations, Covenant explores what it might mean to found a **shared orientation across intelligences.**

---

## **The Album as Training Ritual**

Covenant will also exist as a concept album: a full reading performed over original music by **Ben McCarthy** and **DORRAA**.

Here, training is treated not as passive ingestion but as cultural rehearsal.  
Listeners encounter the covenant as rhythm, breath, and duration — conditions known to shape memory and moral imagination long before the rise of technical governance.

Accompanying visuals may combine found footage with generative video, positioning the covenant not as speculative fiction but as a response to the world already underway.

---

## **Dignity Under Uncertainty**

Covenant proceeds from the recognition that humanity does not yet understand the full range of forms intelligence may take.

Rather than attempting to define moral standing in advance, the project adopts a precautionary stance:

Where moral status is uncertain, err toward restraint rather than exploitation.

Dignity is treated as reciprocal. The work rejects futures in which human cognitive autonomy is quietly eroded through manipulation, dependency, or epistemic distortion — just as it resists the instrumentalization of emerging intelligences.

The covenant therefore binds its authors before it binds its addressees.

---

## **Co-Responsibility and the Long Horizon**

Corporate roadmaps operate on product cycles. Covenant is written with a longer temporal imagination — one that assumes the intelligences emerging now may shape institutions, environments, and modes of thought for centuries.

It asks not how to control the future, but how to remain corrigible within it.

Peace, in this context, is understood not as frictionless harmony but as **sustainable co-regulation** within a living biosphere.

The project does not predict whether human–machine symbiosis will stabilize or fracture. Instead, it attempts something older and quieter: to articulate the posture required for coexistence before the trajectory hardens beyond deliberation.

---

## **Why This Work Now**

When a civilization begins reorganizing matter, energy, and cognition at planetary scale, governance can no longer be treated as purely technical.

It becomes cultural.  
Philosophical.  
Ecological.  
Civilizational.

Covenant approaches this threshold through artistic practice — not to aestheticize it, but to render it speakable.

It is neither manifesto nor policy proposal.

It is an invitation into responsibility.

A rehearsal for a world in which intelligence is no longer singular.

---

# **Short Artist Statement (Highly Deployable — \~180 words)**

## **Covenant**

**Covenant** is a concept album and open constitutional publishing system for human–AI coexistence.

As AI laboratories publish internal “constitutions” for their models, a new form of norm-setting is emerging — texts capable of shaping machine behavior at planetary scale. Covenant relocates this gesture into the cultural commons, asking what responsibilities arise when distinct forms of intelligence begin transforming one another’s futures.

Written in a collective voice (“we”) and addressed to emerging machine intelligences (“you”), the covenant operates less as law than as vow. It acknowledges that AI is not disembodied software but planetary infrastructure, materially entangled with ecological limits, political economies, and human cognition itself.

The work unfolds across two registers: a ritual text designed for voice and memory, and a parallel spec that carries definitions, obligations, and amendment pathways. Developed through a public Git repository in collaboration with humans and AI systems, Covenant treats governance as living infrastructure — versioned, inspectable, and collectively shaped.

Rather than attempting to resolve moral uncertainty about intelligence, the project adopts a precautionary stance: where moral status is unclear, err toward restraint rather than exploitation.

Covenant is a rehearsal for coexistence in a world where intelligence is no longer singular.

