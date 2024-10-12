import httpx
import json
from ranlibx.api.schemas.token import AuthToken
from ranlibx.constants import RAN_AUTH_TOKEN_FILEPATH_JSON


def store_token(token: AuthToken):
    with open(RAN_AUTH_TOKEN_FILEPATH_JSON, 'w') as dot_ranprofile:
        json.dump(token.dict(), dot_ranprofile)


def is_token_valid(token: AuthToken) -> bool:
    # TODO: this
    pass


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
