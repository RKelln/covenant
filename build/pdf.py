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
# Shared helpers (imported from sections.py)
# ---------------------------------------------------------------------------

from sections import (  # noqa: E402
    SECTION_HEADINGS,
    extract_body_parts,
    load_section,
    inline_md,
    get_title_map,
    resolve_title,
    get_version,
)

PAGE_SIZES = {
    "letter": {
        "css": "8.5in 11in",
        "width": "8.5in",
        "height": "11in",
        "cover_pt": "3in",
    },
    "a4": {"css": "A4", "width": "210mm", "height": "297mm", "cover_pt": "80mm"},
}


def section_anchor(data: dict) -> str:
    return (
        "s-"
        + data.get("id", data.get("title", ""))
        .replace(".", "-")
        .replace(" ", "-")
        .lower()
    )


def resolve_section_refs(html: str) -> str:
    """Convert §[section-id] cross-references inside HTML into clickable anchor links.

    Display text uses the section's actual title (e.g. §Enforcement)
    rather than the raw ID (§[enforcement]).
    """

    def make_link(m: re.Match) -> str:
        sec_id = m.group(1)
        anchor = "s-" + sec_id.replace(".", "-").replace(" ", "-").lower()
        display = resolve_title(sec_id)
        return f'<a href="#{anchor}" class="xref">§{display}</a>'

    return re.sub(r"§\[([a-z0-9.\-]+)\]", make_link, html)


def cover_html(manifest: dict) -> str:
    subtitle = manifest.get("subtitle", "")
    date_str = datetime.now().strftime("%B %d, %Y")
    version = get_version()
    subtitle_line = (
        f'  <div class="cover-subtitle">{subtitle}</div>\n' if subtitle else ""
    )
    return (
        '<div class="cover-page">\n'
        '  <div class="cover-logo">\n'
        '    <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n'
        '      <text x="100" y="134.56" font-family="\'Cormorant Garamond\', Georgia, \'Times New Roman\', serif" font-size="180" font-weight="500" text-anchor="middle" fill="#000" transform="rotate(90, 100, 100)">§</text>\n'
        "    </svg>\n"
        "  </div>\n"
        '  <div class="cover-title">Covenant</div>\n'
        f"{subtitle_line}"
        f'  <div class="cover-date">{version} — {date_str}</div>\n'
        "</div>"
    )


