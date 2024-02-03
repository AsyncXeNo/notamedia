import os

from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def get_var(name: str, default: str = None) -> str | None:
    var = os.getenv(name)

    if not var:
        logger.warning(f'environment variable {name} not found')
        return default
    
    return var
