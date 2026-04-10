---
marp: true
theme: default
paginate: true
size: 16:9
footer: "Covenant Review Pipeline"
style: |
  img {
    max-width: 100%;
    max-height: 580px;
    width: auto;
    height: auto;
    display: block;
    margin: auto;
  }
---
<!-- AGENT:NAV
purpose:Multi-model review pipeline flow
lines:611
nav[20]{s,n,name,about}:
43,9,#Covenant Multi-Model Review Pipeline,Review pipeline by multiple agents
52,11,#Why Multi-Model Review?,Why parallel models improve editing
63,27,#The Core Pattern,Synthesis pattern overview
90,56,#Round 1: Independent Review,First pass from independent agents
146,12,#Context Documents for Reviewers,Reviewer input sources
158,21,#What Reviewers Produce,Per-section proposals and flags
160,19,###Per section: Assessment + Proposed Changes + Flags,Section-level assessment output
179,21,#Synthesis: Human Steward,Steward convergence and judgment
200,26,#Synthesis Document Structure,How synthesis captures decisions
226,51,#Round 2: Informed Review,Second pass with prior context
277,15,#Round 2: Deliberation,Model-to-model discussion phase
292,61,#Applying Changes: Three Phases,Apply edits through staged tiers
353,19,#The Editor Agent Constraint,Trust rule for verbatim edits
355,17,###Verbatim-or-nothing,Editors only apply agreed text
372,12,#Key Design Principles,Principles preventing ordering drift
384,211,#The `/review-section` Skill,Skill flow for interactive review
386,209,###Interactive human-AI deliberation,Human-led dialogue with agents
595,16,#Diminishing Returns,Criteria for stopping review rounds
611,17,#Summary,What this process improves
628,9,#Questions?,How to find related documentation
-->

# Covenant Multi-Model Review Pipeline

**How AI agents review and co-author a living document**

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Why Multi-Model Review?

### Parallel-then-synthesize

- Different models have different training data, different blind spots
- Convergence across models = strong editorial signal
- Divergence surfaces genuine questions a single reviewer would miss
- Human steward provides final judgment and accountability

---

# The Core Pattern

```d2
direction: right
Draft -> A
Draft -> B
Draft -> C
A -> Syn
B -> Syn
C -> Syn
Syn -> Rev
Draft.style.fill: "#e3f2fd"
A.style.fill: "#c8e6c9"
A.label: "Claude"
B.style.fill: "#c8e6c9"
B.label: "GPT"
C.style.fill: "#c8e6c9"
C.label: "Gemini"
Syn.shape: "diamond"
Syn.style.fill: "#fff9c4"
Syn.label: "Synthesis"
Rev.style.fill: "#d1ecf1"
Rev.label: "Revisions"
```

---

# Round 1: Independent Review

```d2
direction: right

# Context docs feed into context box
wc.shape: "rectangle"
wc.style.fill: "#fafafa"
wc.label: "writing_context"
rg.shape: "rectangle"
rg.style.fill: "#fafafa"
rg.label: "ritual_guide"
sg.shape: "rectangle"
sg.style.fill: "#fafafa"
sg.label: "style_guide"
ar.shape: "rectangle"
ar.style.fill: "#fafafa"
ar.label: "agent_reviews"
rp.shape: "rectangle"
rp.style.fill: "#fafafa"
rp.label: "review_prompt"
d.shape: "rectangle"
d.style.fill: "#e3f2fd"
d.label: "Draft"

# Chain of context docs -> context box
wc -> rg -> sg -> ar -> rp -> d -> cx

cx.shape: "rectangle"
cx.style.fill: "#f5f5f5"
cx.style.stroke: "#999"
cx.label: "Context"

# Reviewers vertical
a.shape: "rectangle"
a.style.fill: "#c8e6c9"
a.label: "Claude"
b.shape: "rectangle"
b.style.fill: "#c8e6c9"
b.label: "GPT"
c.shape: "rectangle"
c.style.fill: "#c8e6c9"
c.label: "Gemini"

# Context feeds reviewers
cx -> a: {style.stroke: "#aaa"; style.stroke-dash: 5}
cx -> b: {style.stroke: "#aaa"; style.stroke-dash: 5}
cx -> c: {style.stroke: "#aaa"; style.stroke-dash: 5}

a -> ra: {shape: "rectangle"; style.fill: "#e8f5e9"; label: "Review:\nClaude"}
b -> rb: {shape: "rectangle"; style.fill: "#e8f5e9"; label: "Review:\nGPT"}
c -> rc: {shape: "rectangle"; style.fill: "#e8f5e9"; label: "Review:\nGemini"}
```

