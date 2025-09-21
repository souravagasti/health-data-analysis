from functools import lru_cache
from sqlalchemy import create_engine
from src.settings import get_settings

@lru_cache
def get_engine():
    settings = get_settings()
    return create_engine(settings.pg_url, echo=False, future=True)
