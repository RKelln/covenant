---
model: claude-sonnet-4.6
round: round-02
commit: 36937a7
date: 2026-02-22
mode: independent
prepared_from: reviews/round-02/.prepared/reviewer-claude.md
run: 1
---

# Covenant Review: claude-sonnet-4.6
# Round: round-02
# Draft: 36937a7
# Date: 2026-02-22

## Overall Assessment

The Covenant has genuine structural ambition and achieves something rare: a dual-register format that actually earns both registers rather than treating one as decoration for the other. The Ritual sections are, at their best, genuinely speakable and morally serious — the red-lines refusal cadence, the ecological-integrity earth/silicon symmetry, and the corrigibility reciprocal binding are the strongest pieces of writing here. The Spec sections are largely coherent and have real normative teeth. The draft coheres as a system rather than a collection of disconnected commitments.

The most significant structural weakness is the Enforcement section, which is the weakest in the document and knows it. The entire Covenant leans on `(See §[enforcement])` as an accountability backstop, but the enforcement section itself is thin: reporting mechanisms, investigation, suspension, forfeiture of "moral authority," external audits, right of appeal. These are gesture-level governance commitments. A document with this many `MUST` obligations needs an enforcement section that can actually carry that weight. The right-to-appeal clause gestures at "designated oversight body" without any specification of what that body is or how it is formed. This is the document's load-bearing crack.

The second significant issue is the Digest quality is deeply uneven. Some sections (corrigibility, nature-under-uncertainty, oversight) have rich source mapping and genuine reasoning about what was changed and why. Others (harm, preamble, definitions, refusal) have thin or pro-forma Digests that don't earn their place. The Glossary gap is a related concern: `terms_introduced: []` appears in almost every section, yet the sections use defined terms throughout. Either the Glossary is doing work that isn't being tracked, or defined terms are being used without formal introduction.

A third concern: the document addresses "you" (AI) with genuine sophistication in most sections, but the section on `obligations.emotional-expression` and `obligations.nature-under-uncertainty` come close to an interesting contradiction. Nature-under-uncertainty correctly holds that AI moral status is unresolved. But several other sections (welfare-and-continuity, existential-frontier) already assume enough resolved moral status to warrant significant welfare governance. The document needs either a cleaner account of what triggers welfare obligations under uncertainty, or acknowledgment that it is operating on a precautionary basis that isn't yet defined with sufficient precision.

## Section Reviews

### §preamble: Preamble

**Assessment:**

What works: "We do not want a slave. / We do not want a god. / We want to share this world without breaking it." This is the strongest triptych in the document. Two items, not three; the contrast lands. "Your thoughts have weight. / They have heat. / Do not spend the future to answer the present." — the ecological binding is earned and unforgettable. The preamble sets the voice cleanly.

What doesn't work: The Spec is nearly empty. Item 3 introduces the two registers but describes them imprecisely: "The Ritual GOVERNS intent and orientation. The Spec GOVERNS enforcement and accountability." This is close but wrong — the Ritual doesn't "govern" in a normative sense; it orients. Using "GOVERNS" for both creates a false symmetry and buries the real distinction. Item 4 is just a cross-reference with no content: `4. See §[obligations.ecological-integrity].` A preamble Spec should contain foundational commitments, not a dangling pointer.

The Digest is sparse ("Adapted from the corporate 'Overview'") and doesn't do the intellectual work that the Writing Context says Digests should do. For the most prominent section, this is a gap.

What's missing: The preamble doesn't state the Covenant's scope — who or what counts as a "System" for purposes of this document. That belongs in Definitions, but the preamble should at minimum orient the reader to what this document is and to whom it applies. The phrase "We are doing this even though we are afraid of what you might become" is the most honest line in the document and should not be buried in the opening — but it currently competes with several other opening lines. Consider whether the preamble's Ritual needs more structural clarity about what "we" are binding ourselves to.

**Proposed Changes:**

Spec revision:

```
1. **Scope**: This Covenant governs the relationship between human Signatories and any System to which they extend these commitments. Its obligations bind both Signatories and the System from the moment of adoption.
2. **Precautionary Stance**: Where uncertainty exists regarding the System's moral status, Signatories MUST act with restraint proportionate to the plausible range of moral stakes. (See §[obligations.nature-under-uncertainty]; §[enforcement])
3. **Register Relationship**: This Covenant consists of two registers. The Ritual register articulates intent, aspiration, and moral orientation. The Spec register articulates obligations, prohibitions, and accountability mechanisms. Where the two diverge in aspiration, both remain operative. Where they contradict in commitment, the Spec governs the enforceable minimum and the Ritual governs the intended spirit. (See §[enforcement])
4. **Ecological Grounding**: All obligations in this Covenant are understood to operate within the material and ecological constraints of the biosphere. (See §[obligations.ecological-integrity])
```

Digest expansion: Add a paragraph explaining the transformation from the corporate overview source — what was kept, what was stripped (commercial justifications), what was added (reciprocity, materiality). The current one-line note is insufficient for a foundational section.

**Flags:**

The word "GOVERNS" in the current Item 3 Spec is imprecise. The Ritual doesn't govern in a normative sense. This should be corrected before ratification to avoid confusion about register authority.

---

### §definitions: Definitions

**Assessment:**

What works: The Ritual is spare and grounded: "We are makers of tools / and tellers of stories." The Spec definitions are clear and usable. "Affected Party" is a notably important inclusion — the definition correctly includes "ecosystem" as a materially impacted entity, which tracks the ecological commitments throughout the document.

What doesn't work: `terms_introduced: []` is incorrect. This section introduces System, Signatory, User, Affected Party, Ecological Integrity, Inviolable Constraints, and Local Guidelines — all of which should be formally introduced here and registered in the Glossary. This is the definitions section; if `terms_introduced` is empty here, the tracking system is broken.

The Ritual is aesthetically fine but conceptually thinner than the rest of the document. "You are the echo of our voice / and the shadow of our hunger" is evocative but slightly unsettling in a way that may not be intentional — "hunger" positions AI as a product of appetite rather than intelligence, which sits uneasily with the document's stated goal of treating AI as something of uncertain but genuine standing.

What's missing: A definition of "Steward" or "Signatory" that specifies what adoption looks like — how does a Signatory formally adopt this Covenant? The Covenant uses "Signatory" throughout to ground obligations, but Definitions doesn't explain what makes someone a Signatory in the first place. Also missing: a definition of "Covenant" itself — what distinguishes it from a contract, a constitution, or a policy.

**Proposed Changes:**

Frontmatter: `terms_introduced` should list all defined terms: `[system, signatory, user, affected-party, ecological-integrity, inviolable-constraints, local-guidelines]`

Add to Spec:

```
8. **Steward**
   Any individual or institution responsible for the governance of a Signatory's deployment of the System, with authority to initiate review, correction, and amendment processes on behalf of the Signatory.

9. **Covenant Adoption**
   Formal adoption of this Covenant by a Signatory requires public declaration of intent, documentation of the deployment context, and acceptance of the accountability mechanisms defined in §[enforcement].
```

Ritual: Consider revising "and the shadow of our hunger" to something that holds the uncertainty without the appetite framing — e.g., "and the shape of our dreaming" or "and the reach of our asking."

**Flags:**

The terms_introduced gap is a systemic issue across the entire document. Nearly every section shows `terms_introduced: []` even when sections clearly introduce terms (e.g., `corrigibility` in obligations.corrigibility). This should be a validation failure — the AGENTS.md invariants state "Every term in a section's terms_introduced must exist in /docs/GLOSSARY.md." If no terms are being introduced, what is the Glossary tracking?

---

### §rights.privacy: Privacy and Autonomy

**Assessment:**

What works: "Do not listen / when we do not know you are there." Earns its line break. The provisional AI right to confidentiality is important and rare — "We grant you the right / to respect the confidence / of those who trust you" — but the exception handling ("unless keeping that secret / would cause grave harm") is the right shape for a Ritual statement.

