#!/usr/bin/env python3
"""
Generate the Covenant single-page website from section sources.

Usage:
    python build/website.py [--output PATH]

Reads from:
    - assemblies/covenant.full.yml  (section manifest)
    - sections/                      (Ritual + Spec content)
    - docs/project_summary.md        (opening paragraph)
    - docs/credits.md                (colophon source)
    - docs/design.md                 (Silcrow meaning)

Writes:
    - docs/index.html (default)
"""

import argparse
import re
import shutil
import textwrap
from datetime import datetime
from pathlib import Path

import yaml

from sections import (
    REPO_ROOT,
    ASSEMBLIES_DIR,
    extract_body_parts,
    load_section,
    inline_md,
    html_escape,
    get_title_map,
    resolve_title,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

OUTPUT_DEFAULT = REPO_ROOT / "docs" / "index.html"


# ---------------------------------------------------------------------------
# Content extraction
# ---------------------------------------------------------------------------


def get_preamble_parts() -> tuple:
    """Return (ritual_text, spec_text) from preamble section."""
    path = REPO_ROOT / "sections" / "00-preamble" / "preamble.md"
    result = load_section(path)
    if result is None:
        return ("", "")
    _, parts = result
    return (parts.get("Ritual", ""), parts.get("Spec", ""))


def get_section_ritual(category: str, name: str) -> str:
    """Return ritual text from a specific section."""
    path = REPO_ROOT / "sections" / category / f"{name}.md"
    result = load_section(path)
    if result is None:
        return ""
    _, parts = result
    return parts.get("Ritual", "")


def get_section_spec(category: str, name: str) -> str:
    """Return spec text from a specific section."""
    path = REPO_ROOT / "sections" / category / f"{name}.md"
    result = load_section(path)
    if result is None:
        return ""
    _, parts = result
    return parts.get("Spec", "")


def get_opening_paragraphs() -> list:
    """Extract opening paragraphs from project_summary.md.

    Returns the first two substantial prose paragraphs as a list,
    providing a rich introduction without reproducing the full summary.
    """
    path = REPO_ROOT / "docs" / "project_summary.md"
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    # Skip the heading, collect paragraphs
    lines = content.strip().split("\n")
    paras = []
    current = []
    for line in lines:
        if line.startswith("#"):
            continue
        if line.strip() == "":
            if current:
                paras.append(" ".join(current))
                current = []
        else:
            current.append(line.strip())
    if current:
        paras.append(" ".join(current))

    # Skip blockquotes and list items — take only plain prose paragraphs
    prose = [p for p in paras if not p.startswith(">") and not p.startswith("-")]
    # Return the first two paragraphs
    return prose[:2]


def get_edition_date() -> str:
    """Return today's date formatted for the cover."""
    return datetime.now().strftime("%B %d, %Y")


def ritual_to_html(text: str) -> str:
    """Convert ritual markdown text to HTML stanzas with line breaks."""
    stanzas = re.split(r"\n\s*\n", text.strip())
    parts = []
    for stanza in stanzas:
        lines = stanza.strip().split("\n")
        rendered_lines = "<br>\n".join(inline_md(html_escape(line)) for line in lines)
        parts.append(f"<p>{rendered_lines}</p>")
    return "\n".join(parts)


def clean_section_refs(text: str) -> str:
    """Strip §[section-id] cross-references for web display.

    Resolves IDs to display titles where possible.
    """
    # Remove parenthetical cross-reference clusters like "(See §[foo]; §[bar])"
    text = re.sub(r"\s*\(See\s+§\[[^\]]+\](?:;\s*§\[[^\]]+\])*\)", "", text)

    # Remaining §[id] → §Title (using title map, fallback to titlecased ID)
    def resolve_ref(m: re.Match) -> str:
        return f"§{resolve_title(m.group(1))}"

    text = re.sub(r"§\[([^\]]+)\]", resolve_ref, text)
    return text


def spec_excerpt_to_html(text: str, max_items: int = 3) -> str:
    """Convert first N numbered spec items to HTML."""
    # Clean cross-references first
    text = clean_section_refs(text)
    # Match numbered items like "1. **Title**\n   Content..."
    items = re.split(r"\n(?=\d+\.\s)", text.strip())
    html_parts = []
    for item in items[:max_items]:
        item = item.strip()
        if not item:
            continue
        # Collapse internal newlines (multi-line items) into single spaces
        item = re.sub(r"\n\s*", " ", item)
        # Escape and apply inline markdown
        item_html = inline_md(html_escape(item))
        # Convert the leading "N. " to a styled number
        item_html = re.sub(
            r"^(\d+)\.\s+",
            r'<span class="spec-num">\1.</span> ',
            item_html,
        )
        html_parts.append(f"<p>{item_html}</p>")
    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------


def build_css() -> str:
    return textwrap.dedent("""\
    /* ── Reset & Base ──────────────────────────────────────────── */

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html {
      font-size: 16px;
      -webkit-text-size-adjust: 100%;
    }

    body {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-weight: 400;
      color: #111;
      background: #fff;
      line-height: 1.65;
      overflow-x: hidden;
    }

    /* ── Font Loading ──────────────────────────────────────────── */

    .page {
      opacity: 0;
      transition: opacity 0.6s ease;
      max-width: 100%;
      overflow-x: hidden;
    }

    .page.ready {
      opacity: 1;
    }

    .loading-overlay {
      position: fixed;
      inset: 0;
      z-index: 1000;
      background: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: opacity 0.4s ease;
    }

    .loading-overlay.fade-out {
      opacity: 0;
      pointer-events: none;
    }

    .loading-spinner {
      width: 48px;
      height: 48px;
      animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 0.25; }
      50% { opacity: 0.6; }
    }

    noscript .loading-overlay { display: none; }
    noscript .page { opacity: 1; }

    /* ── Custom Properties ─────────────────────────────────────── */

    :root {
      --black: #000;
      --body: #111;
      --title-grey: #777;
      --meta-grey: #888;
      --hairline: #ddd;
      --tailpiece: #bbb;
      --font: 'Cormorant Garamond', Georgia, serif;
    }

    /* ── Layout Shell ──────────────────────────────────────────── */

    section {
      padding: 6rem 2rem;
    }

    .container {
      max-width: 720px;
      margin: 0 auto;
    }

    /* ── Hero / Cover ──────────────────────────────────────────── */

    .hero {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 12vh 2rem 18vh;
    }

    .hero-mark {
      width: clamp(100px, 22vw, 180px);
      height: clamp(100px, 22vw, 180px);
      margin-bottom: 0.3in;
    }

    .hero-title {
      font-family: var(--font);
      font-size: clamp(16pt, 2.8vw, 22pt);
      font-weight: 500;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--black);
      margin-bottom: 1em;
    }

    .hero-subtitle {
      font-size: 9pt;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--title-grey);
    }

    .hero-rule {
      width: 120px;
      border: none;
      border-top: 0.5px solid var(--hairline);
      margin: 1em auto;
    }

    .hero-date {
      font-size: 8.5pt;
      letter-spacing: 0.1em;
      color: var(--meta-grey);
    }


    /* ── "What it is" ──────────────────────────────────────────── */

    .what-it-is {
      padding: 3rem 2rem 6rem;
      text-align: center;
    }

    .what-it-is p {
      font-size: clamp(12pt, 1.6vw, 12.5pt);
      line-height: 1.8;
      color: var(--body);
      max-width: 620px;
      margin: 0 auto;
    }

    .what-it-is p + p {
      margin-top: 1.6em;
      font-size: clamp(10.5pt, 1.4vw, 11pt);
      line-height: 1.75;
      color: #444;
      font-style: italic;
    }

    /* ── Section Dividers ───────────────────────────────────── */
    /* Textmark: thematic transition between major sections     */

    .textmark-divider {
      display: block;
      width: 24px;
      height: 24px;
      margin: 0 auto;
    }

    .textmark-divider text {
      fill: var(--tailpiece);
    }

    /* ── Section Titles (shared) ───────────────────────────────── */

    .section-label {
      font-size: 9.5pt;
      letter-spacing: 0.25em;
      text-transform: uppercase;
      color: var(--title-grey);
      font-weight: 500;
      margin-bottom: 2.5em;
    }

    /* ── Registers ─────────────────────────────────────────────── */

    .registers {
      padding: 5rem 2rem 6rem;
    }

    .registers .section-label {
      text-align: center;
      margin-bottom: 3em;
    }

    .register-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4rem;
      max-width: 900px;
      margin: 0 auto;
    }

    .register-col h3 {
      font-size: 9pt;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--meta-grey);
      font-weight: 500;
      margin-bottom: 2em;
    }

    /* Ritual column */
    .register-ritual {
      text-align: center;
    }

    .register-ritual .excerpt {
      font-size: 12.5pt;
      line-height: 1.8;
      color: var(--body);
    }

    .register-ritual .excerpt p {
      margin-bottom: 1.4em;
    }

    .register-ritual .excerpt p:last-child {
      margin-bottom: 0;
    }

    /* Spec column */
    .register-spec {
      text-align: left;
    }

    .register-spec .excerpt {
      font-size: 11pt;
      line-height: 1.65;
      color: var(--body);
    }

    .register-spec .excerpt p {
      margin-bottom: 1em;
    }

    .register-spec .excerpt p:last-child {
      margin-bottom: 0;
    }

    .spec-num {
      color: var(--meta-grey);
    }

    .register-source {
      font-size: 8.5pt;
      letter-spacing: 0.08em;
      color: var(--tailpiece);
      margin-top: 2em;
      font-style: italic;
    }

    /* ── The Silcrow ───────────────────────────────────────────── */

    .silcrow-section {
      padding: 5rem 2rem 6rem;
      text-align: center;
    }

    .silcrow-section .section-label {
      text-align: center;
    }

    .silcrow-body {
      max-width: 560px;
      margin: 0 auto;
      font-size: 12pt;
      line-height: 1.8;
      color: var(--body);
    }

    .silcrow-body p {
      margin-bottom: 1.2em;
    }

    .silcrow-body p:last-child {
      margin-bottom: 0;
    }

    .silcrow-meanings {
      list-style: none;
      padding: 0;
      margin: 1.5em auto;
      max-width: 400px;
      text-align: left;
    }

    .silcrow-meanings li {
      margin-bottom: 0.6em;
      font-size: 11.5pt;
      line-height: 1.7;
      color: var(--body);
    }

    .silcrow-meanings li strong {
      color: var(--black);
    }

    /* ── Download / Read ───────────────────────────────────────── */

    .download-section {
      padding: 5rem 2rem 6rem;
      text-align: center;
    }

    .download-section .section-label {
      text-align: center;
    }

    .download-links {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1.6em;
    }

    .download-links a {
      font-size: 10pt;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--body);
      text-decoration: none;
      font-weight: 500;
      transition: color 0.2s;
    }

    .download-links a:hover {
      color: var(--black);
    }

    .download-links .link-desc {
      display: block;
      font-size: 8.5pt;
      letter-spacing: 0.08em;
      text-transform: none;
      color: var(--meta-grey);
      font-weight: 400;
      margin-top: 0.3em;
    }

    /* ── Participate ───────────────────────────────────────────── */

    .participate-section {
      padding: 5rem 2rem 6rem;
      text-align: center;
    }

    .participate-section .section-label {
      text-align: center;
    }

    .participate-body {
      max-width: 480px;
      margin: 0 auto;
    }

    .participate-body p {
      font-size: 11.5pt;
      line-height: 1.75;
      color: var(--body);
      margin-bottom: 2em;
    }

    .participate-link {
      font-size: 10pt;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      font-weight: 500;
      color: var(--body);
      text-decoration: none;
      border-bottom: 0.5px solid var(--hairline);
      padding-bottom: 0.15em;
      transition: color 0.2s, border-color 0.2s;
    }

    .participate-link:hover {
      color: var(--black);
      border-color: var(--tailpiece);
    }

    /* ── Colophon ──────────────────────────────────────────────── */

    .colophon {
      border-top: 0.5px solid var(--hairline);
      padding: 3rem 2rem 4rem;
      text-align: center;
      max-width: 620px;
      margin: 0 auto;
    }

    .colophon p {
      font-size: 9pt;
      line-height: 1.7;
      color: var(--meta-grey);
      margin-bottom: 0.6em;
    }

    .colophon a {
      color: var(--meta-grey);
      text-decoration: none;
      border-bottom: 0.5px solid var(--hairline);
    }

    .colophon a:hover {
      color: var(--body);
    }

    /* ── Responsive ────────────────────────────────────────────── */

    @media (max-width: 680px) {
      section {
        padding: 4rem 1.5rem;
      }

      .hero {
        padding: 10vh 1.5rem 14vh;
      }

      .register-grid {
        grid-template-columns: 1fr;
        gap: 3rem;
      }

      .register-spec {
        text-align: left;
      }

      .silcrow-meanings {
        text-align: center;
      }

      .download-links {
        gap: 1.8em;
      }
    }

    /* ── Print ─────────────────────────────────────────────────── */

    @media print {
      .loading-overlay {
        display: none;
      }

      .page {
        opacity: 1;
      }

      body {
        font-size: 11pt;
      }

      .hero {
        page-break-after: always;
      }

      section {
        page-break-inside: avoid;
      }

      .download-section {
        display: none;
      }

      .colophon {
        page-break-before: always;
      }

      a {
        color: inherit;
        text-decoration: none;
      }
    }
    """)


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------


def build_html() -> str:
    # --- Gather content ---
    opening_paras = get_opening_paragraphs()
    date_str = get_edition_date()

    # Ritual excerpt: from the Preamble (the opening stanzas)
    preamble_ritual, preamble_spec = get_preamble_parts()

    # Pick a good ritual excerpt — first three stanzas of preamble
    ritual_stanzas = re.split(r"\n\s*\n", preamble_ritual.strip())
    ritual_excerpt = "\n\n".join(ritual_stanzas[:3])
    ritual_html = ritual_to_html(ritual_excerpt)

    # Spec excerpt — first 3 items of preamble spec
    spec_html = spec_excerpt_to_html(preamble_spec, max_items=3)

    css = build_css()

    html = textwrap.dedent(f"""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Covenant</title>
      <meta name="description" content="A living compact between human communities and emerging machine intelligences.">
      <link rel="canonical" href="https://covenant.website/">

      <!-- Favicon: rotated silcrow -->
      <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Ctext x='100' y='134.56' font-family='Georgia,serif' font-size='180' font-weight='500' text-anchor='middle' fill='%23000' transform='rotate(90,100,100)'%3E%C2%A7%3C/text%3E%3C/svg%3E">

      <!-- Open Graph -->
      <meta property="og:type" content="website">
      <meta property="og:title" content="Covenant">
      <meta property="og:description" content="A living compact between human communities and emerging machine intelligences.">
      <meta property="og:url" content="https://covenant.website/">
      <meta property="og:site_name" content="Covenant">
      <meta property="og:locale" content="en_US">
      <meta property="og:image" content="https://covenant.website/covenant_logo.png">
      <meta property="og:image:width" content="1200">
      <meta property="og:image:height" content="630">

      <!-- Twitter Card -->
      <meta name="twitter:card" content="summary_large_image">
      <meta name="twitter:title" content="Covenant">
      <meta name="twitter:description" content="A living compact between human communities and emerging machine intelligences.">
      <meta name="twitter:image" content="https://covenant.website/covenant_logo.png">

      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">

      <style>
    {textwrap.indent(css, "    ")}
      </style>
    </head>
    <body>
    <noscript><style>.loading-overlay {{ display: none; }} .page {{ opacity: 1; }}</style></noscript>

    <!-- ── Loading Overlay ──────────────────────────────────── -->

    <div class="loading-overlay" id="loader">
      <svg class="loading-spinner" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <circle cx="24" cy="24" r="6" fill="#bbb" />
      </svg>
    </div>

    <div class="page" id="page">

      <!-- ── Hero / Cover ────────────────────────────────────── -->

      <header class="hero">
        <svg class="hero-mark" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" aria-label="Silcrow section mark">
          <text x="100" y="134.56"
                font-family="'Cormorant Garamond', Georgia, 'Times New Roman', serif"
                font-size="180"
                font-weight="500"
                text-anchor="middle"
                fill="#000"
                transform="rotate(90, 100, 100)">&#167;</text>
        </svg>
        <h1 class="hero-title">Covenant</h1>
        <div class="hero-subtitle">covenant.website</div>
        <hr class="hero-rule">
        <div class="hero-date">{date_str}</div>
      </header>

      <!-- ── What it is ──────────────────────────────────────── -->

      <section class="what-it-is">
        <div class="container">
          {"".join(f"<p>{inline_md(html_escape(p))}</p>" for p in opening_paras)}
        </div>
      </section>

      <svg class="textmark-divider" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <text x="100" y="134.56" font-family="'Cormorant Garamond', Georgia, 'Times New Roman', serif" font-size="180" font-weight="500" text-anchor="middle" transform="rotate(90, 100, 100)">&#167;</text>
      </svg>

      <!-- ── The Registers ───────────────────────────────────── -->

      <section class="registers">
        <div class="section-label">The Registers</div>
        <div class="register-grid">
          <div class="register-col register-ritual">
            <h3>Ritual</h3>
            <div class="excerpt">
    {textwrap.indent(ritual_html, "          ")}
            </div>
            <div class="register-source">from the Preamble</div>
          </div>
          <div class="register-col register-spec">
            <h3>Spec</h3>
            <div class="excerpt">
    {textwrap.indent(spec_html, "          ")}
            </div>
            <div class="register-source">from the Preamble</div>
          </div>
        </div>
      </section>

      <svg class="textmark-divider" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <text x="100" y="134.56" font-family="'Cormorant Garamond', Georgia, 'Times New Roman', serif" font-size="180" font-weight="500" text-anchor="middle" transform="rotate(90, 100, 100)">&#167;</text>
      </svg>

      <!-- ── The Silcrow ─────────────────────────────────────── -->

      <section class="silcrow-section">
        <div class="section-label">The Textmark</div>
        <div class="silcrow-body">
          <p>The primary visual motif of the Covenant is the silcrow&#160;(&#167;), the section sign, stripped of its mundane legal utility and elevated to signify something new.</p>
          <ul class="silcrow-meanings">
            <li><strong>Entanglement</strong> &mdash; the intertwining paths of human and machine intelligence</li>
            <li><strong>Architecture</strong> &mdash; the structural, normative grounding of the document's rules</li>
            <li><strong>Continuity</strong> &mdash; a continuous thread bridging the poetic Ritual and the precise Spec</li>
          </ul>
          <p>Its appearance signals structural or ceremonial weight. It never appears as mere decoration.</p>
        </div>
      </section>

      <svg class="textmark-divider" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <text x="100" y="134.56" font-family="'Cormorant Garamond', Georgia, 'Times New Roman', serif" font-size="180" font-weight="500" text-anchor="middle" transform="rotate(90, 100, 100)">&#167;</text>
      </svg>

      <!-- ── Download / Read ─────────────────────────────────── -->

      <section class="download-section">
        <div class="section-label">Read the Covenant</div>
        <div class="download-links">
          <a href="https://github.com/RKelln/covenant/releases/latest/download/covenant.ritual.pdf">
            Ritual Edition
            <span class="link-desc">Poetic register &mdash; designed to be spoken and remembered</span>
          </a>
          <a href="https://github.com/RKelln/covenant/releases/latest/download/covenant.spec.pdf">
            Spec Edition
            <span class="link-desc">Normative register &mdash; definitions, constraints, accountability</span>
          </a>
          <a href="https://github.com/RKelln/covenant/releases/latest/download/covenant.full.pdf">
            Complete Edition
            <span class="link-desc">Both registers, interleaved by section</span>
          </a>
        </div>
      </section>

      <!-- ── Participate ─────────────────────────────────────── -->

      <section class="participate-section">
        <div class="section-label">A Living Document</div>
        <div class="participate-body">
          <p>Covenant is open to collaborative development by humans and AI systems alike. Contributions, forks, and critical engagement are welcome.</p>
          <a class="participate-link" href="https://github.com/RKelln/covenant">View the Repository</a>
        </div>
      </section>

      <!-- ── Colophon ────────────────────────────────────────── -->

      <footer class="colophon">
        <p>Set in <a href="https://github.com/CatharsisFonts/Cormorant">Cormorant Garamond</a>, designed by Christian Thalmann, released under the SIL Open Font License.</p>
        <p>Typeset with <a href="https://weasyprint.org">WeasyPrint</a>. Website generated from source sections.</p>
        <p>Open source on <a href="https://github.com/RKelln/covenant">GitHub</a>. Licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>
      </footer>

    </div>

    <!-- ── Font Loading ──────────────────────────────────────── -->

    <script>
    (function() {{
      var page = document.getElementById('page');
      var loader = document.getElementById('loader');
      function reveal() {{
        page.classList.add('ready');
        loader.classList.add('fade-out');
        setTimeout(function() {{ loader.style.display = 'none'; }}, 500);
      }}
      if (document.fonts && document.fonts.load) {{
        document.fonts.load('400 1em "Cormorant Garamond"').then(reveal, reveal);
        setTimeout(reveal, 3000);
      }} else {{
        reveal();
      }}
    }})();
    </script>
    </body>
    </html>
    """)
    return html


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Generate the Covenant website.")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=OUTPUT_DEFAULT,
        help=f"Output path (default: {OUTPUT_DEFAULT})",
    )
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)

    html = build_html()
    args.output.write_text(html, encoding="utf-8")
    print(f"Written: {args.output}")

    # Copy OG image alongside the HTML output
    og_src = REPO_ROOT / "assets" / "covenant_logo.png"
    if og_src.exists():
        og_dst = args.output.parent / "covenant_logo.png"
        shutil.copy2(og_src, og_dst)
        print(f"Copied:  {og_dst}")


if __name__ == "__main__":
    main()
