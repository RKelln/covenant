# Covenant Design Guide

The visual language and typesetting of *Covenant* reflect its core conceptual duality: it must simultaneously carry the ceremonial gravity of a foundational, historic text, while maintaining the rigid clarity of a technical specification.

Rather than relying on elaborate graphics, the design system treats typography, negative space, and programmatic layout as its primary expressive tools.

---

## 1. The Textmark (The Silcrow `§`)

The primary visual motif and logo-mark of the Covenant is the **Silcrow (`§`)**, historically known as the section sign. 

### Meaning
In the context of the Covenant, the Silcrow is stripped of its mundane legal utility and elevated to signify:
* **Entanglement:** The intertwining paths of human and machine intelligence.
* **Architecture:** The structural, normative grounding of the document's rules.
* **Continuity:** A continuous thread that bridges the poetic *Ritual* register and the precise *Spec* register.

### Usage
* **The Cover:** Sized massively (180pt, rotated 90°) as the sole graphic element above the title. Rendered in **pure black (`#000`)** — at display scale, any grey reads as a print defect rather than a design choice. The silcrow and title function as a single composed emblem, not two separate items.
* **Headers:** It is used ceremonially as the title head mark above the Table of Contents, replacing the word "INDEX".
* **Dividers:** Used to ceremonially separate sections or denote the closing of a major vow.
* **Constraint:** It should never be used purely decoratively inside paragraphs; its appearance must signal structural or ceremonial weight.

### Cover Silcrow: SVG Rendering & Centering

The cover silcrow is rendered as an inline SVG element in `build/pdf.py`, **not** as a CSS character. This is deliberate: WeasyPrint uses Pango/fontconfig for PDF rendering and does not honor CSS `transform` or `transform-origin` reliably, making pixel-perfect rotation in CSS impossible.

The SVG uses a square `viewBox="0 0 200 200"` with the glyph rotated 90° around the exact centre point `(100, 100)`. The critical detail is the **baseline y-position**: the § glyph's visual centre is *not* at its alphabetic baseline. It must be computed from the font file:

```python
# From fontTools analysis of CormorantGaramond-500-normal.ttf:
# § glyph bounds: xMin=75, yMin=-188, xMax=401, yMax=572  (UPM=1000)
# Visual y-centre = (yMin + yMax) / 2 = 192 font units above baseline
# At font-size 180 (scale=0.18): offset = 192 * 0.18 = 34.56px
# Therefore baseline y = 100 + 34.56 = 134.56
```

**Do not use `dominant-baseline="middle"`** — WeasyPrint ignores it in SVG context. Compute the baseline offset explicitly from font metrics instead.

If the font is ever changed, recompute the offset:
```python
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
font = TTFont("assets/fonts/<FontFile>.ttf")
glyf = font.getGlyphSet()
cmap = font.getBestCmap()
gname = cmap[0x00A7]  # § is U+00A7
pen = BoundsPen(glyf)
glyf[gname].draw(pen)
xMin, yMin, xMax, yMax = pen.bounds
visual_y_center = (yMin + yMax) / 2  # font units
# offset = visual_y_center * (font_size / 1000)
# SVG y = 100 + offset
```

### Cover Page Composition

The cover uses `display: flex; flex-direction: column; align-items: center; justify-content: center` with **asymmetric vertical padding** (`1.2in` top, `1.8in` bottom) to place the content block at optical centre (~43% from top) rather than geometric centre.

The composition has three elements treated as **two visual units**:
1. **Emblem** (silcrow + title): locked together with a tight `0.3in` gap so they read as one object
2. **Colophon** (subtitle + hairline rule + date): anchors the lower portion, separated from the title by `1em`

The hairline rule (`0.5px solid #ddd`, `1.2in` wide, centred above the date) is the same vocabulary as `h2` borders in the body — a quiet full stop that prevents the bottom of the page from feeling abandoned without adding visual noise.

