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


def run_uvicorn_server2():
    server = multiprocessing.Popen(
        ["uvicorn", "ranx.api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=None,
        stderr=None,
    )

    return server


def run_uvicorn_server(host: str, port: int):
    #task = asyncio.create_task(uvicorn.run(app, host=host, port=port))
    #task.get_loop().run_forever()
    #asyncio.set_event_loop(loop)
    
    #return task.get_loop()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(uvicorn.run(app, host=host, port=port))


def worker_function(name):
    print(f"Hello from {name}")
    # Simulate some work
    time.sleep(2)
    print(f"{name} has finished")


@app.command()
def test():
    """For testing purposes"""

    def run_fastapi_server():
        run_uvicorn_server(host="0.0.0.0", port=8000)
    
    print("Hello World!")
    
    fastapi_server_process = multiprocessing.Process(target=run_fastapi_server, daemon=True)
    fastapi_server_process.start()
    running_uvicorn_server = True
    
    print("PROCESS STARTED")

    time.sleep(3)

    print("EXITING PROCESS")
    fastapi_server_process.terminate()
    fastapi_server_process.join()
    print("Process Exited")

    running_uvicorn_server = False


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

