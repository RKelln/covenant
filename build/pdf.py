#!/usr/bin/env python3
"""
Generate PDFs from covenant assemblies.

Usage:
    python build/pdf.py [--assembly NAME] [--format FORMAT] [--size SIZE] [--all]

Formats:
    ritual  — one page per section, ritual text centred vertically and
              horizontally, poetry line-breaks preserved.
    flow    — flowing single document (spec or full register).
    hybrid  — for each section: ritual centred on its own page, then spec
              flows on the following page(s). Designed for full assemblies.
    auto    — chooses ritual for *.ritual assemblies, flow for others
              (default).

Sizes:
    letter  — US Letter 8.5" × 11" (default)
    a4      — ISO A4 210mm × 297mm

Examples:
    python build/pdf.py --all
    python build/pdf.py --assembly covenant.ritual --format ritual --size letter
    python build/pdf.py --assembly covenant.full  --format hybrid
    python build/pdf.py --assembly covenant.spec  --size a4
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
ASSEMBLIES_DIR = REPO_ROOT / "assemblies"
DIST_DIR = REPO_ROOT / "dist"

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

SECTION_HEADINGS = ["# Ritual", "# Spec", "# Digest", "# Log"]


def extract_body_parts(body: str) -> dict:
    """Return {'Ritual': ..., 'Spec': ..., ...} from section body text."""
    positions = []
    for h in SECTION_HEADINGS:
        pos = body.find(h)
        if pos != -1:
            positions.append((pos, h))
    positions.sort()

    parts = {}
    for i, (pos, h) in enumerate(positions):
        start = pos + len(h)
        end = positions[i + 1][0] if i + 1 < len(positions) else len(body)
        parts[h.replace("# ", "")] = body[start:end].strip()
    return parts


def load_section(path: Path):
    """Return (metadata_dict, body_parts_dict) or None on failure."""
    content = path.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    data = yaml.safe_load(parts[1])
    body_parts = extract_body_parts(parts[2])
    return data, body_parts


def inline_md(text: str) -> str:
    """Convert basic inline markdown to HTML (bold, italic, code)."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def section_anchor(data: dict) -> str:
    """Return a stable HTML id for a section, derived from its id field."""
    return "s-" + data.get("id", data.get("title", "")).replace(".", "-").replace(" ", "-").lower()


def cover_html(manifest: dict) -> str:
    """Shared cover page HTML for all formats."""
    subtitle = manifest.get("subtitle", "")
    date_str = datetime.now().strftime("%B %d, %Y")
    subtitle_line = f'  <div class="cover-subtitle">{subtitle}</div>\n' if subtitle else ""
    return (
        '<div class="cover-page">\n'
        '  <div class="cover-title">Covenant</div>\n'
        f'{subtitle_line}'
        f'  <div class="cover-date">{date_str}</div>\n'
        '</div>'
    )


def toc_html(sections: list) -> str:
    """Shared table of contents page HTML for all formats."""
    link_style = 'style="color: #333; text-decoration: none; cursor: pointer;"'
    items = "\n".join(
        f'    <li><a href="#{section_anchor(d)}" {link_style}>{d["title"]}</a></li>'
        for d in sections
    )
    return (
        '<div class="toc-page">\n'
        '  <div class="toc-heading">Contents</div>\n'
        '  <ol class="toc-list">\n'
        f'{items}\n'
        '  </ol>\n'
        '</div>'
    )


def load_manifest_sections(manifest: dict) -> list:
    """Load all applicable (data, parts) pairs from a manifest."""
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



PAGE_SIZES = {
    "letter": {"css": "8.5in 11in", "width": "8.5in",  "height": "11in",  "cover_pt": "4.2in"},
    "a4":     {"css": "A4",          "width": "210mm",   "height": "297mm", "cover_pt": "113mm"},
}


# ---------------------------------------------------------------------------
# CSS building blocks — compose into format functions below
# ---------------------------------------------------------------------------

def _page_base_css(ps: dict, margin: str = "0", counter: bool = False) -> str:
    counter_rule = f"""
    @bottom-center {{
        content: counter(page);
        font-size: 8pt;
        color: #aaa;
    }}""" if counter else ""
    return f"""\
@page {{
    size: {ps['css']};
    margin: {margin};{counter_rule}
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
    font-family: Georgia, "Times New Roman", serif;
    background: white;
    color: #111;
}}

"""


