import subprocess
import platform


def install_pixi():
    if platform.system() != "Windows":
        # MacOS and Linux
        subprocess.run("curl -fsSL https://pixi.sh/install.sh | bash", shell=True, check=True)
    else:
        # Windows
        try:
            # Try with PowerShell
            subprocess.run("iwr -useb https://pixi.sh/install.ps1 | iex", shell=True, check=True)
        except subprocess.CalledProcessError:
            # Try with winget
            subprocess.run("winget install prefix-dev.pixi", shell=True, check=True)


def ensure_pixi_installation():
    """Check if pixi is installed and install it if not"""
    try:
        subprocess.run("pixi --version", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Pixi is not installed. Installing pixi...")

        # Install pixi
        install_pixi()

        # Also installs the autocompletion for the respective shell
        # Maybe remove this if it becomes a problem
        # subprocess.run('eval "$(pixi completion --shell bash)"', shell=True, check=True)
        # subprocess.run('eval "$(pixi completion --shell zsh)"', shell=True, check=True)
        # subprocess.run(
        #     'eval "$(pixi completion --shell fish | source)"',
        #     shell=True,
        #     check=True,
        # )
        # subprocess.run(
        #     'eval "$(pixi completion --shell elvish | slurp)"',
        #     shell=True,
        #     check=True,
        # )
