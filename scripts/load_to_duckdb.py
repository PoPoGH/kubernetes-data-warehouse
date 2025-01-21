import duckdb
import os
from pathlib import Path

def load_data_to_duckdb():
    # Database configuration
    DB_NAME = "kubernetes_data.db"
    DATA_DIR = "data"
    
    # Create database if it doesn't exist
    if not os.path.exists(DB_NAME):
        print(f"Creating new DuckDB database: {DB_NAME}")
        conn = duckdb.connect(DB_NAME)
        conn.close()

    # Load each parquet file into DuckDB
    data_dir = Path(DATA_DIR)
    for parquet_file in data_dir.glob("*.parquet"):
        table_name = f"raw_{parquet_file.stem}"
        print(f"Loading {parquet_file} into table {table_name}")
        
        try:
            conn = duckdb.connect(DB_NAME)
            query = f"""
                CREATE OR REPLACE TABLE {table_name} 
                AS SELECT * FROM read_parquet('{parquet_file.as_posix()}')
            """
            conn.execute(query)
            
            # Verify table creation
            tables = conn.execute("SHOW TABLES").fetchall()
            if any(t[0] == table_name for t in tables):
                print(f"Successfully loaded {table_name}")
            else:
                print(f"Failed to load {table_name}")
                
        except Exception as e:
            print(f"Error loading {table_name}: {str(e)}")
        finally:
            conn.close()

    print("Data loading complete")

if __name__ == "__main__":
    load_data_to_duckdb()
