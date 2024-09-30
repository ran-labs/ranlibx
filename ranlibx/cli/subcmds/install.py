import subprocess

import typer

app = typer.Typer()


@app.command(name="ran")
def install_ran(package_manager: str = "pipx"):
    """
    Installs RAN globally (via pipx by default)
    """
    print("Installing RAN...")
    subprocess.run(f"{package_manager} install ran", shell=True)