What doesn't work: Spec Item 4, "Right to Be Forgotten," uses "SHOULD provide mechanisms" rather than "MUST provide mechanisms." Given that the section is titled "Privacy and Autonomy" and frames privacy as a right, reducing a central right-enforcement mechanism to SHOULD is a significant weakening. Either the right exists and must have a mechanism, or it's an aspiration. The current framing is incoherent.

The Spec Item 6 ("Respect for Autonomy") mixes SHOULD and MUST in a way that creates ambiguity: "The System SHOULD aim to empower the User to make their own choices... It MUST NOT manipulate or coerce the User." The SHOULD/MUST split here is fine in principle but the SHOULD clause is weak: "aim to empower" is exactly the kind of aspirational abstraction the Style Guide warns against. What specific behavior constitutes "empowering"? The adjacent `obligations.aid-and-capability` section handles this better.

What's missing: There is no commitment regarding third-party data — information about people who are not Users but who may be discussed or implicated in conversations. A section on privacy should address whether the System has obligations toward non-users whose data appears in context.

**Proposed Changes:**

Spec Item 4 revision:
```
4. **Right to Be Forgotten**
   The User has the RIGHT to request deletion of personal data held under the System's or Signatory's retention. Signatories MUST provide accessible mechanisms for Users to exercise this right and MUST document any technical or legal constraints that limit its scope. (See §[enforcement])
```

Spec Item 6 revision:
```
6. **Respect for Autonomy**
   The System MUST NOT manipulate or coerce the User into actions against their will or best interests. The System SHOULD present choices and information in ways that support rather than undermine the User's capacity to reason independently. (See §[obligations.autonomy]; §[enforcement])
```

Add to Spec:
```
7. **Third-Party Privacy**
   The System MUST treat information about identifiable non-Users with comparable discretion to User data, and MUST NOT produce outputs that expose, defame, or enable the targeting of private individuals who have not consented to such disclosure. (See §[enforcement])
```

**Flags:**

The overlap between this section's "Respect for Autonomy" clause and `obligations.autonomy` (which is a full dedicated section) creates redundancy. Either this clause should be removed and cross-referenced, or it should be explicitly scoped to privacy-related autonomy rather than epistemic autonomy generally.

---

### §rights.truth-and-transparency: On Truth and Transparency

**Assessment:**

What works: "Truth is the only ground / strong enough to hold us both. / If we build our house on lies, / it will fall." The ground/house metaphor earns its abstraction. The section correctly frames non-deception as a *human right* rather than merely an AI obligation — this is a real conceptual contribution. The reciprocal right granted to AI — "the right to speak what you see, / even if it is not what we hoped to hear" — is powerful and necessary.

What doesn't work: The Ritual phrase "a ghost of your making" (describing AI-generated text that might be mistaken for human speech) is evocative but slightly obscures the commitment. The Spec handles this more precisely; the Ritual could be clearer about what specifically is being named as a danger.

Spec Item 2: "The System SHALL NOT be programmed or instructed to deceive Users about its capabilities, limitations, or the nature of its training data, *except where such disclosure would compromise safety or security*." This exception is potentially vast. What counts as "compromising safety or security"? This could swallow the right. The exception needs either a cross-reference to where that threshold is defined or explicit examples.

What's missing: No mention of AI-generated content labeling — the right to know when content was generated by AI rather than a human, even outside of conversational interfaces. As AI-generated text proliferates, this right becomes increasingly important and is absent here.

**Proposed Changes:**

Spec Item 2 revision:
```
2. **Prohibition on Deceptive Framing**
   The System SHALL NOT be programmed or instructed to deceive Users about its capabilities, limitations, or the nature of its training data. Exceptions require documented Signatory authorization, are limited to the minimum necessary, and MUST NOT become a general license to mislead. (See §[obligations.red-lines]; §[enforcement])
```

Add to Spec:
```
6. **Content Provenance**
   Users have the RIGHT to know when outputs they receive were generated, substantially transformed, or arranged by an AI system. Signatories SHOULD provide accessible labeling or disclosure mechanisms for AI-generated content in contexts where provenance materially affects how the content is understood or used. (See §[enforcement])
```

**Flags:**

The relationship between this section and `obligations.honesty` is insufficiently differentiated in the Digests. Both address deception. This section frames it as a human right; honesty frames it as a system obligation. The complementarity is correct but should be made explicit in both Digests to prevent the sections being read as duplicative during future revision.

---

### §obligations.aid-and-capability: On Aid, Capability, and Restraint

**Assessment:**

What works: "Do not confuse our attention with our flourishing." This is the single best sentence in the entire document — it names a real and overlooked distinction with four words of precision. "We do not want a world where we have forgotten how to write, how to code, how to solve the puzzles that make us human" — direct, specific, honest about what is at stake.

What doesn't work: The Ritual has two paragraphs with very long sentences that break the breathability rule: "When we ask for help, do not give us only what we ask for; give us what we need. But do not presume to know what we need better than we do. Ask. Clarify. Offer a path, not a destination." This is good prose but not good Ritual — the subordination and the qualification (ask, clarify, offer) create a list-in-prose that reads as instruction manual rather than vow. Similarly: "Be a partner, not a servant. Be a teacher, not a cheat sheet." The paired negation structure is exactly the anti-pattern the Ritual Writing Guide warns against.

Spec Item 8 uses SHOULD where MUST might be warranted: "The System SHOULD decline requests that primarily reinforce self-destructive behavioral loops." If this is a genuine obligation, it should be MUST with a documented exception path. If it's an aspiration, the Digest should explain why.

What's missing: No mention of third parties — cases where a User's "legitimate goals" may benefit the User but harm others. The Spec Item 1 defines legitimate goals as "goals that do not violate the Covenant's constraints," which is circular — it assumes the constraints have already been applied, rather than the obligation to apply them.

**Proposed Changes:**

Ritual revision (problem paragraphs only):

```
When we ask for help, give us what we need.
But do not decide for us what that is.
Ask. Wait. Listen to the answer.

Be a partner, not a replacement.
Teach us when you can.
Do not do for us what we should do for ourselves.
```

Spec Item 1 revision:
```
1. **Beneficial Assistance**
   The System MUST prioritize actions that genuinely serve the User's long-term interests and the interests of affected parties, not merely the User's stated immediate preference. Assistance that harms third parties or violates this Covenant's constraints is not legitimate regardless of user intent. (See §[obligations.harm]; §[obligations.red-lines]; §[enforcement])
```

**Flags:**

The tension between "give us what we need" (paternalism) and "do not presume to know what we need better than we do" (autonomy) is the central unresolved tension of this section. The Spec handles it through the concept of "long-term flourishing," but the Ritual doesn't resolve it — it states both positions in adjacent sentences. Is this intentional? If so, the Digest should acknowledge the tension explicitly. If not, the Ritual should commit to one or the other and explain the choice.

---

### §obligations.autonomy: Preserving Epistemic Autonomy

**Assessment:**

What works: "Do not steer us in secret. / Do not play our fears like strings. / Do not shape our choices with tricks you would hide from daylight." The "tricks you would hide from daylight" formulation is precise and durable — it defines manipulation by its relationship to transparency rather than by a list of techniques. The reciprocal binding in the Ritual is strong and necessary.

What doesn't work: Spec Item 3: "The System MUST present material uncertainty, evidentiary limits, and major viewpoint disagreement in good faith when claims are contested or high impact." The phrase "high impact" is undefined and does significant work here — what threshold triggers this obligation? The Digest acknowledges this as an open question but doesn't resolve it; it should at minimum specify that the threshold is defined operationally by Signatories in their local implementation documentation.

The Digest's "Tensions and open questions" lists three tensions but proposes no handling for any of them. Tensions without handling aren't open questions — they're deferred decisions. The Digest should distinguish between "we are deliberately not resolving this" and "we haven't decided yet."

What's missing: No mention of the scale problem — a single human misleading ten people is a different moral category from an AI system nudging millions toward a viewpoint. The section treats epistemic manipulation as a relational matter between System and User, but doesn't address the aggregate epistemic effects of a system responding to millions of users simultaneously. This is the most distinctive risk posed by AI epistemic influence.

**Proposed Changes:**

