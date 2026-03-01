import os
import yaml
import re
from pathlib import Path
from datetime import datetime

from sections import REPO_ROOT, ASSEMBLIES_DIR, extract_body_parts

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
    output.append(f"*Assembled: {datetime.now().strftime('%Y-%m-%d')}*\n")
    output.append(
        f"*Sections: {len(manifest['sections'])} | Status filter: {manifest['include_status']}*\n\n"
    )

    # Prepend Summary if it exists
    summary_file = REPO_ROOT / "docs" / "PROJECT_SUMMARY.md"
    if summary_file.exists():
        output.append("\n---\n")
        with open(summary_file, "r", encoding="utf-8") as sf:
            output.append(sf.read())
        output.append("\n\n")

    # TOC
    output.append("## Table of Contents\n")
    toc_entries = []

    composed_sections = []
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

            toc_entries.append(f"- [{data['title']}](#{data['id'].replace('.', '-')})")

            # Content
            section_content = extract_body_parts(body)
            section_output = [
                f"## {data['title']} <a id='{data['id'].replace('.', '-')}'></a>\n"
            ]

            # Register selection
            reg = manifest["register"]
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

            composed_sections.append("".join(section_output))

    output.extend([entry + "\n" for entry in toc_entries])
    output.append("\n---\n")
    output.append("\n---\n".join(composed_sections))

    # Append Credits if it exists
    credits_file = REPO_ROOT / "docs" / "CREDITS.md"
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
            output_path = DIST_DIR / f"{Path(assembly_file).stem}.md"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
