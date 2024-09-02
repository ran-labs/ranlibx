from typing import List, Dict, Set, Union, Optional

import typer
import uvicorn

import subprocess

from ranx.state import AUTH_FLOW_STATE


app = typer.Typer(rich_markup_mode="rich")

@app.command("install ran")
def install():
    """
    Installs RAN globally
    """
    print("Hello World!")
    

@app.command()
def open_auth_server():
    
    pass


@app.command()
def close_auth_server():
    pass


# Start the Typer CLI
if __name__ == "__main__":
    app()

