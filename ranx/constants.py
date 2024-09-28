from pathlib import Path

RANX_PROJECT_ROOT: str = str(Path(__file__).parent.parent)
LIB_ROOT: str = str(Path(__file__).parent)

RAN_DOMAIN: str = "ran.so"

RAN_TOKEN_FILE_NAME: str = ".ranprofile"

RAN_AUTH_TOKEN_FILEPATH_JSON: str = f"~/.ran/{RAN_TOKEN_FILE_NAME}.json"
