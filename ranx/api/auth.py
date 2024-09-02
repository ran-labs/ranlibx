from typing import List, Dict, Set, Union, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status

from ranx.state import AUTH_FLOW_STATE, AuthFlowState


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
    message: str
    auth_token: Optional[AuthToken]


@router.post("/callback")
async def ran_auth_callback(auth_response: RANAuthResponse):
    global AUTH_FLOW_STATE

    # TODO: handle response

    # Effect: will complete any listeners
    AUTH_FLOW_STATE = AuthFlowState.SUCCESS if auth_response.success else AuthFlowState.FAILURE

