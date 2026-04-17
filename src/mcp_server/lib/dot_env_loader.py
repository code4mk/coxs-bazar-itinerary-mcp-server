from functools import lru_cache
from dotenv import load_dotenv


@lru_cache(maxsize=1)
def dot_env_loader() -> None:
    """Layered environment variable loader."""
    # Base config
    load_dotenv(".env")

    # Local overrides
    load_dotenv(".env.local", override=True)
