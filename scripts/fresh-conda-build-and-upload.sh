#!/usr/bin/env bash

# Install rattler-build, grayskull, and conda-recipe-manager
pixi global install rattler-build grayskull conda-recipe-manager

# Build and Upload conda to prefix.dev
./conda-build-and-upload.sh
