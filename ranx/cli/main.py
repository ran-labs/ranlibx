from typing import List, Dict, Set, Union, Optional

import typer
from ranx.cli.subcmds import install

import uvicorn
import asyncio
import multiprocessing

from ranx.state import AUTH_FLOW_STATE, AuthFlowState

import time


# CLI App
app = typer.Typer(rich_markup_mode="rich")

# Subcommands
app.add_typer(install.app, name="install")


def run_uvicorn_server(host: str, port: int):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(uvicorn.run(app, host=host, port=port))


@app.command()
def test():
    """For testing purposes"""

    def run_fastapi_server():
        run_uvicorn_server(host="0.0.0.0", port=8000)
    
    fastapi_server_process = multiprocessing.Process(target=run_fastapi_server)
    asyncio.create_task(fastapi_server_process.start())
    
    print("PROCESS STARTED")

    async def wait():
        await asyncio.sleep(3)

    asyncio.run(wait())

    print("SHUTTING DOWN")
    asyncio.create_task(fastapi_server_process.terminate())
    asyncio.create_task(fastapi_server_process.join())
    print("SHUTDOWN COMPLETE.")


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

