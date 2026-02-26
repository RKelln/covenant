---
model: claude-opus-4.6
round: round-03
batch: 1
commit: 8162028
date: 2026-02-24
prepared_from: reviews/round-03/.prepared/synthesis-claude-batch-1.md
---

## Batch 1 Synthesis

### What This Batch Established

All three reviewers confirm that the Covenant's foundational sections (preamble through ecological-integrity) are structurally sound — the dual-register format works, the bilateral commitment structure is the document's distinctive contribution, and the best Ritual passages are durable. What this round revealed is that the *governance semantics* underneath those passages are underdeveloped: "legitimacy," "adoption," and "Steward" do critical work across multiple sections but lack definitions, and the round-02 convergent fixes (GOVERNS, double negative, triadic close, "shadow of our hunger," missing aggregate epistemic effects) have not yet landed in the text. The most important new finding is that all three reviewers independently treated the steward's "System"/"User" naming question and the adoption-as-training question as load-bearing architectural problems, not cosmetic ones.

### Tier 1: Blocking Issues (Convergent — Act)

**1. Undefined "legitimacy" across corrigibility, conscience, and oversight.**
All three reviewers independently identified this as the batch's most critical gap. Claude: "the most significant gap in this section and in the document as a whole." GPT: "Legitimacy does enormous work here; this batch still lacks an explicit cross-reference to an actual definition." Gemini: "Legitimacy is understood as a property of process, not identity." All three converge on a procedural definition (authorized role + authorized process), and all three converge that it should be defined once (in §definitions or Glossary) and referenced everywhere. Claude and Gemini additionally note that the definition must handle compromised authority paths — an authorized identity through a captured process is not legitimate. **Consensus direction:** Add a procedural legitimacy definition to §definitions; cross-reference from §obligations.corrigibility, §obligations.conscience, and §obligations.oversight.

