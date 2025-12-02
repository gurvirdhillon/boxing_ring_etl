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

if __name__ == "__main__":
    df_fights = load_fight_dataset()
    logging.info("Load Complete - combined dataset inplace")
    print(df_fights.head())
    print(df_fights.columns)

