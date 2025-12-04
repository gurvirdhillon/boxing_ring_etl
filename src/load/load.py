import logging
import pandas as pd
import os


base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
processed_dir = os.path.join(base_dir, "data", "processed", "final_processed_data")

combined_dataset = "boxing-match-fighters.csv"


def load_fight_dataset():
    path = os.path.join(processed_dir, combined_dataset)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Cleaned fight dataset not found at: {path}")

    df = pd.read_csv(path)
    return df


def validate_column_count(df: pd.DataFrame, expected_count: int):
    """Validate DataFrame has expected number of columns."""
    if df.shape[1] != expected_count:
        raise ValueError(f"Expected {expected_count} columns, got {df.shape[1]}.")


def validate_row_count(df: pd.DataFrame, expected_count: int):
    """Validate DataFrame has expected number of rows."""
    if df.shape[0] != expected_count:
        raise ValueError(f"Expected {expected_count} rows, got {df.shape[0]}.")


def save_processed_data(df: pd.DataFrame, output_path):
    """
    Saves processed dataframe to a CSV file.
    """

    # Ensure proper string path
    output_path = str(output_path)

    df.to_csv(output_path, index=False)
    return output_path

if __name__ == "__main__":
    df_fights = load_fight_dataset()
    logging.info("Load Complete - combined dataset inplace")
    print(df_fights.head())
    print(df_fights.columns)

