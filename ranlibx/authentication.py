import json

import httpx

from ranlibx.api.schemas.token import AuthToken
from ranlibx.constants import RAN_AUTH_TOKEN_FILEPATH_JSON, RAN_API_SERVER_URL


def store_token(token: AuthToken):
    with open(RAN_AUTH_TOKEN_FILEPATH_JSON, 'w') as dot_ranprofile:
        json.dump(token.dict(), dot_ranprofile)


def read_token() -> AuthToken:
    with open(RAN_AUTH_TOKEN_FILEPATH_JSON, 'r') as dot_ranprofile:
        data: dict = json.load(dot_ranprofile)
    
    auth_token: AuthToken = AuthToken(**data)
    
    # some small checking just in case
    MIN_TOKEN_LEN: int = 5
    if len(auth_token.token) < MIN_TOKEN_LEN:
        raise Exception("Not a token")
    
    return auth_token


def is_token_valid(token: AuthToken) -> bool:
    # Check if valid
    try:
        res = httpx.post(
            url=f"{RAN_API_SERVER_URL}/v1/auth/cli/are_credentials_valid",
            headers={"Authorization": f"Bearer {token.token}"}
        )

        if not res.is_success:
            return False

        res_data: dict = res.json()
        if not res_data.get("valid"):
            return False

        return True
    except:
        return False


def authenticate(token: AuthToken, verbose: bool = True) -> bool:
    """Validates and Stores an AuthToken. Returns whether it was successful or not"""

    try:
        # Validate the API token
        valid: bool = is_token_valid(token)
        if not valid:
            raise Exception("Invalid API Token.")

        # Store it somewhere
        store_token(token)

        print("Authentication Successful!")
        return True
    except Exception as e:
        if verbose:
            print(f"Error: {e}")

        return False
