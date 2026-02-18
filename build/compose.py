import os
import yaml
import re
from pathlib import Path
from datetime import datetime

# Paths
REPO_ROOT = Path(__file__).parent.parent
ASSEMBLIES_DIR = REPO_ROOT / "assemblies"
DIST_DIR = REPO_ROOT / "dist"

def extract_body_parts(content):
    # Split the body by primary headings (Ritual, Spec, Digest, Log)
    # Using # heading syntax
    parts = {}
    headings = ["# Ritual", "# Spec", "# Digest", "# Log"]
    
    # Sort headings in order of appearance in content
    # Find positions of all headings
    heading_positions = []
    for h in headings:
        pos = content.find(h)
        if pos != -1:
            heading_positions.append((pos, h))
    
    heading_positions.sort()
    
    for i in range(len(heading_positions)):
        pos, h = heading_positions[i]
        start = pos + len(h)
        end = heading_positions[i+1][0] if i+1 < len(heading_positions) else len(content)
        parts[h.replace("# ", "")] = content[start:end].strip()
        
    return parts

def compose_assembly(assembly_file):
    with open(assembly_file, 'r', encoding='utf-8') as f:
        manifest = yaml.safe_load(f)
    
    if not manifest: return

    # Header
    output = []
    output.append(f"# {manifest['title']}\n")
    output.append(f"*Assembled: {datetime.now().strftime('%Y-%m-%d')}*")
    output.append(f"*Sections: {len(manifest['sections'])} | Status filter: {manifest['include_status']}*\n")
    
    # TOC
    output.append("## Table of Contents\n")
    toc_entries = []
    
    composed_sections = []
    for sec_path in manifest['sections']:
        full_path = REPO_ROOT / sec_path
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            parts = content.split('---', 2)
            if len(parts) < 3: continue
            data = yaml.safe_load(parts[1])
            body = parts[2]
            
            if data['status'] not in manifest['include_status']:
                continue
                
            toc_entries.append(f"- [{data['title']}](#{data['id'].replace('.', '-')})")
            
            # Content
            section_content = extract_body_parts(body)
            section_output = [f"## {data['title']} <a id='{data['id'].replace('.', '-')}'></a>\n"]
            
            # Register selection
            reg = manifest['register']
            if reg == 'both':
                if 'Ritual' in section_content:
                    section_output.append("### Ritual\n")
                    section_output.append(section_content['Ritual'] + "\n")
                if 'Spec' in section_content:
                    section_output.append("### Spec\n")
                    section_output.append(section_content['Spec'] + "\n")
            elif reg == 'ritual' and 'Ritual' in section_content:
                section_output.append(section_content['Ritual'] + "\n")
            elif reg == 'spec' and 'Spec' in section_content:
                section_output.append(section_content['Spec'] + "\n")
            
            section_output.append("\n---\n")
            composed_sections.append("".join(section_output))

    output.extend(toc_entries)
    output.append("\n---\n")
    output.extend(composed_sections)
    
    return "".join(output)

def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    
    for assembly_file in ASSEMBLIES_DIR.glob("*.yml"):
        print(f"Composing: {assembly_file.name}")
        content = compose_assembly(assembly_file)
        if content:
            output_path = DIST_DIR / f"{Path(assembly_file).stem}.md"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Written: {output_path}")

if __name__ == "__main__":
    main()
