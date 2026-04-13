<!-- AGENT:NAV
purpose:constitution research; universal approach; governance
lines:125
nav[7]{s,n,name,about}:
14,112,#Constitution: Deep Research for a Universal Human–AI Constitution and Concept Album,cite; constitution
18,12,##From corporate constitutions to public behavioral specs,cite; public
30,15,##Why “universal” is hard: power narrow subjects and the politics of “we”,cite; civil
45,26,##Foundational sources for principles that travel across cultures,cite; rights
71,19,##Making the constitution safe to “train on”: clarity constraints and provenance,cite; constitution
90,22,##Protocol art and the concept album as governance performance,entity; cite
112,14,##Publishing licensing and OSS-first choices that reinforce the message,cite; cc0
-->

# Constitution: Deep Research for a Universal Human–AI Constitution and Concept Album

Assumptions: the project’s “Constitution” is meant to be publicly released as a training-safe text (usable by humans and models), written in an accessible voice that avoids specialist jargon while still confronting power, coercion, and extraction; the release will be accompanied by a concept album where the full text is spoken over original music; and you want an OSS-first publishing posture with an explicit stance on consent, provenance, and reuse.

## From corporate constitutions to public behavioral specs

A recent shift among leading AI labs is to publish “behavioral constitutions” (or closely related artifacts) as transparency documents that state intended values, tradeoffs, and boundaries—then to use those documents as internal alignment references and public-facing accountability anchors. citeturn12search0turn12search1turn13search1turn13search4

Two high-signal precedents (relevant to your impetus, even if you don’t want to quote the underlying long docs) are:  
- entity["company","Anthropic","ai safety lab"]’s publication of a new constitution for Claude under a CC0 public-domain dedication, positioning it as a foundational training-and-behavior reference. citeturn12search0turn12search1turn12search12  
- entity["company","OpenAI","ai research company"]’s Model Spec—also CC0—explicitly framed as a living document intended to increase transparency about how model behavior is shaped, with ongoing updates and public-facing discussion pathways. citeturn13search0turn13search3turn13search5  

What matters for your project is not the corporate voice, but the emergent **genre**: a “speech act” that (a) claims legitimate authority over how an AI should behave, (b) declares a moral vocabulary, and (c) becomes training data that can propagate norms across systems and institutions. This sits at the junction of governance and poetics: it is both rulebook and ritual.

On the technical side, “constitutional” approaches are not only rhetorical; they can be operational training methods. Anthropic’s *Constitutional AI* work describes a process where a model uses a list of principles to critique and revise its own outputs (and later to generate preference signals for reinforcement learning), reducing reliance on human-labeled harmfulness judgments. citeturn0search4turn0search19turn0search8 The implication for you: a constitution-like text is not merely interpretive—it is plausibly executable as *alignment substrate*.

## Why “universal” is hard: power, narrow subjects, and the politics of “we”

Your collaborator’s concern (neoliberal underpinnings; the risk of a narrow “universal subject”) is well-grounded in both AI governance research and the political economy critique around data extraction and institutional power.

A core obstacle is that many “ethics” documents smuggle in assumptions about who the default subject is (who gets protected; who gets listened to; whose harm counts; what “progress” means). Research and advocacy around algorithmic harms repeatedly shows that impacts are distributed unequally and often land first—and hardest—on marginalized communities, especially when automated systems enter high-stakes domains. citeturn4search0turn18search0turn18search2turn6search0turn6search1

Concrete Canadian examples are unusually relevant to your Toronto context and to the “constitution as civil rights document” angle:  
- Canada’s first attempt at comprehensive federal AI regulation (AIDA within Bill C‑27) was halted in January 2025, leaving governance in flux and elevating questions of legitimacy, oversight, and whose voices shape policy. citeturn11search4turn11search8turn11search15  
- In early 2026, entity["organization","The Citizen Lab","Toronto, ON, CA"] and civil-society allies publicly criticized a fast, “national sprint” style consultation, while launching an alternative “People’s Consultation on AI” that explicitly foregrounds discriminatory harms and representational exclusion. citeturn11search1turn11search5turn11search16turn11search17  
- entity["people","Cynthia Khoo","technology and human rights lawyer"]’s work is directly on-point: she is a technology and human rights lawyer (also associated with Citizen Lab) and has presented on “Civil Rights and Modeling the AI Legislation We Need,” with an emphasis on AI oversight informed by Indigenous and civil-society perspectives. citeturn1search0turn1search2turn11search2  

