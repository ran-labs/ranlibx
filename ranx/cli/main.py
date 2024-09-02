from typing import List, Dict, Set, Union, Optional

import typer
from ranx.cli.subcmds import install

import uvicorn
import asyncio
import threading
import signal

from ranx.state import AUTH_FLOW_STATE, AuthFlowState

import time


# CLI App
app = typer.Typer(rich_markup_mode="rich")

# Subcommands
app.add_typer(install.app, name="install")


@app.command()
def test():
    """For testing purposes"""
    
    print("Starting Server...")
    fastapi_server = uvicorn.Server(uvicorn.Config("ranx.api.main:app", host="0.0.0.0", port=8000, log_level="info"))
    
    #asyncio.run(fastapi_server.serve())
    #server_task = asyncio.create_task(asyncio.run(fastapi_server.serve()))

    # Start the server in a separate thread
    server_thread = threading.Thread(target=fastapi_server.run)
    server_thread.start()

    print("HELLO WORLD")

    time.sleep(3)

    async def stop_server(server: uvicorn.Server):
        server.should_exit = True
        print("Handling")
        server.handle_exit(signal.SIGTERM, frame=None)
        print("Handled")
        await server.shutdown()

    # def stop_server(server: uvicorn.Server):
    #     server.process.send_signal(signal.SIGTERM)
    #     server_thread.join()

    # Shutdown the server
    print("Shutting Down...")
    asyncio.run(stop_server(fastapi_server))
    
    #stop_server(fastapi_server)
    print("Server Stopped")

    # Wait for the server thread to fully terminate
    server_thread.join()

    print("Done waiting")


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

