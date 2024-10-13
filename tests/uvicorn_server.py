import asyncio
import threading
import time
import uvicorn


def test():
    """For testing purposes"""

    print("Starting Server...")
    config = uvicorn.Config(
        "ranlibx.api.main:app",
        host="127.0.0.1", #"0.0.0.0"
        port=8000,
        log_level="critical"
    )
    fastapi_server = uvicorn.Server(config)

    # Start the server in a separate thread
    server_thread = threading.Thread(target=fastapi_server.run)
    server_thread.start()

    print("HELLO WORLD")

    time.sleep(3)

    def stop_server(userver: uvicorn.Server):
        userver.should_exit = True
        userver.force_exit = True
        asyncio.run(userver.shutdown())

    # Shutdown the server
    print("Shutting Down...")
    stop_server(fastapi_server)
    print("Server Stopped")

    # Wait for the server thread to fully terminate
    server_thread.join()

    print("Done waiting")
