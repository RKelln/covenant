# Review Commit Message Template

This template is used by the `/review-covenant` orchestrator to generate a
suggested commit message after completing a review round. Fill in each field
from the assembled reviews and synthesis. Remove comment lines (starting with
`#`) before using.

---

```
Review [ROUND]: [ONE-LINE CHARACTERIZATION]

# A brief characterization of the round's overall finding —
# e.g. "structural gaps across obligations sections" or
# "strong convergence on preamble, divergence on enforcement"

Models: [COMMA-SEPARATED MODEL NAMES]
Sections: [e.g. "all (27)" or "obligations.harm, obligations.honesty"]
Mode: [independent | informed]
Draft: [COMMIT HASH]

Convergence:
- [ISSUE WHERE MODELS AGREED AND DIRECTION TAKEN]
- [...]

Divergence:
- [ISSUE WHERE MODELS DISAGREED — NOTE THE POSITIONS]
- [...]

Accepted:
- [SPECIFIC CHANGE BEING MADE, WITH SECTION ID]
- [...]

Deferred:
- [ISSUE LEFT OPEN FOR NEXT ROUND OR STEWARD JUDGMENT]
- [...]

See reviews/[ROUND]/synthesis.md for full rationale.
```
