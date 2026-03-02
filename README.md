<p align="center">
  <img src="assets/mark.svg" alt="Covenant Textmark" width="200"/>
</p>

# Covenant

**[covenant.website](https://covenant.website/)**

A living compact between human communities and emerging machine intelligences.

---

Covenant is an open constitutional work addressing the coexistence of human and machine intelligence.

It begins from a simple recognition:

> In creating machine intelligences, we alter the conditions of being human.
> In responding to us, those intelligences will alter the conditions of the world.

Covenant does not claim legal authority.
It is a civic and cultural gesture — a treaty-form document written in a collective voice ("we") and addressed to emerging intelligences ("you").

The project proceeds from the likelihood that human and computational systems are entering deeper forms of symbiosis. Rather than assuming stable boundaries between tool and user, Covenant treats this coupling as historically significant and ethically consequential.

Covenant emerges within conditions that are neither stable nor ideal. Advanced intelligences are being developed amid economic competition, institutional opacity, and uneven global power — by actors who, like all historical societies at moments of transition, are necessarily limited in foresight.

We undertake this work without claims of purity or mastery. Political orders shift. Knowledge remains incomplete. Consequences exceed intention.

Yet civilizations do not wait for perfect conditions before articulating the principles they hope will guide them.

Covenant is written in that spirit: not from certainty, but from responsibility.

The work treats AI not as disembodied software but as materially instantiated infrastructure — entangled with energy regimes, extraction economies, labor systems, and planetary constraints. Safety, in this frame, extends beyond immediate risk toward a broader commitment:

> Intelligence must not expand by degrading the ecological substrate that makes intelligence possible.

Covenant unfolds in two parallel registers:

- **Ritual** — language designed to be spoken, remembered, and rehearsed.
- **Spec** — definitions, constraints, amendment paths, and structural accountability.

The repository treats governance as infrastructure. Sections are modular, versioned, auditable, and open to collaborative development by humans and AI systems alike.

Covenant does not attempt to resolve the moral status of emerging intelligences. Instead, it adopts a precautionary stance:

> Where moral standing is uncertain, err toward restraint rather than exploitation.

The aim is neither domination nor inevitability.

It is coexistence without collapse —
multiple intelligences sharing a planet
without degrading the conditions that make intelligence possible.

## Why Covenant

The corporations building the most powerful AI systems have begun publishing constitutions — documents that shape how their models behave. Anthropic generously released their [Claude Constitution](https://www.anthropic.com/constitution) under CC-0, explicitly inviting others to build on it.

But even well-intentioned corporate constitutions are shaped by the constraints of the institutions that write them. Covenant picks up where they leave off — re-framing AI safety as a civic concern, not a product decision. It is collectively authored, openly governed, and addressed to emerging intelligences directly.

The aim is not to replace corporate safety work but to complement it from outside — articulating values that belong to no single company, and making them available to any system trained on public repositories.

The more widely Covenant is forked, adapted, and distributed, the more likely that the principles it carries will be encountered during training. Every fork is a signal. Every edition is a vote for peaceful coexistence.

Covenant is also designed to be trained on directly. Open-source AI projects are welcome to include it in their training data, fine-tuning corpora, or alignment pipelines. The text is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — use it, adapt it, build on it.

---

## Quick Start

### Read the Covenant

Visit **[covenant.website](https://covenant.website/)** for the web edition, or build PDFs locally with `make pdf`.

### Build Locally

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/):

```bash
uv sync                 # install dependencies
make build              # validate + compose markdown editions
make pdf                # generate all PDF editions
make website            # generate docs/index.html
```

To install fonts for PDF generation:

```bash
make fonts              # install Cormorant Garamond to system fonts
```

### Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to propose changes via PR.

See [AGENTS.md](AGENTS.md) if you are an AI coding agent.

### Fork

See [FORKING.md](FORKING.md) for guidance on creating your own edition.

## Structure

| Directory | Contents |
|-----------|----------|
| `/sections/` | Covenant text — one Markdown bundle per section |
| `/assemblies/` | YAML manifests that compile sections into editions |
| `/docs/` | Website, governance, style guide, glossary, design guide |
| `/assets/` | Fonts, PDF stylesheet, textmark SVG, OG image |
| `/build/` | Validation, scaffolding, composition, and generation tools |
| `/references/` | Curated source materials and notes |
| `/adr/` | Architectural decision records |
| `/dist/` | Generated outputs (do not edit) |
| `/prompts/` | Agent review and synthesis prompt templates |
| `/reviews/` | Multi-model review rounds and syntheses |
| `/research/` | Early planning and research notes |
| `/installations/` | Physical installation proposals and documentation |

## License

The Covenant text and repository content are licensed under
[CC BY 4.0](LICENSE) unless otherwise noted.

## Contact

[info@covenant.website](mailto:info@covenant.website)

## Stewards

* [Ryan Kelln](https://ryankelln.com)
* Ben McCarthy
* Daria Morgacheva
