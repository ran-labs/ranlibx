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
from pydantic import BaseModel, ValidationError

import json
import logging

from ranx.constants import RAN_DOMAIN  # ran.so
from ranx.state import AUTH_FLOW_STATE


app = FastAPI(
    title="RANx (Global)", contact={"name": "Anemo AI", "email": "support@anemo.ai"}
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


@app.get("/")
async def read_root():
    return {"message": "Welcome to your RANx server!"}


# Main part


@app.get("/listen_for_auth_completion")
async def ran_auth_listen_state():
    # NOTE: IN_PROGRESS should be initiated via the CLI
    if AUTH_FLOW_STATE != "IN_PROGRESS":
        raise HTTPException(
            status_code=404, detail="Authentication Flow must be in progress"
        )

    while AUTH_FLOW_STATE == "IN_PROGRESS":
        pass

    success: bool = AUTH_FLOW_STATE == "SUCCESS"

    return {"success": success}


class AuthToken(BaseModel):
    value: str
    expires_in: int


class RANAuthResponse(BaseModel):
    success: bool
    message: str
    auth_token: Optional[AuthToken]


@app.post("/auth_callback")
async def ran_auth_callback(auth_response: RANAuthResponse):
    global AUTH_FLOW_STATE

    # TODO: handle response
    AUTH_FLOW_STATE = "SUCCESS" if auth_response.success else "ERROR"


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response["message"].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)
