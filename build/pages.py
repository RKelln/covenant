#!/usr/bin/env python3
"""
Generate full HTML reading pages for each Covenant edition.

Usage:
    python build/pages.py [--output-dir PATH]

Produces (in docs/ by default):
    ritual.html    — all sections, ritual register, left-aligned poetic layout
    spec.html      — all sections, spec register, flowing prose layout
    covenant.html  — all sections, both registers side by side per section

Reads from:
    - assemblies/covenant.full.yml   (section manifest — all three pages use same section list)
    - sections/                       (Ritual + Spec content)
"""

import argparse
import re
import textwrap
from pathlib import Path

import yaml

from sections import (
    REPO_ROOT,
    ASSEMBLIES_DIR,
    load_section,
    inline_md,
    html_escape,
    resolve_title,
    get_version,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

OUTPUT_DEFAULT = REPO_ROOT / "docs"
ASSEMBLY_FILE = ASSEMBLIES_DIR / "covenant.full.yml"


# ---------------------------------------------------------------------------
# Section loading
# ---------------------------------------------------------------------------


def load_assembly_sections(assembly_file: Path) -> list:
    """Return list of (frontmatter_dict, body_parts_dict) for all included sections."""
    manifest = yaml.safe_load(assembly_file.read_text(encoding="utf-8"))
    results = []
    for sec_path in manifest.get("sections", []):
        result = load_section(REPO_ROOT / sec_path)
        if result is None:
            continue
        data, parts = result
        if data.get("status") not in manifest.get("include_status", []):
            continue
        results.append((data, parts))
    return results


# ---------------------------------------------------------------------------
# Markdown → HTML converters
# ---------------------------------------------------------------------------


def ritual_to_html(text: str) -> str:
    """Convert ritual markdown to HTML stanzas with line breaks."""
    stanzas = re.split(r"\n\s*\n", text.strip())
    parts = []
    for stanza in stanzas:
        lines = stanza.strip().split("\n")
        rendered = "<br>\n".join(inline_md(html_escape(line)) for line in lines)
        parts.append(f"<p>{rendered}</p>")
    return "\n".join(parts)


def spec_to_html(text: str) -> str:
    """Convert spec markdown to HTML using python-markdown with cross-ref resolution."""
    try:
        import markdown as md_lib

        body = md_lib.markdown(text, extensions=["extra", "nl2br"])
    except ImportError:
        # Fallback: basic paragraph conversion
        paras = re.split(r"\n\s*\n", text.strip())
        body = "\n".join(
            f"<p>{inline_md(html_escape(p.strip()))}</p>" for p in paras if p.strip()
        )

    # Resolve §[section-id] cross-references to linked §Title anchors.
    # All three pages include all sections, so anchors are always present.
    def resolve_ref(m: re.Match) -> str:
        sec_id = m.group(1)
        anchor = "s-" + sec_id.replace(".", "-").replace(" ", "-").lower()
        title = resolve_title(sec_id)
        return f'<a href="#{anchor}">§{title}</a>'

    body = re.sub(r"§\[([^\]]+)\]", resolve_ref, body)
    return body


def section_anchor(data: dict) -> str:
    return "s-" + data.get("id", "").replace(".", "-").replace(" ", "-").lower()


# ---------------------------------------------------------------------------
# Shared page chrome
# ---------------------------------------------------------------------------

# Inline SVG silcrow used as nav logo and section divider
SILCROW_SVG = (
    '<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<text x="100" y="134.56" '
    "font-family=\"'Cormorant Garamond', Georgia, 'Times New Roman', serif\" "
    'font-size="180" font-weight="500" text-anchor="middle" '
    'transform="rotate(90, 100, 100)">&#167;</text>'
    "</svg>"
)

# Navbar rendered at top of every reading page
NAV_HTML = textwrap.dedent("""\
  <nav class="site-nav">
    <a class="nav-home" href="index.html">
      <svg class="nav-mark" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <text x="100" y="134.56"
              font-family="'Cormorant Garamond', Georgia, 'Times New Roman', serif"
              font-size="180" font-weight="500" text-anchor="middle"
              transform="rotate(90, 100, 100)">&#167;</text>
      </svg>
      <span>Covenant</span>
    </a>
    <div class="nav-editions">
      <a href="covenant.html">Complete</a>
      <a href="ritual.html">Ritual</a>
      <a href="spec.html">Specification</a>
    </div>
  </nav>
""")

PAGE_HEADER_TMPL = textwrap.dedent("""\
  <header class="page-header">
    <h1 class="page-title">{title}</h1>
    <p class="page-desc">{desc}</p>
    <a class="page-pdf-link" href="{pdf_url}">Download PDF</a>
  </header>
""")


def toc_html(sections: list, label: str) -> str:
    """Generate an inline table of contents for a reading page."""
    items = []
    for data, _ in sections:
        anchor = section_anchor(data)
        title = html_escape(data.get("title", ""))
        items.append(f'    <li><a href="#{anchor}">{title}</a></li>')
    items_html = "\n".join(items)
    return textwrap.dedent(f"""\
  <nav class="toc" id="toc" aria-label="Table of contents">
    <div class="toc-label">{label}</div>
    <ol class="toc-list">
{items_html}
    </ol>
  </nav>
""")


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------


def build_base_css() -> str:
    """Styles shared by all three reading pages."""
    return textwrap.dedent("""\
    /* ── Reset & Base ─────────────────────────────────────────── */

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html { font-size: 16px; -webkit-text-size-adjust: 100%; }

    body {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-weight: 400;
      color: #111;
      background: #fdfcfa url('watermark.webp') repeat;
      background-size: 1024px;
      line-height: 1.65;
      overflow-x: hidden;
    }

    /* ── Font loading ─────────────────────────────────────────── */

    .page { opacity: 0; transition: opacity 0.6s ease; }
    .page.ready { opacity: 1; }

    .loading-overlay {
      position: fixed; inset: 0; z-index: 1000; background: #fdfcfa;
      display: flex; align-items: center; justify-content: center;
      transition: opacity 0.4s ease;
    }
    .loading-overlay.fade-out { opacity: 0; pointer-events: none; }

    .loading-spinner {
      width: 48px; height: 48px;
      animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse { 0%, 100% { opacity: 0.25; } 50% { opacity: 0.6; } }

    noscript .loading-overlay { display: none; }
    noscript .page { opacity: 1; }

    /* ── Custom properties ────────────────────────────────────── */

    :root {
      --black:      #000;
      --body:       #111;
      --title-grey: #777;
      --meta-grey:  #888;
      --hairline:   #ddd;
      --tailpiece:  #bbb;
      --font: 'Cormorant Garamond', Georgia, serif;
      --fs-display: 1.75rem;
      --fs-body:    1.125rem;
      --fs-ui:      0.917rem;
      --fs-meta:    0.833rem;
      --content-width: 720px;
    }

    /* ── Navigation ───────────────────────────────────────────── */

    .site-nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 1.5rem 2rem;
      border-bottom: 0.5px solid var(--hairline);
      position: sticky;
      top: 0;
      background: rgba(253, 252, 250, 0.96);
      backdrop-filter: blur(4px);
      z-index: 100;
    }

    .nav-home {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      text-decoration: none;
      color: var(--body);
      font-size: var(--fs-ui);
      letter-spacing: 0.15em;
      text-transform: uppercase;
      font-weight: 500;
    }

    .nav-mark {
      width: 22px;
      height: 22px;
    }

    .nav-mark text { fill: var(--body); }

    .nav-editions {
      display: flex;
      gap: 2rem;
    }

    .nav-editions a {
      font-size: var(--fs-ui);
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--title-grey);
      text-decoration: none;
      font-weight: 500;
      transition: color 0.2s;
    }

    .nav-editions a:hover,
    .nav-editions a.current {
      color: var(--body);
    }

    /* ── Page header ──────────────────────────────────────────── */

    .page-header {
      padding: 6rem 2rem 4rem;
      text-align: center;
    }

    .page-title {
      font-size: clamp(var(--fs-display), 3.5vw, 1.85rem);
      font-weight: 500;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--black);
      margin-bottom: 0.8em;
    }

    .page-desc {
      font-size: var(--fs-body);
      color: var(--title-grey);
      max-width: 480px;
      margin: 0 auto;
      line-height: 1.7;
    }

    .page-pdf-link {
      display: inline-block;
      margin-top: 1.6em;
      font-size: var(--fs-meta);
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--meta-grey);
      text-decoration: none;
      border-bottom: 0.5px solid var(--hairline);
      padding-bottom: 0.1em;
      transition: color 0.2s, border-color 0.2s;
    }

    .page-pdf-link:hover {
      color: var(--body);
      border-color: var(--tailpiece);
    }

    /* ── TOC ──────────────────────────────────────────────────── */

    .toc {
      max-width: var(--content-width);
      margin: 0 auto 5rem;
      padding: 0 2rem;
    }

    .toc-label {
      font-size: var(--fs-ui);
      letter-spacing: 0.25em;
      text-transform: uppercase;
      color: var(--title-grey);
      font-weight: 500;
      margin-bottom: 1.5em;
    }

    .toc-list {
      list-style: none;
      column-count: 2;
      column-gap: 3rem;
    }

    .toc-list li {
      margin-bottom: 0.5em;
      break-inside: avoid;
      font-size: var(--fs-ui);
    }

    .toc-list a {
      color: var(--title-grey);
      text-decoration: none;
      letter-spacing: 0.05em;
      transition: color 0.2s;
    }

    .toc-list a:hover { color: var(--body); }

    /* ── Section divider (jump-to-TOC link) ──────────────────── */

    .section-divider {
      display: flex;
      justify-content: center;
      padding: 2rem 0;
    }

    .section-divider a {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 32px;
      height: 32px;
      text-decoration: none;
      border-radius: 50%;
      transition: background 0.2s;
    }

    .section-divider a:hover {
      background: rgba(0,0,0,0.04);
    }

    .section-divider svg {
      width: 20px;
      height: 20px;
    }

    .section-divider text { fill: var(--tailpiece); }

    /* ── Footer ───────────────────────────────────────────────── */

    .page-footer {
      border-top: 0.5px solid var(--hairline);
      padding: 3rem 2rem 4rem;
      text-align: center;
      max-width: 620px;
      margin: 4rem auto 0;
    }

    .page-footer p {
      font-size: var(--fs-meta);
      line-height: 1.7;
      color: var(--meta-grey);
      margin-bottom: 0.6em;
    }

    .page-footer a {
      color: var(--meta-grey);
      text-decoration: none;
      border-bottom: 0.5px solid var(--hairline);
    }

    .page-footer a:hover { color: var(--body); }

    /* ── Section cross-reference links ───────────────────────── */

    .ritual-body a[href^="#s-"],
    .spec-body a[href^="#s-"],
    .full-body a[href^="#s-"] {
      color: inherit;
      text-decoration: underline;
      text-decoration-style: dotted;
      text-decoration-color: var(--tailpiece);
      text-underline-offset: 0.2em;
    }
    .ritual-body a[href^="#s-"]:hover,
    .spec-body a[href^="#s-"]:hover,
    .full-body a[href^="#s-"]:hover {
      text-decoration-color: var(--title-grey);
    }

    /* ── Responsive ───────────────────────────────────────────── */

    @media (max-width: 680px) {
      .site-nav { padding: 1.2rem 1.5rem; }
      .toc-list { column-count: 1; }
      .page-header { padding: 4rem 1.5rem 3rem; }
    }

    /* ── Print ────────────────────────────────────────────────── */

    @media print {
      .loading-overlay { display: none; }
      .page { opacity: 1; }
      .site-nav { position: static; }
      body { font-size: 11pt; }
    }
    """)


def build_ritual_css() -> str:
    return textwrap.dedent("""\
    /* ── Ritual layout ────────────────────────────────────────── */

    .ritual-body {
      max-width: var(--content-width);
      margin: 0 auto;
      padding: 0 2rem 8rem;
    }

    .ritual-section {
      padding: 5rem 0 0;
    }

    .ritual-section:first-child {
      padding-top: 2rem;
    }

    .ritual-section-title {
      font-size: var(--fs-ui);
      letter-spacing: 0.25em;
      text-transform: uppercase;
      color: var(--title-grey);
      font-weight: 500;
      text-align: center;
      margin-bottom: 3em;
    }

    .ritual-text {
      padding-left: 20%;
      font-size: var(--fs-body);
      line-height: 1.85;
      color: var(--body);
    }

    .ritual-text p {
      margin-bottom: 1.6em;
    }

    .ritual-text p:last-child {
      margin-bottom: 0;
    }

    @media (max-width: 680px) {
      .ritual-body { padding: 0 1.5rem 6rem; }

      .ritual-text {
        padding-left: 0;
        width: fit-content;
        margin: 0 auto;
      }
    }
    """)


def build_spec_css() -> str:
    return textwrap.dedent("""\
    /* ── Spec layout ──────────────────────────────────────────── */

    .spec-body {
      max-width: var(--content-width);
      margin: 0 auto;
      padding: 0 2rem 8rem;
    }

    .spec-section {
      padding: 5rem 0 0;
    }

    .spec-section:first-child {
      padding-top: 2rem;
    }

    .spec-section-title {
      font-size: var(--fs-ui);
      letter-spacing: 0.25em;
      text-transform: uppercase;
      color: var(--title-grey);
      font-weight: 500;
      margin-bottom: 2em;
      border-bottom: 0.5px solid var(--hairline);
      padding-bottom: 0.6em;
    }

    .spec-text {
      font-size: var(--fs-body);
      line-height: 1.75;
      color: var(--body);
    }

    .spec-text p { margin-bottom: 0.9em; }
    .spec-text p:last-child { margin-bottom: 0; }

    .spec-text ol, .spec-text ul {
      margin: 0 0 0.9em 1.5em;
      padding: 0;
    }

    .spec-text li { margin-bottom: 0.4em; }

    .spec-text strong { font-weight: 600; }
    .spec-text em { font-style: italic; }
    .spec-text code { font-family: monospace; font-size: 0.875em; }

    .spec-text h1, .spec-text h2, .spec-text h3 {
      font-size: var(--fs-ui);
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--title-grey);
      margin: 1.8em 0 0.7em;
    }

    @media (max-width: 680px) {
      .spec-body { padding: 0 1.5rem 6rem; }
    }
    """)


def build_full_css() -> str:
    return textwrap.dedent("""\
    /* ── Full layout (side-by-side) ───────────────────────────── */

    .full-body {
      max-width: 1160px;
      margin: 0 auto;
      padding: 0 2rem 8rem;
    }

    .full-section {
      padding: 5rem 0 0;
    }

    .full-section:first-child {
      padding-top: 2rem;
    }

    .full-section-title {
      font-size: var(--fs-ui);
      letter-spacing: 0.25em;
      text-transform: uppercase;
      color: var(--title-grey);
      font-weight: 500;
      text-align: center;
      margin-bottom: 1.5em;
      grid-column: 1 / -1;
    }

    .full-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4rem;
      position: relative;
    }

    .full-grid::before {
      content: '';
      position: absolute;
      left: 50%;
      top: 9em;
      bottom: 2em;
      width: 0.5px;
      background: var(--hairline);
      pointer-events: none;
    }

    /* Column headers — visible on first section only */
    .full-col-label {
      font-size: var(--fs-meta);
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--meta-grey);
      font-weight: 500;
      margin-bottom: 1.8em;
    }

    .full-section:not(:first-child) .full-col-label {
      display: none;
    }

    /* Extra top spacing on grid when labels are hidden */
    .full-section:not(:first-child) .full-grid {
      padding-top: 1.4em;
    }

    /* Ritual column */
    .full-ritual {
      text-align: left;
    }

    .full-ritual .full-col-label { text-align: left; padding-left: 20%; }

    .full-ritual-text {
      padding-left: 20%;
      font-size: var(--fs-body);
      line-height: 1.85;
      color: var(--body);
    }

    .full-ritual-text p {
      margin-bottom: 1.5em;
    }

    .full-ritual-text p:last-child { margin-bottom: 0; }

    /* Spec column */
    .full-spec {
      text-align: left;
      padding-left: 2rem;
    }

    .full-spec-text {
      font-size: var(--fs-body);
      line-height: 1.75;
      color: var(--body);
    }

    .full-spec-text p { margin-bottom: 0.9em; }
    .full-spec-text p:last-child { margin-bottom: 0; }

    .full-spec-text ol, .full-spec-text ul {
      margin: 0 0 0.9em 1.5em;
      padding: 0;
    }

    .full-spec-text li { margin-bottom: 0.4em; }

    .full-spec-text strong { font-weight: 600; }
    .full-spec-text em { font-style: italic; }
    .full-spec-text code { font-family: monospace; font-size: 0.875em; }

    .full-spec-text h1, .full-spec-text h2, .full-spec-text h3 {
      font-size: var(--fs-ui);
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--title-grey);
      margin: 1.8em 0 0.7em;
    }

    /* Responsive: stack on narrow screens */
    @media (max-width: 900px) {
      .full-body { padding: 0 1.5rem 6rem; }

      .full-grid {
        grid-template-columns: 1fr;
        gap: 3rem;
      }

      .full-grid::before {
        display: none;
      }

      .full-ritual .full-col-label {
        padding-left: 0;
        width: fit-content;
        margin: 0 auto;
      }

      .full-ritual-text {
        padding-left: 0;
        width: fit-content;
        margin: 0 auto;
      }

      .full-spec {
        padding-left: 0;
        border-top: 0.5px solid var(--hairline);
        padding-top: 3rem;
      }
    }
    """)


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

FONT_SCRIPT = textwrap.dedent("""\
<script>
(function() {
  var page = document.getElementById('page');
  var loader = document.getElementById('loader');
  function reveal() {
    page.classList.add('ready');
    loader.classList.add('fade-out');
    setTimeout(function() { loader.style.display = 'none'; }, 500);
  }
  if (document.fonts && document.fonts.load) {
    document.fonts.load('400 1em "Cormorant Garamond"').then(reveal, reveal);
    setTimeout(reveal, 3000);
  } else {
    reveal();
  }
})();
</script>
""")

LOADING_OVERLAY = textwrap.dedent("""\
<div class="loading-overlay" id="loader">
  <svg class="loading-spinner" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <circle cx="24" cy="24" r="6" fill="#bbb" />
  </svg>
</div>
""")

FOOTER_HTML = textwrap.dedent("""\
  <footer class="page-footer">
    <p>Set in <a href="https://github.com/CatharsisFonts/Cormorant">Cormorant Garamond</a>, designed by Christian Thalmann, released under the SIL Open Font License.</p>
    <p>Licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Open source on <a href="https://github.com/RKelln/covenant">GitHub</a>.</p>
  </footer>
""")

DIVIDER_HTML = textwrap.dedent("""\
<div class="section-divider">
  <a href="#toc" aria-label="Back to contents">
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <text x="100" y="134.56"
            font-family="'Cormorant Garamond', Georgia, 'Times New Roman', serif"
            font-size="180" font-weight="500" text-anchor="middle"
            transform="rotate(90, 100, 100)">&#167;</text>
    </svg>
  </a>
</div>
""")


def page_shell(
    title: str,
    description: str,
    canonical: str,
    css: str,
    current_nav: str,
    body: str,
) -> str:
    version = get_version()
    nav = NAV_HTML.replace(
        f'href="{current_nav}"',
        f'href="{current_nav}" class="current"',
    )
    return textwrap.dedent(f"""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{title} — Covenant {version}</title>
      <meta name="description" content="{description}">
      <link rel="canonical" href="https://covenant.website/{canonical}">

      <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Ctext x='100' y='134.56' font-family='Georgia,serif' font-size='180' font-weight='500' text-anchor='middle' fill='%23000' transform='rotate(90,100,100)'%3E%C2%A7%3C/text%3E%3C/svg%3E">

      <!-- Open Graph -->
      <meta property="og:type" content="website">
      <meta property="og:title" content="{title} — Covenant">
      <meta property="og:description" content="{description}">
      <meta property="og:url" content="https://covenant.website/{canonical}">
      <meta property="og:image" content="https://covenant.website/covenant_logo.png">

      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">

      <style>
    {textwrap.indent(css, "    ")}
      </style>
    </head>
    <body>
    <noscript><style>.loading-overlay {{ display: none; }} .page {{ opacity: 1; }}</style></noscript>

    {LOADING_OVERLAY}
    <div class="page" id="page">

    {nav}
    {body}
    {FOOTER_HTML}
    </div>

    {FONT_SCRIPT}
    </body>
    </html>
    """)


# ---------------------------------------------------------------------------
# Ritual page
# ---------------------------------------------------------------------------


def build_ritual_page(sections: list) -> str:
    css = build_base_css() + build_ritual_css()

    header = PAGE_HEADER_TMPL.format(
        title="Ritual Edition",
        desc="The poetic register &mdash; aspiration, orientation, and moral voice.",
        pdf_url="https://github.com/RKelln/covenant/releases/latest/download/covenant.ritual.pdf",
    )
    toc = toc_html(sections, "Contents")

    section_parts = []
    for i, (data, parts) in enumerate(sections):
        ritual_text = parts.get("Ritual", "").strip()
        if not ritual_text:
            continue
        anchor = section_anchor(data)
        title = html_escape(data.get("title", ""))
        ritual_html = ritual_to_html(ritual_text)
        divider = "" if i == 0 else DIVIDER_HTML
        section_parts.append(
            f"{divider}"
            f'<section class="ritual-section" id="{anchor}">\n'
            f'  <div class="ritual-section-title">{title}</div>\n'
            f'  <div class="ritual-text">\n{textwrap.indent(ritual_html, "    ")}\n  </div>\n'
            f"</section>"
        )

    body = (
        header
        + toc
        + '<div class="ritual-body">\n'
        + "\n".join(section_parts)
        + "\n</div>"
    )

    return page_shell(
        title="Ritual Edition",
        description="The Covenant ritual register — aspiration, moral orientation, and poetic voice.",
        canonical="ritual.html",
        css=css,
        current_nav="ritual.html",
        body=body,
    )


# ---------------------------------------------------------------------------
# Spec page
# ---------------------------------------------------------------------------


def build_spec_page(sections: list) -> str:
    css = build_base_css() + build_spec_css()

    header = PAGE_HEADER_TMPL.format(
        title="Specification Edition",
        desc="The normative register &mdash; obligations, prohibitions, and accountability.",
        pdf_url="https://github.com/RKelln/covenant/releases/latest/download/covenant.spec.pdf",
    )
    toc = toc_html(sections, "Contents")

    section_parts = []
    for i, (data, parts) in enumerate(sections):
        spec_text = parts.get("Spec", "").strip()
        if not spec_text:
            continue
        anchor = section_anchor(data)
        title = html_escape(data.get("title", ""))
        spec_html = spec_to_html(spec_text)
        divider = "" if i == 0 else DIVIDER_HTML
        section_parts.append(
            f"{divider}"
            f'<section class="spec-section" id="{anchor}">\n'
            f'  <div class="spec-section-title">{title}</div>\n'
            f'  <div class="spec-text">\n{textwrap.indent(spec_html, "    ")}\n  </div>\n'
            f"</section>"
        )

    body = (
        header
        + toc
        + '<div class="spec-body">\n'
        + "\n".join(section_parts)
        + "\n</div>"
    )

    return page_shell(
        title="Specification Edition",
        description="The Covenant specification register — obligations, prohibitions, and accountability.",
        canonical="spec.html",
        css=css,
        current_nav="spec.html",
        body=body,
    )


# ---------------------------------------------------------------------------
# Full page
# ---------------------------------------------------------------------------


def build_full_page(sections: list) -> str:
    css = build_base_css() + build_full_css()

    header = PAGE_HEADER_TMPL.format(
        title="Complete Edition",
        desc="Both registers side by side &mdash; ritual and specification for each section.",
        pdf_url="https://github.com/RKelln/covenant/releases/latest/download/covenant.pdf",
    )
    toc = toc_html(sections, "Contents")

    section_parts = []
    for i, (data, parts) in enumerate(sections):
        ritual_text = parts.get("Ritual", "").strip()
        spec_text = parts.get("Spec", "").strip()
        if not ritual_text and not spec_text:
            continue

        anchor = section_anchor(data)
        title = html_escape(data.get("title", ""))

        ritual_html = ritual_to_html(ritual_text) if ritual_text else "<p>&nbsp;</p>"
        spec_html_content = spec_to_html(spec_text) if spec_text else "<p>&nbsp;</p>"

        divider = "" if i == 0 else DIVIDER_HTML
        section_parts.append(
            f"{divider}"
            f'<section class="full-section" id="{anchor}">\n'
            f'  <div class="full-grid">\n'
            f'    <div class="full-section-title">{title}</div>\n'
            f'    <div class="full-ritual">\n'
            f'      <div class="full-col-label" aria-hidden="true">Ritual</div>\n'
            f'      <div class="full-ritual-text">\n{textwrap.indent(ritual_html, "        ")}\n      </div>\n'
            f"    </div>\n"
            f'    <div class="full-spec">\n'
            f'      <div class="full-col-label" aria-hidden="true">Specification</div>\n'
            f'      <div class="full-spec-text">\n{textwrap.indent(spec_html_content, "        ")}\n      </div>\n'
            f"    </div>\n"
            f"  </div>\n"
            f"</section>"
        )

    body = (
        header
        + toc
        + '<div class="full-body">\n'
        + "\n".join(section_parts)
        + "\n</div>"
    )

    return page_shell(
        title="Complete Edition",
        description="The complete Covenant — ritual and specification registers side by side.",
        canonical="covenant.html",
        css=css,
        current_nav="covenant.html",
        body=body,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Generate Covenant reading pages.")
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=OUTPUT_DEFAULT,
        help=f"Output directory (default: {OUTPUT_DEFAULT})",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    sections = load_assembly_sections(ASSEMBLY_FILE)
    print(f"Loaded {len(sections)} sections from {ASSEMBLY_FILE.name}")

    pages = [
        ("ritual.html", build_ritual_page(sections)),
        ("spec.html", build_spec_page(sections)),
        ("covenant.html", build_full_page(sections)),
    ]

    for filename, html in pages:
        out = args.output_dir / filename
        out.write_text(html, encoding="utf-8")
        print(f"Written: {out}")


if __name__ == "__main__":
    main()
