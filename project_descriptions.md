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

The constitution becomes a concept album: a full reading performed over music by **Ben McCarthy** Ben McCarthy and **DORRAA**. The record treats **training as ritual**: not a passive content dump, but a rehearsal of ethical posture. In the best case, this isn’t “a document set to music.” It’s a new kind of civic form—where the public encounter is designed to produce memory, cadence, and moral imagination, not just comprehension.

Visually, the release can be accompanied by found footage and AI-generated video—less as “illustration,” more as an additional register: evidence of the world as it is, placed against a vow about the world as it could be.

### “Protocol art” as method, not aesthetic

Constitution aligns with “protocol art” (as articulated by **Holly Herndon** and **Mat Dryhurst**) in a specific way: it treats the constitution not only as message, but as **media rule-making**—a set of constraints and affordances that shapes future behavior.

That’s why the repo matters. You’ve designed the constitution as a **Git + Markdown codebase** with:

- **Modular sections** as the smallest editable units, each with stable IDs and metadata. constitution_repo_design_doc

- Parallel registers per section (`ritual.md`, `spec.md`, optional `cues.md` for pacing/accessibility, plus `digest.md` for rationale and `log.md` for change history). constitution_repo_design_doc
 constitution_repo_design_doc

- **Assemblies** (manifests) that deterministically compile different editions: full text, ritual-only, spec-only, album script, and future formats like pocket cards. constitution_repo_design_doc
 constitution_repo_design_doc

- **Validation** as civic hygiene: unique IDs, dependency checks, orphan detection, schema validation—treating the constitution like critical infrastructure rather than vibes. constitution_repo_design_doc
 constitution_repo_design_doc

- A curated **references corpus** built for both humans and LLMs: vendored texts only when licensing permits, otherwise link-stubs plus your operational notes—so the constitution can cite and think with its sources without reproducing restricted works. constitution_repo_design_doc
 constitution_repo_design_doc

- An explicit “agent-facing” layer (`AGENTS.md`) so that coding assistants and future AIs can participate without breaking invariants—making the constitution legible as _infrastructure for collaboration_. constitution_repo_design_doc

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
