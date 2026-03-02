.PHONY: all validate compose build clean new-section pdf pdf-ritual pdf-spec pdf-full fonts website serve

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
#   make pdf-ritual SIZE=a4   — override page size
#   make pdf ASSEMBLY=covenant.ritual FORMAT=ritual SIZE=letter
#
# Sizes: letter (default), a4
# Requires: weasyprint and markdown (uv sync installs them)

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

# ── Website ─────────────────────────────────────────────────────────────────
#
#   make website              — generate docs/index.html from section sources
#   make serve                — build website + start local preview server
#

website:
	$(PYTHON) build/website.py

serve: website
	@echo "Serving at http://localhost:8000"
	$(PYTHON) -m http.server 8000 -d docs

# ── Housekeeping ────────────────────────────────────────────────────────────

fonts:
	$(PYTHON) build/install_fonts.py

clean:
	rm -f dist/*.md dist/*.pdf
	@echo "Cleaned dist/"

new-section:
	@test -n "$(ID)" || (echo "Usage: make new-section ID=category.name TITLE=\"Title\"" && exit 1)
	@test -n "$(TITLE)" || (echo "Usage: make new-section ID=category.name TITLE=\"Title\"" && exit 1)
	$(PYTHON) build/scaffold.py $(ID) "$(TITLE)"
