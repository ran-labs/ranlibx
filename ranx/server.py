from typing import List, Dict, Union, Optional
from pydantic import BaseModel

import asyncio
import uvicorn
import threading


class UvicornServerProcess(BaseModel):
    server: uvicorn.Server
    server_thread: threading.Thread

    def begin(self):
        self.server_thread.start()

    def from_server(server: uvicorn.Server):
        server_thread = threading.Thread(target=server.run)
        
        return UvicornServerProcess(server=server, server_thread=server_thread)


active_uvicorn_server_process: UvicornServerProcess = None
