from typing import List, Dict, Set, Union, Optional

import typer
import uvicorn

from ranx.cli.subcmds import install

from ranx.state import AUTH_FLOW_STATE, AuthFlowState


app = typer.Typer(rich_markup_mode="rich")

# Subcommands
app.add_typer(install.app, name="install")


@app.command()
def test():
    """For testing purposes"""
    import subprocess

    subprocess.run('uvicorn ranx.api.main:app && kill $(pgrep -P $uvicorn_pid)', shell=True)


@app.command()
def open_auth_server(host: str = "127.0.0.1", port: int = 8000):
    """Opens a Server for RAN Authentication"""
    global AUTH_FLOW_STATE

    AUTH_FLOW_STATE = AuthFlowState.IN_PROGRESS
    
    # Run the server
    uvicorn.run(
        "server:api",
        host=host,
        port=port,
        reload=False
    )


@app.command()
def close_auth_server():
    """Closes the RAN Authentication Server"""
    global AUTH_FLOW_STATE

    AUTH_FLOW_STATE = AuthFlowState.INACTIVE
    
    # TODO: kill uvicorn server


# Start the Typer CLI
if __name__ == "__main__":
    app()

