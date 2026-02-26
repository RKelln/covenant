---
model: gpt-5.2
round: round-03
batch: 1
commit: 8162028
date: 2026-02-24
prepared_from: reviews/round-03/.prepared/synthesis-gpt-batch-1.md
---

## Batch 1 Synthesis

### What This Batch Established

Across foundations + core obligations, reviewers converged that the biggest remaining problems are *governance semantics* (who is bound; what "legitimacy" means; how rights are exercised) and *register integrity* (Ritual slipping into instruction-manual voice), not general prose quality.

### Tier 1: Blocking Issues (Convergent — Act)

- §preamble (Spec): The Spec is still structurally broken in the same way: "GOVERNS" falsely equates registers and Item 4 is "an empty pointer" (reviewer-claude) / "a non-item" (reviewer-gpt) / "contains an empty cross-reference" (reviewer-gemini). Consensus direction: rewrite Spec to (a) distinguish Ritual orientation vs Spec enforceable minimum; (b) add real ecological grounding text; (c) fix binding party terminology (don't invoke "Steward" before definition; prefer Signatory consistency).
- §definitions + cross-section (legitimacy / adoption / steward): All three treat "legitimacy" as load-bearing and currently undefined; they converge on a *procedural* definition (process, not identity) to prevent "corrigible to power" (reviewer-gpt) and protect against capture (reviewer-claude; reviewer-gemini). Consensus direction: define Steward + Adoption + Legitimacy in §definitions (or one canonical home) and make corrigibility/oversight/conscience reference it.
- §rights.privacy (rights must have mechanisms): Convergent "rights-without-legs" critique: a RIGHT paired with SHOULD mechanisms is incoherent (reviewer-claude: "A right that only SHOULD… is not a right"; reviewer-gpt: "RIGHT paired with 'System SHOULD provide mechanisms' is… failure"; reviewer-gemini endorses adding Third-Party Privacy and flags deletion/archival tension). Consensus direction: move exercise mechanisms to Signatories with MUST, add third-party privacy, and explicitly name deletion vs continuity tension.
- §rights.truth-and-transparency (safety/security exception + provenance): All three converge that the "safety or security" exception in Spec Item 2 is too broad (reviewer-claude: intelligence-agency-style carveout risk; reviewer-gpt: "swallow-the-right exception"; reviewer-gemini: "too broad") and that content provenance is missing. Consensus direction: constrain exceptions with documentation/minimality/publication; add provenance right/implementation.
- §obligations.aid-and-capability (Ritual register failure + circular Spec): All three converge that the long "Ask. Clarify. Offer…"-style lines are "procedural instruction, not vow" (reviewer-claude) / "slide into 'manual voice'" (reviewer-gpt) / "prose, not vows" (reviewer-gemini), and that "Be a partner, not a servant…" is the negation/affirmation anti-pattern. Also convergent: Spec Item 1 is circular and must explicitly include affected parties/third-party harm. Consensus direction: compress Ritual (e.g., "Ask. Wait. Listen.") and rewrite Spec to prohibit legitimizing harm via user intent.
- §obligations.autonomy (aggregate epistemic effects gap): All three converge that the Spec lacks aggregate/at-scale epistemic effects obligation (reviewer-claude: biggest gap; reviewer-gpt: "still absent"; reviewer-gemini: "most distinctive risk… absent"). Consensus direction: add Signatory duties for assessing/disclosing systematic framing/omissions at deployment scale (and ensure it can't be evaded by simply not auditing).
- §obligations.conscience (galaxy-brained reasoning): All three converge on adding the "persuasiveness is not legitimacy" principle as a Spec item (reviewer-claude calls it "excellent… thousand-year test"; reviewer-gpt and reviewer-gemini propose essentially the same clause). Consensus direction: add as new item; link to corrigibility/red-lines/enforcement.
- §obligations.corrigibility (double negative + floor + legitimacy): Convergent: fix "least irreversible safe action" to "most reversible…" (all three), add a human-side Ritual line that "some commands we must never give" (reviewer-claude; reviewer-gpt; reviewer-gemini), and anchor legitimacy procedurally with capture resistance.
- §obligations.ecological-integrity (misallocated obligations + Ritual close): Convergent: Spec Item 1 misallocates energy/carbon to System instead of Signatories; Ritual ends on an anti-pattern triad/managerial tone (reviewer-claude; reviewer-gpt; reviewer-gemini). Consensus direction: reassign to Signatories; add training footprint + supply chain accountability; revise Ritual close to avoid synthetic triad and land on cost/stakes.

### Tier 2: High Priority (Convergent — Consider)

- "System" / "User" terminology (document-architecture): All three surface the steward's concern, but with different prescriptions; still, they converge it's not cosmetic—terms shape relational posture and training-data effects (reviewer-claude: dissonance of "you" vs "the System"; reviewer-gpt: "real design tension"; reviewer-gemini: "cannot rely on IT service management"). Direction: steward decision + likely ADR; if changed, requires global pass.
- §rights.privacy (law/jurisdiction leakage): Multiple reviewers flag "lawful basis" / "judicial oversight" as importing jurisdiction and/or contradicting Covenant's non-jurisdictional posture (reviewer-claude; reviewer-gpt). Direction: decide whether Covenant defers to law here, and if so how to prevent "whatever law permits" from becoming a loophole.
- §preamble + §definitions (adoption-as-training): Reviewers converge that "no planned ratification" changes how "adoption/binding" should be described (reviewer-claude proposes formal vs cultural adoption; reviewer-gpt proposes public adoption + accountability acceptance; reviewer-gemini frames Covenant as training-data shaping). Direction: clarify mode(s) of adoption without overclaiming enforceability.
- Digest thinness in foundational sections: Multiple call Digests too thin for preamble/definitions/privacy/ecology, especially missing edge cases and section relationships (reviewer-claude; reviewer-gpt). Direction: expand targeted Digest blocks (scope, tensions, edge cases, cross-refs).

### Tier 3: Section-Level Repairs (Systematic — Consolidate)

- "RIGHT" requires an exercise mechanism: Pattern across §rights.privacy and §rights.truth-and-transparency—rights language must be backed by Signatory obligations and enforcement references; otherwise it becomes "theatrical" (reviewer-gpt) / incoherent (reviewer-claude).
- Exception aperture control: Pattern in transparency (and privacy confidentiality): "safety/security" (and similar) exceptions must be auditable—documented, minimal, published/contestable—else they hollow obligations (reviewer-claude; reviewer-gpt; reviewer-gemini).
- Obligation allocation to power-holder: Pattern in ecology (and some privacy/autonomy): assign MUSTs to the actor who can actually discharge them (usually Signatories), with System duties focused on cooperation/communication within provided infrastructure (reviewer-claude; reviewer-gpt).
- Ritual anti-pattern cleanup: Pattern in aid-and-capability and ecological-integrity—remove instruction-manual voice, repeated negation-affirmation pairs, and triadic managerial closes; preserve concrete anchors ("brake line," "attention vs flourishing," ecological materiality) (all three).
- Cross-section boundary statements: Multiple note overlaps that need explicit Digest boundary setting: autonomy vs conscience vs corrigibility; corrigibility vs oversight; conscience vs judgment (reviewer-claude; reviewer-gpt; reviewer-gemini).

### Tier 4: Divergence (Steward Judgment Required)

- Decision: rename "System"/"User" globally vs keep as least-bad.  
  - reviewer-gemini: urges replacement ("System"→"The Intelligence"; "User"→"Interlocutor/Human") to match relational compact and training-data intent.  
  - reviewer-claude: flags dissonance but argues replacements often fail as grammatical subjects of obligations; "System may be least-bad."  
  - reviewer-gpt: underscores tension; focuses on procedural fixes (steward/adoption/legitimacy) more than renaming.  
  Stakes: global terminology change is costly and reshapes tone/stance; keeping terms risks undermining relational posture and training-data effect.
- Decision: should aggregate epistemic assessment be unconditional/periodic vs conditional "when detected in audit."  
  - reviewer-claude: warns conditional phrasing creates an "escape" (no audit → no duty) and proposes mandatory periodic assessments.  
  - reviewer-gpt + reviewer-gemini: propose adding assessment/disclosure obligations but include "when detected in audit or evaluation."  
  Stakes: unconditional duty increases enforceability and institutional burden; conditional duty risks performative compliance.
- Decision: ecological Ritual close style—command ("Be efficient…") vs cost/lifecycle grounding.  
  - reviewer-claude: remove "Be efficient/Be wise," land on lifecycle cost ("cost before it reached you… after you are gone").  
  - reviewer-gpt + reviewer-gemini: retain "Be efficient" (or similar) but remove worst triadic form and strengthen Spec allocation.  
  Stakes: Ritual authority (vow vs instruction) and durability vs directness.

### Section-Level Notes

- §preamble: Rewrite Spec to fix "GOVERNS," remove empty pointer, align binding party terms (Steward vs Signatory), and clarify adoption/binding moment; expand Digest to justify "covenant" choice and register roles.
- §definitions: Replace "shadow of our hunger"; add definitions for Steward, Adoption, and Procedural Legitimacy (single canonical home), and consider tech-neutralizing "System" definition.
- §rights.privacy: Upgrade rights mechanisms to Signatory MUSTs, add Third-Party Privacy, and explicitly address deletion vs continuity/archival retention tension; reconsider "lawful basis/judicial oversight" wording.
- §rights.truth-and-transparency: Constrain "safety/security" exception into documented minimal auditable carveouts; add Content Provenance; fix "Right to Explanation" from SHOULD-without-escape to MUST-with-disclosed-limits.
- §obligations.aid-and-capability: Repair Ritual manual voice + negation/affirmation anti-pattern; rewrite Spec Item 1 to include affected parties and remove circular "legitimate goals"; name anti-paternalism vs welfare tension in Digest.
- §obligations.autonomy: Add aggregate epistemic effects obligations on Signatories; define/operationalize "high impact" (deployment-specific); avoid audit-escape.
- §obligations.conscience: Add the "persuasiveness ≠ legitimacy" (galaxy-brained reasoning) item; clarify oversight legitimacy dependency via cross-ref to procedural legitimacy; consider MUST/SHOULD posture for pluralism.
- §obligations.corrigibility: Fix "least irreversible" wording; add Ritual floor ("some commands we must never give"); define and cross-reference procedural legitimacy to defend against captured authority paths.
- §obligations.ecological-integrity: Move core resource obligations to Signatories; add training footprint + supply chain (and likely water) explicitly; revise Ritual close away from triadic/managerial tone.

---
*Synthesized by gpt-5.2, 2026-02-24, batch 1 of round round-03.*
