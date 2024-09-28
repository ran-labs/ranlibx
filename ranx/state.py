from enum import Enum

from ranx import server


class AuthFlowState(Enum):
    INACTIVE = None
    IN_PROGRESS = 0
    SUCCESS = 1
    FAILURE = -1


AUTH_FLOW_STATE: AuthFlowState = AuthFlowState.INACTIVE


def set_auth_flow_state(st: AuthFlowState):
    global AUTH_FLOW_STATE

    AUTH_FLOW_STATE = st


def kill_server(verbose: bool = False):
    """Closes the RAN Authentication Server"""
    global AUTH_FLOW_STATE

    AUTH_FLOW_STATE = AuthFlowState.INACTIVE

    # KILL that uvicorn server in COLD BLOOD
    server.active_uvicorn_server_process.end(verbose=verbose)

    if verbose:
        print("Server murder complete.")
