import os
import yaml
import re
from pathlib import Path
from datetime import datetime

from sections import REPO_ROOT, ASSEMBLIES_DIR, extract_body_parts, get_version

# Paths
DIST_DIR = REPO_ROOT / "dist"


def compose_assembly(assembly_file):
    with open(assembly_file, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    if not manifest:
        return

    # Load all sections into a dict keyed by section ID
    global_reg = manifest["register"]
    sections_by_id = {}
    sections_ordered = []  # preserves order for flat (non-grouped) assemblies
    section_registers = {}  # overrides for specific sections
    for sec_item in manifest["sections"]:
        if isinstance(sec_item, dict):
            sec_path = sec_item["path"]
            override_reg = sec_item.get("register")
        else:
            sec_path = sec_item
            override_reg = None

        full_path = REPO_ROOT / sec_path
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
            parts = content.split("---", 2)
            if len(parts) < 3:
                continue
            data = yaml.safe_load(parts[1])
            body = parts[2]
            if data["status"] not in manifest["include_status"]:
                continue
            section_content = extract_body_parts(body)
            sections_by_id[data["id"]] = (data, section_content)
            sections_ordered.append(data["id"])
            if override_reg:
                section_registers[data["id"]] = override_reg

    def render_section(data, section_content, heading_level=2, show_heading=True):
        anchor = data["id"].replace(".", "-")
        section_output = []
        if show_heading:
            prefix = "#" * heading_level
            section_output.append(f"{prefix} {data['title']} <a id='{anchor}'></a>\n")
        else:
            # Invisible anchor so TOC links still work
            section_output.append(f"<a id='{anchor}'></a>\n")

        reg = section_registers.get(data["id"], global_reg)

        if reg == "both":
            if "Ritual" in section_content:
                section_output.append("### Ritual\n")
                section_output.append(section_content["Ritual"] + "\n")
            if "Summary" in section_content and section_content["Summary"].strip():
                section_output.append("### Summary\n")
                section_output.append(section_content["Summary"] + "\n")
            if "Spec" in section_content:
                section_output.append("### Spec\n")
                section_output.append(section_content["Spec"] + "\n")
        elif reg == "ritual" and "Ritual" in section_content:
            section_output.append(section_content["Ritual"] + "\n")
        elif reg == "spec":
            if "Summary" in section_content and section_content["Summary"].strip():
                section_output.append(section_content["Summary"] + "\n\n")
            if "Spec" in section_content:
                section_output.append(section_content["Spec"] + "\n")
        return "".join(section_output)

    def render_toc():
        groups = manifest.get("groups")
        toc_lines = ["## Table of Contents\n"]
        if groups:
            grouped_ids = {sid for g in groups for sid in g.get("sections", [])}
            for i, group in enumerate(groups, 1):
                song_anchor = f"song-{i}"
                toc_lines.append(f"- [{group['title']}](#{song_anchor})\n")
                for sid in group.get("sections", []):
                    if sid in sections_by_id:
                        data, _ = sections_by_id[sid]
                        anchor = data["id"].replace(".", "-")
                        toc_lines.append(f"  - [{data['title']}](#{anchor})\n")
            for sid in sections_ordered:
                if sid not in grouped_ids:
                    data, _ = sections_by_id[sid]
                    anchor = data["id"].replace(".", "-")
                    toc_lines.append(f"- [{data['title']}](#{anchor})\n")
        else:
            for sid in sections_ordered:
                data, _ = sections_by_id[sid]
                toc_lines.append(
                    f"- [{data['title']}](#{data['id'].replace('.', '-')})\n"
                )
        toc_lines.append("\n---\n")
        return "".join(toc_lines)

    def render_sections_body():
        groups = manifest.get("groups")
        composed = []
        if groups:
            grouped_ids = {sid for g in groups for sid in g.get("sections", [])}
            for i, group in enumerate(groups, 1):
                song_anchor = f"song-{i}"
                title = group["title"]
                url = group.get("url", "").strip()
                if url:
                    song_header = f"# [{title}]({url}) <a id='{song_anchor}'></a>\n"
                else:
                    song_header = f"# {title} <a id='{song_anchor}'></a>\n"
                group_parts = [song_header]
                for sid in group.get("sections", []):
                    if sid in sections_by_id:
                        data, section_content = sections_by_id[sid]
                        group_parts.append(
                            render_section(data, section_content, show_heading=False)
                        )
                composed.append("\n".join(group_parts))
            for sid in sections_ordered:
                if sid not in grouped_ids:
                    data, section_content = sections_by_id[sid]
                    composed.append(
                        render_section(data, section_content, heading_level=2)
                    )
        else:
            for sid in sections_ordered:
                data, section_content = sections_by_id[sid]
                composed.append(render_section(data, section_content, heading_level=2))
        return "\n---\n".join(composed)

    # Build document from pages list.
    # Special keywords: 'cover', 'toc', 'sections'
    # Any other value is treated as a path to a markdown file relative to REPO_ROOT.
    # Default pages list (for backward compatibility): cover, summary, toc, sections, credits.
    pages = manifest.get(
        "pages",
        [
            "cover",
            "docs/project_summary.md",
            "toc",
            "sections",
            "docs/credits.md",
        ],
    )

    output = []
    for page in pages:
        if page == "cover":
            output.append(f"# {manifest['title']}\n")
            output.append(
                f"*{get_version()} — Assembled: {datetime.now().strftime('%Y-%m-%d')}*\n"
            )
            output.append(
                f"*Sections: {len(manifest['sections'])} | Status filter: {manifest['include_status']}*\n\n"
            )
        elif page == "toc":
            output.append(render_toc())
        elif page == "sections":
            output.append(render_sections_body())
        else:
            md_path = REPO_ROOT / page
            if md_path.exists():
                output.append("\n---\n")
                output.append(md_path.read_text(encoding="utf-8"))
                output.append("\n\n")

    return "".join(output)


def main():
    os.makedirs(DIST_DIR, exist_ok=True)

    for assembly_file in ASSEMBLIES_DIR.glob("*.yml"):
        manifest_meta = yaml.safe_load(assembly_file.read_text(encoding="utf-8")) or {}
        if not manifest_meta.get("auto_build", True):
            print(f"Skipping (auto_build: false): {assembly_file.name}")
            continue
        print(f"Composing: {assembly_file.name}")
        content = compose_assembly(assembly_file)
        if content:
            output_stem = manifest_meta.get("output") or Path(assembly_file).stem
            output_path = DIST_DIR / f"{output_stem}.md"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