def _ritual_poetry_css(ps: dict, align: str = "center") -> str:
    return f"""\
/* ── ritual centred page ───────────────────────────────────────────── */

.ritual-page {{
    width: {ps['width']};
    height: {ps['height']};
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: {align};
    padding: 1in 1.2in;
    page-break-after: always;
}}

.ritual-page:last-child {{
    page-break-after: avoid;
}}

.section-title {{
    font-size: 8pt;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 3.5em;
    font-weight: normal;
}}

.ritual-body {{
    font-size: 12.5pt;
    line-height: 1.8;
    color: #111;
    text-align: {align};
}}

.stanza {{
    margin-bottom: 1.6em;
}}

.stanza:last-child {{
    margin-bottom: 0;
}}

"""


def _prose_css() -> str:
    return """\
/* ── prose typography ──────────────────────────────────────────────── */

body {
    font-size: 11pt;
    line-height: 1.65;
}

h2 {
    font-size: 11pt;
    font-weight: normal;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #555;
    margin: 2.8em 0 1em;
    border-bottom: 0.5px solid #ccc;
    padding-bottom: 0.3em;
    page-break-after: avoid;
}

h3 {
    font-size: 9.5pt;
    font-weight: normal;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #888;
    margin: 1.8em 0 0.5em;
    page-break-after: avoid;
}

p  { margin: 0 0 0.8em; }

ol, ul { margin: 0 0 0.8em 1.4em; padding: 0; }
li     { margin-bottom: 0.3em; }

strong { font-weight: bold; }
em     { font-style: italic; }
code   { font-family: monospace; font-size: 9.5pt; }

.section-block {
    margin-bottom: 3em;
    page-break-before: always;
}

.section-block:first-of-type {
    page-break-before: avoid;
}

"""


def _spec_block_css() -> str:
    return """\
/* ── spec flowing block (hybrid) ───────────────────────────────────── */

.spec-block {
    padding: 1in 1.1in;
    page-break-before: always;
    font-size: 11pt;
    line-height: 1.65;
}

.spec-block h2 {
    font-size: 11pt;
    font-weight: normal;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #555;
    margin: 0 0 1.2em;
    border-bottom: 0.5px solid #ccc;
    padding-bottom: 0.3em;
}

.spec-block p              { margin: 0 0 0.8em; }
.spec-block ol,
.spec-block ul             { margin: 0 0 0.8em 1.4em; padding: 0; }
.spec-block li             { margin-bottom: 0.3em; }
.spec-block strong         { font-weight: bold; }
.spec-block em             { font-style: italic; }
.spec-block code           { font-family: monospace; font-size: 9.5pt; }

"""


def cover_toc_css(ps: dict) -> str:
    """Shared cover-page and TOC-page CSS for all formats."""
    return f"""\
/* ── named pages: override any format margin for cover/TOC ─────────── */

@page covenant-cover {{
    size: {ps['css']};
    margin: 0;
}}

@page covenant-toc {{
    size: {ps['css']};
    margin: 0;
}}

/* ── cover page ────────────────────────────────────────────────────── */

.cover-page {{
    page: covenant-cover;
    width: {ps['width']};
    height: {ps['height']};
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    text-align: center;
    padding: {ps['cover_pt']} 1.4in 1in;
    page-break-after: always;
}}

.cover-title {{
    font-size: 22pt;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #111;
    margin-bottom: 0.5em;
    font-weight: normal;
}}

.cover-subtitle {{
    font-size: 9pt;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #aaa;
}}

.cover-date {{
    font-size: 8.5pt;
    letter-spacing: 0.1em;
    color: #bbb;
    margin-top: 1em;
}}

/* ── table of contents page ─────────────────────────────────────────── */

.toc-page {{
    page: covenant-toc;
    width: {ps['width']};
    height: {ps['height']};
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1in 1.2in;
    page-break-after: always;
}}

.toc-heading {{
    font-size: 8pt;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 2em;
    font-weight: normal;
}}

.toc-list {{
    list-style: none;
    margin: 0;
    padding: 0;
    font-size: 10.5pt;
    line-height: 1.85;
    color: #333;
    column-count: 2;
    column-gap: 2.5em;
    text-align: left;
    width: 100%;
}}

.toc-list li {{
    margin-bottom: 0.6em;
    break-inside: avoid;
}}
"""


# ---------------------------------------------------------------------------
# Format CSS — composed from building blocks
# ---------------------------------------------------------------------------

