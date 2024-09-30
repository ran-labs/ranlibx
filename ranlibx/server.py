import asyncio
import threading
from typing import Optional, Union

import uvicorn


class UvicornServerProcess:
    def __init__(self, server: uvicorn.Server, server_thread: threading.Thread):
        self.server = server
        self.server_thread = server_thread

    def start(self):
        self.server_thread.start()

    def end(self, verbose: bool = False):
        if verbose:
            print("Shutting down server...")

        self.server.should_exit = True
        self.server.force_exit = True
        asyncio.run(self.server.shutdown())

        if verbose:
            print("Server Stopped")

        # Wait for the server thread to fully terminate
        self.server_thread.join()

        # After that, do whatever you want

    def from_server(server: uvicorn.Server):
        server_thread = threading.Thread(target=server.run)

        return UvicornServerProcess(server, server_thread)


active_uvicorn_server_process: UvicornServerProcess = None


def set_active_uvicorn_server_process(process: UvicornServerProcess):
    global active_uvicorn_server_process

    active_uvicorn_server_process = process