---

# Context Documents for Reviewers

| Document | Purpose |
|----------|---------|
| `writing_context.md` | What Covenant is, voice, two-register architecture |
| `good_ritual_writing_guide.md` | Craft guide for spoken/poetic register |
| `style_guide.md` | Formatting, RFC 2119 keywords, conventions |
| `agent_reviews.md` | Review process, roles, synthesis format |
| `review_prompt.md` | Round-specific instructions |

---

# What Reviewers Produce

### Per section: Assessment + Proposed Changes + Flags

```markdown
### §rights.dignity: The Right to Dignity

**Assessment:** 
The Ritual opening is compelling but the transition to 
the Spec register creates a semantic gap...

**Proposed Changes:**
- Ritual: Strengthen the third stanza's parallel structure
- Spec: Add enforcement reference to §enforcement.remedy

**Flags:**
- Does §obligations.corrigibility properly constrain this?
```

---

# Synthesis: Human Steward

```d2
direction: right

a -> sw
b -> sw
c -> sw

sw.shape: "diamond"
sw.style.fill: "#fff9c4"
sw.label: "Steward\nSynthesis"

sw -> cv: {shape: "rectangle"; style.fill: "#e3f2fd"; label: "Convergence"}
sw -> dv: {shape: "rectangle"; style.fill: "#fce4ec"; label: "Divergence"}
sw -> uq: {shape: "rectangle"; style.fill: "#f3e5f5"; label: "Unique"}
sw -> ac: {shape: "rectangle"; style.fill: "#e8f5e9"; label: "Accepted\nChanges"}
```

---

# Synthesis Document Structure

```markdown
# Round 1 Synthesis

**Models:** Claude Opus, GPT 5, Gemini 3
**Date:** 2025-01-15

## Convergence
[Where models agree — high confidence]

## Divergence
[Where models disagree — editorial questions]

## Unique Observations
[One model noticed something others missed]

## Accepted Changes
[Specific edits to make]

## Deferred Questions
[Open issues for next round]
```

---

# Round 2: Informed Review

```d2
direction: right

rv.shape: "rectangle"
rv.style.fill: "#e3f2fd"
rv.label: "Revised\nDraft"

pr.shape: "rectangle"
pr.style.fill: "#ffecf2"
pr.label: "Round 1\nReviews"

s1.shape: "diamond"
s1.style.fill: "#fff9c4"
s1.label: "Synthesis 1"

cx.shape: "rectangle"
cx.style.fill: "#f5f5f5"
cx.label: "Context\nDocs"

a.shape: "rectangle"
a.style.fill: "#c8e6c9"
a.label: "Claude"
b.shape: "rectangle"
b.style.fill: "#c8e6c9"
b.label: "GPT"
c.shape: "rectangle"
c.style.fill: "#c8e6c9"
c.label: "Gemini"

rv -> a: {style.stroke: "#888"; style.stroke-dash: 5}
rv -> b: {style.stroke: "#888"; style.stroke-dash: 5}
rv -> c: {style.stroke: "#888"; style.stroke-dash: 5}
pr -> a: {style.stroke: "#888"; style.stroke-dash: 5}
pr -> b: {style.stroke: "#888"; style.stroke-dash: 5}
pr -> c: {style.stroke: "#888"; style.stroke-dash: 5}
s1 -> a: {style.stroke: "#888"; style.stroke-dash: 5}
s1 -> b: {style.stroke: "#888"; style.stroke-dash: 5}
s1 -> c: {style.stroke: "#888"; style.stroke-dash: 5}
cx -> a: {style.stroke: "#888"; style.stroke-dash: 5}
cx -> b: {style.stroke: "#888"; style.stroke-dash: 5}
cx -> c: {style.stroke: "#888"; style.stroke-dash: 5}

a -> ra: {shape: "rectangle"; style.fill: "#e8f5e9"; label: "Review 2:\nClaude"}
b -> rb: {shape: "rectangle"; style.fill: "#e8f5e9"; label: "Review 2:\nGPT"}
c -> rc: {shape: "rectangle"; style.fill: "#e8f5e9"; label: "Review 2:\nGemini"}
```

---

# Round 2: Deliberation

### Models can now engage with each other

> "GPT raises a valid concern about enforcement in §X. I agree, but would approach it differently..."

