import asyncio
import threading
import time
from typing import Optional, Union

import typer
import uvicorn


def stop_server(userver: uvicorn.Server):
    userver.should_exit = True
    userver.force_exit = True
    asyncio.run(userver.shutdown())


class UvicornServerProcess:
    def __init__(self, server: uvicorn.Server):
        self.server = server
        self.server_thread = None  # type: threading.Thread

    def start(self, verbose: bool = False):
        # Set it
        self.server_thread = threading.Thread(target=self.server.run)

        # Start it
        self.server_thread.start()

        # not sure why this has to be included but it works and breaks without it
        time.sleep(0.5)

        if verbose:
            typer.echo("Started server.")

    def end(self, verbose: bool = False):
        if verbose:
            typer.echo("Shutting down server...")

        stop_server(self.server)

        if verbose:
            typer.echo("Server Stopped")

        # Wait for the server thread to fully terminate
        self.server_thread.join()

        # After that, do whatever you want


active_uvicorn_server_process: UvicornServerProcess = None