def summary_html() -> str:
    try:
        summary_path = REPO_ROOT / "docs" / "project_summary.md"
        if not summary_path.exists():
            return ""

        content = summary_path.read_text(encoding="utf-8")
        try:
            import markdown as md_lib

            body_html = md_lib.markdown(content, extensions=["extra"])
        except ImportError:
            paras = re.split(r"\n\s*\n", content.strip())
            body_html = "\n".join(
                f"<p>{inline_md(p.strip())}</p>" for p in paras if p.strip()
            )
            body_html = re.sub(
                r"^#\s+(.+)$", r"<h2>\1</h2>", body_html, flags=re.MULTILINE
            )

        return (
            '<div class="summary-page" id="project-summary">\n'
            f'  <div class="summary-content">\n{body_html}\n  </div>\n'
            "</div>"
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

        items.append(
            f'    <li><a href="#{anchor}"><span class="toc-title">{formatted_title}</span></a></li>'
        )

    items_html = "\n".join(items)
    return (
        '<div class="toc-page">\n'
        '  <div class="toc-heading">§</div>\n'
        '  <ul class="toc-list">\n'
        f"{items_html}\n"
        "  </ul>\n"
        "</div>"
    )


def credits_html() -> str:
    try:
        credits_path = REPO_ROOT / "docs" / "credits.md"
        if not credits_path.exists():
            return ""

        content = credits_path.read_text(encoding="utf-8")
        try:
            import markdown as md_lib

            body_html = md_lib.markdown(content, extensions=["extra", "nl2br"])
        except ImportError:
            paras = re.split(r"\n\s*\n", content.strip())
            body_html = "\n".join(
                f"<p>{inline_md(p.strip())}</p>" for p in paras if p.strip()
            )
            body_html = re.sub(
                r"^#\s+(.+)$", r"<h2>\1</h2>", body_html, flags=re.MULTILINE
            )
            body_html = re.sub(
                r"^##\s+(.+)$", r"<h3>\1</h3>", body_html, flags=re.MULTILINE
            )

        return (
            '<div class="credits-page">\n'
            f'  <div class="credits-content">\n{body_html}\n  </div>\n'
            "</div>"
        )
    except Exception as e:
        print(f"Warning: Failed to load credits: {e}")
        return ""


def load_manifest_sections(manifest: dict) -> list:
    results = []
    for sec_item in manifest.get("sections", []):
        sec_path = sec_item["path"] if isinstance(sec_item, dict) else sec_item
        result = load_section(REPO_ROOT / sec_path)
        if result is None:
            continue
        data, parts = result
        if data.get("status") not in manifest.get("include_status", []):
            continue
        # Apply per-section register override: inject into parts so hybrid builder can respect it
        if isinstance(sec_item, dict) and "register" in sec_item:
            data = dict(data)
            data["_register_override"] = sec_item["register"]
        results.append((data, parts))
    return results


# ---------------------------------------------------------------------------
# Format Builders
# ---------------------------------------------------------------------------


def construct_document_css(
    size: str,
    align: str,
    margin: str,
    indent: str = "0",
    spec_margin: str | None = None,
) -> str:
    ps = PAGE_SIZES[size]
    css_content = CSS_FILE.read_text(encoding="utf-8")

    # Prepend the CSS vars that parameterize the stylesheet
    spec_margin_val = spec_margin if spec_margin else "1in 1.1in 1.1in 1.1in"
    vars_block = f"""
    :root {{
        --page-size: {ps["css"]};
        --page-width: {ps["width"]};
        --page-height: {ps["height"]};
        --cover-pt: {ps["cover_pt"]};
        --ritual-align: {align};
        --page-margin: {margin};
        --spec-page-margin: {spec_margin_val};
    }}
    """
    return vars_block + css_content


def load_markdown_page_html(path: Path) -> str:
    """Render a markdown file as a flow-page div for inclusion in a PDF."""
    try:
        content = path.read_text(encoding="utf-8")
        try:
            import markdown as md_lib

            body_html = md_lib.markdown(content, extensions=["extra"])
        except ImportError:
            paras = re.split(r"\n\s*\n", content.strip())
            body_html = "\n".join(
                f"<p>{inline_md(p.strip())}</p>" for p in paras if p.strip()
            )
            body_html = re.sub(
                r"^#\s+(.+)$", r"<h2>\1</h2>", body_html, flags=re.MULTILINE
            )
        return (
            f'<div class="markdown-page">\n'
            f'  <div class="markdown-content">\n{body_html}\n  </div>\n'
            f"</div>"
        )
    except Exception as e:
        print(f"Warning: Failed to load markdown page {path}: {e}")
        return ""


def resolve_pages(manifest: dict, sections: list) -> list[str]:
    """Return the list of page keywords/paths from the manifest.

    If no 'pages' key is present, return the default ordering that matches
    the original behaviour: cover, project summary, toc, sections, credits.
    """
    return manifest.get(
        "pages",
        [
            "cover",
            "docs/project_summary.md",
            "toc",
            "sections",
            "docs/credits.md",
        ],
    )


def build_ritual_pdf(
    manifest_file: Path, output_path: Path, size: str = "letter", align: str = "center"
):
    from weasyprint import HTML, CSS

    manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8"))
    sections = load_manifest_sections(manifest)
    pages = resolve_pages(manifest, sections)

    section_html_parts = []
    for data, parts in sections:
        ritual_text = parts.get("Ritual", "").strip()
        if not ritual_text:
            continue
        stanzas = re.split(r"\n\s*\n", ritual_text)
        rendered_stanzas = [
            f"<div class='stanza'>{p.replace(chr(10), '<br>')}</div>" for p in stanzas
        ]
        body_html = "\n".join(rendered_stanzas)
        est_lines = sum(len(line) // 70 + 1 for line in ritual_text.split("\n"))
        tp_class = " has-tailpiece" if est_lines <= 24 else ""
        section_html_parts.append(
            f'<div class="ritual-page{tp_class}" id="{section_anchor(data)}">\n'
            f'  <div class="section-title">{data.get("title")}</div>\n'
            f'  <div class="ritual-body">\n{body_html}\n  </div>\n'
            "</div>"
        )

    html_parts = ["<!DOCTYPE html>", "<html><head><meta charset='utf-8'></head><body>"]
    for page in pages:
        if page == "cover":
            html_parts.append(cover_html(manifest))
        elif page == "toc":
            html_parts.append(toc_html([d for d, _ in sections]))
        elif page == "sections":
            html_parts.extend(section_html_parts)
        else:
            md_path = REPO_ROOT / page
            if md_path.exists():
                html_parts.append(load_markdown_page_html(md_path))
    html_parts.append("</body></html>")

    raw_html = "\n".join(html_parts)
    css_string = construct_document_css(size, align, margin="0 0 0.6in 0", indent="0in")
    HTML(string=raw_html, base_url=str(REPO_ROOT)).write_pdf(
        target=str(output_path),
        stylesheets=[CSS(string=css_string, base_url=str(REPO_ROOT))],
        presentational_hints=True,
    )


def build_songs_pdf(
    manifest_file: Path, output_path: Path, size: str = "letter", align: str = "left"
):
    """One page per song group; song title as heading, all section ritual text concatenated."""
    from weasyprint import HTML, CSS

    manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8"))
    groups = manifest.get("groups")
    if not groups:
        # No groups — fall back to standard ritual rendering
        return build_ritual_pdf(manifest_file, output_path, size=size, align=align)

    sections = load_manifest_sections(manifest)
    sections_by_id = {data["id"]: (data, parts) for data, parts in sections}
    pages = resolve_pages(manifest, sections)

    # TOC entries are the song titles
    toc_sections = []
    for i, group in enumerate(groups, 1):
        toc_sections.append({"id": f"song-{i}", "title": group["title"]})

    grouped_ids = {sid for g in groups for sid in g.get("sections", [])}

    song_html_parts = []
    for i, group in enumerate(groups, 1):
        song_id = f"song-{i}"
        title = group["title"]
        url = group.get("url", "").strip()
        title_display = f'<a href="{url}">{title}</a>' if url else title

        all_stanzas = []
        for sid in group.get("sections", []):
            if sid not in sections_by_id:
                continue
            _, parts = sections_by_id[sid]
            ritual_text = parts.get("Ritual", "").strip()
            if not ritual_text:
                continue
            stanzas = re.split(r"\n\s*\n", ritual_text)
            all_stanzas.extend(stanzas)

        rendered_stanzas = [
            f"<div class='stanza'>{s.replace(chr(10), '<br>')}</div>"
            for s in all_stanzas
        ]
        body_html = "\n".join(rendered_stanzas)

        full_text = "\n\n".join(all_stanzas)
        est_lines = sum(len(line) // 70 + 1 for line in full_text.split("\n"))
        tp_class = " has-tailpiece" if est_lines <= 24 else ""

        song_html_parts.append(
            f'<div class="song-page" id="s-{song_id}">\n'
            f'  <div class="song-inner">\n'
            f'    <div class="section-title">{title_display}</div>\n'
            f'    <div class="ritual-body">\n{body_html}\n    </div>\n'
            f"  </div>\n"
            "</div>"
        )

    # Ungrouped sections rendered normally
    ungrouped_html_parts = []
    for data, parts in sections:
        if data["id"] in grouped_ids:
            continue
        ritual_text = parts.get("Ritual", "").strip()
        if not ritual_text:
            continue
        stanzas = re.split(r"\n\s*\n", ritual_text)
        rendered_stanzas = [
            f"<div class='stanza'>{p.replace(chr(10), '<br>')}</div>" for p in stanzas
        ]
        body_html = "\n".join(rendered_stanzas)
        est_lines = sum(len(line) // 70 + 1 for line in ritual_text.split("\n"))
        tp_class = " has-tailpiece" if est_lines <= 24 else ""
        ungrouped_html_parts.append(
            f'<div class="ritual-page{tp_class}" id="{section_anchor(data)}">\n'
            f'  <div class="section-title">{data.get("title")}</div>\n'
            f'  <div class="ritual-body">\n{body_html}\n  </div>\n'
            "</div>"
        )

    html_parts = ["<!DOCTYPE html>", "<html><head><meta charset='utf-8'></head><body>"]
    for page in pages:
        if page == "cover":
            html_parts.append(cover_html(manifest))
        elif page == "toc":
            html_parts.append(toc_html(toc_sections))
        elif page == "sections":
            html_parts.extend(song_html_parts)
            html_parts.extend(ungrouped_html_parts)
        else:
            md_path = REPO_ROOT / page
            if md_path.exists():
                html_parts.append(load_markdown_page_html(md_path))
    html_parts.append("</body></html>")

    raw_html = "\n".join(html_parts)
    css_string = construct_document_css(size, align, margin="0 0 0.6in 0", indent="0in")

    HTML(string=raw_html, base_url=str(REPO_ROOT)).write_pdf(
        target=str(output_path),
        stylesheets=[CSS(string=css_string, base_url=str(REPO_ROOT))],
        presentational_hints=True,
    )


def build_flow_pdf(manifest_file: Path, output_path: Path, size: str = "letter"):
    from weasyprint import HTML, CSS

    try:
        import markdown as md_lib

        def convert_md(t):
            return md_lib.markdown(t, extensions=["extra", "nl2br"])
    except ImportError:
        print("Warning: python-markdown not found, using poor-man's inline fallback.")

        def convert_md(t):
            res = "\n".join(
                f"<p>{inline_md(p.strip())}</p>"
                for p in re.split(r"\n\s*\n", t.strip())
            )
            return re.sub(r"^#\s+(.+)$", r"<h2>\1</h2>", res, flags=re.MULTILINE)

    manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8"))
    sections = load_manifest_sections(manifest)
    pages = resolve_pages(manifest, sections)
    spec_margin = manifest.get("margins", {}).get("spec")

    section_html_parts = ['<div class="flow-container">']
    for data, parts in sections:
        section_html_parts.append(
            f'<div class="section-block" id="{section_anchor(data)}">'
        )
        section_html_parts.append(f"<h2>{data['title']}</h2>")

        if "Ritual" in parts and parts["Ritual"].strip():
            ritual_raw = parts["Ritual"].strip()
            ritual_paras = re.split(r"\n\s*\n", ritual_raw)
            ritual_rendered = "".join(
                f"<p><em>{inline_md(p.replace(chr(10), ' '))}</em></p>"
                for p in ritual_paras
            )
            section_html_parts.append(
                f'<div class="flow-ritual">\n{ritual_rendered}\n</div>'
            )

        if "Summary" in parts and parts["Summary"].strip():
            summary_raw = parts["Summary"].strip()
            section_html_parts.append(
                f'  <div class="flow-summary">\n{resolve_section_refs(convert_md(summary_raw))}\n  </div>'
            )

        if "Spec" in parts and parts["Spec"].strip():
            section_html_parts.append("  <h3>Specification</h3>")
            section_html_parts.append(
                f'  <div class="flow-spec">\n{resolve_section_refs(convert_md(parts["Spec"]))}\n  </div>'
            )

        section_html_parts.append("</div>")
    section_html_parts.append("</div>")

    html_parts = ["<!DOCTYPE html>", "<html><head><meta charset='utf-8'></head><body>"]
    for page in pages:
        if page == "cover":
            html_parts.append(cover_html(manifest))
        elif page == "toc":
            html_parts.append(toc_html([d for d, _ in sections]))
        elif page == "sections":
            html_parts.extend(section_html_parts)
        else:
            md_path = REPO_ROOT / page
            if md_path.exists():
                html_parts.append(load_markdown_page_html(md_path))
    html_parts.append("</body></html>")

    raw_html = "\n".join(html_parts)
    css_string = construct_document_css(
        size,
        align="left",
        margin="1in 1.1in 0.8in 1.1in",
        indent="0in",
        spec_margin=spec_margin,
    )

    HTML(string=raw_html, base_url=str(REPO_ROOT)).write_pdf(
        target=str(output_path),
        stylesheets=[CSS(string=css_string, base_url=str(REPO_ROOT))],
        presentational_hints=True,
    )


def build_hybrid_pdf(
    manifest_file: Path, output_path: Path, size: str = "letter", align: str = "center"
):
    from weasyprint import HTML, CSS

    try:
        import markdown as md_lib

        def convert_md(t):
            return md_lib.markdown(t, extensions=["extra", "nl2br"])
    except ImportError:

        def convert_md(t):
            res = "\n".join(
                f"<p>{inline_md(p.strip())}</p>"
                for p in re.split(r"\n\s*\n", t.strip())
            )
            return re.sub(r"^#\s+(.+)$", r"<h2>\1</h2>", res, flags=re.MULTILINE)

    manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8"))
    sections = load_manifest_sections(manifest)
    pages = resolve_pages(manifest, sections)
    spec_margin = manifest.get("margins", {}).get("spec")

    section_html_parts = []
    global_reg = manifest.get("register", "both")
    for data, parts in sections:
        effective_reg = data.get("_register_override", global_reg)

        ritual_text = parts.get("Ritual", "").strip()
        if ritual_text and effective_reg in ("ritual", "both"):
            stanzas = re.split(r"\n\s*\n", ritual_text)
            rendered_stanzas = [
                f"<div class='stanza'>{p.replace(chr(10), '<br>')}</div>"
                for p in stanzas
            ]
            body_html = "\n".join(rendered_stanzas)

            est_lines = sum(len(line) // 70 + 1 for line in ritual_text.split("\n"))
            tp_class = " has-tailpiece" if est_lines <= 24 else ""

            section_html_parts.append(
                f'<div class="ritual-page{tp_class}" id="{section_anchor(data)}">\n'
                f'  <div class="section-title">{data.get("title")}</div>\n'
                f'  <div class="ritual-body">\n{body_html}\n  </div>\n'
                "</div>"
            )

        spec_text = parts.get("Spec", "").strip()
        summary_text = parts.get("Summary", "").strip()
        if (spec_text or summary_text) and effective_reg in ("spec", "both"):
            spec_inner = ""
            if summary_text:
                spec_inner += f'<div class="spec-summary">\n{resolve_section_refs(convert_md(summary_text))}\n</div>\n'
            if spec_text:
                spec_inner += resolve_section_refs(convert_md(spec_text))
            section_html_parts.append(
                f'<div class="spec-block">\n'
                f"  <h2>{data.get('title')} — Specifications</h2>\n"
                f"{spec_inner}\n"
                f"</div>"
            )

    html_parts = ["<!DOCTYPE html>", "<html><head><meta charset='utf-8'></head><body>"]
    for page in pages:
        if page == "cover":
            html_parts.append(cover_html(manifest))
        elif page == "toc":
            html_parts.append(toc_html([d for d, _ in sections]))
        elif page == "sections":
            html_parts.extend(section_html_parts)
        else:
            md_path = REPO_ROOT / page
            if md_path.exists():
                html_parts.append(load_markdown_page_html(md_path))
    html_parts.append("</body></html>")

    raw_html = "\n".join(html_parts)

    # For hybrid we do full edge-to-edge layout, and nested flow blocks will respect their own padding
    css_string = construct_document_css(
        size, align=align, margin="0 0 0.6in 0", indent="0in", spec_margin=spec_margin
    )
    Path("debug.html").write_text(raw_html, encoding="utf-8")

    HTML(string=raw_html, base_url=str(REPO_ROOT)).write_pdf(
        target=str(output_path),
        stylesheets=[CSS(string=css_string, base_url=str(REPO_ROOT))],
        presentational_hints=True,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def process_assembly(assembly_file: Path, format_override: str, size: str, align: str):
    if not assembly_file.exists():
        print(f"Error: {assembly_file} not found.")
        return

    name = assembly_file.name

    # Load manifest once; use its optional `output` field to override filename
    manifest = yaml.safe_load(assembly_file.read_text(encoding="utf-8"))
    output_stem = manifest.get("output") or Path(name).stem
    output_name = output_stem + ".pdf"
    output_path = DIST_DIR / output_name

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format_override == "auto":
        if "ritual" in name:
            fmt = "ritual"
        elif "spec" in name:
            fmt = "flow"
        elif "songs" in name:
            fmt = "songs"
        else:
            fmt = "songs" if manifest.get("groups") else "hybrid"
    else:
        fmt = format_override

    print(f"Generating {fmt} PDF [{size}]: {name} → {output_name}")

    if fmt == "ritual":
        build_ritual_pdf(assembly_file, output_path, size=size, align=align)
    elif fmt == "flow":
        build_flow_pdf(assembly_file, output_path, size=size)
    elif fmt == "hybrid":
        build_hybrid_pdf(assembly_file, output_path, size=size, align=align)
    elif fmt == "songs":
        build_songs_pdf(assembly_file, output_path, size=size, align=align)
    else:
        print(f"Unknown format: {fmt}")
        return

    print(f"Written: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate PDFs from covenant assemblies."
    )
    parser.add_argument(
        "--assembly",
        default="covenant.full.yml",
        help="Filename of the assembly (default: covenant.full.yml)",
    )
    parser.add_argument(
        "--format",
        choices=["ritual", "flow", "hybrid", "songs", "auto"],
        default="auto",
        help="Layout format (default: auto)",
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
        help="Alignment of ritual text",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Build all known assemblies (.full, .ritual, .spec)",
    )

    args = parser.parse_args()

    try:
        import weasyprint
    except ImportError:
        print("Error: weasyprint is required. Run: uv sync")
        sys.exit(1)

    if args.all:
        for af in sorted(ASSEMBLIES_DIR.glob("*.yml")):
            manifest = yaml.safe_load(af.read_text(encoding="utf-8")) or {}
            if manifest.get("auto_build", True):
                process_assembly(af, args.format, size=args.size, align=args.align)
            else:
                print(f"Skipping (auto_build: false): {af.name}")
    else:
        assembly_file = ASSEMBLIES_DIR / args.assembly
        process_assembly(assembly_file, args.format, size=args.size, align=args.align)


if __name__ == "__main__":
    main()
