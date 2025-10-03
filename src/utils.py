import pandas as pd
from sqlalchemy import text
from src.db import get_engine

def parse_xml(file_path: str):
    """Parse export.xml and return ElementTree root."""
    import xml.etree.ElementTree as ET
    tree = ET.parse(file_path)
    return tree.getroot()

def run_sql_file(sql_file: str, as_table: str | None = None, as_view: str | None = None) -> pd.DataFrame:
    """
    Execute a .sql file. Always returns a DataFrame.
    Optionally persists the result as a table or view.
    
    Args:
        sql_file: Path to the .sql file
        as_table: If provided, will create/replace this table with results
        as_view: If provided, will create/replace this view with results
    """
    engine = get_engine()
    with engine.connect() as conn:
        with open(sql_file, "r") as f:
            base_sql = f.read()
        
        # Always fetch into pandas df
        df = pd.read_sql(text(base_sql), conn)
        
        # Optionally persist
        if as_table:
            # Drop first
            conn.execute(text(f"DROP TABLE IF EXISTS {as_table}"))
            # Then create
            conn.execute(text(f"CREATE TABLE {as_table} AS {base_sql}"))
            conn.commit()
            print(f"Wrote combined_features ({df.shape[0]} records)")
            
        elif as_view:
            # Wrap base_sql inside CREATE OR REPLACE VIEW
            view_sql = f"CREATE OR REPLACE VIEW {as_view} AS {base_sql}"
            conn.execute(text(view_sql))
            conn.commit()
    
    return df

# def load_features_from_table(tableName) -> pd.DataFrame:
#     engine = get_engine()
#     with engine.connect() as conn:
#         return pd.read_sql(f"SELECT * FROM {tableName}", conn)