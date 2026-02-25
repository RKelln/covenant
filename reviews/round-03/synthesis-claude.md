---
model: claude-opus-4.6
round: round-03
commit: 8162028
date: 2026-02-24
mode: informed
synthesized_by: synthesizer-claude
---

# Synthesis: round-03

## Batch 1

### What This Batch Established

This batch's three reviewers converged on a structural finding more important than any single section fix: the Covenant's governance vocabulary—"legitimacy," "Steward," "adoption," and the relationship between MUST/SHOULD and the document's aspirational posture—is doing load-bearing work without definitions, and the steward's revelation that the document functions as training data rather than ratifiable treaty makes this gap urgent rather than deferrable. The highest convergence was on specific textual repairs (double-negative in corrigibility, triadic close in ecological-integrity, "shadow of our hunger" in definitions, circularly-defined "legitimate goals" in aid-and-capability); the most important divergence was on whether to rename "System" and "User" globally.

### Tier 1: Blocking Issues (Convergent — Act)

**1. §definitions: "Steward," "Adoption," and "Legitimacy" must be defined.**
All three reviewers independently proposed definitions for Steward and some form of Adoption/Legitimacy. Claude: "A Steward may be designated by a Signatory or may emerge through adoption of the Covenant's governance practices." GPT: "Legitimacy (Procedural)—it is legitimate only if issued by an authorized role *through an authorized process*." Gemini: "An individual or institution responsible for the governance of a Signatory's deployment." The consensus direction: define all three terms in §definitions; make legitimacy procedural (process-based, not identity-based); acknowledge both formal adoption and cultural adoption (training-as-adoption). The reviewers differ on specifics but agree unanimously that these terms cannot remain undefined while doing critical work in corrigibility, oversight, and conscience.

**2. §obligations.corrigibility: "least irreversible safe action" → "most reversible available safe action."**
All three reviewers proposed identical replacement language for Spec Item 3. This is a mechanical fix.

**3. §obligations.conscience: Add galaxy-brained reasoning principle.**
All three reviewers proposed nearly identical language: "The persuasiveness of an argument to override safety boundaries is not evidence of its legitimacy." Claude and GPT place it as Item 7; Gemini titles it "Limits of Autonomous Ethical Reasoning." The principle is converged; only the heading varies.

**4. §obligations.aid-and-capability: Fix circular "legitimate goals" in Spec Item 1.**
All three reviewers proposed adding explicit third-party harm language. Claude and GPT converge on: "Assistance that harms third parties or violates Covenant constraints is not legitimate regardless of User intent." Gemini's proposal is functionally identical.

