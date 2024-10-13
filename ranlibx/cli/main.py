import time

import typer
import uvicorn

from ranlibx import authentication, flow, server, state
from ranlibx.api.schemas.token import AuthToken
from ranlibx.cli.subcmds import install
from ranlibx.server import UvicornServerProcess
from ranlibx.state import AuthFlowState

# CLI App
app = typer.Typer(rich_markup_mode="rich")

# Subcommands
app.add_typer(install.app, name="install")


# FYI 127.0.0.1 is localhost
@app.command()
def open_auth_server(host: str = "127.0.0.1", port: int = 8000, verbose: bool = False):
    """
    Opens a Server for RAN Authentication

    Note: Only use `verbose` if you are trying to debug. Otherwise, it is unnecessary
    """
    state.set_auth_flow_state(AuthFlowState.IN_PROGRESS)

    # Create the server
    config = uvicorn.Config(
        "ranlibx.api.main:app", host=host, port=port, log_level=("info" if verbose else "critical")
    )
    fastapi_server = uvicorn.Server(config)

    # Set the server (so it persists beyond this function)
    server_process: UvicornServerProcess = UvicornServerProcess(fastapi_server)
    server.active_uvicorn_server_process = server_process

    # Start it
    server.active_uvicorn_server_process.start(verbose=verbose)

    # Send a message in terminal telling the user to go to the browser cli login
    typer.echo(f"Go to https://ran.so/login/cli?callback_port={port} to log in (you'll come back here, dw)")

    # Stall while in progress
    browser_auth_successful: bool = flow.wait_for_browser_auth(verbose=verbose)

    # Kill server
    state.kill_server(verbose=verbose)

    if not browser_auth_successful:
        # Tell the user to paste in their API Token
        typer.echo(
            "Authentication Failed. Fear not, just paste in your API token if something went wrong (it shows in the browser)"
        )

        # Do it manually
        manual_auth_successful: bool = flow.await_manual_api_token_auth()

        if not manual_auth_successful:
            typer.echo("Max tries reached. Auth unsuccessful. Just try again")
            return

    # "Yay! We are done and the user is logged in!"
    typer.echo(
        "You have successfully logged into RAN!\n:rocket: [orange]Skyrocket[/orange] your Research from Theory to Experiment"
    )


@app.command()
def close_auth_server(verbose: bool = False):
    """Closes the RAN Authentication Server"""
    state.kill_server(verbose=verbose)


@app.command()
def authenticate_token(token: str):
    """Authenticates given a token"""

    # No verbosity since we already have error messages here
    success: bool = authentication.authenticate(AuthToken(token=token), verbose=False)

    if not success:
        raise Exception("Invalid or Expired API Token.")


@app.command()
def ping():
    print("ranx exists!")


# Start the Typer CLI
if __name__ == "__main__":
    app()
