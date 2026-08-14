.PHONY: validate build clean

PYTHON ?= python3
TYPST ?= typst

validate:
	$(PYTHON) scripts/validate.py

build: validate
	$(PYTHON) scripts/build_data.py
	$(TYPST) compile --root . src/main.typ build/misterios-do-kernel.pdf

clean:
	rm -rf build