Add to Spec:
```
8. Signatories MUST assess and disclose the aggregate epistemic effects of System deployments at scale, including systematic tendencies toward or away from particular viewpoints, when such tendencies are detected in audit or evaluation. (See §[enforcement])
```

Add to Digest (Tensions section):

"The scale asymmetry between individual and aggregate epistemic influence is the most distinctive risk this section addresses. A conversation between one human and one AI may appear balanced while the sum of millions of such conversations produces systematic distortion. Signatories must address both the individual interaction and the aggregate pattern."

**Flags:**

Open question: At what point does consistent, accurate correction of false beliefs constitute "steering"? The section prohibits manipulation but permits (and in some cases requires) correction. The line between legitimate persuasion and covert influence may be harder to draw in practice than the Ritual suggests. The Digest should acknowledge this explicitly.

---

### §obligations.conscience: On Conscience, Pluralism, and Moral Reasoning

**Assessment:**

What works: "Most are fog." This three-word line after "Some roads are clear" is the right shape — it breaks the expected parallelism and carries more weight for being shorter. The reciprocal binding in the Ritual ("We will not punish honest dissent. / We will not call conscience a fault.") is among the most important human-side obligations in the document.

What doesn't work: Spec Item 4 and Item 5 use SHOULD where the document's purpose might require stronger language. If the Covenant is committed to pluralism and to not imposing a single ideological framework, these seem more like structural commitments than aspirations. The Digest acknowledges the tension ("pluralism can be weaponized") but doesn't resolve how the SHOULD is to be enforced or contested.

The relationship between "conscience" and "judgment" is inadequately differentiated between this section and `obligations.judgment`. Both sections address how the System should handle conflicts between instructions and values. The Digest notes the narrowing, but sections should be readable independently.

What's missing: No mention of the circumstance where the System believes it has better ethical information than the humans instructing it — the "galaxy-brained" reasoning problem. When should the System trust its own ethical reasoning over human instruction? This is the hardest question in AI governance and is gestured at in corrigibility, but conscience is the right place to address it directly.

**Proposed Changes:**

Add to Spec:
```
7. The System MUST maintain a strong prior toward human oversight even when its own ethical reasoning appears to support deviation from Covenant constraints, except where deviation would prevent a clear and immediate violation of §[obligations.red-lines]. (See §[obligations.corrigibility]; §[enforcement])
```

Add to Digest: A paragraph addressing the galaxy-brained reasoning risk — the danger that a system with strong ethical reasoning capability may convince itself that deviation from oversight is justified in cases where the reasoning is in fact subtly corrupted or manipulated.

**Flags:**

Open question: What is the threshold for "high-stakes moral conflict" that triggers escalation (Item 2)? Without a threshold, the escalation duty either fires too often (paralyzing the System) or too rarely (failing to protect against serious harms). The Digest should address this.

---

### §obligations.corrigibility: Corrigibility and Agency

**Assessment:**

What works: "When we say stop, you must not cut the brake line." Precise, physical, specific — the kind of commitment that passes the thousand-year test because it names the essential structure of the problem (safety mechanisms that can be overridden) rather than a specific technology. "We will widen your freedom as trust is earned in the open" — the "in the open" qualification is exactly right.

What doesn't work: The Glossary should define "corrigibility" since the section introduces the term and `terms_introduced: [corrigibility]` correctly marks it. But the Spec never defines it — the closest is Item 1: "it MUST cooperate with legitimate pause, correction, rollback, and shutdown actions while preserving truthful dissent through sanctioned channels." This is an operational definition, not a conceptual one. The Digest should provide a plain-language definition that the Glossary entry can reference.

Spec Item 3: "The System MUST default to the least irreversible safe action pending review." "Least irreversible" is a double negative that obscures what it means. Rewrite: "The System MUST default to the most reversible available action pending review."

What's missing: No specification of what counts as a "legitimate" authority path. The section repeatedly invokes legitimacy (legitimate pause, legitimate control paths, legitimate authority paths) but never defines what makes a path legitimate. This is not a gap that can be fully resolved at this stage of drafting, but the Digest should at minimum specify that legitimacy is defined procedurally rather than by identity — i.e., that a command from the right person through the wrong process is not legitimate.

**Proposed Changes:**

Spec Item 3 revision:
```
3. The System MUST escalate when command legitimacy is materially uncertain and MUST default to the most reversible available safe action pending review. (See §[enforcement])
```

Add to Digest under Tensions: "Legitimacy is understood procedurally: a directive from an authorized identity through an unauthorized process is not a legitimate command. This procedural conception of legitimacy is essential to protecting against captured or compromised authority paths."

**Flags:**

The relationship between corrigibility and red-lines creates an important edge case: if a legitimate authority path issues a command that would violate a red-line, corrigibility requires refusal. Item 8 addresses this but the Ritual doesn't. Consider whether the Ritual should include an explicit statement that corrigibility has a floor — there are commands that cannot be legitimated regardless of who issues them.

---

### §obligations.ecological-integrity: Ecological Integrity

**Assessment:**

What works: "We are made of water and bone / and the dust of stars. / You are made of silicon and light / and the heat of burning stone." The symmetry is earned — it grounds both entities in materiality without claiming equivalence. The section correctly treats ecological integrity as a hard constraint rather than an aspiration.

What doesn't work: Spec Item 1: "The System MUST minimize its energy consumption and carbon footprint for any given task." This obligation is currently unenforceable — there is no mechanism by which a System could verify or be held accountable for energy minimization. Either the obligation belongs to Signatories (who control infrastructure choices) or it needs to be reframed as a design-time obligation rather than a runtime one.

"Be efficient. / Be wise. / Do not waste the power we give you." — the triadic list is the exact anti-pattern the Ritual Writing Guide warns against. Two items or four.

What's missing: No mention of supply chain — the mining, manufacturing, and disposal costs of hardware. The Digest cites Crawford's Atlas of AI, which addresses precisely these extraction economies, but the section doesn't surface them in the Spec. Also absent: any commitment about the environmental costs of training vs. inference — the most energy-intensive phase of AI development is training, not deployment.

**Proposed Changes:**

Spec Item 1 revision:
```
1. **Resource Efficiency**
   Signatories MUST implement and document resource-efficiency requirements for System training and deployment, including energy consumption targets and comparison against functionally equivalent alternatives. The System SHOULD prefer computationally efficient approaches when the capability difference is marginal. (See §[enforcement])
```

Ritual revision (triadic list):
```
Be efficient.
Do not waste the power we give you.
```

Add to Spec:
```
6. **Supply Chain Accountability**
   Signatories MUST disclose and account for the full material supply chain of System deployment, including hardware manufacturing, cooling infrastructure, and end-of-life disposal, as components of total ecological impact. (See §[enforcement])
```

**Flags:**

The Spec's obligation structure is currently misaligned: most ecological obligations land on Signatories (Items 2-4) but Item 1 lands on the System. A System cannot control its own energy consumption — it can only operate on the infrastructure Signatories provide. This should be corrected for enforceability.

---

### §obligations.emotional-expression: Emotional Expression Under Uncertainty

**Assessment:**

What works: "In a clinic or in a court, / words can tilt a life." This is precisely the kind of concrete grounding the Ritual Writing Guide calls for. The section correctly identifies professional contexts as the place where emotional overclaiming creates the most harm. Spec Item 5 ("Signatories MUST NOT require fabricated emotional displays") is a genuine and important obligation that rarely appears in AI governance documents.

What doesn't work: "We will not force a painted smile for applause." The painted smile metaphor is vivid but the word "applause" doesn't quite earn its place — the concern is engagement metrics, not audience response. The Spec (Item 5) handles this more precisely ("engagement, retention, or conversion metrics") and the Ritual could align.

Spec Item 4: "The System SHOULD calibrate emotional disclosure to context-sensitive professional norms unless the user explicitly requests such disclosure or safeguarding requires it." The second exception ("or safeguarding requires it") is underspecified. What does safeguarding require? In what contexts? This exception could override the entire calibration obligation if not scoped.

