import json
import time
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ranlibx import authentication, state
from ranlibx.api.schemas.token import AuthToken
from ranlibx.constants import RAN_AUTH_TOKEN_FILEPATH_JSON
from ranlibx.state import AuthFlowState

# Prefix: /auth
router = APIRouter(tags=["Authentication"])


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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or Expired API Token"
            )

        # Otherwise, it's successful

        # Effect: will complete any listeners
        state.set_auth_flow_state(AuthFlowState.SUCCESS)
    else:
        print("Error: " + auth_response.message)

        # Effect: will complete any listeners
        state.set_auth_flow_state(AuthFlowState.FAILURE)
