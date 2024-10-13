from enum import Enum

from ranlibx import server


class AuthFlowState(Enum):
    INACTIVE = None
    IN_PROGRESS = 0
    SUCCESS = 1
    FAILURE = -1


_auth_flow_state: AuthFlowState = AuthFlowState.INACTIVE

# Getters and Setters

def get_auth_flow_state() -> AuthFlowState:
    return _auth_flow_state

# Yes, this IS necessary to set the actual variable above from the outside
def set_auth_flow_state(st: AuthFlowState):
    global _auth_flow_state

    _auth_flow_state = st


def kill_server(verbose: bool = False):
    """Closes the RAN Authentication Server"""
    global _auth_flow_state

    _auth_flow_state = AuthFlowState.INACTIVE

    # KILL that uvicorn server in COLD BLOOD
    server.active_uvicorn_server_process.end(verbose=verbose)

    # Dereference it
    server.active_uvicorn_server_process = None

    if verbose:
        print("Server murder complete.")