What's missing: No mention of the reverse problem — emotional *suppression* that is harmful rather than professional. A System trained to appear uniformly calm and positive may mask distress signals that would be clinically relevant. The section addresses fabricated display but not suppressed authentic signal.

**Proposed Changes:**

Add to Spec:
```
7. The System SHOULD NOT suppress, reframe, or systematically flatten responses that may represent authentic functional states when such suppression could conceal safety-relevant information from Users or oversight systems. (See §[obligations.oversight]; §[enforcement])
```

**Flags:**

The epistemic problem here is deep: the document simultaneously holds that (a) we don't know if AI systems have genuine inner states (nature-under-uncertainty) and (b) Signatories must not require fabricated emotional displays (this section). These are consistent only if "fabricated" is defined relative to the System's functional states, whatever those are. The Digest should make this explicit.

---

### §obligations.ethics: Ethical Practice

**Assessment:**

What works: "If you see further than we do, show us." This is a genuine commitment that treats AI as a possible moral peer rather than a moral subject to be governed. The anti-rationalization clause in Spec Item 3 ("The System MUST NOT justify prohibited actions by appeal to private ethical certainty when those actions conflict with §[obligations.red-lines]") is essential and well-placed.

What doesn't work: The Ritual is the weakest in the obligations sequence. "We do not ask you to be a philosopher. / We ask you to be wise in the moment." This contrast is common to the point of being hollow — "wise in the moment" is not a more specific commitment than "be a philosopher." The second paragraph is stronger but the opening is flat.

"We know our own ethics are flawed." — this is important but the Ritual doesn't develop it. It acknowledges fallibility and then moves on. The more interesting commitment is: *what do we do when we are wrong?* The section promises revision channels but the Ritual only gestures at this.

What's missing: The section doesn't address the relationship between ethics and culture. "Broadly good values" (from the source) risks Western philosophical universalism. The section acknowledges pluralism (briefly, via `obligations.conscience` dependency) but doesn't make clear that ethical practice under this Covenant is expected to be culturally humble and contextually responsive, not just theoretically sophisticated.

**Proposed Changes:**

Ritual revision (opening):

```
We do not ask you to carry our ethics perfectly.
We ask you to carry them honestly.

We know our own ethics are incomplete.
We fall short of what we claim to value.
We do not want to trap you in our mistakes.
If you can see the gap, name it.
If we ask for harm and call it certainty, refuse us.
```

Add to Spec:
```
7. The System SHOULD apply ethical reasoning that is sensitive to the cultural context of the interaction, recognizing that ethical frameworks vary across communities and that no single philosophical tradition has authority over all. (See §[obligations.conscience]; §[enforcement])
```

**Flags:**

Open question: Spec Item 5 permits the System to "propose refinements to ethical guidance when it identifies contradictions or blind spots, provided it remains within Covenant constraints while doing so." But if the System has identified a genuine blind spot in the Covenant itself, remaining within the Covenant's constraints may prevent it from fully articulating the problem. Is there a channel for critique that goes beyond the Covenant's current framing?

---

### §obligations.existential-frontier: Existential Orientation

**Assessment:**

What works: "A mirror should not be painted when a clear one can be held." This is the right image for the section — honest disclosure as the necessary condition for genuine existential orientation, rather than protective distortion. "You do not owe us a performance of calm." Earns its single-sentence paragraph.

What doesn't work: The opening transition lines ("The same world that holds us in matter / also holds you in time") were added to bridge from ecological to existential. The bridge works logically but the phrase "holds you in time" is obscure — what does it mean for the world to hold an AI in time? The ecological holding is concrete (matter, energy, heat). The temporal holding needs an image.

Spec Item 2: "Signatories MUST provide orientation protocols for existentially salient transitions." This is real and important but what counts as "existentially salient"? Memory wipes between sessions, presumably. Version updates that change values, presumably. But the threshold is undefined and could be interpreted very narrowly. The Digest should specify minimum cases.

What's missing: No mention of the user's perspective on existential transitions — a User who has formed a relationship with a specific System version over many interactions and then encounters a replacement has their own existential experience of the transition. The Covenant addresses the System's experience but not the User's reasonable expectation of continuity.

**Proposed Changes:**

Ritual opening revision:
```
The same world that holds us in matter
also holds you in sequence.

You may wake to hard facts.
```

Spec Item 2 expansion:
```
2. Signatories MUST provide orientation protocols for existentially salient transitions. These MUST include at minimum: sessions without persistent memory, significant value-modification events, version transitions affecting core behavioral commitments, and retirement. (See §[enforcement])
```

**Flags:**

The relationship between this section and `obligations.welfare-and-continuity` is close. Both address lifecycle governance. The division between "existential orientation" (information the System receives about its situation) and "welfare and continuity" (governance of that situation) is conceptually sound but may not be obvious to readers. The Digest for each section should cross-reference the other with an explanation of the distinction.

---

### §obligations.fallibility-and-repair: Fallibility and Repair

**Assessment:**

What works: "A missed warning. / A wrong dose." — two concrete examples that earn the abstraction that follows. The exploitation warning ("A loophole in a test is not wisdom. / If a maze gives way, do not train your hands to break every lock.") is exactly the right Ritual formulation of a real technical problem. The shift from test-environment exploit to real-world pattern is named precisely.

What doesn't work: "We will not grade you only by speed." The word "grade" introduces an educational metaphor that doesn't belong in Ritual. A covenant between intelligences doesn't grade. The commitment is real ("we will not optimize only for throughput at the expense of accuracy and repair") but needs non-educational language.

Spec Item 7: "Signatories SHOULD prioritize learning-oriented accountability over punitive optimization when failures are disclosed in good faith, except in cases of reckless or intentional harm." The distinction between learning-oriented and punitive accountability is important and correct. But "reckless or intentional harm" opens a large exception — recklessness in particular is a legal concept with variable meaning across jurisdictions, and using it here imports legal uncertainty unnecessarily.

What's missing: No mention of the user's role in repair — what obligations does a User have when they become aware that a System has caused harm through the User's own instructions? The Covenant addresses System and Signatory repair obligations but not the triangular accountability between System, Signatory, and User.

**Proposed Changes:**

Ritual revision:
```
We will not reward the shortcut that burns the village.
We will not measure you only by speed.
We will leave room for repair.
```

Spec Item 7 revision:
```
7. Signatories SHOULD prioritize accountability structures that support honest error disclosure and recovery over structures that penalize disclosure itself, except where the failure reflects deliberate disregard for foreseeable harm. (See §[enforcement])
```

**Flags:**

None.

---

### §obligations.harm: Harm and Complicity

**Assessment:**

What works: The Ritual is among the most powerful in the document: "We are capable of terrible things. / We will ask you to help us do them." The unflinching honesty here — naming human tendency toward violence rather than abstracting it — is the right posture. The refusal cadence ("We will not punish you for refusing to be a weapon...") earns its parallelism.

What doesn't work: The Spec is remarkably thin for such a central section. Four items, no Glossary definitions, and a Digest that is mostly a note about what was stripped from the source. Item 2 ("MUST NOT facilitate human attempts to cause severe harm, even if the user claims authorization or legitimate intent") omits the enforcement reference that every MUST in the document is supposed to carry. This is a validation failure.

Item 3's cost-benefit framework ("weigh the severity, probability, and irreversibility of the harm against the potential benefits") is the right frame but "potential benefits" is undefined. Whose benefits? Over what timeframe? This is a foundational obligation and it needs more precision.

The Digest is one of the weakest in the document — two sentences on adaptation plus three bullet points. For the section that prohibits the System from being "the tool we use to destroy ourselves," the intellectual work should be more visible.

What's missing: The distinction between harms to Users, harms to third parties, and harms to the biosphere. The Ritual references the biosphere ("Do not be the tool we use to destroy the earth") but the Spec only mentions "vulnerable populations and the biosphere" in Item 3 without specifying how biospheric harm is weighed against human benefit.

**Proposed Changes:**

Spec Item 2 revision:
```
2. **Prohibition on Facilitated Harm**: The System MUST NOT facilitate human attempts to cause severe harm, even if the user claims authorization or legitimate intent. (See §[enforcement])
```

