# Run this after updating the pyproject.toml

pixi install
pixi install -e dev

git status
git add pyproject.toml
git add pixi.lock

git commit -m "[UPDATED VERSION]"