def ritual_css(size: str = "letter", align: str = "center") -> str:
    ps = PAGE_SIZES[size]
    return (
        _page_base_css(ps)
        + _ritual_poetry_css(ps, align=align)
        + cover_toc_css(ps)
    )


def flow_css(size: str = "letter") -> str:
    ps = PAGE_SIZES[size]
    return (
        _page_base_css(ps, margin="1in 1.1in 1.1in 1.1in", counter=True)
        + _prose_css()
        + cover_toc_css(ps)
    )


def hybrid_css(size: str = "letter", align: str = "center") -> str:
    ps = PAGE_SIZES[size]
    return (
        _page_base_css(ps)
        + _ritual_poetry_css(ps, align=align)
        + _spec_block_css()
        + cover_toc_css(ps)
    )


def ritual_text_to_html(text: str) -> str:
    """Convert ritual plain-text to stanza-per-div HTML."""
    stanzas = re.split(r"\n\s*\n", text.strip())
    html_parts = []
    for stanza in stanzas:
        lines = [inline_md(ln.strip()) for ln in stanza.strip().splitlines() if ln.strip()]
        if not lines:
            continue
        inner = "<br>\n        ".join(lines)
        html_parts.append(f'<div class="stanza">{inner}</div>')
    return "\n      ".join(html_parts)


