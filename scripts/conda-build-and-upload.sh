#!/usr/bin/env bash

# NOTE: This should be executed as `scripts/conda-build-and-upload.sh`, not `./conda-build-and-upload.sh`
# Additionally, this file assumes you already have the prerequisites installed

# Find the built PyPI package
pypi_build=$(find ./dist -maxdepth 1 -type f -name "*.tar.gz" | head -n 1)

# make temp directory
mkdir scripts/temp

# Generate a meta.yaml from the local pypi build that already happened
grayskull pypi "$pypi_build" --output scripts/temp

cd scripts/temp
pwd # for debug purposes

# Convert meta.yaml to a recipe.yaml
conda-recipe-manager convert ranlibx/meta.yaml > ./recipe.yaml # scripts/temp/recipe.yaml

# Build it for conda with rattler-build
rattler-build build --recipe ./recipe.yaml

# move the output folder outside (scripts/temp/output -> scripts/output)
mv ./output ../output

# go back to root and remove temp directory
cd ../..
rm -rf temp

# Get the .conda file to upload
conda_build=$(find ./scripts/output/noarch -maxdepth 1 -type f -name "*.conda" | head -n 1)

# Upload to prefix.dev
pixi run -e dev python3 scripts/upload-prefixdev.py "$conda_build" "$PREFIX_DEV_TOKEN"