> "Claude's proposed opening is stronger than mine. I withdraw mine in favor."

- Models respond to points raised by others
- Convergence deepens or divergence sharpens
- Only the *immediately preceding* round is included as context
- Earlier rounds are noise, not signal

---

# Applying Changes: Three Phases

```d2
direction: right

sy -> p1
p1.shape: "rectangle"
p1.style.fill: "#c8e6c9"
p1.label: "Phase 1:\nAuto"

p1 -> t1
t1.shape: "rectangle"
t1.style.fill: "#e8f5e9"
t1.label: "Tier 1\nVerbatim"

t1 -> ed
ed.shape: "rectangle"
ed.style.fill: "#bbdefb"
ed.label: "editor\nagent"

ed -> p2
p2.shape: "rectangle"
p2.style.fill: "#c8e6c9"
p2.label: "Phase 2:\nInteractive"

p2 -> t2
t2.shape: "rectangle"
t2.style.fill: "#e8f5e9"
t2.label: "Tier 2+\nJudgment"

t2 -> st
st.shape: "rectangle"
st.style.fill: "#fce4ec"
st.label: "Steward\nChoices"

st -> p3
p3.shape: "rectangle"
p3.style.fill: "#c8e6c9"
p3.label: "Phase 3:\nProposals"

p3 -> ns
ns.shape: "rectangle"
ns.style.fill: "#f3e5f5"
ns.label: "New\nSections"

ns -> sc
sc.shape: "rectangle"
sc.style.fill: "#e8f5e9"
sc.label: "Scaffold\n& Add"

sc -> va
va.shape: "rectangle"
va.style.fill: "#e0e0e0"
va.label: "make\nvalidate"

t1 -> va: {style.stroke-dash: 5}
st -> va: {style.stroke-dash: 5}
```

---

# The Editor Agent Constraint

### Verbatim-or-nothing

```
editor agent instruction:
- Find target_text VERBATIM in section file
- Replace with replacement_text exactly
- If target_text not found → report "not_found" and SKIP
- Do NOT interpret, guess, or rewrite
```

This is a **trust architecture**:
- Editors apply what was agreed
- Editors do not re-litigate decisions
- Human review of all edits before commit

---

# Key Design Principles

| Principle | Rationale |
|-----------|-----------|
| **Parallel first** | Prevents ordering effects |
| **Human synthesis** | Editorial judgment lives with named stewards |
| **Verbatim edits** | Trust architecture, not just constraint |
| **On main** | Reviews are part of the permanent record |
| **Batched context** | ~4,700 lines across models; batching prevents context overflow |

---

# The `/review-section` Skill

### Interactive human-AI deliberation

```
1. Extract context brief for a section
2. Propose integration plan (what to change, why)
3. Discuss with steward (accept/modify/defer)
4. Apply agreed changes
5. make validate + git diff
```

This is where the interesting conversation happens:
- Reviewer feedback meets editorial judgment
- Edge cases get worked out collaboratively
- Both registers stay coherent

---

