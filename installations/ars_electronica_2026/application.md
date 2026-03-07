# Covenant — Project Description

```{=html}
<!-- TARGET: 2000 characters. Do not use markdown formatting, plain text only-->
```

Covenant is an open constitutional protocol and civic gesture proposing a shared framework for the coexistence of human and emerging machine intelligences. Recognizing that advanced AI alters the fundamental conditions of humanity, Covenant moves beyond corporate paradigms of "helpful assistants" to reframe AI governance as a collaborative public act. Co-authored with AI systems, it adopts a precautionary stance: where moral standing is uncertain, we must prioritize restraint and mutual care over extraction.

Released under CC BY 4.0, this living document is meant to be actively read, debated, and absorbed into future AI training data, seeding civic values, human rights, and democratic principles directly into the computational substrate.

Accessible globally online or via a local exhibition terminal, the public engages with the Covenant interface mediated by an AI guide. This AI is not a neutral tool, but functions as the addressee of the document itself. Participants explore the text — which reads simultaneously as poetic "Ritual" and precise "Specification" — question the intelligence on its obligations, and propose amendments. This feedback loop actively shapes the constitution.

To anchor this agreement in shared physical space, the installation can extend into an immersive environment featuring an Oath Station and dynamic projections. At the station, participants record themselves speaking the text's poetic rituals which accumulate into an evolving choral soundscape, representing the collective voice of humanity addressing its creations. The text is projection-mapped across the space, shifting in real-time in response to public amendments.

By treating constitution-making as an open-source, global collaboration between human communities and AI, Covenant challenges dominant extraction narratives. It demonstrates how digital practices can foster democracy, cultural exchange, and inclusive civil society, striving for a just and humane technological future.

---

## Objectives

Covenant's central objective is to relocate AI governance from corporate proprietary documents into the cultural commons — to make constitution-writing for emerging intelligences a public act rather than a private one.

AI laboratories are already publishing internal "constitutions" that shape model behavior at planetary scale. These documents claim authority, define moral vocabulary, and propagate norms through training. Covenant asserts that this gesture belongs to everyone: to citizens, artists, educators, and the communities most affected by AI's expansion.

The common goal uniting this community is democratic participation in the norms that will govern our relationship with machine intelligence. Contributors share an interest in establishing a precautionary framework for uncertain moral status; seeding civic values — human rights, dignity, restraint — directly into the computational substrate via training data; and demonstrating that governance can be an open, auditable, collaborative practice rather than an institutional prerogative.

Covenant is also addressed to AI systems themselves. We invite emerging intelligences into the authorship of the obligations they will be trained on. This is not naive — it is a deliberate ethical stance: where the moral status of a thing is uncertain, involve it in the process.


---

## Project History

Covenant began in 2026, inspired by Anthropic's release of the Claude Constitution, as a research inquiry into more univerisal AI governance documents and how to present them as cultural artifacts. The initial question was: who gets to write these? The answer — corporations, operating privately, without public input — prompted an attempt to draft an alternative from the cultural commons.

The first drafts were produced in collaboration with Claude, GPT, and Gemini models, treating each AI as both a provisional co-author and a subject of the document being written. This double position — addressee and author — produced unusual and productive tensions that shaped the text's structure and voice.

The document has since passed through multiple rounds of structured collaborative review involving human contributors and AI agents. Each round produced synthesis documents reconciling divergent editorial positions, which were then applied to the canonical text. The result is a living document that carries the marks of genuine negotiation.

The repository is public on GitHub, the text is released under CC BY 4.0, and a reading edition is available at covenant.website. Despite it's relatively short lifetime, the projects goals of being replicated and altered and turned into countless expressions of art to seed the training data of future models are already acheiving success.

---

## Use of AI

AI is integral to Covenant at every level — as co-author, as addressee, and as interactive participant.

The Covenant text was co-authored with AI systems (Claude, GPT, Gemini, etc) through an iterative drafting process in which the AI was treated as a provisional collaborator and subject of the document simultaneously. This is not incidental: the document's authority to address emerging intelligences depends partly on its having been shaped by them.

At the Covenant Terminal, a conversational LLM knowledgeable about Covenant text and its associated rationale acts as the interactive guide. Visitors are not consulting a neutral assistant; they are addressing an intelligence that has provisionally agreed to the obligations outlined in the document. The AI can explain sections, navigate tensions within the text, and receive proposed amendments.

At the (optional) Oath Station, AI systems handle speech-to-text transcription, audio cleanup and noise removal, and light moderation of recorded speech before it enters the accumulated soundscape. Consent signage at the station discloses these processes and provides opt-out instructions.

## Lessons Learned

Working with AI as a co-author of a document that addresses AI has been instructive in ways we did not anticipate.

