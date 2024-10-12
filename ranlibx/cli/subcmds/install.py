import subprocess

import typer

from ranlibx._external import install_checks

app = typer.Typer()


@app.command(name="ran")
def install_ran(package_manager: str = "pipx"):
    """
    Installs RAN globally (via pipx by default).
    """
    print("Installing RAN...")
    try:
        subprocess.run(f"{package_manager} install ranlib", shell=True, check=True)
    except subprocess.CalledProcessError:
        # Try with pixi
        print(f"Installation with {package_manager} didn't work")

        if package_manager == "pixi":
            # Don't have redundancy
            return

        print("Attempting with pixi...")

        # First, check if pixi is installed
        install_checks.ensure_pixi_installation()

        # Install via pixi (globally)
        subprocess.run("pixi global install ranlib", shell=True, check=True)
