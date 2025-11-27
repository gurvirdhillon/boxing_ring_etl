import pandas as pd


# the file in its raw messy form yet to be transformed
raw_directory = "../../data/raw/"
raw_file_name = "boxing_matches_messy_data.csv"

# when the process of cleaning is complete this will be where it is uploaded
processed_data_directory = "../../data/processed/"
processed_file_name = "boxing_match.csv"


def clean_boxing_dataset(boxer: pd.DataFrame) -> pd.DataFrame:
    boxer_cleaned = boxer.copy()
    # removing all the duplicates
    boxer_cleaned = remove_duplicates(boxer)
    
    boxer_cleaned = handle_nulls(boxer)
    
    return boxer_cleaned


def remove_duplicates(boxer: pd.DataFrame) -> pd.DataFrame:
    # return boxer.drop_duplicates()
    return boxer.shape

def handle_nulls(boxer: pd.DataFrame) -> pd.DataFrame:
    pass

if __name__ == "__main__":
    df_raw = pd.read_csv(raw_directory + raw_file_name)
    df_clean = clean_boxing_dataset(df_raw.copy())
    # print(df_raw)
