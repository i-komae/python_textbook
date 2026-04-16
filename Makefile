.DEFAULT_GOAL := pdf

MAIN := main
BUILD_DIR := build
CACHE_DIR := $(BUILD_DIR)/texmf-cache
VAR_DIR := $(BUILD_DIR)/texmf-var

LATEXMK := latexmk
MAKEINDEX_STYLE := $(abspath styles/index.ist)
MAKEINDEX_CMD := upmendex -g -s "$(MAKEINDEX_STYLE)" %O -o %D %S
LATEXMK_MAKEINDEX_FLAG := -e '$$makeindex=q{$(MAKEINDEX_CMD)}'
LATEXMK_FLAGS := -f -lualatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=$(BUILD_DIR) $(LATEXMK_MAKEINDEX_FLAG)
LATEXMK_FORCE_FLAGS := -f -gg -lualatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=$(BUILD_DIR) $(LATEXMK_MAKEINDEX_FLAG)
OPEN_PDF := sh scripts/open_pdf.sh

SOURCES := $(MAIN).tex $(wildcard .latexmkrc) $(wildcard chapters/*.tex) $(wildcard assets/figures/*) $(wildcard styles/*)

.PHONY: all pdf clean distclean

open: $(MAIN).pdf
	$(OPEN_PDF) $(MAIN).pdf

all: | $(BUILD_DIR) $(CACHE_DIR) $(VAR_DIR)
	TEXMFCACHE=$(CACHE_DIR) TEXMFVAR=$(VAR_DIR) $(LATEXMK) $(LATEXMK_FORCE_FLAGS) $(MAIN).tex
	cp $(BUILD_DIR)/$(MAIN).pdf $(MAIN).pdf
	cp $(BUILD_DIR)/$(MAIN).synctex.gz .
	$(OPEN_PDF) $(MAIN).pdf

pdf: $(MAIN).pdf

$(MAIN).pdf: $(BUILD_DIR)/$(MAIN).pdf
	cp $(BUILD_DIR)/$(MAIN).pdf $@
	cp $(BUILD_DIR)/$(MAIN).synctex.gz .
	$(OPEN_PDF) $@

$(BUILD_DIR)/$(MAIN).pdf: $(SOURCES) | $(BUILD_DIR) $(CACHE_DIR) $(VAR_DIR)
	TEXMFCACHE=$(CACHE_DIR) TEXMFVAR=$(VAR_DIR) $(LATEXMK) $(LATEXMK_FLAGS) $(MAIN).tex

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(CACHE_DIR):
	mkdir -p $(CACHE_DIR)

$(VAR_DIR):
	mkdir -p $(VAR_DIR)

clean:
	TEXMFCACHE=$(CACHE_DIR) TEXMFVAR=$(VAR_DIR) $(LATEXMK) -c -output-directory=$(BUILD_DIR) $(MAIN).tex

distclean: clean
	rm -f $(BUILD_DIR)/$(MAIN).pdf
	rm -f $(MAIN).pdf
	rm -f $(MAIN).synctex.gz