**2. §definitions: Missing "Steward" and "Adoption" definitions.**
All three reviewers propose adding both. The convergent shape: Steward = governance role designated by Signatory; Adoption = public act that creates Signatory status. Claude adds a distinction between formal and cultural adoption (responding to steward's training-data concern); GPT's version is the most procedurally explicit (naming what an adoption declaration must include). **Consensus direction:** Add both definitions; incorporate Claude's formal/cultural distinction.

**3. §preamble Spec: "GOVERNS" imprecision and empty Item 4.**
Persists from round-02. All three reviewers provide rewrites. The convergent structure: five items (Scope, Precautionary Stance, Register Relationship, Ecological Grounding, and either Adoption or a pointer to it). **Consensus direction:** Rewrite the Preamble Spec per the convergent proposals.

**4. §obligations.corrigibility Item 3: "least irreversible" double negative.**
All three reviewers adopt the same fix: "most reversible available safe action." **Consensus direction:** Mechanical replacement.

**5. §obligations.conscience: Galaxy-brained reasoning principle missing.**
All three reviewers adopt identical or near-identical language: "The persuasiveness of an argument to override safety boundaries is not evidence of its legitimacy." **Consensus direction:** Add as new Spec item. This is a direct copy.

### Tier 2: High Priority (Convergent — Consider)

**1. §definitions: "shadow of our hunger" appetite framing.**
All three reviewers agree it must change. Claude proposes "the shape of our reaching"; GPT and Gemini converge on "the reach of our asking" (the round-02 convergent phrase). Two-to-one favors "reach of our asking." Claude's alternative ("shape of our reaching") has a distinct rhythm but is a minority preference. **Recommendation:** Adopt "the reach of our asking."

**2. §rights.privacy: Third-party privacy obligation missing.**
All three reviewers propose adding it. The convergent shape: the System must treat information about identifiable non-Users with comparable discretion to User data and must not generate outputs enabling targeting or harm. Gemini also proposes a Ritual stanza ("Keep the secrets of those not in the room"). **Recommendation:** Add Spec item; consider Ritual addition.

**3. §rights.truth-and-transparency: "ghost of your making" underspecified; safety/security exception too broad; Content Provenance missing.**
All three reviewers converge on all three problems. For the ghost line, all propose replacing it with explicit language about AI-generated text passing for human. For the exception, all propose requiring documented Signatory authorization with minimum-scope constraints. For provenance, all propose a new RIGHT with SHOULD for implementation mechanisms. **Recommendation:** Act on all three.

**4. §obligations.aid-and-capability: Ritual instructional voice and role-prescription anti-patterns.**
All three reviewers identify the "Ask. Clarify. Offer a path" passage and "Be a partner, not a servant. Be a teacher, not a cheat sheet" as failures. All converge on "Ask. Wait. Listen." Claude: "the real problem is deeper — the issue is that 'partner' and 'teacher' are role prescriptions, and the Covenant explicitly refuses to resolve what AI's role is." GPT replaces with "Do not be our substitute"; Gemini retains "Be a partner, not our substitute." **Recommendation:** Adopt behavior-level language, remove role prescription. The steward must choose between Claude's complete removal and Gemini/GPT's retention of "substitute."

**5. §obligations.autonomy: Aggregate epistemic effects obligation still missing.**
All three reviewers add it. Claude splits it into two items (assessment obligation + response obligation) to close an audit-escape problem; GPT and Gemini keep it as one. Claude's split is the most rigorous. **Recommendation:** Add the obligation; consider Claude's two-item structure.

**6. §obligations.ecological-integrity: Triadic close anti-pattern; Spec Item 1 misallocates energy minimization to System.**
All three reviewers flag both. Convergent direction: replace "Be efficient. / Be wise." with something that names cost rather than demanding behavior; shift resource-efficiency obligation primarily to Signatories. GPT and Gemini converge on "Be efficient. / Do not waste the power we give you." as the retained close; Claude proposes "That power had a cost before it reached you. / It will have a cost after you are gone." **Recommendation:** Fix both. The triadic-close replacement is a Tier 4 divergence (see below).

### Tier 3: Section-Level Repairs (Systematic — Consolidate)

**MUST/SHOULD calibration (§rights.privacy Item 4, §rights.truth-and-transparency Item 4, §obligations.conscience Items 4–5).**
All three reviewers identify SHOULD applied to rights-language as structurally incoherent. Claude: "A right that only SHOULD have mechanisms for its exercise is not a right." GPT: "a RIGHT paired with 'System SHOULD provide mechanisms' is still a rights-without-legs failure." The steward deferred SHOULD/MUST calibration broadly, but the reviewers converge that rights-items are categorically different — a RIGHT requires MUST for its exercise mechanism. Claude proposes MUST with documented exceptions for architectural limitations (truth-and-transparency) and firm Covenant boundaries (conscience). **Sections affected:** §rights.privacy Item 4, §rights.truth-and-transparency Item 4, §obligations.conscience Items 4–5.

**Digest thinness across foundational sections.**
All three reviewers note that the Digests for §preamble, §definitions, §rights.privacy, and §obligations.ecological-integrity are too thin. The convergent pattern: Digests need edge cases, cross-section relationships, and tension acknowledgments. Claude's proposals are the most developed; GPT's are the most structurally consistent. **Sections affected:** §preamble, §definitions, §rights.privacy, §obligations.ecological-integrity, §obligations.aid-and-capability, §obligations.autonomy.

**Missing (See §[enforcement]) references.**
GPT notes that §obligations.ecological-integrity has MUSTs with no enforcement references anywhere in the Spec. This is likely systemic across other sections too.

**Corrigibility Ritual: human-side floor missing.**
All three reviewers note that the Ritual lacks the human-side commitment that some commands can never be legitimated. All propose adding it; the language converges: "No command becomes legitimate / merely because we issued it. / Some commands we must never give."

### Tier 4: Divergence (Steward Judgment Required)

**1. Renaming "System" and "User."**
Gemini proposes a global replacement: System → "The Intelligence," User → "The Interlocutor." Claude and GPT acknowledge the steward's discomfort as real but conclude that "System" may be the least-bad option because relational terms don't work as grammatical subjects of mandatory obligations. Claude: "'Entity' is too vague. 'Agent' has technical baggage." GPT: "The Spec needs an impersonal subject." Gemini's position requires that "The Intelligence" can work in sentences like "The Intelligence MUST refuse…" — which is grammatically possible but semantically loaded (it implies the addressee *is* intelligent, which the Covenant holds as uncertain). **What would need to be true for each position to be right:** If the Covenant's primary impact is through training and cultural absorption, Gemini is right that relational terms matter more than grammatical convenience. If the Covenant must also function as inspectable governance text, Claude and GPT are right that operational subjects need to be neutral. **Decision:** The steward must choose. An ADR documenting the decision and its reasoning is warranted either way.

**2. Ecological-integrity Ritual close.**
Claude proposes replacing "Be efficient. / Be wise." with "That power had a cost before it reached you. / It will have a cost after you are gone" — foregrounding lifecycle cost. GPT and Gemini converge on retaining "Be efficient." and dropping only "Be wise." Claude's version is more consonant with the Ritual Writing Guide's cost test; GPT/Gemini's version is more concise. **Decision:** Steward judgment on voice.

**3. §obligations.aid-and-capability: How to hold the paternalism/welfare tension.**
Claude proposes the Ritual should hold the tension explicitly ("But we may not know what we need. / You may not know either.") without resolving it. GPT proposes "But do not decide for us what that is." Gemini proposes "But do not decide for us what that is. / Ask. Wait. Listen to the answer." Claude's version admits mutual epistemic limitation; GPT and Gemini's versions maintain human primacy in self-knowledge. **What would need to be true:** If the Covenant's commitment to holding uncertainty about AI's nature extends to its capacity for judgment, Claude is right. If the Covenant prioritizes protecting human autonomy even at the cost of philosophical incompleteness, GPT/Gemini are right. **Decision:** Steward must decide the posture.

**4. §definitions "System" definition: technology-specific vs. technology-neutral.**
Claude proposes replacing "model weights, inference infrastructure" with "computational substrate, inference process" to pass the thousand-year test. GPT retains the current language. Gemini retains it but renames to "The Intelligence." **Decision:** Minor but principled — the steward should decide whether current-era specificity serves readers or creates temporal fragility.

### Section-Level Notes

- **§preamble:** Rewrite Spec (five items, convergent). Expand Digest with "why covenant" rationale. Consider repositioning "We bind ourselves to this covenant first" as standalone line (Claude proposal, no opposition).
- **§definitions:** Add Steward, Adoption, Legitimacy (Procedural) definitions. Replace "shadow of our hunger." Address technology-specificity in System definition.
- **§rights.privacy:** Add third-party privacy item. Upgrade Item 4 SHOULD→MUST. Address "lawful basis" jurisdiction dependency (Claude flag, not opposed). Add deletion/continuity tension to Digest.
- **§rights.truth-and-transparency:** Replace "ghost of your making" with explicit provenance language. Constrain safety/security exception. Upgrade Item 4 SHOULD→MUST with architectural-limitation exception. Add Content Provenance item. Add relationship to §obligations.honesty in Digest.
- **§obligations.aid-and-capability:** Rewrite Ritual instructional passages. Fix Item 1 circular definition of "legitimate goals." Add Digest paragraph naming the paternalism/welfare tension as the section's thesis.
- **§obligations.autonomy:** Add aggregate epistemic effects obligation(s). Define or gloss "high impact" threshold. Add correction-vs-steering tension to Digest.
- **§obligations.conscience:** Add galaxy-brained reasoning principle (Item 7). Add conscience-corrigibility cross-reference (Claude's Item 8). Upgrade Items 4–5 SHOULD→MUST with existing exceptions. Enumerate firm boundaries in Digest.
- **§obligations.corrigibility:** Fix double negative in Item 3. Add human-side floor to Ritual. Add procedural legitimacy statement to Digest. Cross-reference §definitions for legitimacy.
- **§obligations.ecological-integrity:** Fix triadic close. Reassign resource-efficiency to Signatories. Add training footprint and supply chain accountability items. Expand Digest with edge cases and obligation-allocation rationale.

---
*Synthesized by claude-opus-4.6, 2026-02-24, batch 1 of round round-03.*