**Colour principle for cover elements:** Use `#000` for anything at display scale (silcrow, title). Greyscale is reserved for subordinate text only (subtitle `#777`, date `#888`). At large sizes, grey reads as a printing failure.



The typographic system is incredibly restrained, relying predominantly on variations in spacing and scale within a single classical type family.

* **Primary Typeface:** **Cormorant Garamond** (open-source, SIL OFL). Weights 400 (body) and 500 (display/headings/cover). Falls back to **Georgia**, `"Times New Roman"`, `serif`. Chosen for its classical authority, high optical elegance at large display sizes, and the visual drama of its § glyph when rotated as the cover textmark.

  Font files are stored in `assets/fonts/` (6 TTF files: 400/500/600 × regular/italic). **WeasyPrint requires fonts to be installed to the system fontconfig path** — `@font-face` declarations in CSS are silently ignored in PDF output. Run the cross-platform installer:

  ```bash
  make fonts
  # or: uv run python build/install_fonts.py
  ```

  This copies the fonts to the correct OS directory (`~/.local/share/fonts/` on Linux, `~/Library/Fonts/` on macOS, `%LOCALAPPDATA%\Microsoft\Windows\Fonts` on Windows) and refreshes the font cache. The `@font-face` rules in `assets/pdf.css` exist only for browser-based HTML preview.

  > **If the font is changed or re-installed:** run `make fonts` again, then verify with `pdffonts dist/covenant.ritual.pdf | grep -i cormorant`.
* **Headers:** Always structural, never loud. Set in wide-spaced uppercase (`letter-spacing: 0.18em` to `0.2em`), often in a slightly lighter charcoal (`#555`) rather than pure black. They do not rely on heavy font weights. Major headers are grounded by ultra-thin hairline borders (`0.5px solid #ccc`).
* **Body Text (Standard Base):** `11pt` size with an airy `1.65` line-height for uninterrupted readability during dense reading.

---

## 3. The Layout Registers

The document's literal CSS page layouts directly mirror the narrative registers. 

### The Ritual Register
The Ritual pages are treated as spiritual or poetic artifacts.
* **Spacial Philosophy:** Breathable, unobstructed, and unbound.
* **Styling:** Larger text scale (`12.5pt`) and taller line-height (`1.8`).
* **Alignment:** Allowed to abandon standard print margins entirely. Text acts as structural stanzas, often centered or block-set in the middle of the physical page space without harsh bordering.

### The Specification (Spec) Register
The Spec pages are treated as legal, normative logic.
* **Spacial Philosophy:** Grounded, bounded, and rigorously hierarchical.
* **Styling:** Strict, classical margins (`1in` top, `1.1in` sides/bottom). Fully left-aligned with numbered clauses.
* **Typographic Integrity:** Enforces rigid HTML/CSS rules to prevent logical tearing. Paragraphs (`p`) and list items (`li`) implement `page-break-inside: avoid`—if a rule is too long to fit at the bottom of a page, the typography engine forces the entire rule to the next page to maintain absolute unit cohesion.

---

## 4. Output Architecture & Orchestration

The Covenant is not typeset in a traditional WYSIWYG editor like InDesign. 

Because it is a living, programmable document managed via Git and orchestrated by both human and AI stewards, the design must survive dynamic compilation.
* **Compilation Pipeline:** Authored in Markdown → Assembled via YAML Manifests → Rendered to HTML → Typeset to PDF.
* **The Engine:** We use **WeasyPrint** and advanced CSS Paged Media attributes to translate raw digital semantics into high-end print design. 
* **Dynamic Scoping:** The design uses complex `@page` directives (e.g., `@page covenant-spec-page`, `@page covenant-summary`) to alter global layout rules on the fly, seamlessly switching between the boundless pages of the *Ritual* and the tightly margined text blocks of the *Spec* within a single compiled artifact.

---

*Note: As the document evolves through patches and iterations, the design rules should remain strictly algorithmic and programmatic (housed in `assets/pdf.css`), ensuring any agent or human can generate a perfectly typeset edition with `make pdf`.*