import pandas as pd
from sqlalchemy.engine import Engine

def write_table(df: pd.DataFrame, table_name: str, schema_name: str, engine: Engine):
    """Write DataFrame into Postgres (replace existing)."""
    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema_name,
        if_exists="replace",
        index=False
    )


def read_table(table_name: str, schema_name: str, engine: Engine) -> pd.DataFrame:
    """Read full table into DataFrame."""
    return pd.read_sql(f"SELECT * FROM {schema_name}.{table_name}", engine)