def build_ritual_pdf(assembly_file: Path, output_path: Path, size: str = "letter", align: str = "center") -> None:
    try:
        from weasyprint import CSS, HTML
    except ImportError:
        sys.exit(
            "weasyprint is not installed.\n"
            "Run: uv pip install weasyprint  or  uv sync"
        )

    with open(assembly_file, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    sections = load_manifest_sections(manifest)
    pages_html = [cover_html(manifest), toc_html([d for d, _ in sections])]

    for data, parts in sections:
        if "Ritual" not in parts:
            continue

        ritual_html = ritual_text_to_html(parts["Ritual"])

        pages_html.append(
            f"""\
<div class="ritual-page" id="{section_anchor(data)}">
  <div class="section-title">{data['title']}</div>
  <div class="ritual-body">
    {ritual_html}
  </div>
</div>"""
        )

    full_html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{manifest['title']}</title>
</head>
<body>
{''.join(pages_html)}
</body>
</html>
"""

    DIST_DIR.mkdir(exist_ok=True)
    HTML(string=full_html, base_url=str(REPO_ROOT)).write_pdf(
        str(output_path),
        stylesheets=[CSS(string=ritual_css(size, align=align))],
    )
    print(f"Written: {output_path}")



def md_block_to_html(text: str) -> str:
    """
    Convert the block-level markdown used in spec sections to HTML.
    Falls back gracefully if the 'markdown' package is unavailable.
    """
    try:
        import markdown as md_lib

        return md_lib.markdown(text, extensions=["extra"])
    except ImportError:
        # Minimal fallback: wrap paragraphs
        paras = re.split(r"\n\s*\n", text.strip())
        return "\n".join(f"<p>{inline_md(p.strip())}</p>" for p in paras if p.strip())


def build_flow_pdf(assembly_file: Path, output_path: Path, size: str = "letter") -> None:
    try:
        from weasyprint import CSS, HTML
    except ImportError:
        sys.exit(
            "weasyprint is not installed.\n"
            "Run: uv pip install weasyprint  or  uv sync"
        )

    with open(assembly_file, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    sections = load_manifest_sections(manifest)
    register = manifest.get("register", "both")

    body_parts = [cover_html(manifest), toc_html([d for d, _ in sections])]

    for data, parts in sections:
        section_html = [f'<div class="section-block" id="{section_anchor(data)}">']
        section_html.append(f'<h2>{data["title"]}</h2>')

        if register in ("both", "ritual") and "Ritual" in parts:
            if register == "both":
                section_html.append('<h3>Ritual</h3>')
            # Poetry style for ritual even in flow docs
            section_html.append('<div class="ritual-poetry">')
            ritual_html = ritual_text_to_html(parts["Ritual"])
            section_html.append(f'<div class="ritual-body" style="text-align:left">{ritual_html}</div>')
            section_html.append('</div>')

        if register in ("both", "spec") and "Spec" in parts:
            if register == "both":
                section_html.append('<h3>Spec</h3>')
            section_html.append(md_block_to_html(parts["Spec"]))

        section_html.append('</div>')
        body_parts.append("\n".join(section_html))

    full_html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{manifest['title']}</title>
</head>
<body>
{chr(10).join(body_parts)}
</body>
</html>
"""

    DIST_DIR.mkdir(exist_ok=True)
    HTML(string=full_html, base_url=str(REPO_ROOT)).write_pdf(
        str(output_path),
        stylesheets=[CSS(string=flow_css(size))],
    )
# ---------------------------------------------------------------------------
# HYBRID format — ritual centred page + flowing spec, per section
# ---------------------------------------------------------------------------


def build_hybrid_pdf(assembly_file: Path, output_path: Path, size: str = "letter", align: str = "center") -> None:
    """Ritual centred on its own page, spec flows on the next page(s)."""
    try:
        from weasyprint import CSS, HTML
    except ImportError:
        sys.exit(
            "weasyprint is not installed.\n"
            "Run: uv sync"
        )

    with open(assembly_file, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    sections = load_manifest_sections(manifest)
    pages_html = [cover_html(manifest), toc_html([d for d, _ in sections])]

    for data, parts in sections:
        # Ritual page (centred)
        if "Ritual" in parts:
            ritual_html = ritual_text_to_html(parts["Ritual"])
            anchor = section_anchor(data)
            pages_html.append(
                f"""\
<div class="ritual-page" id="{anchor}">
  <div class="section-title">{data['title']}</div>
  <div class="ritual-body">
    {ritual_html}
  </div>
</div>"""
            )

        # Spec block (flowing, new page)
        if "Spec" in parts:
            spec_html = md_block_to_html(parts["Spec"])
            # anchor on spec block only if there's no ritual page to anchor to
            anchor_attr = f' id="{section_anchor(data)}"' if "Ritual" not in parts else ""
            pages_html.append(
                f"""\
<div class="spec-block"{anchor_attr}>
  <h2>{data['title']}</h2>
  {spec_html}
</div>"""
            )

    full_html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{manifest['title']}</title>
</head>
<body>
{''.join(pages_html)}
</body>
</html>
"""

    DIST_DIR.mkdir(exist_ok=True)
    HTML(string=full_html, base_url=str(REPO_ROOT)).write_pdf(
        str(output_path),
        stylesheets=[CSS(string=hybrid_css(size, align=align))],
    )
    print(f"Written: {output_path}")

def resolve_format(assembly_stem: str, explicit_format: str | None) -> str:
    if explicit_format and explicit_format != "auto":
        return explicit_format
    if "ritual" in assembly_stem:
        return "ritual"
    if "full" in assembly_stem:
        return "hybrid"
    return "flow"


def process_assembly(assembly_file: Path, fmt: str | None, size: str = "letter", align: str = "center") -> None:
    stem = assembly_file.stem
    chosen_fmt = resolve_format(stem, fmt)
    output_path = DIST_DIR / f"{stem}.pdf"

    print(f"Generating {chosen_fmt} PDF [{size}]: {assembly_file.name} → {output_path.name}")

    if chosen_fmt == "ritual":
        build_ritual_pdf(assembly_file, output_path, size=size, align=align)
    elif chosen_fmt == "hybrid":
        build_hybrid_pdf(assembly_file, output_path, size=size, align=align)
    else:
        build_flow_pdf(assembly_file, output_path, size=size)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate PDFs from covenant assemblies.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--assembly",
        metavar="NAME",
        help="Assembly stem name, e.g. covenant.ritual (omit to use --all)",
    )
    parser.add_argument(
        "--format",
        choices=["ritual", "flow", "hybrid", "auto"],
        default="auto",
        help="PDF layout format (default: auto)",
    )
    parser.add_argument(
        "--size",
        choices=["letter", "a4"],
        default="letter",
        help="Page size (default: letter)",
    )
    parser.add_argument(
        "--align",
        choices=["center", "left"],
        default="center",
        help="Ritual text alignment: center (default) or left-justified in a centred column",
    )
    parser.add_argument(
        "--all",
        dest="all_assemblies",
        action="store_true",
        help="Generate PDFs for all assemblies",
    )

    args = parser.parse_args()

    if args.all_assemblies:
        for af in sorted(ASSEMBLIES_DIR.glob("*.yml")):
            process_assembly(af, args.format, size=args.size, align=args.align)
    elif args.assembly:
        af = ASSEMBLIES_DIR / f"{args.assembly}.yml"
        if not af.exists():
            sys.exit(f"Assembly not found: {af}")
        process_assembly(af, args.format, size=args.size, align=args.align)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
