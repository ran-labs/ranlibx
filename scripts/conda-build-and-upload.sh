#!/usr/bin/env bash

# Install rattler-build, grayskull, and conda-recipe-manager
pixi global install rattler-build grayskull conda-recipe-manager

# Generate a meta.yaml
mkdir temp && cd temp

grayskull pypi ranlibx

# Convert meta.yaml to a recipe.yaml
conda-recipe-manager convert ranlibx/meta.yaml > ./recipe.yaml

# Build it for conda with rattler-build
rattler-build build --recipe ./recipe.yaml

# Move the output folder outside
mv ./output ../output

# go back and remove the directory
cd ..
rm -rf temp

# Get the .conda file to upload
build=$(find ./output/noarch -maxdepth 1 -type f -name "*.conda" | head -n 1)

# Upload to prefix.dev
python3 scripts/upload-prefixdev.py "$build" "$PREFIX_DEV_TOKEN"
