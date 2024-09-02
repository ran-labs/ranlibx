from enum import Enum


class AuthFlowState(Enum):
    INACTIVE = None
    IN_PROGRESS = 0
    SUCCESS = 1
    FAILURE = -1


AUTH_FLOW_STATE: AuthFlowState = AuthFlowState.INACTIVE
