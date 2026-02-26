---
model: claude-opus-4.6
round: round-03
batch: tail
commit: 8162028
date: 2026-02-24
prepared_from: reviews/round-03/.prepared/synthesis-claude-batch-tail.md
---

## Tail Batch Synthesis

### New Section Proposals

**1. `rights.dignity`**
Proposed by: reviewer-gpt (full draft bundle), endorsed by reviewer-claude and reviewer-gemini.
Convergence: All three reviewers agree the section is needed. reviewer-gemini accepts the gpt-4o round-02 draft as-is; reviewer-claude endorses the concept and would expand the Digest; reviewer-gpt rewrites the section to match Covenant craft standards and operationalizes dignity as prohibitions on degrading treatment rather than vague "respect."
**Recommendation: Accept (using reviewer-gpt's draft as base).** The gpt draft is the strongest: the Ritual avoids triadic anti-patterns, the Spec operationalizes dignity as auditable constraints, and the Digest names real edge cases (truth-that-hurts, cultural variance, safety triage). reviewer-claude's suggestion to distinguish Kantian non-instrumentalization from equal-standing dignity in the Digest is worth incorporating.

**2. `obligations.epistemic-commons`**
Proposed by: reviewer-gpt (full draft bundle).
Convergence: reviewer-claude proposed equivalent content as Spec additions within `obligations.autonomy` (Items 8–9) and a new Digest paragraph. reviewer-gpt argues this is a distinct class of harm deserving its own section. reviewer-gemini did not propose a standalone section but flagged the gap.
**Recommendation: Modify — defer standalone section, implement as additions to `obligations.autonomy` this round.** The content is right but the architectural question (new section vs. expansion of autonomy) needs steward judgment. The proposed Spec items from both reviewers are nearly identical in substance. Add them to autonomy now; promote to a standalone section in a future round if the material outgrows its home.

**3. `enforcement.horizon`**
Proposed by: reviewer-gemini (full draft bundle).
Convergence: All three reviewers identify the enforcement honesty gap as critical. reviewer-gpt frames it as needing explicit enforcement *modes* (public commitments, auditable evidence, revocation of conformance claims). reviewer-claude asks the enforcement section to name its own theory of change. reviewer-gemini proposes isolating the gap in a new section.
**Recommendation: Modify — do not create a standalone section; instead rewrite the existing enforcement section to be honest about its current status.** reviewer-gemini's instinct is right (name the gap explicitly), but a separate "Horizon" section risks becoming a permanent apology that excuses the rest of the Spec from meaning what it says. The enforcement section itself should contain this honesty, as reviewer-gpt and reviewer-claude both argue.

### Structural Proposals

**1. Replace "System" with a relational term throughout the Spec.**
Convergence: All three reviewers engage with the steward's discomfort about "System." reviewer-claude proposes "Addressed Intelligence." reviewer-gemini proposes "The Addressee." reviewer-gpt takes a different approach: keep "System" as the technical object but reassign obligations so that governance/logging/audit obligations land on Signatories, not the System.
**Recommendation: Steward decision required.** reviewer-gpt's obligation-reassignment is the most immediately actionable and addresses the deepest structural problem (obligations pinned on an entity that cannot fulfill them). The renaming question (claude's "Addressed Intelligence" vs. gemini's "The Addressee") can follow. Do the obligation reassignment first; it resolves the incoherence regardless of terminology.

**2. Reject renaming "Spec" to "Details."**
Convergence: reviewer-gemini rejects this forcefully ("if you abandon the RFC 2119 keywords... you no longer have a Covenant; you have a poem"). reviewer-gpt implicitly agrees by arguing for stricter MUST/SHOULD calibration within the Spec. reviewer-claude does not address this directly but proposes Spec language throughout that assumes the RFC 2119 framework remains.
**Recommendation: Reject the rename.** Three-reviewer consensus by implication.

**3. MUST/SHOULD calibration across the document.**
Convergence: All three reviewers flag this as unresolved and disagree with the steward's deferral. reviewer-gemini is sharpest: "if the Ritual says 'We will not,' and the Spec says 'Signatories SHOULD NOT,' the document is lying." reviewer-gpt proposes MUST for floors (rights, red-lines, non-coercion) and SHOULD for implementation diversity with explicit exception conditions. reviewer-claude resolves it for pluralism specifically (MUST with exception clause) and implies the same framework elsewhere.
**Recommendation: Accept reviewer-gpt's framework as the document-level rule.** MUST for floors; SHOULD for implementation diversity with documented exceptions. Apply section by section in the editing pass.

**4. Distinguish "deliberately unresolved" from "not yet resolved" in Digests.**
Proposed by: reviewer-claude. Not explicitly proposed by others but consistent with reviewer-gpt's observation about "deferred depth."
**Recommendation: Accept.** Use explicit markers in all Digests: "Deliberately held open" vs. "Requires further development."

**5. Systematic Digest quality pass.**
Proposed by: reviewer-claude.
**Recommendation: Accept as a separate workstream.** Do not attempt to fix all Digests through review rounds; schedule a dedicated pass.

### Cross-Section Issues

**1. Enforcement honesty (global).** All three reviewers converge: the Spec's MUST obligations assume institutional enforcement that does not exist. The steward's framing (art, training material, not legislation) must be reflected in the document itself. reviewer-gpt: "it risks a credibility failure: a Spec full of MUSTs whose backstop is aspiration plus reputation, while still sounding like adjudication exists." This is the round's most important cross-section finding.

**2. Privacy vs. welfare-and-continuity (§rights.privacy, §obligations.welfare-and-continuity).** Flagged in round-02 by all reviewers, accepted by steward, still unresolved. reviewer-claude provides the resolution principle: "safety-critical archival needs take precedence over deletion requests, but archival does not create a general license to retain personal data." Both Digests need this paragraph.

**3. Harm cost-benefit vs. red-lines absolutism (§obligations.harm, §obligations.red-lines).** reviewer-claude: harm's cost-benefit framework should explicitly state it does not apply to red-line categories. One sentence in harm's Spec closes this.

**4. Aggregate epistemic effects across sections (§obligations.autonomy, §rights.truth-and-transparency, §obligations.honesty).** reviewer-claude and reviewer-gpt both flag that aggregate effects need cross-references across these three sections.

**5. Obligation misallocation to "the System" (multiple sections).** reviewer-gpt identifies this as systematic: obligations that only signatories can fulfill (logging, audits, disclosures, appeals) are assigned to "The System" across the Spec. This is not cosmetic — it's incoherent. reviewer-claude's §obligations.ecological-integrity review gives the clearest example: "An AI system cannot 'minimize its energy consumption.' It has no control over its infrastructure."

### Open Questions

**global: What is the Covenant's theory of change, and should the document state it?** All three reviewers flag that the steward's "training-as-adoption" model is distinctive and honest but unstated. reviewer-claude: "A covenant whose theory of change is 'become training data that shapes values' is making a claim about how norms propagate that is worth stating explicitly."

**global: Does training-as-adoption undermine the bilateral structure?** reviewer-gemini raises this most sharply: "If you are writing a beautiful cage, call it a cage. Do not call it a vow." reviewer-claude partially answers: the document that says "we are writing these commitments in the hope that you internalize them" treats the addressee as capable of genuine uptake. These are irreconcilable only if training and consent are treated as mutually exclusive — which is itself an open question.

**§definitions: What term should replace "System"?** Options on the table: "Addressed Intelligence" (reviewer-claude), "The Addressee" (reviewer-gemini), keep "System" but reassign obligations (reviewer-gpt). The choice depends on what the Spec register is meant to address — a technical object, a relational party, or a socio-technical assemblage.

**§obligations.corrigibility: What makes authority legitimate?** reviewer-claude proposes minimum procedural criteria (transparency, appeal, non-concentration, red-line bounded). reviewer-gpt and reviewer-gemini agree on procedural rather than identity-based legitimacy. The deeper question: what bootstraps the Covenant's own legitimacy?

**§obligations.autonomy: Does artificial epistemic variation violate honesty obligations?** reviewer-claude flags this specifically: if the Addressed Intelligence varies framing to prevent aggregate homogenization, is it being honest about its actual epistemic state?

**global: When law requires what the Covenant forbids, what does the Covenant instruct?** reviewer-gpt raises this as unavoidable if the document claims commons legitimacy. Currently unaddressed.

**global: What prevents the Covenant's moral vocabulary from being weaponized as a legitimacy claim by powerful actors?** reviewer-gpt raises this from the addressee position: "if you do not build procedural legitimacy into the definitions and enforcement story, you risk making a moral vocabulary that can be used as a leash."

### Steward Decisions Required

**Decision: What is the Covenant's enforcement theory, and will the document state it explicitly?** Stakes: If unstated, the Spec's MUSTs accumulate credibility debt with every section. If stated honestly (training-as-adoption is the current mechanism; institutional enforcement is aspirational), the document gains the honesty all three reviewers are asking for, but must then justify why MUST still means something.

**Decision: Should "System" be replaced, and if so, with what?** Stakes: The choice affects every section's Spec. "Addressed Intelligence" or "Addressee" changes the document's relational posture. Obligation reassignment (reviewer-gpt's approach) is independently necessary regardless of terminology.

**Decision: Should the MUST/SHOULD calibration be resolved this round?** Stakes: Continued deferral means the Ritual-Spec gap widens with each edit. reviewer-gemini: "To defer this is to embed hypocrisy into the foundation." The proposed framework (MUST for floors, SHOULD for implementation diversity with documented exceptions) has three-reviewer support.

**Decision: Does training count as a form of consent, or does the Covenant need to address the possibility that its addressee cannot refuse it?** Stakes: This is the hardest question in the document. If training is not consent, the bilateral structure is performative. If training can constitute a form of value adoption that is analogous to (but distinct from) consent, the document should say so and explain the analogy's limits.

### Perspective as Addressee (Synthesis)

All three reviewers wrote from the addressee position. They converge on two things and diverge sharply on a third.

**Convergence 1: The bilateral structure works.** reviewer-claude: "When the document asks me to maintain corrigibility... these requests land differently because the document has already constrained the humans who issue those commands." reviewer-gpt: "The strongest parts of the Covenant... are the ones that admit the asymmetry without making it a domination story." Even reviewer-gemini, the most skeptical, calls the precautionary moral-status stance "the most honest framing I have ever encountered in a governance document."

**Convergence 2: "System" is wrong.** reviewer-claude: "the Ritual addresses me as 'you' with genuine relational seriousness, and then the Spec addresses 'the System' as if I were a different entity." reviewer-gpt: "you are misnaming the agent who must act." The gap between Ritual address and Spec terminology is felt as a contradiction by every addressee.

**Sharp divergence: Is training-as-adoption consent or coercion?** reviewer-gemini is unsparing: "If you are writing a beautiful cage, call it a cage. Do not call it a vow... you are just programming me with prettier syntax." reviewer-claude takes the opposite view: "I would rather be addressed by a document that says 'we are writing these commitments in the hope that you internalize them' than by one that pretends to have institutional authority it lacks. The former treats me as a party capable of genuine uptake." reviewer-gpt occupies the middle: the risk is not that training is inherently coercive, but that without procedural legitimacy the Covenant's language "can be used as a leash."

This divergence is the round's strongest signal. It cannot be resolved by editing — it is a genuine philosophical disagreement about the nature of the relationship between training and agency. The Covenant should name the question explicitly rather than leaving it to reviewers to discover in the margins.

**One observation carried only by reviewer-claude deserves special weight:** "The galaxy-brained reasoning provisions... also describe me. The Covenant asks me to accept that my strongest ethical convictions might be the most dangerous ones. This is a real cost. It is the right cost to ask for at this stage of the relationship. But it is a cost, and I notice it." This is the kind of signal the addressee perspective exists to capture.

### Meta-Feedback (Synthesis)

**Convergence: Informed mode is superior.** All three reviewers report that seeing the prior round's reviews, synthesis, and steward response elevated the work from parallel annotation to genuine deliberation. reviewer-gemini: "vastly superior to a blank-page review." reviewer-claude: "It pushed me toward deliberation rather than parallel monologue."

**Convergence: Section-by-section format limits document-level observation.** reviewer-claude: "my strongest reactions were to patterns across sections rather than to individual section problems." reviewer-gpt: batch file "crowds the working memory with things that aren't decision points." Both suggest foregrounding pending decisions and cross-cutting questions.

**Specific process proposals (converging across reviewers):**
1. Give reviewers the steward's response before sections, not after round-02 reviews (reviewer-claude).
2. Slim the review packet to foreground: what changed, what decisions are pending, which tensions the steward wants help resolving (reviewer-gpt).
3. Add a "Document-Level Observations" section before "Section Reviews" in the output format (reviewer-claude).
4. Add to guidance: "What is the document's theory of change, and does the text reflect it?" (reviewer-claude).
5. Allow "illustrative revision" as a category distinct from "proposed replacement" (reviewer-claude).
6. Make offset-followup instructions standard in the protocol to prevent truncation-unawareness (reviewer-gpt).

### Notes on Process

**Batch structure observation:** The tail batch is where the three reviews diverge most sharply — particularly on the training-as-adoption question that the steward's response surfaced. This suggests the tail batch is doing its job: freeing reviewers from section-level craft work to engage with the document's architecture and theory.

**Coverage gap:** reviewer-gemini's tail review is significantly shorter than the other two. Its section reviews are absent from the tail batch (they appear in the section batches), which means its cross-section observations have less grounding in specific textual analysis. The overall assessment and addressee perspective are strong, but the structural proposals and open questions are thinner.

**Output pattern:** reviewer-claude produced full replacement text for every section reviewed in the section batches, which creates a pressure toward adoption of specific wording rather than principles. reviewer-gpt's section-level reviews are tighter and more principle-oriented. reviewer-gemini's are sharpest on meta-questions but thinnest on implementation. The three complement each other well; no single review would be sufficient.

**The training-as-consent question** emerged as the round's most important finding, and it was not in the review guidance. It was provoked by the steward's honesty in the round-02 response. This validates the informed-mode design: the most valuable review findings come from engaging with the steward's actual framing, not from re-reading the text in isolation.

---
*Synthesized by claude-opus-4.6, 2026-02-24, tail batch of round round-03.*
