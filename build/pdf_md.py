#!/usr/bin/env python3
"""Render a generic Markdown file to PDF using repo-managed Python dependencies.

This avoids system-level pandoc/pdf-engine issues by using:
- markdown (Python package) for Markdown -> HTML
- weasyprint (Python package) for HTML -> PDF

Usage:
    uv run python build/pdf_md.py --file path/to/file.md [--out path/to/file.pdf]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import markdown as md_lib
import yaml
from weasyprint import CSS, HTML


def extract_frontmatter(text: str) -> tuple[dict, str]:
  """Extract leading YAML frontmatter and return (metadata, body)."""

  lines = text.splitlines(keepends=True)
  if not lines or lines[0].strip() != "---":
    return {}, text

  for idx in range(1, len(lines)):
    if lines[idx].strip() == "---":
      raw_meta = "".join(lines[1:idx])
      body = "".join(lines[idx + 1 :])
      data = yaml.safe_load(raw_meta) or {}
      if not isinstance(data, dict):
        data = {}
      return data, body

  return {}, text


def markdown_to_html(markdown_text: str) -> str:
  return md_lib.markdown(
    markdown_text,
    extensions=[
      "extra",
      "attr_list",
      "sane_lists",
      "smarty",
      "toc",
      "tables",
    ],
  )


def metadata_flag(metadata: dict, key: str, default: bool = False) -> bool:
  value = metadata.get(key, default)
  if isinstance(value, bool):
    return value
  if isinstance(value, str):
    return value.strip().lower() in {"1", "true", "yes", "on"}
  return bool(value)


def render_markdown_to_pdf(md_file: Path, out_file: Path) -> None:
    source = md_file.read_text(encoding="utf-8")
    metadata, source = extract_frontmatter(source)

    title = str(metadata.get("title") or md_file.stem.replace("-", " ").title())
    subtitle = f"By {metadata.get('artist')}" if metadata.get("artist") else ""
    cover_enabled = metadata_flag(metadata, "cover", default=True)
    layout = str(metadata.get("layout") or "default").strip().lower()
    doc_class = "doc brief-layout" if layout == "brief" else "doc"

    body = markdown_to_html(source)

    cover = f"""
  <section class="cover-page">
    <div class="cover-inner">
      <div class="cover-logo">
        <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
          <text x="100" y="134.56" font-family="'Cormorant Garamond', Georgia, 'Times New Roman', serif" font-size="180" font-weight="500" text-anchor="middle" fill="#000" transform="rotate(90, 100, 100)">§</text>
        </svg>
      </div>
      <h1 class="cover-title">{title}</h1>
      {f'<div class="cover-subtitle">{subtitle}</div>' if subtitle else ''}
    </div>
  </section>
  """

    html_doc = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{title}</title>
</head>
<body>
  {cover if cover_enabled else ''}
  <main class=\"{doc_class}\">{body}</main>
</body>
</html>
"""

    css = CSS(
        string="""
@page {
  size: Letter;
  margin: 0.9in;
}

@page covenant-cover {
  size: Letter;
  margin: 0;
}

body {
  font-family: "Avenir Next", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.5;
  color: #111;
}

.doc {
  max-width: 7in;
  margin: 0 auto;
}

.brief-layout {
  max-width: 6.8in;
}

.brief-layout > :first-child {
  margin-top: 0 !important;
}

.cover-page {
  page: covenant-cover;
  width: 8.5in;
  height: 11in;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 1.3in;
  page-break-after: always;
}

.cover-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transform: translateY(-0.35in);
}

.cover-logo {
  margin-bottom: 0.28in;
}

.cover-logo svg {
  display: block;
}

.cover-title {
  margin: 0;
  color: #000;
  font-size: 22pt;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-weight: 500;
  font-family: "Cormorant Garamond", Georgia, "Times New Roman", serif;
}

.cover-subtitle {
  margin-top: 0.28in;
  font-size: 9pt;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #777;
}


blockquote {
  margin: 0.7rem 0;
  padding: 0.15rem 0.45rem;
  border: 0;
  font-family: "Cormorant Garamond", Georgia, "Times New Roman", serif;
  font-size: 12.5pt;
  line-height: 1.5;
}

blockquote.hero-quote,
p.hero-quote {
  margin-top: 0.52in;
  margin-bottom: 0.52in;
  margin-left: auto;
  margin-right: auto;
  max-width: 6.6in;
  padding: 0;
  border: 0;
  font-size: 17pt;
  line-height: 1.28;
  color: #1a1a1a;
  font-weight: 500;
  text-align: center;
  font-family: "Cormorant Garamond", Georgia, "Times New Roman", serif;
}

blockquote.hero-quote p {
  margin: 0;
}

blockquote.hero-quote-soft,
p.hero-quote-soft,
blockquote.hero-quote-left,
p.hero-quote-left {
  margin: 0.36in auto;
  max-width: 6.6in;
  padding: 0;
  border: 0;
  font-size: 13.5pt;
  line-height: 1.32;
  color: #202020;
  font-weight: 500;
  text-align: center;
  font-family: "Cormorant Garamond", Georgia, "Times New Roman", serif;
}

blockquote.hero-quote-soft p,
p.hero-quote-soft,
blockquote.hero-quote-left p,
p.hero-quote-left {
  margin: 0;
}

h1, h2, h3, h4 {
  page-break-after: avoid;
  break-after: avoid-page;
  line-height: 1.2;
}

/* Reusable explicit page-break classes for markdown attr_list */
.page-break-before,
h1.page-break-before,
h2.page-break-before,
h3.page-break-before,
h4.page-break-before,
h5.page-break-before,
h6.page-break-before {
  break-before: page;
  page-break-before: always;
}

.page-break-after,
h1.page-break-after,
h2.page-break-after,
h3.page-break-after,
h4.page-break-after,
h5.page-break-after,
h6.page-break-after {
  break-after: page;
  page-break-after: always;
}

h1 { font-size: 22pt; margin: 0 0 0.5rem; font-weight: 500; }
h2 { font-size: 16pt; margin: 1.2rem 0 0.4rem; }
h3 { font-size: 13pt; margin: 1rem 0 0.3rem; }

p {
  margin: 0.7rem 0;
}

ul, ol {
  margin: 0.55rem 0 0.7rem 1.2rem;
  padding: 0;
}

li + li {
  margin-top: 0.18rem;
}

p, li {
  orphans: 3;
  widows: 3;
}

.brief-layout p {
  margin: 0.48rem 0;
}

.brief-layout ul,
.brief-layout ol {
  margin: 0.3rem 0 0.55rem 1.15rem;
}

.brief-layout li + li {
  margin-top: 0.1rem;
}

.brief-layout h2 {
  font-size: 14pt;
  margin: 0.8rem 0 0.2rem;
}

.brief-layout .section-gap {
  height: 0.1in;
}

.brief-layout blockquote.hero-quote,
.brief-layout p.hero-quote {
  margin-top: 0.34in;
  margin-bottom: 0.28in;
}

.brief-layout blockquote.hero-quote-soft,
.brief-layout p.hero-quote-soft,
.brief-layout blockquote.hero-quote-left,
.brief-layout p.hero-quote-left {
  margin: 0.18in auto;
  max-width: 6in;
  font-size: 14pt;
  line-height: 1.22;
}

img {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 0.6rem auto;
}

a {
  color: inherit;
  text-decoration: none;
}

hr {
  border: 0;
  border-top: 1px solid #d0d0d0;
  margin: 0.8rem 0;
}
"""
    )

    out_file.parent.mkdir(parents=True, exist_ok=True)
    # base_url ensures relative image paths resolve from the source file's folder
    HTML(string=html_doc, base_url=str(md_file.parent)).write_pdf(
        target=str(out_file), stylesheets=[css]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Markdown file to PDF")
    parser.add_argument("--file", required=True, help="Path to source markdown file")
    parser.add_argument(
        "--out",
        help="Output PDF path (default: same directory/name as source with .pdf)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    md_file = Path(args.file)

    if not md_file.exists():
        raise SystemExit(f"Error: file not found: {md_file}")

    if md_file.suffix.lower() != ".md":
        raise SystemExit(f"Error: expected a .md file, got: {md_file}")

    out_file = Path(args.out) if args.out else md_file.with_suffix(".pdf")

    print(f"Building {md_file} -> {out_file}")
    render_markdown_to_pdf(md_file, out_file)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