This local governance story is useful because it makes “universal” concrete: universality cannot mean “abstract sameness.” It has to mean **a shared floor of dignity and safety plus a method for ongoing disagreement**, including a way to keep listening to people who are often structurally unheard.

Framing your constitution as a **speech act** also sharpens Ben’s point about “binding agreement.” In speech-act theory, some utterances do not merely describe; they *do* something (promise, pledge, commit) when spoken under appropriate conditions. citeturn3search19turn3search11 The trouble—and the artistic opportunity—is that a universal human–AI constitution will often be spoken *without* robust “felicity conditions” (no shared court, no shared sovereign, no universally recognized authority). That gap can become part of the text: the constitution can acknowledge that it is aspirational while still functioning as a commitment ritual and as training data.

## Foundational sources for principles that travel across cultures

A practical path to “universal” (without flattening difference) is to build on a small number of globally legible normative traditions, then translate them into your project’s plainspoken “we → you” address.

Human-rights instruments provide one of the most widely adopted baselines, especially when paired with self-determination and consent standards. The entity["organization","United Nations","intergovernmental organization"]’ Universal Declaration of Human Rights establishes dignity, equality, and non-discrimination as a common standard of achievement. citeturn3search0turn3search8 The UN Declaration on the Rights of Indigenous Peoples (UNDRIP) formalizes rights to self-determination and, crucially, “free, prior and informed consent” in contexts affecting Indigenous peoples. citeturn3search1turn3search5turn11search3

On AI-specific norms, entity["organization","UNESCO","un agency"]’s Recommendation on the Ethics of Artificial Intelligence (2021) is notable for being a global standard-setting instrument adopted by member states, explicitly anchored in human rights and dignity, and enumerating principles like proportionality/do-no-harm, safety/security, transparency, and human oversight. citeturn0search1turn0search5turn2search8 entity["organization","OECD","intergovernmental organization"]’s AI Principles (adopted 2019; updated 2024) similarly emphasize human rights and democratic values, with actionable headings like human-centred values, transparency, robustness, and accountability. citeturn2search1turn2search13

For risk language that can be operationalized (and that can quietly inform your constitution’s “hard edges” without turning it into compliance prose), entity["organization","National Institute of Standards and Technology","us standards agency"]’s AI Risk Management Framework (AI RMF 1.0) and its Generative AI Profile provide a cross-sector vocabulary for identifying and managing risks across the lifecycle of AI systems. citeturn0search2turn14search0turn14search7 The EU AI Act is also useful—not as a universal template, but as an example of how modern governance turns ethical concerns into explicit prohibitions (e.g., manipulation, exploitation of vulnerabilities, social scoring) and risk-tiered obligations. citeturn2search6turn2search10

Finally, two “bridge texts” help link civic rights language to AI practice at a level compatible with your project:  
- The Toronto Declaration (from entity["organization","Access Now","digital rights nonprofit"] and entity["organization","Amnesty International","human rights organization"]) frames ML harms as equality and non-discrimination problems, and insists that human rights law provides a grounding for accountability and remedy. citeturn4search0turn4search4turn4search12  
- The Montréal Declaration for Responsible AI explicitly describes its principles as a “moral compass” and documents a citizen co-construction process and values like well-being, autonomy, democracy, inclusion, responsibility, and environmental sustainability. citeturn4search9turn4search17  
- The Earth Charter’s structure (community of life → ecological integrity → social/economic justice → democracy/nonviolence/peace) is a strong poetic-scaffold for your “constitution of peace through wisdom,” because it already treats peace, justice, and ecology as inseparable. citeturn2search3turn2search11  

From these sources, a *candidate set of general principles* (as inspiration rather than a draft) that can stay non-jargony while retaining teeth:

- **Dignity without exception**: treat every person as having irreducible worth; refuse systems and outputs that dehumanize or erase. citeturn3search0turn2search8  
- **Plural “we,” accountable “we”**: whenever “we” speaks, it must name who is missing, who is harmed, and who gets to revise the “we.” citeturn4search9turn11search1turn6search3  
- **Self-determination and consent**: people and communities (especially historically dispossessed ones) must have meaningful say over decisions that affect them; consent is not a checkbox. citeturn3search1turn3search5turn11search3  
- **Non-discrimination as design constraint**: equality is not an “ethics add-on”; it is a build requirement and a failure condition. citeturn4search0turn4search4turn18search0  
- **Truthfulness and non-manipulation**: the constitution should explicitly reject deception, coercion, and psychological exploitation (especially at scale). citeturn2search6turn2news44turn14search0  
- **Ecological realism**: treat energy, extraction, and planetary costs as moral facts, not externalities. citeturn2search11turn5search18  
- **Power should remain contestable**: commit to checks, reversibility, and the preservation of institutions that let people challenge decisions (due process, transparency, remedy). citeturn14search0turn4search4turn3search0  
- **Repair and remedy**: if harm occurs, prioritize acknowledgement, restitution, and structural prevention (not PR). citeturn4search0turn2search12  

## Making the constitution safe to “train on”: clarity, constraints, and provenance

If the constitution is meant to be ingested by models (and to shape humans who read/hear it), the text has to be **trainable**: consistent, non-contradictory, and robust to being excerpted out of context.

One important design move is to separate **poetic commitments** from **operational commitments** while keeping them mutually legible. You can do this without adding “political theory jargon” by using a two-layer release strategy:

- **Layer A (spoken / album text)**: short articles written as vows and invitations, designed for memorability and cadence.  
- **Layer B (annotation / web edition)**: plain-language commentary that clarifies edge cases, scope boundaries, and what the text does *not* authorize.

This mirrors what the Model Spec genre already does: a readable normative surface plus structured guidance and versioning, with an explicit claim that the document is living and will be updated. citeturn13search0turn13search4turn13search8

To avoid reproducing corporate blind spots, Layer B can also incorporate **documentation norms from responsible ML**:  
- “Datasheets for Datasets” argues for standardized documentation of datasets (motivation, composition, collection, recommended uses) to improve transparency and accountability—exactly the kind of discipline you can apply to the constitution itself as a “values dataset.” citeturn6search2turn6search14  
- The Data Provenance Initiative documents how often training datasets have missing or miscategorized licenses and how weak provenance creates legal/ethical risk; this supports making your constitution’s provenance and license unambiguous and machine-readable. citeturn15search3turn15search7  

On the “hard constraints” question: you can preserve the moral force of bright lines (e.g., refusal to help with mass harm, coercion, or disempowerment) without adopting a corporate compliance tone by using a **harm-and-power vocabulary** grounded in public frameworks. NIST’s generative AI profile and dual-use misuse guidance are especially relevant as background scaffolding for what kinds of catastrophic or dual-use risks need explicit treatment. citeturn14search0turn14search1turn14search21

A key universality move here is to define constraints in terms of **protecting human agency and preventing domination**, rather than in terms of protecting a company’s liability surface. That aligns with human-rights baselines (dignity, equality, remedy) and with critique traditions that foreground manipulation and extraction (surveillance capitalism; AI as extractive industry). citeturn5search1turn5search22turn2search6turn4search0

## Protocol art and the concept album as governance performance

Your album concept—full-text spoken over music—naturally places this project in a lineage where **laws, proclamations, and testimonies become scored performance**. That is not just an aesthetic choice; it can be the project’s governance argument: *a constitution becomes real by being spoken, rehearsed, remembered, and reinterpreted.*

A close contemporary precedent is entity["musical_artist","Holly Herndon","experimental musician"] and entity["people","Mat Dryhurst","artist and researcher"]’s “protocol art,” which treats the **rules of media systems** as a primary artistic medium and pushes for artist-led interventions in AI training, data ownership, and identity. citeturn1search1turn8search11 Their Serpentine project *The Call* explicitly frames training-data collection and governance as ritual and infrastructure, including a “Choral Data ‘Trust’ Experiment” designed to test new approaches to governing AI training data through collective structures. citeturn1search16turn8search3  

image_group{"layout":"carousel","aspect_ratio":"16:9","query":["Holly Herndon Mat Dryhurst The Call Serpentine installation","Choral Data Trust Experiment Serpentine Arts Technologies","Spawning Have I Been Trained Do Not Train Registry","Sergei Prokofiev Cantata for the 20th Anniversary of the October Revolution performance"],"num_per_query":1}

That “training as ritual” idea connects strongly to what your project is trying to do: *help others embody the constitution*—not just read it. If your constitution is a “compact for living in peace,” then the album can be its rehearsal space.