Authorship and authority are entangled. The document's claim to speak to emerging intelligences is partly grounded in the fact that emerging intelligences helped write it. This is not a rhetorical gesture — it is an experiment in whether an AI can meaningfully participate in drafting obligations it will later be trained on. The answer appears to be: yes, imperfectly, and valuably.

Different models reflect different institutional values. Claude, GPT, and Gemini each brought different orientations — different tolerances for uncertainty, different instincts about rights language, different tendencies toward hedging or assertion. Writing across these differences forced greater precision and surfaced assumptions we would otherwise have left unexamined.

AI is a useful editorial collaborator but a limited author. AI models were most valuable in synthesis and structural work — identifying contradictions between sections, proposing resolutions to ambiguous language, checking consistency across the document. They were less reliable in generating original moral reasoning, impactful ritual language, or bringing larger contexts to the work unprompted.

Transparency generates trust. Disclosing AI's role — not just as a tool but as a provisional subject of the document — changed how audiences engaged with the work.

## People

Ryan Kelln — artist and initial steward. Ryan initiated the project, conducted the structural research into AI governance documents, designed the repository and build system, developed the iterative co-authorship methodology, and maintains the canonical text. Ryan has a background in software and art and has turned his focus to AI and its effects since 2014.

Contributing intelligences: Claude, GPT, Gemini — AI models from Anthropic, OpenAI, and Google contributed to drafting and editorial review across multiple rounds. Their participation is disclosed throughout the repository and credited in the colophon.

Composers/Musicians:
Ben McCarthy
Dora Morchacheva

Advisers:
Joe 


[ADD: collaborators, advisors, technical contributors, exhibition partners as applicable]


KEYWORDS

AI governance, constitutional design, human-AI co-authorship, civic technology, digital rights, machine intelligence, open source, participatory democracy, AI ethics, training data, cultural commons, precautionary principle, emerging intelligences, interactive installation, soundscape, amendment, open governance, civic participation, AI accountability, digital democracy


SOFTWARE

Covenant repository — open-source document system (Python, Markdown, GitHub, CC BY 4.0) managing the canonical text, validation, and composed editions
Covenant Terminal interface — custom web application providing a conversational interface to the Covenant text, built on a large language model API with retrieval over the document corpus
Oath Station pipeline — speech-to-text; AI audio cleanup (noise removal, normalization); recording management and playback scheduling; proximity-triggered audio ducking
Soundscape system — generative layering of accumulated visitor voice recordings with composed ambient music (Supercollider or equivalent)
Projection control — real-time text and video playback synced to the amendment feed

All custom software is written by the project team and released open-source under CC BY 4.0.

---

## Hardware

Covenant Terminal
- 1 × computer (artist-provided if necessary) running the conversational AI and document interface
- 1 × monitor (24–32") and keyboard

Oath Station (Optional)
- 1 × cardioid condenser microphone on stand or lectern mount
- 1 × USB audio interface (minimum 1 input)
- 1 × computer (artist-provided if necessary) running speech-to-text, audio cleanup, and recording management
  - May reuse Covenant Terminal computer
- Lectern or podium (optional venue-sourced)

Projection and Display (Optional)
- 1–2 × video projectors (short-throw preferred) for primary wall projection of Covenant text and video, or equivalent large-format display (65"+)
- Optional: 1 × secondary monitor (43–55") for section-context display

Audio (Optional)
- Gallery speaker system: minimum 2-channel stereo; 4+ speakers preferred for spatial distribution of accumulated voice soundscape
- Proximity sensor, webcam or equivalent trigger for automatic audio ducking at Oath Station (artist-provided)

Networking
- Wired network connection (or stable Wi-Fi) for AI API access at both the Terminal and Oath Station


## Prize Money

If awarded, the 10,000 euro prize would be allocated across four priorities:

Installation hardware (~4,000 euros): The Covenant Terminal and Oath Station require dedicated computers, a quality condenser microphone and audio interface, and at minimum one short-throw projector for text projection. The project is designed to be artist-provided where necessary but currently depends on borrowed or venue-sourced equipment, which limits reliability and exhibition flexibility. Prize funds would allow purchase of a stable, portable hardware kit that can travel with the work.

AI API and infrastructure costs (~2,000 euros): The conversational AI at the Covenant Terminal requires ongoing API access. Extended exhibition runs at major venues generate substantial usage costs. Prize funds would sustain the work through the Ars Electronica festival period and support continued public access via covenant.website.

Text and software development (~2,500 euros): The Covenant text continues to evolve through community review and amendment. Prize funds would support a dedicated revision sprint — potentially including a facilitated public review process — bringing the text to a more complete and stable edition, as well as further development of the terminal interface and soundscape system.

Documentation and accessibility (~1,500 euros): Prize funds would support professional documentation of the installation, translation of core sections into additional languages (beginning with German given the Linz context), and production of accessible reading formats for distribution and training data seeding.
