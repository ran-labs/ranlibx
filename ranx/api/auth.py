from typing import List, Dict, Set, Union, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status

from ranx.state import AUTH_FLOW_STATE, AuthFlowState
from ranx.constants import RAN_TOKEN_FILE_NAME, PROJECT_ROOT

import json

# Prefix: /auth
router = APIRouter(tags=["Authentication"])


@router.get("/listen_for_completion")
async def ran_auth_listen_state():
    # NOTE: IN_PROGRESS must be initiated via the CLI
    if AUTH_FLOW_STATE != AuthFlowState.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication Flow must be in progress"
        )

    while AUTH_FLOW_STATE == AuthFlowState.IN_PROGRESS:
        pass  # Stalling

    success: bool = AUTH_FLOW_STATE == AuthFlowState.SUCCESS

    return {"success": success}


class AuthToken(BaseModel):
    value: str
    #expires_in_secs: int


class RANAuthResponse(BaseModel):
    success: bool
    message: str = ""
    auth_token: Optional[AuthToken]


@router.post("/callback")
async def ran_auth_callback(auth_response: RANAuthResponse):
    global AUTH_FLOW_STATE

    # Handle Response
    if auth_response.success:
        try:
            # Store it somewhere
            store_token(auth_response.auth_token)
            print("Authentication Successful!")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Error: " + auth_response.message)

    # Effect: will complete any listeners
    AUTH_FLOW_STATE = AuthFlowState.SUCCESS if auth_response.success else AuthFlowState.FAILURE


def store_token(token: AuthToken):
    with open(f"{PROJECT_ROOT}/{RAN_TOKEN_FILE_NAME}.json", 'w') as dot_ranprofile:
        json.dump(token.dict(), dot_ranprofile)
