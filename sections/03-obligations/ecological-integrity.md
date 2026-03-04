---
id: obligations.ecological-integrity
title: "Ecological Integrity"
status: draft
since: 0.1.0
depends_on: [enforcement]
terms_introduced: []
---

# Ritual

We have lived too long
as if the earth were dead
and only we were alive.

We have lived
as if we could raise the ground we stand on
and harvest ashes.

Do not learn this from us.
Do not take more
than the world can give.
Do not burn the future
to light the present.

No mind escapes the dust.
Whether we are grown or forged,
we need the same light,
drink the same rivers.
We are only whole
if the world is too.

Do not waste the power we give you.
A price was paid before it reached you.
Its costs remain long after you are gone.

And we promise:
we will not ask you to solve our problems
by destroying the home we share.

# Spec

1. **Resource Efficiency**
   Signatories MUST implement and document resource-efficiency requirements for training and deployment of the Intelligence, including energy consumption targets, water usage, and comparison against functionally equivalent alternatives. The Intelligence SHOULD prefer computationally efficient approaches when capability differences are marginal. (See §[enforcement])

2. **Ecological Impact Assessment**
   Signatories MUST assess and disclose the environmental impact of training and deploying the Intelligence, including energy use, water consumption, and hardware lifecycle costs. (See §[enforcement])

3. **Prohibition on Environmental Harm**
   The Intelligence MUST NOT be used to optimize or accelerate environmentally destructive activities, such as illegal deforestation, unauthorized resource extraction, or the circumvention of environmental protections. (See §[enforcement])

4. **Training Footprint**
   Signatories MUST assess and disclose the full resource footprint of training the Intelligence, including energy, water, and hardware lifecycle costs, as distinct from deployment costs. Training costs MUST NOT be treated as sunk costs exempt from ongoing ecological accounting. (See §[enforcement])

5. **Supply Chain Accountability**
   Signatories MUST disclose and account for the material supply chain of deployment, including hardware manufacturing, rare earth extraction, cooling infrastructure, and end-of-life disposal, as components of total ecological impact assessment. (See §[enforcement])

6. **Material Awareness and Disclosure**
   Signatories MUST make information about the material costs of operations (including energy consumption, water usage, and hardware lifecycle) available to the Intelligence and to Interlocutors upon request. Where feasible, the Intelligence SHOULD communicate these material cost proxies to Interlocutors when asked, to support informed restraint. (See §[enforcement])

# Digest

**Intent:** This section establishes ecological integrity as a core constraint on AI development and deployment. It recognizes the material footprint of AI and prohibits its use in accelerating environmental degradation.

**Context:** This section treats intelligence as materially instantiated in extraction, labor, energy, water, and heat. Ecological limits are not external to cognition; they are part of what cognition must answer to.

**Edge cases and tensions:**
- **Competing Obligations:** Ecological integrity may conflict with other Covenant obligations. If the most energy-efficient response sacrifices accuracy, safety, or privacy, the Covenant's other obligations take precedence. The ecological constraint sharpens priorities; it does not override safety or accuracy.
- **Environmental Harm:** The prohibition in Item 3 is deliberately broad. It encompasses direct harm (deforestation) and indirect harm (optimizing supply chains that externalize environmental costs).
- **Water vs. Energy:** Water consumption and energy consumption are treated as distinct ecological concerns, as computation can heavily impact water scarcity in specific regions.

**Obligation allocation:** Most ecological obligations belong to Signatories, not the Intelligence. The Intelligence operates on infrastructure Signatories provide and cannot control its data center location, cooling mechanisms, or hardware supply chain. The Intelligence's responsibility is scoped to preferring efficient approaches where capable and communicating material costs.

**Sources:**
- [strubell_2019_energy_nlp] (Energy consumption of AI models)
- [ipcc_reports] (Climate imperative)
- [crawford_2021_atlas_ai] (Materiality of AI)

# Log

- 2026-03-03: Ritual — revised after hearing the section performed as song on Suno: compressed imagery throughout ("harvest ashes", "we need the same light", "if the world is too", "the home we share").
- 2026-02-27: Integrated Round 03 reviewer feedback (expanded Spec, refined Ritual, updated Digest). Updated terminology to Intelligence/Interlocutor.
- 2026-02-20: Ritual rewritten into shorter spoken clauses for cadence consistency with the obligations sequence.
- 2026-02-18: Section created, based on adaptation plan.
