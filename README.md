# ranx

This CLI is for some of the global RAN operations such as authentication through the terminal that are not necessarily needed if one were to be a consumer of the RAN the library.
For now, its purpose is for opening and closing receiver servers for auth through terminal, but it is also gonna be used as a global RAN CLI (project agnostic) so you can literally use it like an `npx` (or in this case, [px](https://github.com/AmeerArsala/px))

**NOTE: This is designed to be installed GLOBALLY (e.g. via `pipx` or `pixi global`). This is so that users need only install it on their system one time and that's it.**

## Usage

```bash
pipx install ranlibx
```

```bash
ranx --help
```

## Development

Prequisites: you must have [pixi](https://pixi.sh) and [pipelight](https://pipelight.dev) installed.
```bash
# Install dependencies
pixi install -e dev
pixi run -e dev setup  # This just runs `pipelight enable git-hooks` WHICH IS MANDATORY

# If you want to access the shell, similar to `micromamba activate` or `conda activate` (highly recommended during development)
pixi shell --change-ps1=false -e dev
```

To do releases:
1. After committing your code changes, change the version in `pyproject.toml`
2. Run `scripts/update-version.sh`. It will make an update version commit on your behalf
3. Create a release and push your code like so:

```bash
git tag v1.2.3
git push origin main v1.2.3
```

