# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = symbiflow-arch-defs
SOURCEDIR     = source
BUILDDIR      = build

CONDA_DIR       = build/conda
CONDA_ENV_FILE  = environment.yml

# Put it first so that "make" without argument is like "make help".

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

env:
	@rm -rf $(CONDA_DIR)
	@mkdir -p $(CONDA_DIR)
	@wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh\
		-O $(CONDA_DIR)/miniconda.sh
	@bash $(CONDA_DIR)/miniconda.sh -f -b -p  $(CONDA_DIR) && \
		echo "Conda environment created successfully..."
	@./$(CONDA_DIR)/bin/conda env create -q -f $(CONDA_ENV_FILE) && \
		echo "Conda packages installed successfully..."
	@echo "To use conda environment type:\nsource enter-env.sh"

env-clean:
	@rm -rf $(CONDA_DIR)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
