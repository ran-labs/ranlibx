# Run this after updating the pyproject.toml

pixi install
pixi install -e dev

git status
git add pyproject.toml
git add pixi.lock

version=$(python3 scripts/helpers/read-version.py)

git commit -m "[UPDATE] v$version"

# Must happen after or else will point to a previous commit
git tag "v$version"