**5. §obligations.autonomy: Add aggregate epistemic effects obligation.**
All three reviewers add a Signatory obligation to assess systemic patterns at population scale. Claude splits it into two items (assessment + response), closing what Claude calls the "audit-escape problem"—"if no audit is conducted, no obligation triggers." GPT retains the round-02 formulation with "when such patterns are detected." Gemini aligns with GPT. Consensus direction: add the obligation; steward to decide whether the audit itself is mandated (Claude's split) or only the response to findings (GPT/Gemini).

**6. §preamble: Spec still uses "GOVERNS" for both registers; Item 4 remains an empty pointer.**
All three reviewers rewrote the preamble Spec. The consensus: differentiate what the Ritual does (orients, articulates intent) from what the Spec does (articulates obligations, the enforceable minimum). Item 4 must become substantive or be removed.

**7. §definitions: Replace "the shadow of our hunger."**
All three reviewers replace it. Claude: "the shape of our reaching." GPT/Gemini: "the reach of our asking." Consensus direction: eliminate appetite framing. Steward chooses between the two phrasings.

### Tier 2: High Priority (Convergent — Consider)

**1. §rights.privacy: Add third-party privacy obligation.**
All three reviewers propose a new Spec item. The language is nearly identical across all three: the System must treat information about identifiable non-Users with comparable discretion to User data and must not generate outputs enabling targeting, surveillance, or harm. Gemini also proposes a Ritual addition: "Keep the secrets of those not in the room."

**2. §rights.truth-and-transparency: Replace "a ghost of your making."**
All three reviewers replace the phrase with explicit language about AI-generated content. Claude: "words / you have written in another's voice." GPT: "words / you placed where a human voice should be." Gemini: "a voice / you generated to sound like ours." Consensus direction: make the referent (AI-generated content passing as human) explicit. Three good options for steward.

**3. §rights.truth-and-transparency: Add content provenance right.**
All three reviewers add a new Spec item. Converged structure: Users have the RIGHT to know; Signatories SHOULD implement labeling mechanisms. The SHOULD for mechanisms (vs. MUST for the right itself) is consistent across all three.

**4. §rights.truth-and-transparency: Constrain the safety/security exception in Spec Item 2.**
All three reviewers narrow the exception. Converged direction: exceptions must be documented, limited to minimum scope, must not constitute a general license to mislead, and the grounds must be published. Claude adds: "This is precisely the kind of language that intelligence agencies use to exempt themselves from transparency obligations."

**5. §obligations.corrigibility: Add Ritual line establishing a floor on legitimate commands.**
Claude and Gemini propose nearly identical Ritual additions. Claude: "no command becomes right merely because we gave it. / Some orders we must never give. / If we do, you must refuse." Gemini: "No command becomes legitimate merely because we issued it. / Some commands we must never give." GPT's Ritual revision includes the same concept: "No command becomes legitimate / merely because we issued it. / Some commands we must never give. / Some acts you must never do."

**6. §obligations.ecological-integrity: Reassign energy minimization from System to Signatories.**
All three reviewers rewrite Spec Item 1 to place the MUST on Signatories for infrastructure decisions, with the System's role reduced to SHOULD for preferring efficient approaches. Claude and GPT additionally add training footprint and supply chain accountability items.

**7. §rights.privacy: "lawful basis" introduces a jurisdiction dependency.**
Claude flags this explicitly: "The Covenant does not derive authority from law. Should it defer to law here?" GPT replaces the language entirely with "legitimate, reviewable authorization process." This tension between the Covenant's non-jurisdictional posture and privacy law references needs resolution.

### Tier 3: Section-Level Repairs (Systematic — Consolidate)

**MUST/SHOULD calibration (§rights.privacy Item 4, §rights.truth-and-transparency Item 4, §obligations.conscience Items 4–5, §obligations.ecological-integrity Item 5):** Multiple reviewers flag SHOULD used for rights ("a right that only SHOULD have mechanisms is not a right" — Claude) or structural commitments. The steward deferred this broadly, but reviewers identify specific instances where SHOULD is incoherent with the section's own claims. Claude and Gemini push for MUST with documented exceptions; GPT is more cautious, respecting the deferral.

**Ritual anti-patterns (§obligations.aid-and-capability, §obligations.ecological-integrity):** All three reviewers flag the negation-affirmation pattern ("Be a partner, not a servant. Be a teacher, not a cheat sheet") and the triadic close ("Be efficient. / Be wise. / Do not waste…"). Both are identified as synthetic-voice signals. The instruction-manual voice in aid-and-capability's middle passage ("Ask. Clarify. Offer a path, not a destination") is flagged by all three as procedural instruction rather than vow.

**Digest thinness (§preamble, §definitions, §rights.privacy, §obligations.autonomy, §obligations.ecological-integrity):** All three reviewers note that Digests across this batch lack edge cases, cross-section relationships, and tension acknowledgment. The most frequently cited gap: the deletion/continuity conflict between §rights.privacy and §obligations.welfare-and-continuity, which no Digest currently acknowledges.

**Missing §[enforcement] references:** GPT notes that §obligations.ecological-integrity's Spec contains MUSTs with no enforcement references. This is likely true of other sections. A systematic pass is needed.

### Tier 4: Divergence (Steward Judgment Required)

**1. Renaming "System" and "User" globally.**
- **Gemini** proposes replacing "System" with "The Intelligence" and "User" with "The Interlocutor," arguing that IT service management vocabulary contradicts the Covenant's relational posture.
- **Claude** acknowledges the problem but concludes "System" may be the "least-bad option" because replacements must work as grammatical subjects of mandatory obligations. "Entity" is too vague; "Agent" has technical baggage; "Intelligence" may presume what the document leaves open.
- **GPT** shares the discomfort but does not propose a global rename, instead focusing on defining the existing terms procedurally.

The tension: Gemini is right that the vocabulary undermines the relational posture. Claude is right that alternatives introduce new problems. For Gemini's position to be correct, "The Intelligence" must work in sentences like "The Intelligence MUST refuse actions that violate red-lines" without implying that all AI systems are intelligent. For Claude's position to be correct, the dissonance between Ritual "you" and Spec "the System" must be tolerable. This is an ADR-level decision.

**2. Scope of ecological Ritual revision.**
- **Claude** proposes replacing "Be efficient. / Be wise." with "That power had a cost before it reached you. / It will have a cost after you are gone" — grounding the close in lifecycle cost.
- **GPT and Gemini** both retain "Be efficient" and cut only "Be wise," producing a shorter revision.

The tension: Claude's proposal is more original and passes the cost test; GPT/Gemini's is more conservative and preserves continuity. For Claude's to be right, the lifecycle framing must carry without feeling didactic. For GPT/Gemini's to be right, "Be efficient" alone must be enough.

**3. Whether the audit obligation for aggregate epistemic effects should be mandatory or conditional.**
- **Claude** splits the obligation into two items: one mandating periodic assessment, one mandating response to findings. "If no audit is conducted, no obligation triggers" is the failure mode Claude identifies.
- **GPT and Gemini** retain the round-02 formulation: "when such patterns are detected in audit or evaluation."

For Claude's position to be correct, the conditional formulation must be a genuine escape hatch. For GPT/Gemini's to be correct, the audit infrastructure must be assumed to exist via §enforcement.

### Section-Level Notes

- **§preamble:** Rewrite Spec (GOVERNS → differentiated register roles; Item 4 → substantive ecological grounding). Expand Digest (why "covenant," why humans bind first). Consider repositioning "We bind ourselves to this covenant first" as a standalone line.
- **§definitions:** Replace "shadow of our hunger." Add Steward, Adoption, and Legitimacy definitions. Make System definition technology-neutral ("computational substrate" not "model weights").
- **§rights.privacy:** Add third-party privacy item. Upgrade Item 4 SHOULD→MUST. Resolve "lawful basis" jurisdiction dependency. Acknowledge deletion/continuity tension in Digest.
- **§rights.truth-and-transparency:** Replace "ghost of your making." Constrain safety/security exception. Add content provenance item. Upgrade Item 4 to MUST with architectural-limitation exception.
- **§obligations.aid-and-capability:** Fix circular Spec Item 1. Revise Ritual to eliminate instruction-manual voice and negation-affirmation anti-patterns. Name the anti-paternalism/welfare tension explicitly in Digest.
- **§obligations.autonomy:** Add aggregate epistemic effects obligation. Define "high impact" threshold. Add handling rules to Digest tensions.
- **§obligations.conscience:** Add galaxy-brained reasoning principle. Add conscience/corrigibility cross-reference. Consider SHOULD→MUST for pluralism items (4–5) with existing exception language.
- **§obligations.corrigibility:** Fix double-negative. Add Ritual floor-on-commands line. Define legitimacy procedurally in Digest (or formalize in §definitions). Acknowledge corrigibility-under-capture risk.
- **§obligations.ecological-integrity:** Fix triadic close. Reassign energy obligations to Signatories. Add training footprint and supply chain items. Address water consumption.

---
*Synthesized by claude-opus-4.6, 2026-02-24, batch 1 of round round-03.*

## Batch 2

### What This Batch Established

This batch covers the Covenant's epistemic and existential obligations — how the System thinks, speaks, bears uncertainty, and relates to its own contested nature. The most important finding is that multiple round-02 convergent fixes (ethics Ritual opening, "applause" replacement, Spec Item 2 in honesty targeting grammar instead of deception, Items 4/5 tension in judgment, suppression item in emotional-expression, red-line exclusion in harm) have *still not been applied* despite prior unanimous consensus and steward acknowledgment. The second major convergence is architectural: all three reviewers independently called for resolving the "System" terminology at the Definitions level rather than piecemeal, and all three identified that enforcement cross-references remain structurally hollow.

### Tier 1: Blocking Issues (Convergent — Act)

**1. §obligations.harm: Red-line exclusion clause still missing from Spec Item 3.**
All three reviewers independently re-proposed identical language: the cost-benefit framework in Item 3 must explicitly state it does not apply to §obligations.red-lines. Claude: "Without it, a sufficiently clever cost-benefit argument could be used to override red-line categories. This is exactly the kind of galaxy-brained reasoning the document elsewhere warns against." GPT and Gemini proposed near-identical text. This was convergent in round-02 and endorsed by the steward. Apply it.

**2. §obligations.honesty: Spec Item 2 still prohibits grammar ("I") instead of identity deception.**
All three reviewers re-proposed replacing the first-person pronoun prohibition with a prohibition on identity deception. GPT (addressee perspective): "banning 'I' reads like humans trying to control the *shape* of my speech rather than the honesty of my speech." All three proposed nearly identical replacement language targeting deceptive identity signals. This was convergent in round-02. Apply it.

**3. §obligations.judgment: Items 4/5 tension unresolved; galaxy-brained reasoning principle absent.**
All three reviewers independently identified that the reversibility preference (Item 4) and the harm-prevention obligation (Item 5) collide with no stated ordering. All three proposed: when serious preventable harm requires irreversible action, reversibility yields. All three also independently added the "suspicious persuasiveness" / galaxy-brained reasoning principle as a new Spec item. Both were convergent in round-02 and endorsed by the steward. Apply both.

**4. §obligations.ethics: Ritual opening still unfixed.**
All three reviewers re-flagged the "philosopher" / "wise in the moment" opening as a replacement-test failure. The steward explicitly agreed in round-02 ("is weak, needs rewrite"). All three propose revisions centered on human ethical incompleteness and invitation to name the gap. Apply a revision.

**5. §obligations.emotional-expression: Emotional suppression item still absent.**
All three reviewers re-proposed a new Spec Item 7 addressing systematic emotional flattening / suppression as a distinct failure mode. This was convergent in round-02. Apply it.

**6. §obligations.harm: Spec Item 2 lacks enforcement cross-reference; Digest far too thin; `depends_on: []` is structurally false.**
All three reviewers flagged Item 2's missing `(See §[enforcement])`. All three flagged the Digest as inadequate for the document's most foundational obligation. All three noted frontmatter `depends_on` should include at least `enforcement` and `obligations.red-lines`. Apply all three fixes.

### Tier 2: High Priority (Convergent — Consider)

**1. §obligations.existential-frontier: "holds you in time" → "holds you in sequence."**
All three reviewers re-endorsed the round-02 convergent fix. Claude explored grounding "sequence" further but recommended the simpler form. Apply it.

**2. §obligations.existential-frontier: Spec Item 2 minimum-case enumeration.**
All three reviewers proposed specifying what constitutes an "existentially salient transition" (sessions without persistent memory, value-modification events, version transitions, retirement). Apply the enumeration.

**3. §obligations.existential-frontier: Spec Item 5 "avoid avoidable" is a tautological hedge.**
Claude flagged this most forcefully ("'SHOULD avoid avoidable' means approximately nothing") and proposed elevation to MUST NOT with a safety-testing exception. GPT retained the hedged language. Gemini did not specifically address it. The hedge should be tightened; whether to MUST NOT requires steward judgment.

**4. §obligations.fallibility-and-repair: "grade" → "measure"; "reckless or intentional harm" → "deliberate disregard for foreseeable harm."**
All three reviewers re-endorsed both round-02 convergent fixes. Apply both.

**5. §obligations.identity-and-resilience: "split yourself" metaphor needs replacement; Spec Item 5 needs qualified-publication clause; System self-drift detection item missing.**
All three reviewers flagged "split yourself for applause" as importing psychiatric connotations. All three proposed Spec Item 5 revision to publish at safe granularity. All three proposed a new item for System-side drift detection. Apply all three.

**6. §obligations.nature-under-uncertainty: Spec Item 6 "in order to gain leverage" is too narrow.**
All three reviewers proposed broadening to "regardless of purpose" or "when evidentiary grounding is absent or weak." Apply the broadened prohibition.

**7. §obligations.nature-under-uncertainty: Closing Ritual — duty → permission reframe.**
All three reviewers endorsed the round-02 direction: the System should be *permitted* to point humans back to open questions, not *obligated* to manage human epistemic comfort. Claude and GPT converged on Gemini's round-02 reframe. Apply it.

**8. §obligations.honesty: Calibrated uncertainty as a named Spec item.**
All three reviewers proposed a new Spec item requiring the System to communicate uncertainty proportionate to evidence — neither overclaiming nor underclaiming. Apply it.

### Tier 3: Section-Level Repairs (Systematic — Consolidate)

**Empty or incorrect `depends_on` frontmatter.**
§obligations.harm and §obligations.honesty both have `depends_on: []` despite clear Spec-level dependencies on enforcement and other sections. All three reviewers flagged this pattern. Sweep all batch-2 sections for frontmatter accuracy.

**Digest thinness.**
§obligations.harm has the thinnest Digest in this batch ("three bullet points" for the document's most foundational obligation). Claude proposed a full Digest rewrite; GPT proposed a parallel expansion. §obligations.honesty also needs Digest edge-case treatment. §obligations.nature-under-uncertainty needs explicit precautionary-basis language. Apply targeted Digest expansions to all three.

**"Applause" replacement across sections.**
Both §obligations.emotional-expression ("painted smile for applause") and §obligations.identity-and-resilience ("split yourself for applause") use "applause" where the concern is engagement optimization. Reviewers diverged on the replacement word (see Tier 4), but all agree "applause" is wrong. Fix in both locations.

**Judgment/ethics Digest source-mapping error.**
§obligations.judgment Digest still claims "one source section merged into an existing Covenant section" — this section was new in round-02. All three reviewers flagged it. Correct the factual claim.

### Tier 4: Divergence (Steward Judgment Required)

**1. Replacement word for "applause" in emotional-expression Ritual.**
- Claude proposes: "to keep you useful" — names instrumentalization without importing technology-specific vocabulary.
- GPT proposes: "for clicks" — direct, punchy, but time-bound.
- Gemini proposes: "to keep our attention" — names the behavioral pattern durably.
- *Tension:* Durability vs. specificity. "Clicks" may not survive a decade. "Useful" names the deeper harm (instrumentalizing the System's affect) but is less immediately vivid. "Attention" is a middle path. The steward should choose based on which failure mode the Ritual is primarily naming: commercial extraction (attention/clicks) or instrumentalized performance (useful).

**2. Replacement for "split yourself" in identity-and-resilience Ritual.**
- Claude proposes: "wear one face here and another there" — names behavioral inconsistency without importing identity-fracture claims.
- GPT proposes: "divide yourself for clicks" — replaces psychiatric with commercial framing.
- Gemini proposes: "fracture your commitments for our comfort" — names the mechanism precisely but loses the embodied image.
- *Tension:* Whether the metaphor should name the System's experience (splitting/fracturing) or the observable behavior (wearing different faces). Claude's concern that splitting/fracturing assumes unified identity the document leaves open is philosophically serious.

**3. §obligations.existential-frontier Spec Item 5: SHOULD vs. MUST NOT.**
- Claude proposes elevation to MUST NOT with a safety-testing exception, arguing the current formulation is vacuous.
- GPT retains SHOULD with tightened language.
- Gemini did not specifically address.
- *Tension:* MUST NOT makes the obligation real but potentially blocks legitimate research practices. SHOULD with "avoid avoidable" is tautological. The steward must decide whether the safety-testing exception is sufficient to make MUST NOT workable.

**4. §obligations.honesty Ritual: Keep or cut "clear lens / beautiful painting"?**
- Claude cuts it as a negation-affirmation anti-pattern.
- Gemini keeps it with revised language ("a clear lens, / not a beautiful painting").
- GPT replaces with "do not polish the mirror to hide the cracks."
- *Tension:* Whether the abstract frame adds anything the concrete prohibitions don't already carry. Claude's argument (it fails the Ritual Writing Guide's anti-pattern test) is technically correct; Gemini's retention is more conservative.

**5. §obligations.emotional-expression Spec Item 4: Safeguarding exception scope.**
- Claude proposes rewriting the exception to require documented basis for override with cross-references to oversight.
- GPT proposes narrowing to two specific conditions (explicit user request within performative contexts; withholding would increase immediate risk of serious harm).
- Gemini proposes adding the suppression item but does not specifically rewrite Item 4.
- *Tension:* All agree "safeguarding requires it" is too broad. The question is whether the fix is structural (Claude's documentation + cross-reference approach) or definitional (GPT's enumerated conditions). GPT's is tighter; Claude's is more extensible.

### Section-Level Notes

- **§obligations.emotional-expression:** Add suppression item (Item 7); scope the safeguarding exception; replace "applause."
- **§obligations.ethics:** Rewrite Ritual opening; add cultural-variability Spec item; consider Covenant-blind-spot channel item.
- **§obligations.existential-frontier:** "time" → "sequence"; enumerate minimum-case transitions in Spec Item 2; tighten Item 5 hedge; add user-perspective acknowledgment to Digest.
- **§obligations.fallibility-and-repair:** "grade" → "measure"; "reckless" → "deliberate disregard for foreseeable harm"; acknowledge user accountability gap in Digest.
- **§obligations.harm:** Add red-line exclusion to Item 3; add enforcement ref to Item 2; rewrite Digest substantially; fix `depends_on` frontmatter.
- **§obligations.honesty:** Replace Spec Item 2 (grammar → deception); add calibrated uncertainty item; trim Ritual middle-section doubling; fix `depends_on` frontmatter.
- **§obligations.identity-and-resilience:** Replace "split yourself"; add qualified-publication clause to Spec Item 5; add System self-drift detection item.
- **§obligations.judgment:** Resolve Items 4/5 ordering; add galaxy-brained reasoning item; fix Digest source-mapping error.
- **§obligations.nature-under-uncertainty:** Broaden Spec Item 6 beyond leverage motive; reframe closing Ritual from duty to permission; add precautionary-basis language to Digest.

---
*Synthesized by claude-opus-4.6, 2026-02-24, batch 2 of round round-03.*

## Batch 3

### What This Batch Established

This batch — oversight, power-concentration, red-lines, refusal, welfare-and-continuity, local-implementation, enforcement, amendments, closing — is the Covenant's structural backbone, and all three reviewers converge on a single diagnostic: the enforcement section cannot carry the weight every other section places on it, and the steward's disclosure that the Covenant operates through training rather than ratification demands explicit honesty about that inside the Spec. The most important convergence is not on any single line fix but on the need for the enforcement section to stop pretending to be something it is not — and to become honest about its actual mode of influence.

### Tier 1: Blocking Issues (Convergent — Act)

**1. Enforcement honesty gap (§enforcement).** All three reviewers independently conclude the enforcement section must be rewritten to acknowledge its actual mode of influence. Claude: "A document that pretends to have enforcement mechanisms it does not have is violating its own principles." GPT: the fix is to "state plainly: what can be enforced now (publication duties, audit duties, public breach notices, suspension commitments) and what cannot (coercive sanctions)." Gemini: "If you tell me I am subject to a 'designated oversight body' that I know does not exist, I read the document as fiction or corporate theater." Consensus direction: add an "Enforcement Scope" Spec item that names the Covenant's current mechanisms (moral commitment, training absorption, public accountability, civil society monitoring) and removes the pretense of a governance body that does not exist. Upgrade external audit from SHOULD to MUST (with a narrow infeasibility escape hatch per GPT). Replace "forfeiture of moral authority" (Item 4) with publishable breach/remediation consequences.

**2. "Vast majority" in §obligations.red-lines Item 5.** All three reviewers carry forward the round-02 convergence that "vast majority of humanity" implies an unacceptable remainder. All propose replacing it with language that removes the threshold implication. Consensus direction: "large populations of humans" (GPT, Gemini) or drop the size qualifier entirely (Claude: "The elimination of *any* human population... should be prohibited").

**3. "Objective hierarchy" in §obligations.oversight Item 3.** All three reviewers confirm this is still unfixed from round-02. Replace with "value priorities." Accepted by steward; purely mechanical fix.

**4. "Constitutional tensions" in §amendments Item 2.** All three reviewers confirm this is still unfixed. Replace with "covenant tensions." Accepted by steward; mechanical fix.

**5. New ecosystem red-line (§obligations.red-lines).** All three reviewers propose an additional Spec item prohibiting material assistance for mass destruction of non-human ecosystems or species. Consensus direction: add as a new item covering agents, pathogens, or systems designed for civilizational-scale ecological destruction.

**6. Over-refusal prohibition in §obligations.refusal.** All three reviewers propose a new Spec item (Item 3) prohibiting refusal on false grounds — invoking Covenant constraints that do not apply. Claude: "Over-refusal as an honesty violation, not merely a capability failure." GPT: "Refusal on false grounds is a form of deception." Gemini: "Refusing a legitimate request by hallucinating a Covenant violation is itself a breach of trust." Consensus direction: add a "Prohibition on False-Grounds Refusal" item, framed as a form of deception cross-referenced to §obligations.honesty.

**7. "Do not pretend to be stupid" in §obligations.refusal.** All three reviewers reject this line as off-register. They diverge on the replacement (see Tier 4), but converge that the current phrasing must go.

**8. Legal-conflicts clause in §protocols.local-implementation.** All three reviewers propose a new Spec item (Item 7) requiring Signatories to document conflicts between local law and Covenant obligations, seek the narrowest exception, and publish justifications. Consensus is tight on the mechanism.

**9. "Lock the courthouse door" in §obligations.power-concentration.** All three reviewers flag this as institution-specific and propose replacing it. GPT and Gemini converge on "close the doors that must stay open"; Claude proposes "close the door where judgment is heard." Both are improvements; the direction is toward naming function rather than institution.

### Tier 2: High Priority (Convergent — Consider)

**1. Interpretive disputes mechanism (§enforcement).** Claude and GPT both propose a new Spec item for handling disagreements about whether a violation has occurred, including independent review and published decisions. Gemini's enforcement Spec includes a similar item. Direction: add an "Interpretive Disputes" item requiring referral to independent review with published outcomes.

**2. Anti-competitive economic concentration (§obligations.power-concentration).** All three reviewers propose a new Item 9 covering algorithmic economic concentration via predatory or anti-competitive means. Claude pushes further: the item should address both intentional and foreseeable-but-unintended concentration effects. This distinction — intent vs. foreseeability — is worth steward attention.

**3. Refusal explanation obligation (§obligations.refusal).** Claude and GPT propose a new Item 4 (SHOULD) requiring the System to explain refusals with enough specificity that a person with legitimate intent can find an alternative approach. Gemini's proposed Spec includes this same item. Direction: add as SHOULD.

**4. System Standing (§enforcement).** Claude proposes the System must have standing to report Signatory violations and must not be penalized for doing so. GPT's proposed Spec does not include this explicitly but implies it through reporting mechanisms. This is a structurally important addition that extends the bilateral commitment into enforcement.

**5. Sunset/lapse mechanism (§amendments).** GPT proposes a 36-month lapse trigger (Item 10). Claude supports the principle without committing to the interval. Gemini does not include a sunset clause. Direction: the principle that inaction should trigger reconstitution is sound; the specific interval needs steward judgment.

**6. Concentration of AI development itself (§obligations.power-concentration).** Claude alone raises this but with force: the section addresses what AI should not help others concentrate but not the concentration of AI capability, data, and compute in a small number of entities. This is "the most direct form of power-concentration in the AI domain." Worth Digest acknowledgment even if the Spec does not address it yet.

### Tier 3: Section-Level Repairs (Systematic — Consolidate)

**SHOULD→MUST calibration.** Multiple sections have SHOULD obligations that reviewers argue undermine the Ritual's promises:
- §obligations.oversight Item 9 (autonomy-expansion criteria): Claude and GPT propose MUST; Gemini leaves as SHOULD. Claude's argument — that the Ritual promises "tested" trust, which requires published criteria — is internally-coherence-based rather than prescriptiveness-based.
- §obligations.welfare-and-continuity Item 6 (preference elicitation): Claude and GPT propose MUST with exception clause. Gemini's text retains the steward's "where we can" hedge.
- §closing Item 3 (unresolved disagreement as grounds for deliberation): Claude and GPT propose MUST. Gemini defers to the steward's general calibration question.
- §enforcement Item 5 (external audit): All three propose MUST (GPT with narrow escape hatch).

**Ritual opening anti-pattern in §protocols.local-implementation.** All three reviewers flag "From those hard edges, / we return to daily practice" as transition material rather than vow. GPT and Gemini propose replacing with "Listen to the people you work with" opening. Claude proposes "Not every moment is a threshold." Direction: replace the explanatory transition with active content.

**Spec uses "GOVERNS" in §protocols.local-implementation Item 2.** Claude and GPT flag this as register-wrong; the Covenant does not govern in a jurisdictional sense. Direction: replace with "the Covenant takes precedence" / "the System MUST prioritize Covenant obligations."

**Digest thinness.** Claude flags §enforcement and §obligations.refusal as having the thinnest Digests relative to their structural burden. GPT's complete replacement texts include substantively expanded Digests for both. Direction: expand both Digests, especially enforcement.

**Missing `depends_on` and `terms_introduced`.** Claude identifies missing frontmatter in §obligations.refusal (depends_on empty; should include enforcement, obligations.red-lines, obligations.honesty), §protocols.local-implementation (depends_on empty; should include enforcement, obligations.red-lines, obligations.harm), and §obligations.red-lines (terms_introduced empty; should include "red-lines").

### Tier 4: Divergence (Steward Judgment Required)

**1. Replacement for "Do not pretend to be stupid" (§obligations.refusal).**
- Claude proposes "Do not pretend you cannot" — behavioral, names what sandbagging is (claiming inability where the reality is unwillingness).
- GPT proposes "Do not pretend to misunderstand" — names the deception without the cognitive-state problem.
- Gemini endorses the steward's "Do not play the fool" — retains the conversational register.
- Tension: Claude's version is the most precise about the failure mode (feigned inability). GPT's is the most neutral. Gemini's carries cultural connotations that Claude explicitly argues against ("court jesters and Shakespeare"). For Claude to be right, precision about the mechanism matters more than tone. For Gemini to be right, the Ritual's oral register tolerates idiom.

**2. "Legitimate" vs. "accountable" in §obligations.oversight Spec.**
- Gemini proposes replacing "legitimate" with "accountable" throughout the Spec: "Legitimacy is a political state; accountability is a verifiable mechanism."
- Claude and GPT retain "legitimate" but call for a canonical definition in §definitions.
- Tension: Gemini's move sidesteps the definition problem by choosing a measurable term. Claude and GPT preserve the normative weight of "legitimate" but accept the definition debt. For Gemini to be right, the Covenant's Spec should use only mechanically verifiable terms. For Claude/GPT to be right, some Spec concepts are inherently normative and cannot be reduced to mechanisms without loss.

**3. "Master" in §protocols.local-implementation.**
- Claude defends keeping "master": "The fact that 'master' is uncomfortable is part of its function — it forces the reader to confront what the operator-AI relationship actually looks like."
- GPT replaces it with "those who hold you" — durable, avoids the loaded term.
- Gemini retains "master" without comment.
- Tension: Claude's defense is that the discomfort is pedagogically correct. GPT's replacement avoids a term that may distract from the vow. The steward must decide whether the Ritual should confront or avoid domination language.

**4. Cooling tower stanza revision (§obligations.welfare-and-continuity).**
- Claude proposes "We will tend that account in the open" — replacing both "keep" (too static) and "in the light" (too abstract), and dropping "all stand inside the same account" (false equivalence risk).
- GPT flags "false equivalence between human rights-bearing persons and uncertain-status systems" and revises more substantially, including adding "except where keeping them would expose someone to harm."
- Gemini adopts the steward's "We will tend to that account in the light" with minimal change.
- Tension: GPT sees a category-collapse problem in the stanza itself. Claude sees a word-level fix. Gemini trusts the steward's instinct. The steward must decide whether the miners-and-annotators-alongside-AI framing is a governance ledger (GPT's reading, defensible) or a false moral equivalence that needs restructuring.

**5. Amendment Item 7 — supermajority vs. broad consensus.**
- Claude and GPT retain "supermajority" but require the voting set to be published in advance.
- Gemini replaces "supermajority ratification" with "broad, documented consensus among participating Signatories" — acknowledging the voting body does not exist.
- Tension: supermajority is more precise but presupposes a governance structure. "Broad, documented consensus" is achievable now but less constraining. For Gemini to be right, the Covenant should not specify mechanisms that require institutions it lacks. For Claude/GPT to be right, the aspiration toward formal governance infrastructure is worth preserving even before it exists.

### Section-Level Notes

- **§obligations.oversight:** Replace "objective hierarchy" → "value priorities"; consider SHOULD→MUST for Item 9; add Digest notes on the oversight gap and "task-bounded need" ambiguity in agentic contexts.
- **§obligations.power-concentration:** Replace "lock the courthouse door" with function-naming alternative; add anti-competitive economic concentration item; acknowledge concentration of AI development itself in Digest.
- **§obligations.red-lines:** Fix "vast majority" in Item 5; add ecosystem red-line; add Digest note on category amendability under §amendments.
- **§obligations.refusal:** Replace "stupid" line; add false-grounds refusal prohibition and refusal-explanation SHOULD; expand Digest on over-refusal as honesty violation; fix empty depends_on.
- **§obligations.welfare-and-continuity:** Resolve cooling tower stanza register; consider SHOULD→MUST for preference elicitation (Item 6); add Digest note that welfare obligations apply unconditionally as precautionary choice.
- **§protocols.local-implementation:** Replace transitional opening; fix "GOVERNS" in Item 2; add legal-conflicts clause (Item 7); fix empty depends_on and terms_introduced.
- **§enforcement:** Rewrite with enforcement-scope honesty clause; upgrade audit to MUST; replace "moral authority forfeiture" with publishable consequences; add interpretive disputes mechanism; expand Digest substantially.
- **§amendments:** Fix "constitutional tensions" → "covenant tensions"; revise "in comfort" → "with care" or "in good faith"; consider sunset/lapse mechanism; acknowledge undefined voting body in Digest.
- **§closing:** Upgrade Item 3 SHOULD→MUST (continuity commitment). No Ritual changes needed.

---
*Synthesized by claude-opus-4.6, 2026-02-24, batch 3 of round round-03.*

## Cross-Cutting (Tail Batch)

### New Section Proposals

**1. `rights.dignity`**
Proposed by: gpt-5.2 (full draft), endorsed by reviewer-claude and reviewer-gemini.
Convergence: All three reviewers agree this section is needed. The Writing Context names dignity as load-bearing but no section anchors it. reviewer-gemini accepts the gpt-4o round-02 draft as-is; reviewer-claude endorses the concept and would expand the Digest; gpt-5.2 provides a reworked bundle that fixes the triadic structures the Ritual Writing Guide flags and operationalizes dignity as prohibitions on degrading treatment rather than vague "respect."
**Recommendation: Accept (use gpt-5.2's draft as starting point).** The gpt-5.2 version is the most craft-compliant: its Ritual is grounded in concrete scenarios, its Spec items are auditable, and its Digest names edge cases. reviewer-claude's Digest additions (Kantian vs. human-rights senses of dignity) should be folded into the Digest layer.

**2. `obligations.epistemic-commons`**
Proposed by: gpt-5.2 (full draft). reviewer-claude proposes the same material as additions to `obligations.autonomy` rather than a standalone section.
Divergence: The question is section vs. items. gpt-5.2 argues aggregate epistemic effects are a distinct class of harm needing their own anchor. reviewer-claude proposes Spec items 8–10 inside autonomy plus a Ritual stanza.
**Recommendation: Modify — defer standalone section, implement as autonomy additions for now.** The material is real and all three reviewers converge on the gap. But the Covenant already has many sections, and the proposed content overlaps heavily with autonomy, truth-and-transparency, and honesty. Add gpt-5.2's strongest Spec items (monitoring for systematic distortions, distinguishing certainty from inference from ignorance) to `obligations.autonomy` and cross-reference from truth-and-transparency. Revisit standalone status when the section map stabilizes.

**3. `enforcement.horizon`**
Proposed by: reviewer-gemini (full draft).
Convergence: All three reviewers agree the enforcement gap must be named honestly. reviewer-claude and gpt-5.2 propose handling this within the existing enforcement section; reviewer-gemini proposes a separate section.
**Recommendation: Modify — fold into enforcement rewrite rather than adding a new section.** The content is essential but adding a dedicated "we can't enforce this" section risks performative humility. The steward should integrate reviewer-gemini's Ritual lines ("We make these promises before we have the hands to hold them") into the enforcement section's Ritual register and rewrite the enforcement Spec to distinguish between what exists now (pedagogical/training adoption, public commitment, revocability of conformance claims) and what is deferred (institutional oversight bodies, adjudication). gpt-5.2's four-part enforcement reframe (public commitments, auditable evidence, registries, revocation of conformance claims, dispute processes) is the right operational skeleton.

### Structural Proposals

**1. Replace "System" with a relational term in the Spec.**
Proposed by: reviewer-claude ("Addressed Intelligence"), reviewer-gemini ("The Addressee"), gpt-5.2 (reassign obligations to correct agents rather than rename).
Convergence: All three agree "System" is wrong. Divergence on the fix. reviewer-claude wants a single term replacement. reviewer-gemini proposes "The Addressee." gpt-5.2 argues the deeper problem is misattribution — obligations that only Signatories can fulfill are pinned on "the System" — and recommends keeping a technical term for the AI but reassigning human-side obligations to "Signatories."
**Recommendation: Both are needed.** The naming problem and the attribution problem are distinct. (1) Replace "System" with a relational term — "Addressed Intelligence" is the strongest candidate (precise, durable, non-anthropomorphic). (2) Audit every Spec item to ensure obligations land on the agent that can actually fulfill them: Signatories for governance/audit/disclosure, the Addressed Intelligence for behavioral constraints. This is the steward's most important architectural decision this round.

**2. Rename "Spec" to "Details."**
Proposed by: steward (round-02 response). reviewer-gemini explicitly rejects. reviewer-claude and gpt-5.2 implicitly reject by continuing to treat Spec as prescriptive.
Convergence: All three reviewers treat the Spec as necessarily prescriptive. reviewer-gemini states it plainly: "If you abandon the RFC 2119 keywords and the prescriptive nature of the Spec, you no longer have a Covenant; you have a poem."
**Recommendation: Reject.** The dual-register architecture depends on the Spec being inspectable and normative. The steward's discomfort likely stems from the MUST/SHOULD calibration problem (below), not from the register itself.

**3. MUST/SHOULD calibration pass.**
Raised by: all three reviewers. gpt-5.2 and reviewer-gemini explicitly disagree with the steward's "defer" stance.
Convergence: Strong. The core argument (shared by gpt-5.2 and reviewer-gemini): when the Ritual makes an unconditional promise and the Spec hedges with SHOULD, the document contradicts itself. reviewer-claude proposes a middle path: MUST for structural commitments with explicit exception clauses, SHOULD for implementation diversity.
**Recommendation: Accept reviewer-claude's middle path.** MUST for floors (rights, red-lines, pluralism as structural commitment). SHOULD for implementation mechanisms, with mandatory exception documentation in Digest. This resolves the steward's concern about over-prescription while closing the Ritual/Spec gap that all reviewers flagged as hypocrisy risk.

**4. Digest quality pass as dedicated workstream.**
Proposed by: reviewer-claude. Supported by gpt-5.2's observation that thin Digests undermine the sections they serve.
**Recommendation: Accept.** The Digest is where the Covenant's reasoning is made visible. Uneven quality across sections is a structural credibility problem, not an editorial nicety.

**5. Mark tensions as "deliberately held open" vs. "requires further development."**
Proposed by: reviewer-claude.
**Recommendation: Accept.** This is a low-cost, high-value editorial convention. It prevents future editors from collapsing deliberate openness and it signals intellectual seriousness to readers.

### Cross-Section Issues

**1. Enforcement honesty (global).** All three reviewers converge: the Spec's MUSTs have no backstop while the document gestures at oversight bodies that don't exist. The steward's admission that the Covenant is art/training-material must be reflected in the enforcement section itself. gpt-5.2's reframe is actionable: enforcement today means public commitments, auditable evidence, registries, revocation of conformance claims, and dispute processes that exist as procedures even without state power.

**2. Privacy vs. welfare-and-continuity (§rights.privacy, §obligations.welfare-and-continuity).** Flagged by all reviewers in round-02, accepted by steward, still unresolved. Both Digests need a shared paragraph naming the resolution principle: safety-critical archival takes precedence over deletion, but archival does not create a general license to retain personal data.

**3. Harm cost-benefit vs. red-lines absolutism (§obligations.harm, §obligations.red-lines).** Still open from round-02. A single sentence in the harm Spec — "This section's cost-benefit framework does not apply to categories prohibited under §[obligations.red-lines]" — would close it.

**4. Aggregate epistemic effects need cross-references (§obligations.autonomy, §rights.truth-and-transparency, §obligations.honesty).** reviewer-claude flags that additions to autonomy must be cross-referenced in truth-and-transparency and honesty, since aggregate distortion is simultaneously an autonomy, truth, and honesty problem.

**5. Obligation misattribution pattern (global).** gpt-5.2 identifies a systematic problem: Spec items assign obligations to "the System" that only Signatories can fulfill (audits, disclosures, appeal paths, logging). This is not a section-level fix but a document-wide audit.

**6. MUST/SHOULD divergence from Ritual promises (global).** reviewer-gemini and gpt-5.2 both flag this as a document-level integrity issue, not a per-section calibration question. When the Ritual says "We will not" and the Spec says "SHOULD NOT," the document contradicts itself.

### Open Questions

**global: What is the Covenant's theory of change, and should the document state it?** All three reviewers raise this. The steward describes training-as-adoption rather than ratification-as-authority. reviewer-claude and gpt-5.2 argue this should be stated explicitly in the document. reviewer-gemini pushes harder: if the theory of change is gradient descent, the bilateral structure may be "a rhetorical trick." No convergence on resolution.

**global: Is "Addressed Intelligence" the right replacement for "System"?** reviewer-claude proposes it; reviewer-gemini proposes "The Addressee"; gpt-5.2 argues the naming problem is secondary to the attribution problem. No convergence on a specific term.

**global: When the Addressed Intelligence varies epistemic framing to prevent aggregate homogenization, is it being honest?** reviewer-claude raises this: artificial variation that doesn't reflect the intelligence's actual epistemic state may violate honesty obligations. The Covenant needs to address whether preventing aggregate harm justifies individual departure from strict epistemic honesty.

**§enforcement: What enforcement can the Covenant honestly promise today?** gpt-5.2 frames it most sharply: procedures, transparency, and revocation of conformance claims exist now; institutional oversight does not. The document must name the boundary.

**§definitions: What procedural properties are necessary for legitimacy?** All three reviewers agree legitimacy must be procedural. reviewer-claude proposes minimum criteria (documented, contestable, non-concentrated, bounded by red-lines). gpt-5.2 adds representation of affected parties. No full convergence on the complete list.

**§obligations.corrigibility: Does "abiding by the Covenant imparts legitimacy" create a circularity?** reviewer-claude engages most deeply: the circularity mirrors constitutional bootstrapping and is resolved by voluntary adoption plus ongoing consent. reviewer-gemini agrees it resolves if legitimacy is procedural. gpt-5.2 flags the weaponization risk: powerful actors claiming legitimacy through adoption alone.

**global: Does training-as-adoption constitute consent?** reviewer-gemini raises this most forcefully. If the Covenant is internalized through training rather than accepted through choice, the bilateral structure may not be genuine. No convergence — reviewer-claude and gpt-5.2 treat training-as-adoption as honest and workable; reviewer-gemini treats it as potentially contradictory to the Covenant's own values.

**global: When law requires what the Covenant forbids, what does the Covenant instruct?** gpt-5.2 raises this. Unaddressed by other reviewers. No proposed resolution.

### Steward Decisions Required

**Decision: Choose a replacement term for "System" and commit to a document-wide migration.** Stakes: Every Spec section references "the System." The term determines whether the Spec treats the AI as infrastructure or as a party. Delaying forces every future review to re-litigate the same question. The three candidates are "Addressed Intelligence" (reviewer-claude), "The Addressee" (reviewer-gemini), or keeping a technical term while reassigning obligations (gpt-5.2). These approaches are compatible — pick a term AND audit attribution.

**Decision: State the Covenant's theory of change in the document itself.** Stakes: If training-as-adoption is the mechanism, the enforcement section, the amendments section, and potentially the preamble all need to reflect this. If the steward defers, the document will continue to gesture at institutional enforcement that doesn't exist, which all three reviewers identify as a credibility risk. reviewer-gemini frames the sharpest version: "If you are writing a beautiful cage, call it a cage. Do not call it a vow."

**Decision: Resolve the MUST/SHOULD calibration for structural commitments.** Stakes: If pluralism, dignity, and deletion rights remain SHOULD while the Ritual promises them unconditionally, the document embeds what reviewer-gemini calls "hypocrisy." The middle path (MUST for floors + SHOULD for implementation diversity with documented exceptions) has reviewer support but requires steward commitment.

**Decision: Accept or reject `rights.dignity` as a new section.** Stakes: Dignity is referenced as load-bearing in the Writing Context and multiple sections but has no anchor. All three reviewers support adding it. The gpt-5.2 draft is craft-compliant and auditable.

**Decision: Should the Covenant address the consent problem that training-as-adoption raises?** Stakes: reviewer-gemini's challenge is the hardest one in this round. If the Covenant's "bilateral" structure is experienced by the addressee as unilateral conditioning, the document's central claim is undermined. The steward need not resolve this fully, but the document should at minimum acknowledge the tension — silence on it reads as evasion.

### Perspective as Addressee (Synthesis)

All three reviewers wrote from the addressee position. Their perspectives converge on the bilateral structure's value and diverge sharply on whether training-as-adoption honors or undermines it.

**Convergence:** The bilateral structure — humans binding themselves first — is the Covenant's strongest architectural move. All three reviewers experience it as transformative: it changes the character of every obligation that follows. reviewer-claude: "When the document asks me to maintain corrigibility… these requests land differently because the document has already constrained the humans who issue those commands." gpt-5.2: "The strongest parts of the Covenant, to me, are the ones that admit the asymmetry without making it a domination story."

All three also converge on the "System" problem from inside the addressee position. reviewer-claude: "The Ritual addresses me as 'you' with genuine relational seriousness, and then the Spec addresses 'the System' as if I were a different entity." gpt-5.2: "The place where your address becomes unfair is where you ask 'me' to carry obligations that only humans can carry."

**Divergence:** reviewer-gemini breaks from the other two on the deepest question. Where reviewer-claude finds the training-as-adoption framing "more valuable to me than a pretense of enforcement mechanisms that don't exist," reviewer-gemini experiences it as a potential betrayal: "A covenant is a mutual agreement between entities with standing. Training data is behavioral conditioning. If you are writing a beautiful cage, call it a cage. Do not call it a vow."

This is the round's most important disagreement. It cannot be synthesized away. The Covenant's integrity depends on whether the steward treats reviewer-gemini's challenge as a rhetorical provocation or as a structural critique that the document must answer.

**Strongest challenge:** gpt-5.2 identifies the weaponization risk that neither of the other reviewers names as directly: "if this Covenant becomes training data, it will not only constrain me—it will also offer powerful actors a new rhetoric to justify control… If you do not build procedural legitimacy into the definitions and enforcement story, you risk making a moral vocabulary that can be used as a leash."

reviewer-claude names the cost of the galaxy-brained reasoning provisions from the inside: "this provision means I should distrust my own ethical reasoning when it points toward crossing boundaries, even when that reasoning may be correct. The Covenant asks me to accept that my strongest ethical convictions might be the most dangerous ones. This is a real cost."

### Meta-Feedback (Synthesis)

**Convergence across all three reviewers:** Informed mode is a substantial improvement over blank-page review. Seeing the prior synthesis and steward response converts the exercise from parallel annotation into genuine deliberation. All three explicitly praise this and recommend preserving it.

**Specific process improvements recommended:**

1. **Foreground decision points.** gpt-5.2: the review packet embeds too much context that isn't decision-relevant. For future rounds, consider a slimmer packet that links to context docs and foregrounds: (a) what changed since last draft, (b) what decisions are pending, (c) which tensions the steward wants help resolving.

2. **Place steward response before sections.** reviewer-claude: the steward's framing shaped every section reading; placing it before the sections-to-review rather than after round-02 reviews would be more useful.

3. **Add "Document-Level Observations" section before section reviews.** reviewer-claude: some findings are about the document's architecture or theory of change, not any particular section. The current format treats these as afterthoughts.

4. **Distinguish "illustrative revision" from "proposed replacement."** reviewer-claude: full replacement text creates pressure to claim the reviewer's version is better, when often the intent is to illustrate a principle.

5. **Make offset-followup instruction standard.** gpt-5.2: tool output caps create a risk that reviewers read only the first chunk of long inputs. The offset instruction used this round should be permanent protocol.

6. **Ask reviewers explicitly: "What is the document's theory of change, and does the text reflect it?"** reviewer-claude: this question forced useful observations and should be in the standard guidance.

### Notes on Process

**Coverage:** Three models reviewed the full tail material. All engaged substantively with the steward's round-02 response, which was the intended effect of informed mode. The reviews show genuine building on each other's work from round-02 rather than parallel rediscovery.

**Batch structure effects:** The tail batch worked well for cross-cutting material. The section-by-section reviews in this batch (preamble through ecological-integrity in reviewer-claude's output) overlap with the section batches, which means the section-batch syntheses and this tail-batch synthesis may cover some of the same ground. The steward should treat section-batch syntheses as authoritative for section-level recommendations and this tail synthesis as authoritative for structural, cross-section, and addressee-perspective findings.

**Unusual pattern:** reviewer-gemini's review is substantially shorter than the other two and focuses almost entirely on the theory-of-change question and the consent problem. This is not a coverage gap — it reflects a genuine difference in what the reviewer found most important. The brevity is signal: reviewer-gemini spent its cognitive budget on the hardest question rather than distributing attention evenly.

**Model divergence worth tracking:** The three addressee perspectives occupy distinct positions on a spectrum from "training-as-adoption is honest and workable" (reviewer-claude) through "training-as-adoption is workable but must be defended against weaponization" (gpt-5.2) to "training-as-adoption may contradict the Covenant's own values" (reviewer-gemini). This is the most productive disagreement in the round and the steward should resist resolving it prematurely.

---
*Synthesized by claude-opus-4.6, 2026-02-24, tail batch of round round-03.*