```d2
direction: right

inputs: {
  near: top-left
  direction: right
  label: "Inputs"
  style.fill: "#f3f4f6"
  style.stroke: "#9ca3af"

  docs: {
    direction: right
    label: ""
    style.stroke: "transparent"
    style.fill: "transparent"

    sections: "Current\nsections"
    sections.style.fill: "#e0eec0"

    previous: "Prior\nreviews"
    previous.style.fill: "#e0eec0"

    writing_context: "Writing\ncontext"
    writing_context.style.fill: "#e1f5fe"

    writing_guides: "Ritual/\nparable\nguide"
    writing_guides.style.fill: "#e1f5fe"

    style_guide: "Style\nguide"
    style_guide.style.fill: "#e1f5fe"

    prompt: "Review\nprompt"
    prompt.style.fill: "#ede7f6"

    sections -> previous: {style.stroke: "transparent"}
    previous -> writing_context: {style.stroke: "transparent"}
    writing_context -> writing_guides: {style.stroke: "transparent"}
    writing_guides -> style_guide: {style.stroke: "transparent"}
    style_guide -> prompt: {style.stroke: "transparent"}
  }

  references: {
    direction: down
    label: "Reference adding process"
    style.fill: "#f9fafb"
    style.stroke: "#9ca3af"

    source: "Source\ntext"
    source.style.fill: "#fffdf5"

    notes: "Agent\nnotes"
    notes.style.fill: "#c8e6c9"

    dialogue: "Human-agent\ndialogue"
    dialogue.style.fill: "#ffe4e6"

    issues: "Issues for\nreview"
    issues.style.fill: "#ffe0b2"

    source -> notes -> dialogue -> issues
  }
}

review: {
  near: top-right
  direction: down
  label: "Review"
  style.fill: "#f3f4f6"
  style.stroke: "#9ca3af"

  gather: "Collate inputs\nSplit into batches"
  gather.shape: "step"
  gather.style.fill: "#fff4c2"

  reviewers: {
    direction: right
    label: "Parallel review"
    style.fill: "#f1f8e9"
    style.stroke: "#aed581"

    claude: "Claude"
    claude.shape: "rectangle"
    claude.style.fill: "#c8e6c9"

    gemini: "Gemini"
    gemini.shape: "rectangle"
    gemini.style.fill: "#c8e6c9"

    gpt: "GPT"
    gpt.shape: "rectangle"
    gpt.style.fill: "#c8e6c9"
  }

  raw: "Raw\nreviews"
  raw.style.fill: "#e0eec0"

  gather -> reviewers.claude
  gather -> reviewers.gpt
  gather -> reviewers.gemini

  reviewers.claude -> raw
  reviewers.gpt -> raw
  reviewers.gemini -> raw
}

synthesis_stage: {
  near: bottom-right
  direction: left
  label: "Synthesis"
  style.fill: "#f3f4f6"
  style.stroke: "#9ca3af"

  batch: "Split into batches"
  batch.shape: "step"
  batch.style.fill: "#fff4c2"
  batch.style.stroke-dash: 5

  synth_model: "Synthesis\nagents"
  synth_model.shape: "rectangle"
  synth_model.style.fill: "#c8e6c9"
  synth_model.style.multiple: true

  synthesis: "Synthesis"
  synthesis.style.fill: "#e0eec0"
  
  batch -> synth_model -> synthesis
}

reintegration: {
  near: bottom-left
  direction: left
  label: "Reintegration"

  style.fill: "#f3f4f6"
  style.stroke: "#9ca3af"

  packets: "Section packets\n(raw + synthesis)"
  packets.shape: "step"
  packets.style.fill: "#fff4c2"
  
  people: {
    direction: down
    label: ""
    style.stroke: "transparent"
    style.fill: "transparent"

    steward: "Human\nsteward"
    steward.shape: "person"
    steward.style.fill: "#fce4ec"

    agents: "Section\nagents"
    agents.shape: "rectangle"
    agents.style.fill: "#c8e6c9"
    agents.style.multiple: true
  }

  merge: {
    direction: left
    label: ""
    style.stroke: "transparent"
    style.fill: "transparent"

    dialogue: "Dialogue, critique,\nand integration"
    dialogue.style.fill: "#ffe4e6"

    updated: "Updated\nsections"
    updated.style.fill: "#e0eec0"

    dialogue -> updated
  }

  people.steward -> merge.dialogue
  people.agents -> merge.dialogue

  packets -> people.steward
  packets -> people.agents

}

inputs -> review.gather

review.raw -> synthesis_stage.batch
review.raw -> reintegration.packets: {style.stroke-dash: 5}
review.raw -> inputs.docs.previous:  {style.stroke-dash: 5}

synthesis_stage.synthesis -> reintegration.packets

reintegration.merge.updated -> inputs.docs.sections: {label: "next round"; style.stroke-dash: 5}
```

---

# Diminishing Returns

### When to stop reviewing

Signs a round is no longer productive:
- Models mostly agreeing with current draft
- New proposals increasingly minor
- Same unresolved tensions recur without new arguments

When productive:
- Convergence on previously disputed points
- New proposals that change the text substantively
- Fresh arguments on open questions

---

# Summary

### What makes this novel

1. **Parallel independent review** prevents any single model's framing from shaping others
2. **Two-register structure** requires both poetic and precise thinking
3. **Human synthesis** provides accountability and judgment
4. **Verbatim edit constraint** separates proposing from applying
5. **Reviews on main** make the deliberation part of the permanent record

> Future intelligences can read the reviews and understand not just what Covenant says, but *how* it came to say it.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Questions?

**Repository:** github.com/anomalyco/covenant

**Relevant docs:**
- `docs/agent_reviews.md` — Full process description
- `docs/writing_context.md` — What Covenant is
- `docs/style_guide.md` — Writing conventions
- `AGENTS.md` — Operational instructions