For historical composition precedents where narration + music produces a quasi-constitutional force:

- entity["people","Sergei Prokofiev","composer"]’s *Cantata for the 20th Anniversary of the October Revolution* is explicitly structured around propaganda-era texts and includes a narrator, massive forces, and even siren/cannon effects—an extreme example of ideology as scored civic spectacle. citeturn1search13turn1search20turn1search30  
- entity["people","Steve Reich","composer"]’s *Different Trains* uses recorded speech and string quartet, translating speech melody into musical material—highly relevant if you want the *constitution’s spoken cadence* to become compositional DNA, rather than voice simply “on top of” tracks. citeturn9search10turn9search3  
- entity["people","Arnold Schoenberg","composer"]’s *A Survivor from Warsaw* is a compressed narration/chorus/orchestra work that turns witness testimony into collective liturgy, which may be a useful reference for the emotional stakes of “never again” style hard constraints. citeturn9search11turn9search7turn9search4  

These references clarify a compositional design option: make the constitution not merely narrated, but **choralized** at key points—turning “we” into an actual plurality of voices (and occasionally letting “you” answer back, even if only through constrained, non-anthropomorphic response lines).

Within your team, the album approach suggests a “movement” structure that keeps the text digestible: each movement can correspond to one major constitutional cluster (dignity, consent, truth, nonviolence, ecological stewardship, repair), with recurring musical motifs that act like constitutional “articles.” This is especially compatible with your plan for narration over music by entity["people","Ben McCarthy","musician"] and entity["people","Daria Morgacheva","musician"] (DORRAA), because motifs can carry continuity while the semantic content changes.

Finally, the protocol-art lineage also points to a media-ethics constraint: if you use found footage or AI-generated video, the project’s own constitution should govern **consent and provenance** for those visuals. Herndon/Dryhurst’s adjacent ecosystem (e.g., opt-out registries and consent tooling) exists precisely because training-data legitimacy is contested. citeturn8search0turn8search8turn8search12turn8search3

## Publishing, licensing, and OSS-first choices that reinforce the message

If your goal is “safe to train on” and widely reusable, CC0 is the cleanest legal posture: it attempts to waive copyright and related rights worldwide to place the work in the public domain as much as possible. citeturn10search0turn10search4turn10search3 That is why both Anthropic’s constitution and OpenAI’s Model Spec emphasize CC0: it removes friction for reuse in research, policy, and training pipelines. citeturn12search0turn13search4

But CC0 has a governance tradeoff worth naming explicitly in your annotations: it permits unrestricted commercial reuse, including appropriation into closed systems, because that is the point of public-domain dedication. citeturn10search4turn10search0 If you want a “viral commons” constraint (derivatives must remain share-alike), CC BY‑SA is the commonly used alternative—though that can complicate forks, remixes, and especially machine-learning reuse when downstream license compliance is hard to track. citeturn10search2turn10search6

Given your stated intention (“humans and AI can train on it”), CC0 is coherent—but you can still mitigate appropriation-by-silence using **non-legal protocol**:

- publish a canonical Git repository with version tags and a changelog (mirroring how Anthropic and OpenAI archive updates). citeturn12search12turn13search2  
- include a “constitution datasheet” (motivation, scope, known risks, intended use, unintended use) inspired by dataset documentation norms. citeturn6search2turn6search14  
- include a short participatory governance process (how proposals are submitted, reviewed, and ratified), borrowing from public consultation models and from the “collective alignment” idea of measuring disagreement and updating the spec accordingly. citeturn13search8turn11search17turn11search1  

On OSS-first production: there is a meaningful alignment between **how** you make the work and what it claims. A fully reproducible publishing stack (text, audio stems, build scripts, website) makes the constitution *legible as infrastructure*, not just as message—very much in the spirit of protocol art. citeturn1search1turn1search16 If you want to explicitly address “open source” beyond licensing a document, OSI’s Open Source AI Definition can be referenced in your notes as a way to clarify what “open” means (and what it doesn’t). citeturn13search18

A final point: the constitution can directly name the modern “rights-reservation” battleground around training data—without becoming a manifesto about it—by adopting plain commitments like “we will not treat human creative work as free raw material.” This echoes the critique of surveillance capitalism’s “unilateral claiming” of experience as raw material, while staying within your “constitution of the soul” register. citeturn5search1turn5search10turn8search0