import json
import logging
from typing import Literal, Optional, Union

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    exceptions,
    status,
)
from fastapi.middleware.cors import CORSMiddleware

# from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from ranx.api import auth
from ranx.constants import RAN_DOMAIN  # ran.so
from ranx.state import kill_server

app = FastAPI(title="RANx (Global)", contact={"name": "Anemo AI", "email": "support@anemo.ai"})

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
