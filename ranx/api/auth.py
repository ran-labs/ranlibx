import json
import time
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ranx.constants import RAN_AUTH_TOKEN_FILEPATH_JSON
from ranx.state import AUTH_FLOW_STATE, AuthFlowState, set_auth_flow_state

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


class AuthToken(BaseModel):
    value: str
    # expires_in_secs: int


class RANAuthResponse(BaseModel):
    success: bool
    message: str = ""
    auth_token: Optional[AuthToken]


@router.post("/callback")
async def ran_auth_callback(auth_response: RANAuthResponse):
    # Handle Response
    if auth_response.success:
        try:
            # Store it somewhere
            store_token(auth_response.auth_token)
            print("Authentication Successful!")
        except Exception as e:
            print(f"Error: {e}")

        # Effect: will complete any listeners
        set_auth_flow_state(AuthFlowState.SUCCESS)
    else:
        print("Error: " + auth_response.message)

        # Effect: will complete any listeners
        set_auth_flow_state(AuthFlowState.FAILURE)


def store_token(token: AuthToken):
    with open(RAN_AUTH_TOKEN_FILEPATH_JSON, 'w') as dot_ranprofile:
        json.dump(token.dict(), dot_ranprofile)
