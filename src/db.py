from functools import lru_cache
from sqlalchemy import create_engine, text
from src.settings import get_settings
import pandas as pd
from sqlalchemy.engine import Engine

@lru_cache
def get_engine():
    settings = get_settings()
    print ("Using Postgres at:", settings.pg_url.replace(settings.POSTGRES_PASSWORD, "*****"))
    return create_engine(settings.pg_url, echo=False, future=True)


def write_table(df: pd.DataFrame, table_name: str, schema_name: str, engine: Engine):
    """Write DataFrame into Postgres (replace existing)."""
    engine.connect()  # ensure engine is connected
    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema_name,
        if_exists="replace",
        index=False
    )
@lru_cache
def read_table(table_name: str, schema_name: str, engine: Engine) -> pd.DataFrame:
    """Read full table into DataFrame."""
    return pd.read_sql(f"SELECT * FROM {schema_name}.{table_name}", engine)


def execute_sql(sql: str, engine: Engine):
    """Execute arbitrary SQL."""
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

