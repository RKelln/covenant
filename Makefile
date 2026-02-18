.PHONY: validate compose build clean new-section

PYTHON := python3

validate:
	$(PYTHON) build/validate.py

compose:
	$(PYTHON) build/compose.py

build: validate compose

clean:
	rm -f dist/*.md
	@echo "Cleaned dist/"

new-section:
	@test -n "$(ID)" || (echo "Usage: make new-section ID=category.name TITLE=\"Title\"" && exit 1)
	@test -n "$(TITLE)" || (echo "Usage: make new-section ID=category.name TITLE=\"Title\"" && exit 1)
	$(PYTHON) build/scaffold.py $(ID) "$(TITLE)"
