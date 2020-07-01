#!/bin/bash

CONDA_DIR=${PWD}/build/conda
CONDA_DIR_NAME=symbiflow-arch-defs

export PATH="${CONDA_DIR}/bin:$PATH"

# Use Conda hook for user shell
SHELL_NAME=`basename $SHELL`
CONDA_HOOK_COMMAND="${CONDA_DIR}/bin/conda shell.${SHELL_NAME} hook"
eval "$(${CONDA_HOOK_COMMAND})"

conda activate ${CONDA_DIR_NAME}
