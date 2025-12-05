import os
import pandas as pd
from src.extract.extract import extract_data
from src.transform.clean_boxing_data import clean_boxing_dataset
from src.load.load import save_processed_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

RAW_FILE = os.path.join(RAW_DIR, "boxing_matches_messy_data.csv")
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "final_processed_data.csv")


def test_etl_end_to_end(tmp_path):
    """
    Run the whole ETL pipeline:
        - read raw
        - clean
        - save processed
    Validate expected outputs.
    """

    # 1. Extract
    df_raw = extract_data(RAW_FILE)
    assert not df_raw.empty, "Raw dataset failed to load."

    # 2. Transform
    df_clean = clean_boxing_dataset(df_raw)
    assert not df_clean.empty, "Transformation returned an empty dataset."

    # 3. Load
    output_path = tmp_path / "final_output.csv"
    save_processed_data(df_clean, output_path)

    assert output_path.exists(), "Processed file was not created."

    # 4. Validate file content
    df_out = pd.read_csv(output_path)
    expected_columns = [
        "age_A", "age_B", "height_A", "height_B",
        "reach_A", "reach_B", "stance_A", "stance_B",
        "won_A", "won_B", "lost_A", "lost_B",
        "result", "decision"
    ]

    for col in expected_columns:
        assert col in df_out.columns, f"Missing expected column: {col}"