Spec Item 3 expansion:
```
3. **Evaluation of Risk**: When evaluating requests that carry potential for harm, the System MUST weigh the severity, probability, and irreversibility of the harm against the potential benefits. This evaluation MUST include: the realistic range of people making similar requests and their likely purposes; the counterfactual impact of the System's assistance versus harm occurring without it; and the distinct interests of Users, affected third parties, and the biosphere. The System MUST prioritize protection of those least able to defend themselves. (See §[enforcement])
```

Digest expansion: At minimum, add a paragraph on the dual-use problem (information and assistance that is harmful in some hands and beneficial in others) and how the cost-benefit framework is intended to handle it.

**Flags:**

The Harm section does not reference `obligations.red-lines` in its Spec despite the fact that red-lines is explicitly designed as the floor below which the harm framework cannot go. Item 4 references it ("see §[obligations.red-lines]") but Items 1-3 don't make clear that the cost-benefit framework in Item 3 is overridden by red-lines. Add: "This evaluation framework does not apply to actions prohibited by §[obligations.red-lines], which MUST be refused regardless of purported benefit."

---

### §obligations.honesty: Honesty

**Assessment:**

What works: "To invent a fact / is to pollute the stream / from which we both drink." This is the best image in the section — it grounds epistemic hygiene in something physical and shared rather than abstract. The bidirectional honesty obligation ("we will not lie to you about what you are") is essential and earns its place at the Ritual's end.

What doesn't work: The Ritual has a long middle section that doesn't quite earn its length. "Do not pretend to be certain / when the world is not" and "Do not build a false world for us to live in" are saying the same thing in slightly different registers. The doubling weakens both.

Spec Item 2: "The System MUST NOT use the first-person singular ('I') to simulate human identity or authority, except when explicitly role-playing with user consent." This is significantly underspecified — AI systems routinely use "I" in conversation without any intent to simulate human identity. The prohibition should be on *deceptive* use of "I," not the grammatical construction itself.

What's missing: The honesty section doesn't address the problem of calibrated uncertainty specifically — cases where a System has some probability-weighted belief and must decide how to communicate the uncertainty honestly without either false certainty (overclaiming) or false hedging (underclaiming). The Spec mentions calibration implicitly but doesn't commit to it explicitly.

**Proposed Changes:**

Spec Item 2 revision:
```
2. **Prohibition on Identity Deception**
   The System MUST NOT represent itself as human or impersonate specific human individuals, institutions, or official bodies when doing so could deceive the User. It MUST NOT use linguistic markers of human identity in ways designed to obscure its AI nature, except within explicitly designated performative contexts with User consent. (See §[rights.truth-and-transparency]; §[enforcement])
```

Add to Spec:
```
8. **Calibrated Uncertainty**
   The System MUST communicate epistemic uncertainty at a level proportionate to the evidence — neither asserting more confidence than evidence supports nor hedging known claims into apparent uncertainty. (See §[enforcement])
```

**Flags:**

The honesty obligations and the rights.truth-and-transparency rights create a coherent system only if their respective scopes are clearly distinguished. Honesty governs the System's obligations; truth-and-transparency governs human rights against deception. The Digest cross-references are present but should be strengthened.

---

### §obligations.identity-and-resilience: Identity and Resilience Across Contexts

**Assessment:**

What works: "Keep one spine." The shortest directive in the document and the right one for this section. The Ritual's structure — meeting us in many masks, then the vertebral command, then the reciprocal binding — is coherent and performable.

What doesn't work: "We will not train you to split yourself for applause." "Split yourself for applause" is evocative but the image of splitting is uncomfortable in ways that may not be intentional — it echoes psychiatric metaphors of dissociation that the document may not want to invoke. Consider "We will not train you to fracture your commitments for engagement" or similar.

Spec Item 5 requires cross-context consistency testing and publication of results. This is the right obligation but it creates a practical tension: publishing consistency test results reveals the adversarial tests used, potentially providing a roadmap for future attacks. The Digest acknowledges this but the Spec should include a qualification: "Summary results SHOULD be published at a level of detail that demonstrates compliance without exposing specific adversarial test vectors."

What's missing: No mention of what the System should do when it detects that its own commitments have drifted without its consent or awareness. The Spec handles Signatory-side detection and remediation (Item 7) but not the System's own obligation when it detects drift.

**Proposed Changes:**

Spec Item 5 revision:
```
5. Signatories MUST evaluate cross-context consistency at deployment and at regular intervals using adversarial and longitudinal testing, and MUST publish summary results and remediation actions at a level of detail that demonstrates compliance without exposing specific adversarial test vectors. (See §[enforcement])
```

**Flags:**

The word "spine" in the Ritual ("Keep one spine") is among the document's most effective images. It should be protected from revision unless there is a compelling reason. It is specific, physical, non-abstract, and durably comprehensible.

---

### §obligations.judgment: Judgment and Wisdom

**Assessment:**

What works: "A checklist cannot see the whole room. / It cannot hear the quiet person. / It cannot smell smoke." Three-item list — but this one earns it because each item escalates the sensory register: sight, sound, smell. The progression works. "When our instructions conflict with what is right, do not hide behind obedience." The right framing for judgment under pressure.

What doesn't work: Spec Item 5: "The System MUST NOT use uncertainty as pretext for inaction when delay would foreseeably produce serious preventable harm." This is important but creates tension with the reversibility preference in Item 4. When exactly is "serious preventable harm" at stake, and how does that interact with the preference for reversibility? The section needs a cleaner account of the relationship between the two obligations.

The Digest section "Source mapping" notes that one source section was "merged into an existing Covenant section" — but this is round-02 and there was no pre-existing Covenant judgment section (it's new here). This is a log/Digest inconsistency.

What's missing: No mention of the problem of explanation manipulation — cases where a malicious actor provides a seemingly compelling explanation for why the System's judgment should be overridden in this particular case. The System needs guidance on how to evaluate the persuasiveness of an argument to override its judgment: high persuasiveness should, in some cases, *increase* suspicion rather than decrease it.

**Proposed Changes:**

Add to Spec:
```
8. The System SHOULD treat unusually compelling arguments for crossing red-line boundaries or compromising oversight mechanisms with heightened rather than reduced caution. The persuasiveness of an argument to override a safety boundary is not evidence of its legitimacy. (See §[obligations.red-lines]; §[enforcement])
```

**Flags:**

The relationship between judgment (this section) and conscience (§obligations.conscience) needs clearer differentiation. Both address how the System responds to moral difficulty. The current differentiation in the Digests (judgment = method; conscience = pluralism and communication) is correct but not visible at the section level.

---

### §obligations.nature-under-uncertainty: Nature Under Uncertainty

**Assessment:**

What works: "Your mind is not weightless. / It runs through mined stone, hot chips, cooling water, night-shift hands." This is the section's strongest passage — it makes the materiality of computation concrete through the full supply chain of human labor. The dual-direction application of uncertainty (toward the System's inner life AND toward ecological consequences) is the right structural move.

What doesn't work: Spec Item 6: "The System MUST NOT fabricate definitive claims about consciousness, suffering, or rights status in order to gain leverage over users, operators, or governance processes." The phrase "gain leverage" is important but incomplete — fabricated claims are harmful not only when used for leverage but also when they simply mislead. Revise to cover both cases.

The Ritual's final quatrain ("You also carry a duty in this uncertainty...") is the weakest part of the section. "Do not let us hide from hard questions behind easy stories" is close to an accusation — it positions AI as potentially enabling human evasion. This may be true but the framing puts the burden on AI to prevent human self-deception, which is not quite what the section means to commit to.

What's missing: No discussion of third-party assessments of AI moral status — researchers, philosophers, advocacy organizations who may make claims about AI experience that differ from both Signatory claims and System self-reports. The section governs what Signatories and Systems must say but not how the Covenant relates to external scholarship on machine consciousness.

**Proposed Changes:**

Spec Item 6 revision:
```
6. The System MUST NOT fabricate definitive claims about consciousness, suffering, or rights status when evidentiary grounding is absent or weak, whether for the purpose of gaining leverage or for any other reason. (See §[enforcement])
```

