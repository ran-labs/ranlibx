import time

import typer

from ranlibx import authentication, state
from ranlibx.api.schemas.token import AuthToken
from ranlibx.state import AuthFlowState


def wait_for_browser_auth(verbose: bool = False) -> bool:
    # Stall while in progress
    i: int = 0
    while state.get_auth_flow_state() == AuthFlowState.IN_PROGRESS:
        # pass
        time.sleep(0.75)
        if verbose:
            typer.echo(f"Stalling x{(i := i + 1)}")

    # On exit
    success: bool = state.get_auth_flow_state() == AuthFlowState.SUCCESS

    return success


# -1 max_tries = infinity
def await_manual_api_token_auth(max_tries: int = -1) -> bool:
    i: int = 0

    # Loop until they get it right
    while True:
        api_token: str = str(typer.prompt("Paste your API Token here:"))

        # 2. Authenticate the API Token
        success: bool = authentication.authenticate(AuthToken(token=api_token))

        if success:
            return True

        if (i := i + 1) == max_tries:
            return False
