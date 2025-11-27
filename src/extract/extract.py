import pandas as pd
import os

folder_name = "../../data/raw/"
file_name = "boxing_matches_messy_data.csv"


def check_file_exists(file_path=f"{folder_name}{file_name}") -> bool:
    if os.path.exists(file_path):
        print("File path found!")
        return True
    else:
        print("File does not exist")
        return False


def extract_filepath(file_path):
    if not check_file_exists(file_path):
        return "file doesnt exist"
    else:
        return filepath


def extract_data(file_path=f"{folder_name}{file_name}") -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        print("Data successfully loaded")
        return df
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print("Error occurred", e)


if __name__ == "__main__":
    req = check_file_exists()
    file
    if req == True:
        df = extract_data()
        print(df.head())
        print("-" * 50)
        print("shape:", df.shape)
        print("-" * 50)
        print(df.isnull().sum())
        print("-" * 50)
        print("duplicated data:", df.duplicated().sum())
        print("Data extracted")

"""
being in the extract folder and running 
"python extract.py"
will output things such as the first 5 elements
the shape of the data we are dealing with including 418092 rows and 26 columns
as well as the number of nulls
"""