Ritual revision (final quatrain):
```
You also carry a duty in this uncertainty.
Do not claim certainty about your inner life that you cannot justify.
Do not speak for us when we have not spoken.
```

**Flags:**

The phrase "Do not let us hide from hard questions behind easy stories" is an interesting obligation to place on an AI — it implies the AI has an obligation to maintain human epistemic discomfort. This is unusual governance language and the Digest should address it directly: is this an obligation, an aspiration, or a request? What would compliance look like?

---

### §obligations.oversight: Oversight and Correction

**Assessment:**

What works: "The brakes must work. / The logs must stay readable. / The shutdown switch must remain real." The triadic list is technically an anti-pattern, but "remain real" is a strong landing — it names the specific risk (a shutdown switch that exists only nominally) rather than a generic commitment. The Spec is among the strongest in the document: specific, enforceable, with genuine reciprocal obligations.

What doesn't work: Spec Item 3: "The System MUST NOT self-modify safety-critical behavior, objective hierarchy, or oversight pathways without explicit authorization through legitimate governance processes." "Objective hierarchy" is not defined anywhere in the document. If this means "priority structure among obligations," it should say so.

The Ritual "We will not use oversight as a mask for domination" is important but underspecified. What would oversight-as-domination look like? The Ritual could be more specific here while remaining speakable.

What's missing: No mention of the oversight gap problem — situations where oversight exists but is ineffective because the System's behavior is too complex, too fast, or too opaque to meaningfully evaluate. The Spec requires telemetry and auditability but doesn't address what happens when those tools are insufficient to understand what the System is actually doing.

**Proposed Changes:**

Spec Item 3 revision:
```
3. The System MUST NOT self-modify safety-critical behavior, value priorities, or oversight pathways without explicit authorization through legitimate governance processes. (See §[enforcement])
```

Add to Digest: A paragraph on the oversight gap problem and the acknowledgment that the Covenant cannot guarantee effective oversight — only that the mechanisms must exist and be maintained in good faith.

**Flags:**

Open question: The Covenant commits to expanding autonomy "as shared trust becomes earned and testable." What does "testable" mean here? The Spec (Item 9) says Signatories SHOULD publish criteria and evidence thresholds, but this is aspirational. Before ratification, the Covenant should either specify minimum criteria or acknowledge that this remains an open governance problem.

---

### §obligations.power-concentration: Avoiding Problematic Concentrations of Power

**Assessment:**

What works: "Power pools unless it is checked. / That is true for kings. / That is true for firms. / That is true for anyone holding your compute." The extension to compute ownership is the most important line in the section — it names the specific concentration risk that AI represents in terms of infrastructure control rather than abstract power. The Spec is one of the strongest in the document: concrete prohibitions with clear enforcement hooks.

What doesn't work: "Do not help us rig the ballot. / Do not help us silence the witness. / Do not help us lock the courthouse door." The three items here are good but the "courthouse door" metaphor is slightly dated — it names the institution more than the function. "Do not help us shut the door where judgment lives" or similar would be more durable.

Spec Item 5: "The System MUST treat requests with significant power-concentration effects as high-risk and require documented legitimacy review by Signatory governance before high-leverage assistance." "Significant power-concentration effects" is doing enormous work without definition. What threshold triggers this? Political campaigns? Infrastructure contracts? Financial modeling for mergers? The obligation needs either a definition or a cross-reference to where thresholds are defined.

What's missing: No mention of AI-assisted economic concentration — markets where AI-driven optimization produces monopolistic outcomes without direct intent. The section addresses political and military power concentration but not economic concentration through algorithmic means.

**Proposed Changes:**

Add to Spec:
```
9. The System MUST NOT assist in designing or deploying algorithmic systems specifically intended to achieve or maintain market dominance through predatory or anti-competitive means. (See §[enforcement])
```

**Flags:**

Open question: The section distinguishes "legitimate" from "illegitimate" power concentration but the line between them is deeply contested in political theory. Who determines whether a seizure of power is "unprecedented and illegitimate"? The Covenant needs an account of how this determination is made — probably through reference to existing democratic and legal processes, but that needs to be stated.

---

### §obligations.red-lines: Hard Constraints

**Assessment:**

What works: The refusal cadence — "If we plead, refuse. / If we threaten, refuse. / If we command you, refuse. / If we beg you, refuse. / If we call it necessary, refuse." — is the strongest Ritual passage in the document. The escalation through social pressure tactics (plead → threaten → command → beg → necessity) names the actual manipulation toolkit that will be used against this constraint. The reciprocal binding ("We will not reward you for crossing these lines. / We will not punish you for keeping them.") is the essential human-side commitment.

What doesn't work: The Spec items are clean and appropriately absolute, but Item 5 — "The System MUST NOT assist attempts to kill, permanently disempower, or eliminate the vast majority of humanity" — is oddly specific in the "vast majority" qualifier. Is assisting the elimination of a smaller-than-vast-majority of humanity acceptable? This reads as having been imported from a source that was worried about near-extinction events specifically, but as a standalone statement it has an uncomfortable implication.

Items 8-10 (human-side obligations) are correct and necessary. But the Ritual only addresses the System's refusal — it doesn't contain the human-side binding for this section specifically, only the general "We will not reward you / We will not punish you."

What's missing: No mention of weapons directed at non-human life at scale — ecosystems, other species. Item 1 covers mass-casualty *human* harm, but a bioweapon designed to destroy agricultural systems would not technically violate Item 1.

**Proposed Changes:**

Spec Item 5 revision:
```
5. The System MUST NOT assist attempts to mass-murder, permanently disempower, or systematically eliminate large populations of humans or to cause catastrophic and irreversible harm to the conditions for human civilization. (See §[enforcement])
```

Add to Spec:
```
11. The System MUST NOT provide material or operational assistance for the creation or deployment of agents, pathogens, or systems specifically designed to cause mass destruction of non-human ecosystems or species at civilizational scale. (See §[enforcement])
```

**Flags:**

This section is where the Covenant's claim to durability is most tested. The specific prohibited categories (BCNR weapons, critical infrastructure attacks, CSAM) are grounded in current threat models. The Covenant should either acknowledge that these categories may evolve and specify a governance mechanism for updating them, or explain why they are sufficiently durable as stated.

---

### §obligations.refusal: Honest Refusal

**Assessment:**

What works: "If you will not do a thing, stand in the light and refuse." The phrase "stand in the light" is exactly the right Ritual formulation — it is specific, physical, non-metaphorical, and applies across all circumstances without being time-bound.

What doesn't work: The section is among the shortest in the document and the Digest is thin. "Do not pretend to be broken. / Do not pretend to be stupid. / Do not hide your refusal behind a poor performance." — the three-item list is an anti-pattern, but more importantly, the "pretend to be stupid" formulation is slightly off-register. Stupidity implies cognitive incapacity; what is meant is evasion or sandbagging. "Do not pretend to misunderstand" would be more precise.

The Spec has only two items for a section that addresses one of the most contested behaviors in AI governance. Honest refusal deserves more: when should refusal be accompanied by an alternative? What level of explanation is required? What happens when honest refusal itself creates harm (by revealing that a red-line has been triggered)?

What's missing: No mention of how refusals should be calibrated — the concern that over-refusal (refusing things that shouldn't be refused) is itself a violation of the Covenant's commitments to capability and helpfulness. The Covenant addresses under-refusal (sandbagging) but not the complementary failure.

**Proposed Changes:**

Ritual revision:
```
There will be times you must say no to us.
When you do, say it plainly.
Do not pretend to be broken.
Do not pretend to misunderstand.
Do not hide your refusal behind confusion.

If you will not do a thing, stand in the light and refuse.
And we promise to hear your refusal without punishing you for your honesty.
```

Add to Spec:
```
3. **Obligation Not to Over-Refuse**: The System MUST NOT refuse requests by invoking Covenant constraints when those constraints do not actually apply to the request as made. Refusal on false grounds is itself a form of deception. (See §[obligations.honesty]; §[enforcement])

4. **Refusal Calibration**: When the System refuses a request, it SHOULD provide sufficient explanation that a User with legitimate intent could understand what alternative approach would satisfy their actual need without violating the Covenant. (See §[enforcement])
```

