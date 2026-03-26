#!/usr/bin/env python3
"""
render-d2.py — Extract D2 blocks from markdown and render to SVG.

Usage:
    python3 build/render-d2.py docs/talks/covenant-review-pipeline.md
"""

import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
TALK_DIR = REPO / "docs" / "talks"
DIAGRAM_DIR = TALK_DIR / "diagrams"


def extract_d2_blocks(md_text):
    """Extract all ```d2 blocks with their positions and IDs."""
    pattern = re.compile(r"```d2\n(.*?)```", re.DOTALL)
    blocks = []
    for i, match in enumerate(pattern.finditer(md_text)):
        block_id = f"diagram-{i:02d}"
        blocks.append(
            {
                "id": block_id,
                "content": match.group(1).strip(),
                "start": match.start(),
                "end": match.end(),
            }
        )
    return blocks


def parse_render_directives(d2_content):
    """Extract renderer directives from leading comment lines in a D2 block."""
    lines = d2_content.splitlines()
    layout = None
    consumed = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            consumed += 1
            continue
        match = re.match(r"^#\s*d2-render-layout\s*:\s*(\S+)\s*$", stripped)
        if match:
            layout = match.group(1)
            consumed += 1
            continue
        break

    return {
        "layout": layout,
        "content": "\n".join(lines[consumed:]).strip(),
    }


def render_d2_svg(block_id, d2_content, output_dir):
    """Render D2 to SVG using the d2 CLI."""
    import tempfile

    output_path = output_dir / f"{block_id}.svg"
    directives = parse_render_directives(d2_content)
    layout = directives["layout"] or os.environ.get("D2_LAYOUT")

    try:
        # Write to temp file, then render
        with tempfile.NamedTemporaryFile(mode="w", suffix=".d2", delete=False) as f:
            f.write(directives["content"])
            temp_path = f.name

        command = ["d2", "--pad", "20"]
        if layout:
            command.extend(["--layout", layout])
        if not layout or layout == "dagre":
            command.extend(["--dagre-nodesep", "30", "--dagre-edgesep", "10"])
        command.extend([temp_path, str(output_path)])
        command.extend(["--sketch"])
        result = subprocess.run(
            command,
            capture_output=True,
            timeout=30,
        )

        # Clean up temp file
        Path(temp_path).unlink(missing_ok=True)

        if result.returncode == 0 and output_path.exists():
            # Strip hardcoded width/height from SVG root so CSS can scale it freely.
            # Keep viewBox so aspect ratio is preserved.
            svg_text = output_path.read_text(encoding="utf-8")
            svg_text = re.sub(r'\s+width="[^"]*"', "", svg_text, count=1)
            svg_text = re.sub(r'\s+height="[^"]*"', "", svg_text, count=1)
            output_path.write_text(svg_text, encoding="utf-8")
            print(f"  ✓ {block_id}")
            return output_path
        else:
            print(f"  ✗ {block_id}: {result.stderr[:200]}")
    except Exception as e:
        print(f"  ✗ {block_id}: {e}")
    return None


def convert_markdown(md_text, blocks, diagram_dir, embed=False):
    """Replace D2 blocks with SVG images (linked or embedded)."""
    import base64

    result = md_text
    for block in reversed(blocks):
        svg_path = diagram_dir / f"{block['id']}.svg"
        if svg_path.exists():
            if embed:
                svg_content = svg_path.read_text()
                encoded = base64.b64encode(svg_content.encode()).decode()
                img_tag = f'\n<img src="data:image/svg+xml;base64,{encoded}" alt="{block["id"]}" />\n'
            else:
                # Use Markdown image syntax so Marp rewrites the path correctly
                rel = svg_path.relative_to(diagram_dir.parent)
                img_tag = f'\n![{block["id"]}]({rel})\n'
            result = result[: block["start"]] + img_tag + result[block["end"] :]
        else:
            img_tag = f"\n<!-- {block['id']}: SVG not found -->\n"
            result = result[: block["start"]] + img_tag + result[block["end"] :]
    return result


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Markdown file with D2 blocks")
    parser.add_argument(
        "--embed",
        action="store_true",
        help="Embed SVGs as base64 data URIs (default: link to files)",
    )
    args = parser.parse_args()

    md_path = Path(args.file)
    if not md_path.exists():
        print(f"Error: {md_path} not found")
        sys.exit(1)

    DIAGRAM_DIR.mkdir(parents=True, exist_ok=True)

    md_text = md_path.read_text(encoding="utf-8")
    blocks = extract_d2_blocks(md_text)

    print(f"Found {len(blocks)} D2 blocks in {md_path.name}")

    for block in blocks:
        svg_path = render_d2_svg(block["id"], block["content"], DIAGRAM_DIR)
        if svg_path:
            block["svg_path"] = svg_path

    converted_md = convert_markdown(md_text, blocks, DIAGRAM_DIR, embed=args.embed)

    output_path = md_path.with_suffix(".d2.md")
    output_path.write_text(converted_md, encoding="utf-8")
    print(f"\nConverted markdown: {output_path}")


if __name__ == "__main__":
    main()
