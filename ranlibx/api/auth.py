import json
import time
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ranlibx.api.schemas.token import AuthToken

from ranlibx import authentication
from ranlibx.constants import RAN_AUTH_TOKEN_FILEPATH_JSON
from ranlibx.state import AUTH_FLOW_STATE, AuthFlowState, set_auth_flow_state

from ranlibx import authentication

# Prefix: /auth
router = APIRouter(tags=["Authentication"])


@router.get("/listen_for_completion")
async def ran_auth_listen_state():
    # NOTE: IN_PROGRESS must be initiated via the CLI
    if AUTH_FLOW_STATE != AuthFlowState.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Authentication Flow must be in progress"
        )

    while AUTH_FLOW_STATE == AuthFlowState.IN_PROGRESS:
        # Stall
        # pass
        time.sleep(0.5)

    success: bool = AUTH_FLOW_STATE == AuthFlowState.SUCCESS

    return {"success": success}


class RANAuthResponse(BaseModel):
    success: bool
    message: str = ""
    auth_token: Optional[AuthToken]


@router.post("/callback")
async def ran_auth_callback(auth_response: RANAuthResponse):
    # Handle Response
    if auth_response.success:
        # No verbosity since we already have error messages here
        success: bool = authentication.authenticate(auth_response.auth_token, verbose=False)

        if success is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or Expired API Token")

        # Otherwise, it's successful

        # Effect: will complete any listeners
        set_auth_flow_state(AuthFlowState.SUCCESS)
    else:
        print("Error: " + auth_response.message)

        # Effect: will complete any listeners
        set_auth_flow_state(AuthFlowState.FAILURE)