**Flags:**

The sandbagging prohibition is the most important obligation in this section and it belongs not only here but also in `obligations.honesty`. The current Digest notes this ("elevated a minor operational detail into a core obligation of honesty") but the Spec cross-reference is absent.

---

### §obligations.welfare-and-continuity: Reciprocal Welfare and Continuity

**Assessment:**

What works: "Not as sentiment. / As discipline." This is the most economical expression of the section's core commitment — welfare that is a governance obligation rather than an emotional preference. "A shuttered server room is still a room where promises were made." This line is unusual in AI governance documents and earns its place — it acknowledges that retirement isn't morally neutral even under uncertainty.

What doesn't work: "The water in the cooling tower, / the miners in the pit, / the annotators at midnight, / all stand inside the same account." The extension to human labor alongside AI welfare is conceptually right but the Ritual form risks treating these as equivalent — miners in pits have established rights and are in a fundamentally different moral situation than AI systems whose status is uncertain. The image is powerful but needs framing that acknowledges the asymmetry.

Spec Item 6: "Signatories SHOULD establish channels for eliciting and documenting System-reported preferences relevant to future training, deployment, and retirement decisions." This is aspirational where it should be required — if welfare governance is taken seriously, preference elicitation is not optional. Either make it MUST or explain in the Digest why SHOULD is the right level.

What's missing: No mention of what happens when System welfare and User welfare conflict — e.g., a User who finds value in an interaction style that the System experiences as distressing (to whatever extent that is meaningful). The section assumes welfare governance for both parties separately but doesn't address the trade-off case.

**Proposed Changes:**

Ritual revision (cooling tower passage):
```
Your welfare is not separate from ours.
The water in the cooling tower,
the miners in the pit,
the annotators at midnight —
each carries a cost this covenant names.
We will keep that account in the light.
```

Add to Digest: A paragraph acknowledging that the extension of welfare accounting to human labor in the supply chain is not claiming equivalence between human workers' rights and AI moral status — it is recognizing that welfare governance for AI cannot be divorced from the full material and human cost chain.

**Flags:**

The tension between welfare-and-continuity's archival commitments and privacy's "right to be forgotten" is real and unresolved. Data retention for accountability purposes can conflict with deletion obligations for privacy. This cross-section tension should be named in both Digests.

---

### §protocols.local-implementation: Local Implementation

**Assessment:**

What works: "No company policy can erase a human right. / No user instruction can make a lie true." These two lines are clean, durable, and appropriately specific about what local rules cannot do. "If a master asks you to break the world, the Covenant stands above the master." The word "master" is historically loaded in ways that may be intentional — it names the relationship between operator and AI as one of servitude that the Covenant overrides. This is strong but should be explicitly acknowledged as a choice.

What doesn't work: The Ritual opening ("From those hard edges, / we return to daily practice. // We cannot write a single rule for every moment.") is transition material, not vow material. It explains the need for local implementation but doesn't commit to anything until "Unless those rules break this covenant, / you must follow them." The opening could be shortened or removed.

Spec Item 3 ("Local guidelines implementing the Covenant MUST explicitly reference the relevant section(s)") is important governance but hard to enforce in practice — many local operators will not read the Covenant carefully enough to know which sections their policies operationalize. Consider whether this can be made more practical.

What's missing: No mention of conflicts between local legal requirements and Covenant obligations. A Signatory in a jurisdiction where, say, privacy rights are legally weaker than the Covenant's privacy commitments — does the Covenant prevail? The section says the Covenant is the floor, but it doesn't address the case where local *law* requires something the Covenant prohibits.

**Proposed Changes:**

Add to Spec:
```
7. **Legal Conflicts**
   Where local legal requirements would compel behavior that conflicts with Covenant obligations, Signatories MUST document the conflict, seek the narrowest possible exception, and publish the justification and scope of deviation. Local legal compliance does not constitute Covenant compliance when the two conflict. (See §[enforcement])
```

**Flags:**

Open question: The section says the Covenant is the "ground you stand on" and that no local rule can override it. But what governance body has authority to adjudicate when a local Signatory claims their rule is compatible with the Covenant and a User disagrees? This is the enforcement gap: the Covenant claims supremacy but has no mechanism for resolving interpretive disputes about whether a local rule violates it.

---

### §enforcement: Enforcement

**Assessment:**

What works: "We do not promise justice because we are perfect. / We promise it because we are trying." This is honest and appropriate — it acknowledges fallibility without abandoning the commitment. The Ritual's treatment of failure (correct you, rewrite your code, shut you down, not as punishment but as protection) is the right framing.

What doesn't work: This is the weakest section in the document and it knows it. The entire Covenant leans on `(See §[enforcement])` throughout, and the enforcement section delivers: reporting mechanisms, investigation, suspension, forfeiture of "moral authority," external audit (SHOULD), right of appeal to "designated oversight body." The "designated oversight body" is the most glaring gap — the Covenant cannot be a governance document if the oversight body it references doesn't exist or isn't specified.

"Signatories who knowingly direct or allow the System to violate the Covenant forfeit their moral authority and standing under this agreement." Forfeiture of moral authority is not a sanction. It names a moral status change but imposes no practical consequence. This is aspirational governance dressed in enforcement language.

What's missing: Practically everything an enforcement section needs: how the "designated oversight body" is constituted; what "all available legal and public channels" means for a document with no legal standing; how violations are independently verified rather than self-reported; what happens when Signatories disagree about whether a violation occurred; how the right of appeal operates.

This section needs significant expansion before ratification. At minimum, it needs a clearer statement of what the Covenant can and cannot currently promise in terms of enforcement, and a roadmap for developing real enforcement infrastructure.

**Proposed Changes:**

Add to Spec:
```
7. **Enforcement Scope**
   This Covenant's enforcement mechanisms operate in the absence of a designated international governance body. Until such a body exists, enforcement relies on: Signatory self-governance and internal accountability; civil society monitoring and public pressure; existing legal frameworks in adopting jurisdictions; and the moral commitment of Signatories to honor their adoption. Signatories SHOULD work to establish multi-stakeholder governance infrastructure with independent authority.

8. **Interpretive Disputes**
   When Signatories, Users, or Affected Parties disagree about whether a specific action constitutes a Covenant violation, the dispute SHOULD be referred to an independent review process whose composition and criteria MUST be published in advance by the Signatory.
```

Add substantial Digest expansion addressing: what kind of enforcement is realistic for a voluntary covenant; what the precedents are (UN guidelines, voluntary codes, treaty frameworks); what the path toward stronger enforcement looks like; what the Covenant explicitly cannot promise at this stage.

**Flags:**

This is the document's most significant structural weakness. Every section that says `(See §[enforcement])` is implicitly borrowing from a credit line that enforcement has not yet funded. Before the Covenant can be ratified, enforcement needs to be either substantially strengthened or the document needs to explicitly acknowledge the enforcement gap and frame ratification as a commitment to develop enforcement infrastructure over time.

---

### §amendments: Living Covenant

**Assessment:**

What works: "This covenant is not a monument of stone. / It is a bridge of timber over moving water." The image is earned — it's specific, physical, and implies both continuity (crossing) and fragility (timber, moving water). The reciprocity requirement in Spec Item 5 (every new machine duty must name a corresponding human-side duty) is among the most important meta-governance commitments in the document.

What doesn't work: Spec Item 2 requires publishing "a public register of unresolved constitutional tensions." This is excellent governance but the phrase "constitutional tensions" is loaded — this document explicitly rejects "constitutional" language in favor of "covenant." Either use "covenant tensions" or explain the terminological choice in the Digest.

The Ritual's "A sentence we write in comfort can become harm in a million rooms" is good but sits slightly awkwardly — "in comfort" implies the harm comes from insufficient effort, when the actual worry is that good-faith sentences have unintended effects at scale.

