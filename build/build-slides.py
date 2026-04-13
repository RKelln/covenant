#!/usr/bin/env python3
"""
build-slides.py — Build Marp slide sources by rendering D2 blocks and bundling assets.

Usage:
    python3 build/build-slides.py outreach/talks/covenant-review-pipeline.md
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

REPO = Path(__file__).parent.parent
TALK_DIR = REPO / "outreach" / "talks"
DIST_TALK_DIR = REPO / "dist" / "talks"


def talk_name_for(md_path):
    """Return a stable bundle name for a talk source file."""
    name = md_path.name
    for suffix in (".marp.md", ".md"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return md_path.stem


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


def build_output_paths(md_path):
    """Map a talk source file to its generated bundle paths."""
    resolved_md_path = md_path.resolve()
    talk_name = talk_name_for(resolved_md_path)
    talk_dir = DIST_TALK_DIR / talk_name
    asset_dir = talk_dir / "assets"
    output_path = talk_dir / f"{talk_name}.md"
    diagram_dir = asset_dir / "diagrams"
    return output_path, asset_dir, diagram_dir


def classify_asset_type(source_path):
    """Map a file extension to a normalized asset type folder."""
    ext = source_path.suffix.lower()
    if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif"}:
        return "images"
    if ext in {".ttf", ".otf", ".woff", ".woff2"}:
        return "fonts"
    if ext in {".mp4", ".webm", ".mov", ".m4v"}:
        return "video"
    if ext in {".mp3", ".wav", ".ogg", ".m4a", ".flac"}:
        return "audio"
    if ext in {".pdf", ".txt", ".md", ".json", ".csv"}:
        return "docs"
    return "misc"


def trim_type_prefix(rel_path, asset_type):
    """Avoid redundant nesting like assets/fonts/fonts/..."""
    if not rel_path.parts:
        return rel_path
    first = rel_path.parts[0].lower()
    prefixes = {
        "images": {"images", "image", "img"},
        "fonts": {"fonts", "font"},
        "video": {"video", "videos"},
        "audio": {"audio", "sounds", "sound"},
        "docs": {"docs", "doc", "documents"},
    }
    if first in prefixes.get(asset_type, set()):
        trimmed = (
            Path(*rel_path.parts[1:])
            if len(rel_path.parts) > 1
            else Path(rel_path.name)
        )
        return trimmed
    return rel_path


def bundle_asset_subpath(source_path, source_dir):
    """Choose an assets/<type>/ path inside a talk bundle for a local file."""
    source_path = source_path.resolve()
    source_dir = source_dir.resolve()
    repo_assets_dir = (REPO / "assets").resolve()
    talk_dir = TALK_DIR.resolve()
    repo_root = REPO.resolve()
    asset_type = classify_asset_type(source_path)

    if source_path.is_relative_to(source_dir):
        rel_path = source_path.relative_to(source_dir)
    elif source_path.is_relative_to(talk_dir):
        rel_path = source_path.relative_to(talk_dir)
    elif source_path.is_relative_to(repo_assets_dir):
        rel_path = source_path.relative_to(repo_assets_dir)
    elif source_path.is_relative_to(repo_root):
        rel_path = source_path.relative_to(repo_root)
    else:
        rel_path = Path(source_path.name)

    rel_path = trim_type_prefix(rel_path, asset_type)
    return Path(asset_type) / rel_path


def copy_bundle_asset(source_path, source_dir, asset_dir):
    """Copy a local asset into a talk bundle and return its new path."""
    target_path = asset_dir / bundle_asset_subpath(source_path, source_dir)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)
    return target_path


def rewrite_reference_path(raw_path, source_dir, output_dir, asset_dir):
    """Rewrite a relative asset path into the talk bundle asset directory."""
    stripped = raw_path.strip()
    if not stripped:
        return raw_path

    parsed = urlsplit(stripped)
    if parsed.scheme or stripped.startswith(("#", "/", "//")):
        return raw_path

    resolved_path = (source_dir / parsed.path).resolve(strict=False)
    if not resolved_path.exists() or resolved_path.is_dir():
        return raw_path

    bundled_path = copy_bundle_asset(resolved_path, source_dir, asset_dir)
    relative_path = os.path.relpath(bundled_path, output_dir)
    rewritten = parsed._replace(path=Path(relative_path).as_posix())
    return urlunsplit(rewritten)


def rewrite_local_references(md_text, source_dir, output_dir, asset_dir):
    """Copy local assets into a talk bundle and rewrite references to them."""

    def replace_markdown_link(match):
        return (
            f"{match.group(1)}"
            f"{rewrite_reference_path(match.group(2), source_dir, output_dir, asset_dir)}"
            f"{match.group(3)}"
        )

    def replace_html_attr(match):
        rewritten = rewrite_reference_path(
            match.group(3),
            source_dir,
            output_dir,
            asset_dir,
        )
        return f"{match.group(1)}={match.group(2)}{rewritten}{match.group(2)}"

    def replace_css_url(match):
        rewritten = rewrite_reference_path(
            match.group(2),
            source_dir,
            output_dir,
            asset_dir,
        )
        return f"url({match.group(1)}{rewritten}{match.group(1)})"

    md_text = re.sub(
        r"(\!?\[[^\]]*\]\()([^\s)]+)(\))",
        replace_markdown_link,
        md_text,
    )
    md_text = re.sub(
        r"\b(src|href|poster)=(['\"])([^'\"]+)\2",
        replace_html_attr,
        md_text,
    )
    md_text = re.sub(
        r"url\((['\"]?)([^)'\"]+)\1\)",
        replace_css_url,
        md_text,
    )
    return md_text


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
                rel = svg_path.relative_to(diagram_dir.parent.parent)
                img_tag = f"\n![{block['id']}]({rel})\n"
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

    output_path, asset_dir, diagram_dir = build_output_paths(md_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    asset_dir.mkdir(parents=True, exist_ok=True)
    diagram_dir.mkdir(parents=True, exist_ok=True)

    md_text = md_path.read_text(encoding="utf-8")
    blocks = extract_d2_blocks(md_text)

    print(f"Found {len(blocks)} D2 blocks in {md_path.name}")

    for block in blocks:
        svg_path = render_d2_svg(block["id"], block["content"], diagram_dir)
        if svg_path:
            block["svg_path"] = svg_path

    converted_md = convert_markdown(md_text, blocks, diagram_dir, embed=args.embed)
    converted_md = rewrite_local_references(
        converted_md,
        md_path.parent,
        output_path.parent,
        asset_dir,
    )

    output_path.write_text(converted_md, encoding="utf-8")
    print(f"\nConverted markdown: {output_path}")


if __name__ == "__main__":
    main()
