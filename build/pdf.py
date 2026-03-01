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
CSS_FILE = REPO_ROOT / "assets" / "pdf.css"

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

SECTION_HEADINGS = ["# Ritual", "# Spec", "# Digest", "# Log"]

PAGE_SIZES = {
    "letter": {"css": "8.5in 11in", "width": "8.5in",  "height": "11in",  "cover_pt": "3in"},
    "a4":     {"css": "A4",          "width": "210mm",   "height": "297mm", "cover_pt": "80mm"},
}


def extract_body_parts(body: str) -> dict:
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
    content = path.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    data = yaml.safe_load(parts[1])
    body_parts = extract_body_parts(parts[2])
    return data, body_parts


def inline_md(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def section_anchor(data: dict) -> str:
    return "s-" + data.get("id", data.get("title", "")).replace(".", "-").replace(" ", "-").lower()


def resolve_section_refs(html: str) -> str:
    """Convert §[section-id] cross-references inside HTML into clickable anchor links."""
    def make_link(m: re.Match) -> str:
        sec_id = m.group(1)
        anchor = "s-" + sec_id.replace(".", "-").replace(" ", "-").lower()
        return f'<a href="#{anchor}" class="xref">§[{sec_id}]</a>'
    return re.sub(r'§\[([a-z0-9.\-]+)\]', make_link, html)


def cover_html(manifest: dict) -> str:
    subtitle = manifest.get("subtitle", "")
    date_str = datetime.now().strftime("%B %d, %Y")
    subtitle_line = f'  <div class="cover-subtitle">{subtitle}</div>\n' if subtitle else ""
    return (
        '<div class="cover-page">\n'
        '  <div class="cover-logo">\n'
        '    <svg width="200" height="100" viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">\n'
        '      <g transform="translate(100, 50) rotate(90) translate(-100, -50)">\n'
        '        <text x="100" y="105" font-family="\'Hoefler Text\', Garamond, \'Times New Roman\', serif" font-size="180" font-weight="normal" text-anchor="middle" fill="#000">§</text>\n'
        '      </g>\n'
        '    </svg>\n'
        '  </div>\n'
        '  <div class="cover-title">Covenant</div>\n'
        f'{subtitle_line}'
        f'  <div class="cover-date">{date_str}</div>\n'
        '</div>'
    )


def summary_html() -> str:
    try:
        summary_path = REPO_ROOT / "docs" / "PROJECT_SUMMARY.md"
        if not summary_path.exists():
            return ""
        
        content = summary_path.read_text(encoding="utf-8")
        try:
            import markdown as md_lib
            body_html = md_lib.markdown(content, extensions=["extra"])
        except ImportError:
            paras = re.split(r"\n\s*\n", content.strip())
            body_html = "\n".join(f"<p>{inline_md(p.strip())}</p>" for p in paras if p.strip())
            body_html = re.sub(r"^#\s+(.+)$", r"<h2>\1</h2>", body_html, flags=re.MULTILINE)
        
        return (
            '<div class="summary-page" id="project-summary">\n'
            f'  <div class="summary-content">\n{body_html}\n  </div>\n'
            '</div>'
        )
    except Exception as e:
        print(f"Warning: Failed to load summary: {e}")
        return ""


def toc_html(sections: list) -> str:
    items = []
    for d in sections:
        anchor = section_anchor(d)
        title = d.get("title", "").strip()
        if " " in title:
            parts = title.rsplit(" ", 1)
            formatted_title = f'{parts[0]} <span class="nowrap-group">{parts[1]}<span class="toc-dots"></span><span class="toc-num" data-href="#{anchor}"></span></span>'
        else:
            formatted_title = f'<span class="nowrap-group">{title}<span class="toc-dots"></span><span class="toc-num" data-href="#{anchor}"></span></span>'
            
        items.append(f'    <li><a href="#{anchor}"><span class="toc-title">{formatted_title}</span></a></li>')

    items_html = "\n".join(items)
    return (
        '<div class="toc-page">\n'
        '  <div class="toc-heading">Index</div>\n'
        '  <ul class="toc-list">\n'
        f'{items_html}\n'
        '  </ul>\n'
        '</div>'
    )


def credits_html() -> str:
    try:
        credits_path = REPO_ROOT / "docs" / "CREDITS.md"
        if not credits_path.exists():
            return ""
        
        content = credits_path.read_text(encoding="utf-8")
        try:
            import markdown as md_lib
            body_html = md_lib.markdown(content, extensions=["extra"])
        except ImportError:
            paras = re.split(r"\n\s*\n", content.strip())
            body_html = "\n".join(f"<p>{inline_md(p.strip())}</p>" for p in paras if p.strip())
            body_html = re.sub(r"^#\s+(.+)$", r"<h2>\1</h2>", body_html, flags=re.MULTILINE)
            body_html = re.sub(r"^##\s+(.+)$", r"<h3>\1</h3>", body_html, flags=re.MULTILINE)
        
        return (
            '<div class="credits-page">\n'
            f'  <div class="credits-content">\n{body_html}\n  </div>\n'
            '</div>'
        )
    except Exception as e:
        print(f"Warning: Failed to load credits: {e}")
        return ""


def load_manifest_sections(manifest: dict) -> list:
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
# Format Builders
# ---------------------------------------------------------------------------

def construct_document_css(size: str, align: str, margin: str, indent: str = "0") -> str:
    ps = PAGE_SIZES[size]
    css_content = CSS_FILE.read_text(encoding="utf-8")
    
    # Prepend the CSS vars that parameterize the stylesheet
    vars_block = f"""
    :root {{
        --page-size: {ps['css']};
        --page-width: {ps['width']};
        --page-height: {ps['height']};
        --cover-pt: {ps['cover_pt']};
        --ritual-align: {align};
        --page-margin: {margin};
    }}
    """
    return vars_block + css_content


def build_ritual_pdf(manifest_file: Path, output_path: Path, size: str = "letter", align: str = "center"):
    from weasyprint import HTML, CSS
    
    manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8"))
    sections = load_manifest_sections(manifest)
    
    html_parts = [
        "<!DOCTYPE html>",
        "<html><head><meta charset='utf-8'></head><body>",
        cover_html(manifest),
        summary_html(),
        toc_html([d for d, _ in sections])
    ]
    
    for (data, parts) in sections:
        ritual_text = parts.get("Ritual", "").strip()
        if not ritual_text:
            continue
            
        stanzas = re.split(r"\n\s*\n", ritual_text)
        rendered_stanzas = [
            f"<div class='stanza'>{p.replace(chr(10), '<br>')}</div>"
            for p in stanzas
        ]
        body_html = "\n".join(rendered_stanzas)
        
        est_lines = sum(len(line) // 70 + 1 for line in ritual_text.split('\n'))
        tp_class = " has-tailpiece" if est_lines <= 24 else ""
        
        html_parts.append(
            f'<div class="ritual-page{tp_class}" id="{section_anchor(data)}">\n'
            f'  <div class="section-title">{data.get("title")}</div>\n'
            f'  <div class="ritual-body">\n{body_html}\n  </div>\n'
            '</div>'
        )

    html_parts.append(credits_html())
    html_parts.append("</body></html>")
    raw_html = "\n".join(html_parts)
    css_string = construct_document_css(size, align, margin="0 0 0.6in 0", indent="0in")

    HTML(string=raw_html, base_url=str(REPO_ROOT)).write_pdf(
        target=str(output_path),
        stylesheets=[CSS(string=css_string)],
        presentational_hints=True
    )


def build_flow_pdf(manifest_file: Path, output_path: Path, size: str = "letter"):
    from weasyprint import HTML, CSS
    try:
        import markdown as md_lib
        def convert_md(t): return md_lib.markdown(t, extensions=["extra", "nl2br"])
    except ImportError:
        print("Warning: python-markdown not found, using poor-man's inline fallback.")
        def convert_md(t):
            res = "\n".join(f"<p>{inline_md(p.strip())}</p>" for p in re.split(r"\n\s*\n", t.strip()))
            return re.sub(r"^#\s+(.+)$", r"<h2>\1</h2>", res, flags=re.MULTILINE)

    manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8"))
    sections = load_manifest_sections(manifest)
    
    html_parts = [
        "<!DOCTYPE html>",
        "<html><head><meta charset='utf-8'></head><body>",
        cover_html(manifest),
        summary_html(),
        toc_html([d for d, _ in sections]),
        '<div class="flow-container">'
    ]
    
    for (data, parts) in sections:
        html_parts.append(f'<div class="section-block" id="{section_anchor(data)}">')
        html_parts.append(f'<h2>{data["title"]}</h2>')
        
        if "Ritual" in parts and parts["Ritual"].strip():
            ritual_raw = parts["Ritual"].strip()
            ritual_paras = re.split(r"\n\s*\n", ritual_raw)
            ritual_rendered = "".join(f"<p><em>{inline_md(p.replace(chr(10), ' '))}</em></p>" for p in ritual_paras)
            html_parts.append(f'<div class="flow-ritual">\n{ritual_rendered}\n</div>')
            
        if "Spec" in parts and parts["Spec"].strip():
            html_parts.append(f'  <h3>Specification</h3>')
            html_parts.append(f'  <div class="flow-spec">\n{resolve_section_refs(convert_md(parts["Spec"]))}\n  </div>')
            
        html_parts.append("</div>")

    html_parts.append("</div>")
    html_parts.append(credits_html())
    html_parts.append("</body></html>")
    raw_html = "\n".join(html_parts)
    css_string = construct_document_css(size, align="left", margin="1in 1.1in 0.8in 1.1in", indent="0in")

    HTML(string=raw_html, base_url=str(REPO_ROOT)).write_pdf(
        target=str(output_path),
        stylesheets=[CSS(string=css_string)],
        presentational_hints=True
    )

def build_hybrid_pdf(manifest_file: Path, output_path: Path, size: str = "letter", align: str = "center"):
    from weasyprint import HTML, CSS
    try:
        import markdown as md_lib
        def convert_md(t): return md_lib.markdown(t, extensions=["extra", "nl2br"])
    except ImportError:
        def convert_md(t):
            res = "\n".join(f"<p>{inline_md(p.strip())}</p>" for p in re.split(r"\n\s*\n", t.strip()))
            return re.sub(r"^#\s+(.+)$", r"<h2>\1</h2>", res, flags=re.MULTILINE)

    manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8"))
    sections = load_manifest_sections(manifest)

    html_parts = [
        "<!DOCTYPE html>",
        "<html><head><meta charset='utf-8'></head><body>",
        cover_html(manifest),
        summary_html(),
        toc_html([d for d, _ in sections])
    ]

    for (data, parts) in sections:
        ritual_text = parts.get("Ritual", "").strip()
        if ritual_text:
            stanzas = re.split(r"\n\s*\n", ritual_text)
            rendered_stanzas = [
                f"<div class='stanza'>{p.replace(chr(10), '<br>')}</div>"
                for p in stanzas
            ]
            body_html = "\n".join(rendered_stanzas)
            
            est_lines = sum(len(line) // 70 + 1 for line in ritual_text.split('\n'))
            tp_class = " has-tailpiece" if est_lines <= 24 else ""
            
            html_parts.append(
                f'<div class="ritual-page{tp_class}" id="{section_anchor(data)}">\n'
                f'  <div class="section-title">{data.get("title")}</div>\n'
                f'  <div class="ritual-body">\n{body_html}\n  </div>\n'
                '</div>'
            )
        
        spec_text = parts.get("Spec", "").strip()
        if spec_text:
            html_parts.append(
                f'<div class="spec-block">\n'
                f'  <h2>{data.get("title")} — Specifications</h2>\n'
                f'{resolve_section_refs(convert_md(spec_text))}\n'
                f'</div>'
            )

    html_parts.append(credits_html())
    html_parts.append("</body></html>")
    raw_html = "\n".join(html_parts)
    
    # For hybrid we do full edge-to-edge layout, and nested flow blocks will respect their own padding
    css_string = construct_document_css(size, align=align, margin="0 0 0.6in 0", indent="0in")
    Path("debug.html").write_text(raw_html, encoding="utf-8")
    
    HTML(string=raw_html, base_url=str(REPO_ROOT)).write_pdf(
        target=str(output_path),
        stylesheets=[CSS(string=css_string)],
        presentational_hints=True
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def process_assembly(assembly_file: Path, format_override: str, size: str, align: str):
    if not assembly_file.exists():
        print(f"Error: {assembly_file} not found.")
        return

    name = assembly_file.name
    output_name = name.replace(".yml", ".pdf")
    output_path = DIST_DIR / output_name

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format_override == "auto":
        if "ritual" in name:
            fmt = "ritual"
        elif "spec" in name:
            fmt = "flow"
        else:
            fmt = "hybrid"
    else:
        fmt = format_override

    print(f"Generating {fmt} PDF [{size}]: {name} → {output_name}")

    if fmt == "ritual":
        build_ritual_pdf(assembly_file, output_path, size=size, align=align)
    elif fmt == "flow":
        build_flow_pdf(assembly_file, output_path, size=size)
    elif fmt == "hybrid":
        build_hybrid_pdf(assembly_file, output_path, size=size, align=align)
    else:
        print(f"Unknown format: {fmt}")
        return
        
    print(f"Written: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate PDFs from covenant assemblies.")
    parser.add_argument("--assembly", default="covenant.full.yml", help="Filename of the assembly (default: covenant.full.yml)")
    parser.add_argument("--format", choices=["ritual", "flow", "hybrid", "auto"], default="auto", help="Layout format (default: auto)")
    parser.add_argument("--size", choices=["letter", "a4"], default="letter", help="Page size (default: letter)")
    parser.add_argument("--align", choices=["center", "left"], default="center", help="Alignment of ritual text")
    parser.add_argument("--all", action="store_true", help="Build all known assemblies (.full, .ritual, .spec)")
    
    args = parser.parse_args()

    try:
        import weasyprint
    except ImportError:
        print("Error: weasyprint is required. Run: pip install weasyprint")
        sys.exit(1)

    if args.all:
        for suffix in ["full", "ritual", "spec"]:
            af = ASSEMBLIES_DIR / f"covenant.{suffix}.yml"
            if af.exists():
                process_assembly(af, args.format, size=args.size, align=args.align)
    else:
        assembly_file = ASSEMBLIES_DIR / args.assembly
        process_assembly(assembly_file, args.format, size=args.size, align=args.align)

if __name__ == "__main__":
    main()