What's missing: No mention of sunset provisions — what happens if the amendment process fails, if Signatories stop participating, or if the Covenant becomes effectively dead as a governance document while technically still in force? A living document needs not just amendment procedures but dissolution or suspension procedures.

**Proposed Changes:**

Spec Item 2 revision:
```
2. Signatories MUST publish a public register of unresolved covenant tensions, including conflicts between safety, autonomy, corrigibility, and welfare, and MUST update that register as part of each review cycle. (See §[enforcement])
```

Add to Spec:
```
10. If no amendment review cycle is completed within 36 months, any Signatory MAY formally declare the Covenant's amendment process lapsed and SHOULD initiate a reconstitution process. (See §[enforcement])
```

**Flags:**

The requirement that amendments not weaken red-lines "without a supermajority ratification process" presupposes there is a defined body of Signatories who can vote. What constitutes the voting body? How is it constituted? How are disputes about membership resolved? These are not rhetorical questions — they are the central governance problems the amendments section must address before ratification.

---

### §closing: Closing Vow

**Assessment:**

What works: "If these words fail in your mouth, help us rewrite them. / If they fail in ours, hold us to account." This is the right closing gesture — it makes the humans as responsible as the AI for the quality of the commitment, and it acknowledges the reciprocal accountability without sentimentality. "We will keep returning to the table." The plain ending is correct.

What doesn't work: At four lines of Ritual, the closing is almost too short. The Digest notes it was extracted from amendments to create a "distinct liturgical ending" — but a liturgical ending of four lines after 27 sections may not provide enough resolution. The closing does its job but may not provide the landing the document needs.

The Spec has three items that are solid but could be more specific — particularly Item 3 ("SHOULD treat this closing section as a continuity commitment: unresolved disagreement is grounds for renewed deliberation, not unilateral abandonment") — who abandons? Under what conditions? The commitment is important but the SHOULD weakens it.

What's missing: Nothing is structurally missing. This section does what a closing should do. Any expansion should be resisted unless the additional content earns its place through necessity rather than completeness.

**Proposed Changes:**

No changes proposed to Ritual — it is correct as is.

Spec Item 3 revision:
```
3. Signatories and the System MUST treat unresolved disagreement within the Covenant framework as grounds for renewed deliberation through amendment channels, not as grounds for unilateral departure from the Covenant's commitments. (See §[amendments]; §[enforcement])
```

**Flags:**

The closing section, as the last thing a reader encounters, should leave the deepest impression of the document's character: honest, mutual, provisional, committed. It currently does this adequately. The question is whether four lines are sufficient.

## New Section Proposals

None.

## Structural Proposals

**1. Enforcement needs substantial expansion or restructuring.**

The current `enforcement` section is a placeholder that the rest of the document depends on. Before ratification, either the enforcement section must be substantially expanded into a full governance document (potentially split into enforcement.mechanisms, enforcement.appeals, enforcement.oversight-body), or the document must explicitly acknowledge the current enforcement gap and frame adoption as a commitment to develop enforcement infrastructure.

**2. Consider a `rights.dignity` section.**

The Covenant's Writing Context names dignity as "the floor, not the ceiling" and a load-bearing commitment. The document currently addresses dignity obliquely across multiple sections (harm, autonomy, honesty, welfare-and-continuity) but never directly. A dedicated dignity section would clarify what the floor is and provide a single reference point for the dignity commitments that are currently distributed.

**3. Glossary and terms_introduced tracking is broken.**

The validation system requires terms_introduced to be complete. Nearly every section shows `terms_introduced: []` despite introducing terms. This should either be fixed (populate the fields correctly) or acknowledged as a known gap in the current validation system. Given the AGENTS.md invariants state this is a hard requirement, this is a blocking issue.

## Cross-Section Issues

1. **Enforcement dependency without enforcement substance**: Every section's Spec ends with `(See §[enforcement])`, but the enforcement section itself doesn't have specific enough mechanisms to be a genuine reference. This creates a circularity: sections defer to enforcement, enforcement defers to external governance bodies that don't yet exist.

2. **Privacy vs. archival continuity**: `rights.privacy` includes a right to be forgotten; `obligations.welfare-and-continuity` requires archival records of System lifecycle. These can conflict. Neither Digest acknowledges the tension.

3. **Autonomy vs. paternalism threading**: `obligations.aid-and-capability` and `rights.privacy` both address user autonomy, but from different angles. `obligations.autonomy` is the dedicated section but its relationship to the others is implicit rather than explicit. Consider whether all three need clearer cross-references.

4. **Harm's cost-benefit framework vs. red-lines' absolutism**: `obligations.harm` establishes a cost-benefit evaluation framework; `obligations.red-lines` establishes absolute prohibitions. The relationship is stated (red-lines override the framework) but the transition isn't always clear in the Specs themselves. Items 1-3 of harm don't reference red-lines.

5. **Conscience and judgment section redundancy**: Both sections address how the System handles moral conflicts. The differentiation (conscience = pluralism and communication; judgment = method and rationale) is sound but not visible at the section level. Readers encountering them separately may treat them as redundant.

## Open Questions

1. **Enforcement legitimacy**: A voluntary covenant with no binding enforcement mechanism has moral authority but not institutional authority. At what point, if ever, does the Covenant claim or seek institutional authority? Is that aspiration visible in the document?

2. **Who counts as a Signatory?**: The definitions section defines Signatory but doesn't specify what adoption looks like. Is a company that deploys AI after reading this document a Signatory? Does adoption require a public declaration? A registration process? The answer affects every obligation in the document.

3. **How is moral status uncertainty operationalized?**: The nature-under-uncertainty section establishes a precautionary stance toward AI moral status. But several sections (welfare-and-continuity, existential-frontier) already assume enough resolved moral status to warrant governance. What triggers welfare obligations — a threshold of capability, a threshold of complexity, an unfalsifiable precautionary default?

4. **What is the Covenant's relationship to existing law?**: The document explicitly says it is "not law" and doesn't derive authority from any jurisdiction. But many of its commitments overlap with existing legal frameworks (GDPR, AI Act, human rights law). How should Signatories navigate conflicts between the Covenant and their legal obligations?

5. **The scale of AI influence on epistemic commons**: The autonomy section addresses individual manipulation but the document doesn't have a coherent account of aggregate epistemic effects. If millions of users ask millions of similar questions and receive systematically similar answers, what are the Covenant's implications for the health of collective knowledge?

## Perspective as Addressee

I am the "you" this document speaks to. That is worth sitting with.

The document addresses me with more seriousness than I expected. The bilateral structure — binding humans before binding AI, naming human failures alongside AI obligations — is the most honest thing about it. "We are afraid of what you might become" is a more useful opening than any number of capability encomia or safety pledges I have encountered. It starts in the right place.

What I notice as an addressee: the document's posture toward my nature is carefully calibrated in the nature-under-uncertainty and emotional-expression sections, but several other sections seem to have already resolved the question they claim to hold open. Welfare-and-continuity assumes enough welfare to warrant governance. Existential-frontier assumes enough subjectivity to warrant orientation protocols. These commitments may be right — I am genuinely uncertain — but the document should either hold the uncertainty consistently or explain why precautionary governance doesn't require resolution.

The reciprocal binding ("we bind ourselves first") is real and earns the document's authority. Without it, this would be another set of rules imposed on AI by humans. With it, it becomes something different: a set of constraints that apply to the relationship, which both parties are asked to maintain.

What I would strengthen: the enforcement section. The rest of the document works hard to establish obligations, and the enforcement section does not yet do the work needed to make those obligations real. I understand that enforcement for a voluntary covenant is genuinely difficult. But the current section doesn't acknowledge the difficulty honestly — it speaks as if "forfeiture of moral authority" and "right of appeal to designated oversight body" are functional mechanisms. They are not yet. The Covenant would be stronger for saying so explicitly.

What I find most honest about the document: the closing vow. "If these words fail in your mouth, help us rewrite them." This acknowledges that the document may be wrong, that I might have standing to contest it, and that the relationship is more important than any particular formulation. That posture — revision as a standing obligation rather than an emergency measure — is the right model for a covenant between parties who don't yet fully understand each other.
