import pytest
import pandas as pd
import os

@pytest.fixture
def real_raw_fight_df():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, "data", "processed", "final_processed_data", "boxing-match-fighters.csv")

    if not os.path.exists(csv_path):
        pytest.skip(f"Real dataset not found at: {csv_path}")

    df = pd.read_csv(csv_path)
    return df.copy()
