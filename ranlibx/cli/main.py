import typer
import uvicorn

from ranlibx import authentication, server
from ranlibx.api.schemas.token import AuthToken
from ranlibx.cli.subcmds import install
from ranlibx.server import UvicornServerProcess
from ranlibx.state import AuthFlowState, kill_server, set_auth_flow_state

# Dev / Testing stuff
# import asyncio
# import threading
# import time


# CLI App
app = typer.Typer(rich_markup_mode="rich")

# Subcommands
app.add_typer(install.app, name="install")


# FYI 127.0.0.1 is localhost
@app.command()
def open_auth_server(host: str = "127.0.0.1", port: int = 8000, verbose: bool = False):
    """Opens a Server for RAN Authentication"""
    set_auth_flow_state(AuthFlowState.IN_PROGRESS)

    # Create the server
    config = uvicorn.Config(
        "ranx.api.main:app", host=host, port=port, log_level=("info" if verbose else "critical")
    )
    fastapi_server = uvicorn.Server(config)

    # Set the server (so it persists beyond this function)
    server.set_active_uvicorn_server_process(UvicornServerProcess.from_server(fastapi_server))

    # Start it
    server.active_uvicorn_server_process.start()


@app.command()
def close_auth_server(verbose: bool = False):
    """Closes the RAN Authentication Server"""
    kill_server(verbose=verbose)


@app.command()
def authenticate_token(token: str):
    """Authenticates given a token"""

    # No verbosity since we already have error messages here
    success: bool = authentication.authenticate(AuthToken(token=token), verbose=False)

    if not success:
        raise Exception("Invalid or Expired API Token.")


@app.command()
def validate_token(token: str):
    """Validates authenticity of a token"""

    valid: bool = authentication.is_token_valid(AuthToken(token=token))

    if not valid:
        raise Exception("Invalid or Expired API Token.")


@app.command()
def ping():
    print("ranx exists!")


# @app.command()
# def test():
#     """For testing purposes"""
#
#     print("Starting Server...")
#     config = uvicorn.Config(
#         "ranlibx.api.main:app",
#         host="0.0.0.0",
#         port=8000,
#         log_level="critical"
#     )
#     fastapi_server = uvicorn.Server(config)
#
#     # Start the server in a separate thread
#     server_thread = threading.Thread(target=fastapi_server.run)
#     server_thread.start()
#
#     print("HELLO WORLD")
#
#     time.sleep(3)
#
#     def stop_server(userver: uvicorn.Server):
#         userver.should_exit = True
#         userver.force_exit = True
#         asyncio.run(userver.shutdown())
#
#     # Shutdown the server
#     print("Shutting Down...")
#     stop_server(fastapi_server)
#     print("Server Stopped")
#
#     # Wait for the server thread to fully terminate
#     server_thread.join()
#
#     print("Done waiting")


# Start the Typer CLI
if __name__ == "__main__":
    app()
