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

    # Header
    output = []
    output.append(f"# {manifest['title']}\n")
    output.append(
        f"*{get_version()} — Assembled: {datetime.now().strftime('%Y-%m-%d')}*\n"
    )
    output.append(
        f"*Sections: {len(manifest['sections'])} | Status filter: {manifest['include_status']}*\n\n"
    )

    # Prepend Summary if it exists
    summary_file = REPO_ROOT / "docs" / "project_summary.md"
    if summary_file.exists():
        output.append("\n---\n")
        with open(summary_file, "r", encoding="utf-8") as sf:
            output.append(sf.read())
        output.append("\n\n")

    # Load all sections into a dict keyed by section ID
    reg = manifest["register"]
    sections_by_id = {}
    sections_ordered = []  # preserves order for flat (non-grouped) assemblies
    for sec_path in manifest["sections"]:
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

    def render_section(data, section_content, heading_level=2, show_heading=True):
        anchor = data["id"].replace(".", "-")
        section_output = []
        if show_heading:
            prefix = "#" * heading_level
            section_output.append(f"{prefix} {data['title']} <a id='{anchor}'></a>\n")
        else:
            # Invisible anchor so TOC links still work
            section_output.append(f"<a id='{anchor}'></a>\n")
        if reg == "both":
            if "Ritual" in section_content:
                section_output.append("### Ritual\n")
                section_output.append(section_content["Ritual"] + "\n")
            if "Spec" in section_content:
                section_output.append("### Spec\n")
                section_output.append(section_content["Spec"] + "\n")
        elif reg == "ritual" and "Ritual" in section_content:
            section_output.append(section_content["Ritual"] + "\n")
        elif reg == "spec" and "Spec" in section_content:
            section_output.append(section_content["Spec"] + "\n")
        return "".join(section_output)

    # TOC
    output.append("## Table of Contents\n")
    toc_entries = []
    groups = manifest.get("groups")

    if groups:
        # Build a set of section IDs covered by groups for quick lookup
        grouped_ids = {sid for g in groups for sid in g.get("sections", [])}
        for i, group in enumerate(groups, 1):
            song_anchor = f"song-{i}"
            toc_entries.append(f"- [{group['title']}](#{song_anchor})")
            for sid in group.get("sections", []):
                if sid in sections_by_id:
                    data, _ = sections_by_id[sid]
                    anchor = data["id"].replace(".", "-")
                    toc_entries.append(f"  - [{data['title']}](#{anchor})")
        # Any sections not in any group still get their own TOC entry
        for sid in sections_ordered:
            if sid not in grouped_ids:
                data, _ = sections_by_id[sid]
                anchor = data["id"].replace(".", "-")
                toc_entries.append(f"- [{data['title']}](#{anchor})")
    else:
        for sid in sections_ordered:
            data, _ = sections_by_id[sid]
            toc_entries.append(f"- [{data['title']}](#{data['id'].replace('.', '-')})")

    output.extend([entry + "\n" for entry in toc_entries])
    output.append("\n---\n")

    # Compose body
    composed_sections = []
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
            composed_sections.append("\n".join(group_parts))
        # Ungrouped sections appended at the end
        for sid in sections_ordered:
            if sid not in grouped_ids:
                data, section_content = sections_by_id[sid]
                composed_sections.append(
                    render_section(data, section_content, heading_level=2)
                )
    else:
        for sid in sections_ordered:
            data, section_content = sections_by_id[sid]
            composed_sections.append(
                render_section(data, section_content, heading_level=2)
            )

    output.append("\n---\n".join(composed_sections))

    # Append Credits if it exists
    credits_file = REPO_ROOT / "docs" / "credits.md"
    if credits_file.exists():
        output.append("\n---\n")
        with open(credits_file, "r", encoding="utf-8") as cf:
            output.append(cf.read())

    return "".join(output)


def main():
    os.makedirs(DIST_DIR, exist_ok=True)

    for assembly_file in ASSEMBLIES_DIR.glob("*.yml"):
        print(f"Composing: {assembly_file.name}")
        content = compose_assembly(assembly_file)
        if content:
            manifest_meta = (
                yaml.safe_load(assembly_file.read_text(encoding="utf-8")) or {}
            )
            output_stem = manifest_meta.get("output") or Path(assembly_file).stem
            output_path = DIST_DIR / f"{output_stem}.md"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
