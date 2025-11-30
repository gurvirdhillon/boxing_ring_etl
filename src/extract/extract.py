import pandas as pd
import os
from typing import Optional
from src.utils.logging_utils import setup_logger

logger = setup_logger("EXTRACT")

def get_file_path(file_name: str) -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, "data", "raw", file_name)


def file_exists(file_path: str) -> bool:
    """Only check existence — no prints here."""
    return os.path.exists(file_path)


def extract_data(file_name = "boxing_matches_messy_data.csv") -> Optional[pd.DataFrame]:
    """Extract CSV into DataFrame safely using full path."""
    file_path = get_file_path(file_name)

    if not file_exists(file_path):
        print(f"File not found at: {file_path}")
        return None

    try:
        df = pd.read_csv(file_path)
        print(f"Data successfully loaded from: {file_path}")
        return df

    except Exception as e:
        print(f"⚠ Error during loading: {e}")
        return e


if __name__ == "__main__":
    df = extract_data()
    if df is not None:
        print("Preview of data in the extraction process:")
        print(df.head())
        print(df.shape)


"""
being in the extract folder and running 
"python extract.py"
will output things such as the first 5 elements
the shape of the data we are dealing with including 418092 rows and 26 columns
as well as the number of nulls
"""
