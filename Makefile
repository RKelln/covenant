.PHONY: all validate compose build clean clean-slides new-section pdf pdf-ritual pdf-spec pdf-full pdf-md fonts website serve watermark watermark-interactive

PYTHON := uv run python

# ── Primary targets ────────────────────────────────────────────────────────
#
#   make all                  — validate, compose, generate PDFs + website
#   make build                — validate + compose (markdown only)
#

all: validate pdf website

validate:
	$(PYTHON) build/validate.py

compose:
	$(PYTHON) build/compose.py

build: validate compose

# ── PDF generation ─────────────────────────────────────────────────────────
#
#   make pdf                  — all assemblies, format auto-detected
#   make pdf-ritual           — ritual layout, US Letter
#   make pdf-spec             — flowing spec document
#   make pdf-full             — per section: ritual centred page, then spec pages (hybrid)
#   make pdf-md FILE=path.md  — generic markdown → PDF via Python markdown + weasyprint
#   make pdf-ritual SIZE=a4   — override page size
#   make pdf ASSEMBLY=covenant.ritual FORMAT=ritual SIZE=letter
#   make pdf-md FILE=path.md OUT=path.pdf
#
# Sizes: letter (default), a4
# Requires: markdown and weasyprint Python packages (uv sync installs them)

ASSEMBLY ?=
FORMAT   ?= auto
SIZE     ?= letter
ALIGN    ?= left

pdf: compose
ifdef ASSEMBLY
	$(PYTHON) build/pdf.py --assembly $(ASSEMBLY) --format $(FORMAT) --size $(SIZE) --align $(ALIGN)
else
	$(PYTHON) build/pdf.py --all --format $(FORMAT) --size $(SIZE) --align $(ALIGN)
endif

pdf-ritual: compose
	$(PYTHON) build/pdf.py --assembly covenant.ritual --format ritual --size $(SIZE) --align $(ALIGN)

pdf-spec: compose
	$(PYTHON) build/pdf.py --assembly covenant.spec --format flow --size $(SIZE)

pdf-full: compose
	$(PYTHON) build/pdf.py --assembly covenant.full --format hybrid --size $(SIZE) --align $(ALIGN)

pdf-md:
	@test -n "$(FILE)" || (echo "Usage: make pdf-md FILE=path/to/file.md [OUT=path/to/output.pdf]" && exit 1)
	@test -f "$(FILE)" || (echo "Error: FILE not found: $(FILE)" && exit 1)
	$(PYTHON) build/pdf_md.py --file "$(FILE)" $(if $(OUT),--out "$(OUT)",)

# ── Website ─────────────────────────────────────────────────────────────────
#
#   make website              — generate docs/index.html from section sources
#   make serve                — build website + start local preview server
#

website:
	$(PYTHON) build/website.py
	$(PYTHON) build/pages.py

serve: website
	@echo "Serving at http://localhost:8000"
	$(PYTHON) -m http.server 8000 -d docs

# ── Watermark ───────────────────────────────────────────────────────────────
#
#   make watermark             — generate tile + x-ray to assets/
#   make watermark-interactive — launch local web UI with live sliders
#

watermark:
	$(PYTHON) build/watermark.py --xray

watermark-interactive:
	$(PYTHON) build/watermark.py --interactive

# ── Slides ──────────────────────────────────────────────────────────────────
#
#   make slides                              — build all talks in docs/talks/
#   make slides FILE=docs/talks/covenant-review-pipeline.md
#   make slides-pdf                          — render all talks to PDF
#   make slides-open                         — build and open in browser
#

D2_LAYOUT ?= elk
TALK_FILES = $(wildcard docs/talks/*.md)
SLIDE_INPUTS = $(if $(FILE),$(FILE),$(TALK_FILES))
TALK_NAME = $(if $(FILE),$(patsubst %.marp,%,$(basename $(notdir $(FILE)))),)
SLIDES_TALK_DIR = $(if $(TALK_NAME),dist/talks/$(TALK_NAME),)
SLIDES_DIST_FILE = $(if $(TALK_NAME),$(SLIDES_TALK_DIR)/$(TALK_NAME).md,)
SLIDES_HTML_FILE = $(if $(TALK_NAME),$(SLIDES_TALK_DIR)/$(TALK_NAME).html,)
SLIDES_PDF_FILE = $(if $(TALK_NAME),$(SLIDES_TALK_DIR)/$(TALK_NAME).pdf,)

slides:
	@set -e; \
	if [ -n "$(FILE)" ] && [ ! -f "$(FILE)" ]; then \
		echo "Error: FILE not found: $(FILE)"; \
		echo "Available talks:"; \
		ls -1 docs/talks/*.md; \
		exit 1; \
	fi; \
	for file in $(SLIDE_INPUTS); do \
		talk_name="$${file##*/}"; \
		talk_name="$${talk_name%.md}"; \
		talk_name="$${talk_name%.marp}"; \
		talk_dir="dist/talks/$$talk_name"; \
		dist_file="$$talk_dir/$$talk_name.md"; \
		html_file="$$talk_dir/$$talk_name.html"; \
		echo "Building $$file -> $$html_file"; \
		D2_LAYOUT=$(D2_LAYOUT) $(PYTHON) build/build-slides.py $$file; \
		marp --allow-local-files --output $$html_file $$dist_file; \
	done

slides-pdf:
	@set -e; \
	if [ -n "$(FILE)" ] && [ ! -f "$(FILE)" ]; then \
		echo "Error: FILE not found: $(FILE)"; \
		echo "Available talks:"; \
		ls -1 docs/talks/*.md; \
		exit 1; \
	fi; \
	for file in $(SLIDE_INPUTS); do \
		talk_name="$${file##*/}"; \
		talk_name="$${talk_name%.md}"; \
		talk_name="$${talk_name%.marp}"; \
		talk_dir="dist/talks/$$talk_name"; \
		dist_file="$$talk_dir/$$talk_name.md"; \
		pdf_file="$$talk_dir/$$talk_name.pdf"; \
		echo "Building $$file -> $$pdf_file"; \
		D2_LAYOUT=$(D2_LAYOUT) $(PYTHON) build/build-slides.py --embed $$file; \
		marp --allow-local-files --pdf --output $$pdf_file $$dist_file; \
	done

slides-open: slides
	@set -e; \
	if [ -n "$(FILE)" ]; then \
		html_files="$(SLIDES_HTML_FILE)"; \
	else \
		html_files=`find dist/talks -mindepth 2 -maxdepth 2 -name '*.html' | sort`; \
	fi; \
	for html_file in $$html_files; do \
		open $$html_file 2>/dev/null || \
		xdg-open $$html_file 2>/dev/null || \
		echo "Open $$html_file manually"; \
	done

# ── Housekeeping ────────────────────────────────────────────────────────────

fonts:
	$(PYTHON) build/install_fonts.py

clean-slides:
	rm -rf dist/talks
	@echo "Cleaned dist/talks/"

clean:
	rm -f dist/*.md dist/*.pdf dist/*.html
	@echo "Cleaned dist/"

new-section:
	@test -n "$(ID)" || (echo "Usage: make new-section ID=category.name TITLE=\"Title\"" && exit 1)
	@test -n "$(TITLE)" || (echo "Usage: make new-section ID=category.name TITLE=\"Title\"" && exit 1)
	$(PYTHON) build/scaffold.py $(ID) "$(TITLE)"
