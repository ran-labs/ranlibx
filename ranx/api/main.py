from typing import List, Dict, Set, Union, Optional, Literal

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Request,
    exceptions,
)
from fastapi.middleware.cors import CORSMiddleware

# from starlette.middleware.sessions import SessionMiddleware

from fastapi.responses import JSONResponse
from pydantic import ValidationError

import json
import logging

from ranx.api import auth
from ranx.state import kill_server
from ranx.constants import RAN_DOMAIN  # ran.so


app = FastAPI(
    title="RANx (Global)",
    contact={"name": "Anemo AI", "email": "support@anemo.ai"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"https://{RAN_DOMAIN}",
        f"https://lib.{RAN_DOMAIN}",
        f"https://auth.{RAN_DOMAIN}",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth")


@app.get("/")
async def read_root():
    return {"message": "Welcome to your RANx server!"}


# Yes, this is NOT async for a good reason (im pretty sure)
@app.get("/kill")
def kill(verbose: bool = False):
    kill_server(verbose=verbose)


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response["message"].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)
