#!/usr/bin/env bash

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Install rattler-build, grayskull, and conda-recipe-manager
pixi global install rattler-build grayskull conda-recipe-manager

# Build and Upload conda to prefix.dev
"$SCRIPT_DIR/conda-build-and-upload.sh"
