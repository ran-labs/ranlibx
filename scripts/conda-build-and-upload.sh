#!/usr/bin/env bash

# This file assumes you already have the prerequisites installed

# make temp directory
mkdir temp
cd temp

# Generate a meta.yaml
grayskull pypi ranlibx

# Convert meta.yaml to a recipe.yaml
conda-recipe-manager convert ranlibx/meta.yaml > ./recipe.yaml

# Build it for conda with rattler-build
rattler-build build --recipe ./recipe.yaml

# move the output folder outside
mv ./output ../scripts/output

# go back and remove the directory
cd ..
rm -rf temp

# Get the .conda file to upload
build=$(find ./scripts/output/noarch -maxdepth 1 -type f -name "*.conda" | head -n 1)

# Upload to prefix.dev
pixi run -e dev python3 scripts/upload-prefixdev.py "$build" "$PREFIX_DEV_TOKEN"

