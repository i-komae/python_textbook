MAIN := main
BUILD_DIR := build
CACHE_DIR := $(BUILD_DIR)/texmf-cache
VAR_DIR := $(BUILD_DIR)/texmf-var

LATEXMK := latexmk
LATEXMK_FLAGS := -f -gg -pv -lualatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=$(BUILD_DIR)

SOURCES := $(MAIN).tex $(wildcard chapters/*.tex) $(wildcard assets/figures/*)

.PHONY: all pdf clean distclean

all: pdf

pdf: $(MAIN).pdf

$(MAIN).pdf: $(BUILD_DIR)/$(MAIN).pdf
	cp $(BUILD_DIR)/$(MAIN).pdf $@

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
