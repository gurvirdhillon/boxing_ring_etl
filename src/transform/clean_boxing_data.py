import pandas as pd
import random as rd
import numpy as np
import os
from datetime import datetime, timedelta
import logging as logger


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

raw_directory = os.path.join(BASE_DIR, "data", "raw/")
processed_data_directory = os.path.join(BASE_DIR, "data", "processed/")

raw_file_name = "boxing_matches_messy_data.csv"
processed_file_name = "boxing_match.csv"

second_clean_file = "fighters.csv"


def clean_boxing_dataset(boxer: pd.DataFrame) -> pd.DataFrame:
    boxer_cleaned = boxer.copy()
    # removing all the duplicates
    boxer_cleaned = remove_duplicates(boxer)
    return boxer_cleaned


def remove_duplicates(boxer: pd.DataFrame) -> pd.DataFrame:
    return boxer.drop_duplicates()


def clean_age_col(df):
    df['age_A'] = df['age_A'].abs()
    df['age_B'] = df['age_B'].abs()

    df['age_A'] = df['age_A'].apply(lambda x: rd.randint(18, 43) if pd.isna(x) else x)
    df['age_B'] = df['age_B'].apply(lambda x: rd.randint(18, 43) if pd.isna(x) else x)
    
    return df


def estimate_height(weight):
    if weight < 62: return np.random.normal(168, 5)   # Featherweight
    elif weight < 70: return np.random.normal(173, 6) # Lightweight
    elif weight < 80: return np.random.normal(178, 6) # Middleweight
    elif weight < 90: return np.random.normal(183, 7) # Light Heavy
    else:
        return np.random.normal(188, 7)             # Heavyweight


def reach_estimation(height):
    if height < 165:
        return np.random.normal(height + 3, 3)
    elif height < 175:
        return np.random.normal(height + 7, 3)
    elif height < 185:
        return np.random.normal(height + 9, 4)
    else:
        return np.random.normal(height + 11, 4)


def clean_reach(df):
    df['reach_A'] = df.apply(lambda row: reach_estimation(row['height_A']) if pd.isna(row['reach_A']) else row['reach_A'], axis=1)
    df['reach_B'] = df.apply(lambda row: reach_estimation(row['height_B']) if pd.isna(row['reach_B']) else row['reach_B'], axis=1)
    df['reach_A'] = df['reach_A'].apply(lambda x: np.nan if x < 150 or x > 220 else x)
    df['reach_B'] = df['reach_B'].apply(lambda x: np.nan if x < 150 or x > 220 else x)
    df['reach_A'] = df['reach_A'].fillna(
    df['height_A'].apply(lambda r: reach_estimation(r)))

    df['reach_B'] = df['reach_B'].fillna(df['height_B'].apply(lambda r: reach_estimation(r)))
    return df


def clean_stance_columns(column):
    return (
        column
        .str.strip()
        .str.lower() 
        .replace(['nan', 'none', '', 'null'], np.nan)
        .replace({
            'orthodox': 'Orthodox',
            'southpaw': 'Southpaw',
            'orthdox': 'Orthodox',     # Handling any possible misspellings
            ' southpaw ': 'Southpaw',
            ' orthodox ': 'Orthodox',
        })
    )


def clean_stance(df):
    df['stance_A'] = clean_stance_columns(df['stance_A'])
    df['stance_B'] = clean_stance_columns(df['stance_B'])
    
    stances = ['Orthodox', 'Southpaw', 'Switch-up', 'Peek-a-boo']
    
    df['stance_A'] = df['stance_A'].fillna(np.random.choice(stances, p=[0.55, 0.25, 0.15, 0.05]))
    df['stance_B'] = df['stance_B'].fillna(np.random.choice(stances, p=[0.55, 0.25, 0.15, 0.05]))
    
    return df


def clean_height(df):
    df['height_A'] = df['height_A'].abs()
    df['height_B'] = df['height_B'].abs()

    df['height_A'] = df.apply(lambda row: estimate_height(row['weight_A']) if pd.isna(row['height_A']) else row['height_A'], axis=1)
    df['height_B'] = df.apply(lambda row: estimate_height(row['weight_B']) if pd.isna(row['height_B']) else row['height_B'], axis=1)

    df['height_A'] = df['height_A'].abs()
    df['height_B'] = df['height_B'].abs()

    df['height_A'] = df['height_A'].apply(lambda x: np.nan if x < 150 or x > 210 else x)
    df['height_B'] = df['height_B'].apply(lambda x: np.nan if x < 150 or x > 210 else x)

    df['height_A'] = df.apply(lambda row: estimate_height(row['weight_A']) if pd.isna(row['height_A']) else row['height_A'], axis=1)
    df['height_B'] = df.apply(lambda row: estimate_height(row['weight_B']) if pd.isna(row['height_B']) else row['height_B'], axis=1)

    df['height_A'] = df['height_A'].fillna(df['height_A'].mean())
    df['height_B'] = df['height_B'].fillna(df['height_B'].mean())
    
    return df


def estimate_weight(height):
    if height < 165: return np.random.normal(60, 5)
    elif height < 170: return np.random.normal(65, 6)
    elif height < 175: return np.random.normal(72, 7)
    elif height < 180: return np.random.normal(78, 8)
    elif height < 185: return np.random.normal(85, 9)
    else:
        return np.random.normal(95, 10)


def clean_weight(df):
    df['weight_A'] = df['weight_A'].apply(lambda x: np.nan if x < 40 or x > 130 else x)
    df['weight_B'] = df['weight_B'].apply(lambda x: np.nan if x < 40 or x > 130 else x)

    df['weight_A'] = df.apply(lambda row: estimate_weight(row['height_A']) if pd.isna(row['weight_A']) else row['weight_A'], axis=1)
    df['weight_B'] = df.apply(lambda row: estimate_weight(row['height_B']) if pd.isna(row['weight_B']) else row['weight_B'], axis=1)
    
    return df


def clean_won(df):
    df['won_A'] = df['won_A'].abs()
    df['won_B'] = df['won_B'].abs()
    
    df['won_A'] = df['won_A'].round().astype('Int64')
    df['won_B'] = df['won_B'].round().astype('Int64')
    
    df.loc[df['won_A'] > 70, 'won_A'] = np.random.randint(1, 51, size=df[df['won_A'] > 70].shape[0])
    df.loc[df['won_B'] > 70, 'won_B'] = np.random.randint(1, 51, size=df[df['won_B'] > 70].shape[0])
    
    return df
    

def clean_lost(df):
    df['lost_A'] = df['lost_A'].abs()
    df['lost_B'] = df['lost_B'].abs()
    
    df['lost_A'] = df['lost_A'].round().astype('Int64')
    df['lost_B'] = df['lost_B'].round().astype('Int64')
    
    df.loc[df['lost_A'] > 130, 'lost_A'] = np.random.randint(1, 120, size=df[df['lost_A'] > 130].shape[0])
    df.loc[df['lost_B'] > 130, 'lost_B'] = np.random.randint(1, 120, size=df[df['lost_B'] > 130].shape[0])
    
    return df
    

def clean_draws(df):
    df['drawn_A'] = df['drawn_A'].apply(lambda x: np.nan if x < 0 or x > 20 else x)
    df['drawn_B'] = df['drawn_B'].apply(lambda x: np.nan if x < 0 or x > 20 else x)
    
    df['drawn_A'] = df['drawn_A'].fillna(df['drawn_A'].median())
    df['drawn_B'] = df['drawn_B'].fillna(df['drawn_B'].median())
    
    df['drawn_A'] = df['drawn_A'].astype('Int64')
    df['drawn_B'] = df['drawn_B'].astype('Int64')
    
    return df


def clean_kos(df):
    # sanitize lost columns
    df['lost_A'] = df['lost_A'].abs()
    df['lost_B'] = df['lost_B'].abs()
    
    # Remove invalid KO values
    df['kos_A'] = df['kos_A'].apply(lambda x: x if pd.notna(x) and 0 <= x <= 70 else np.nan)
    df['kos_B'] = df['kos_B'].apply(lambda x: x if pd.notna(x) and 0 <= x <= 70 else np.nan)

    # Cap KOs at wins — SAFE VERSION
    df['kos_A'] = df.apply(
        lambda row: min(row['kos_A'], row['won_A'])
        if pd.notna(row['kos_A']) and pd.notna(row['won_A'])
        else np.nan,
        axis=1
    )

    df['kos_B'] = df.apply(
        lambda row: min(row['kos_B'], row['won_B'])
        if pd.notna(row['kos_B']) and pd.notna(row['won_B'])
        else np.nan,
        axis=1
    )

    # Convert to floats for calculations
    df['kos_A'] = df['kos_A'].astype('float')
    df['kos_B'] = df['kos_B'].astype('float')
    df['won_A'] = df['won_A'].astype('float')
    df['won_B'] = df['won_B'].astype('float')

    # Compute average KO ratio
    avg_ko_ratio = (df['kos_A'] / df['won_A']).mean(skipna=True)
    
    if pd.isna(avg_ko_ratio) or avg_ko_ratio == 0:
        avg_ko_ratio = 0.5

    
    # Fill missing KO values using KO ratio
    df['kos_A'] = df.apply(
        lambda row: round(row['won_A'] * avg_ko_ratio)
        if pd.isna(row['kos_A']) and pd.notna(row['won_A']) and row['won_A'] > 0
        else row['kos_A'],
        axis=1
    )

    df['kos_B'] = df.apply(
        lambda row: round(row['won_B'] * avg_ko_ratio)
        if pd.isna(row['kos_B']) and pd.notna(row['won_B']) and row['won_B'] > 0
        else row['kos_B'],
        axis=1
    )

    # Final integer conversion
    df['kos_A'] = df['kos_A'].round().astype('Int64')
    df['kos_B'] = df['kos_B'].round().astype('Int64')

    return df


def clean_score_cards(df):
    judge_cols = [
        'judge1_A', 'judge1_B',
        'judge2_A', 'judge2_B',
        'judge3_A', 'judge3_B'
    ]

    # 1. Remove invalid scores (<0 or >120)
    for col in judge_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].apply(lambda x: np.nan if x < 0 or x > 120 else x)

    # 2. Row-wise fill: A judges use A-side mean, B judges use B-side mean
    A_side = ['judge1_A', 'judge2_A', 'judge3_A']
    B_side = ['judge1_B', 'judge2_B', 'judge3_B']

    df[A_side] = df[A_side].apply(lambda row: row.fillna(row.mean()), axis=1) # give the mean value of the rows data for judges score data
    df[B_side] = df[B_side].apply(lambda row: row.fillna(row.mean()), axis=1)

    # 3. If still NaN (all judges missing), fill with plausible values
    df[A_side] = df[A_side].fillna(114) # usually 114 given
    df[B_side] = df[B_side].fillna(114)

    return df


def infer_results(df, row):
    # Check KO win first (only if NOT NaN)
    if pd.notna(row['kos_A']) and row['kos_A'] > 0:
        return 'win_A'
    if pd.notna(row['kos_B']) and row['kos_B'] > 0:
        return 'win_B'
    
    # get scores
    a_score = 0
    b_score = 0

    for a, b in [
        ('judge1_A', 'judge1_B'),
        ('judge2_A', 'judge2_B'),
        ('judge3_A', 'judge3_B'),
    ]:
        if pd.notna(row[a]): a_score += row[a]
        if pd.notna(row[b]): b_score += row[b]

    if a_score > b_score:
        return 'win_A'
    if a_score < b_score:
        return 'win_B'

    return 'draw'

def fill_decision(row):
    # Keep existing decision if its not na
    if pd.notna(row.get('decision', None)):
        return row['decision']

    # KO overrides everything
    if pd.notna(row['kos_A']) and row['kos_A'] > 0:
        return 'KO'
    if pd.notna(row['kos_B']) and row['kos_B'] > 0:
        return 'KO'

    # Points decision
    if pd.notna(row['result']):
        if row['result'] in ['win_A', 'win_B']:
            return 'UD'
        if row['result'] == 'draw':
            return 'DRAW'

    return 'UNKNOWN'


def assign_weight_class_fight(weight):
    if weight <= 50.8: return "Flyweight"
    elif weight <= 53.5: return "Bantamweight"
    elif weight <= 57.2: return "Featherweight"
    elif weight <= 61.2: return "Lightweight"
    elif weight <= 63.5: return "Super Lightweight"
    elif weight <= 66.7: return "Welterweight"
    elif weight <= 69.9: return "Super Welterweight"
    elif weight <= 72.6: return "Middleweight"
    elif weight <= 76.2: return "Super Middleweight"
    elif weight <= 79.4: return "Light Heavyweight"
    elif weight <= 90.7: return "Cruiserweight"
    else: return "Heavyweight"


def weight_class(df):
    df['class_A'] = df['weight_A'].apply(assign_weight_class_fight)
    df['class_B'] = df['weight_B'].apply(assign_weight_class_fight)
    
    weight_classes = {
        "Minimumweight": 1, "Light Flyweight": 2, "Flyweight": 3, "Super Flyweight": 4,
        "Bantamweight": 5, "Super Bantamweight": 6, "Featherweight": 7, "Super Featherweight": 8,
        "Lightweight": 9, "Super Lightweight": 10, "Welterweight": 11,
        "Super Welterweight": 12, "Middleweight": 13, "Super Middleweight": 14,
        "Light Heavyweight": 15, "Cruiserweight": 16, "Heavyweight": 17
    }

# Giving ranks directly (vectorized)
    df['rank_A'] = df['class_A'].map(weight_classes)
    df['rank_B'] = df['class_B'].map(weight_classes)

    df['class_diff'] = abs(df['rank_A'] - df['rank_B'])

# Finding invalid fights (>1 class apart)
    invalid = df['class_diff'] > 1
    print(f"Invalid fights before fix: {invalid.sum()}")

    adjust_A = np.random.rand(len(df)) > 0.5  # True = adjust A, False = adjust B

    df.loc[invalid & adjust_A, 'class_A'] = df.loc[invalid & adjust_A, 'class_B']
    df.loc[invalid & adjust_A, 'weight_A'] = df.loc[invalid & adjust_A, 'weight_B']

    df.loc[invalid & ~adjust_A, 'class_B'] = df.loc[invalid & ~adjust_A, 'class_A']
    df.loc[invalid & ~adjust_A, 'weight_B'] = df.loc[invalid & ~adjust_A, 'weight_A']

    df['rank_A'] = df['class_A'].map(weight_classes)
    df['rank_B'] = df['class_B'].map(weight_classes)
    df['class_diff'] = abs(df['rank_A'] - df['rank_B'])
    
    return df

# the second df transformation


def drop_columns(df):
    # Define columns to drop
    columns_to_drop = ['Promoter', 'Ceiling', 'Action', 'Trainer']

    # Drop only columns that actually exist
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

    # If "Unnamed: 0" exists, set it as index
    if 'Unnamed: 0' in df.columns:
        df = df.set_index('Unnamed: 0')
        df.index.name = 'Boxer_ID'

    return df


def assign_weight_class_fighter(weight):
    if weight < 52:
        return 'Flyweight'
    elif weight < 57:
        return 'Featherweight'
    elif weight < 63:
        return 'Lightweight'
    elif weight < 69:
        return 'Welterweight'
    elif weight < 76:
        return 'Middleweight'
    elif weight < 91:
        return 'Cruiserweight'
    else:
        return 'Heavyweight'


def standardise_weight(df):
    # find column containing 'weight'
    weight_col = next((col for col in df.columns if 'weight' in col.lower()), None)
    
    if not weight_col:
        raise KeyError("No weight column found in dataframe")

    df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce') * 0.45359237 # this weight was taken from online which converted 1lb to kg
    df['Weight_Class'] = df[weight_col].apply(assign_weight_class_fighter)
    df = df.reset_index().rename(columns={'index': 'Boxer_ID'})
    return df


def merge_matchups(df, sample_size=5000):
    # Keep only necessary columns to reduce memory
    df_small = df[['Boxer', 'Sex', 'Weight_Class']].drop_duplicates()

    # Group by sex and weight class
    matchups = []
    for _, group in df_small.groupby(['Sex', 'Weight_Class']):
        boxers = group['Boxer'].tolist()
        if len(boxers) > 1:
            pairs = [(boxers[i], boxers[j]) for i in range(len(boxers)) for j in range(i+1, len(boxers))]
            matchups.extend(pairs)

    # Convert to DataFrame
    matchups_df = pd.DataFrame(matchups, columns=['Boxer_A', 'Boxer_B'])

    # Sample to control size
    if len(matchups_df) > sample_size:
        matchups_df = matchups_df.sample(sample_size, random_state=42)

    return matchups_df


def drop_unnamed(df):
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')
    return df


def fight_validation(df):
    return df[df['Boxer_A'] != df['Boxer_B']]

def merge_datasets(fight_df, fighter_df):
    # Merge A-side attributes
    merged = fight_df.merge(
        fighter_df.add_prefix("_A").rename(columns={"Boxer_A": "Boxer_A"}),
        on="Boxer_A", how="left"
    )

    # Merge B-side attributes
    merged = merged.merge(
        fighter_df.add_prefix("B_").rename(columns={"Boxer_B": "Boxer_B"}),
        on="Boxer_B", how="left"
    )

    return merged


def place_dates(start_date, end_date):
    delta = end_date - start_date
    random_days = np.random.randint(0, delta.days)
    return (start_date + timedelta(days=int(random_days))).date()


def assign_unique_fight_dates(df, fighter_col_A="Boxer_A", fighter_col_B="Boxer_B", start=datetime(2010, 1, 1), end=datetime(2025, 12, 31)):
    assigned_dates = {}
    generated_dates = []

    for _, row in df.iterrows():
        fighterA = row[fighter_col_A]
        fighterB = row[fighter_col_B]

        while True:
            date_candidate = place_dates(start, end)

            # Check if either fighter already has that date assigned
            clash = False
            for fighter in [fighterA, fighterB]:
                if fighter in assigned_dates and date_candidate in assigned_dates[fighter]:
                    clash = True
                    break

            if not clash:
                # Assign this date to both fighters
                for fighter in [fighterA, fighterB]:
                    assigned_dates.setdefault(fighter, set()).add(date_candidate)
                generated_dates.append(date_candidate)
                break

    df = df.copy()
    df["Fight_Date"] = generated_dates
    return df


def boxer_dataset_transformation(df):
    df = clean_boxing_dataset(df)
    df = remove_duplicates(df)
    
    df = clean_weight(df)
    df = clean_height(df)
    df = clean_reach(df)
    
    df = clean_age_col(df)

    df = clean_won(df)    
    df = clean_kos(df)
    df = clean_lost(df)
    df = clean_draws(df)
    df = clean_stance(df)
    df = clean_score_cards(df)

    df['result'] = df.apply(lambda row: infer_results(df, row), axis=1)
    df['decision'] = df.apply(lambda row: fill_decision(row), axis=1)

    return df


def get_boxer_name_column(df):
    for col in ['Boxer', 'Name', 'Fighter', 'Full Name', 'Boxer_Name']:
        if col in df.columns:
            return col
    raise KeyError(f"No valid boxer name column found. Available columns: {df.columns.tolist()}")


EXPECTED_FIGHTER_COLUMNS = {
    'Rating_A', 'Boxer_A', 'Country_A', 'Weight_A', 'age_A',
    'height_A', 'reach_A', 'stance_A', 'won_A', 'lost_A',
    'drawn_A', 'kos_A', 'judge1_A', 'judge2_A', 'judge3_A', 'class_A',
    'rank_A',

    'Rating_B', 'Boxer_B', 'Country_B', 'Weight_B', 'age_B',
    'height_B', 'reach_B', 'stance_B', 'won_B', 'lost_B',
    'drawn_B', 'kos_B', 'judge1_B', 'judge2_B', 'judge3_B', 'class_B',
    'rank_B',

    'Sex', 'Weight_Class', 'decision', 'class_diff',
    'result', 'Fight_Date'
}


def fight_data_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates and enforces the schema for fight records
    containing both Fighter A and Fighter B columns.
    """

    df_clean = df.copy()

    for col in EXPECTED_FIGHTER_COLUMNS:
        if col not in df_clean.columns:
            df_clean[col] = pd.NA

    return df_clean[list(EXPECTED_FIGHTER_COLUMNS)]


def fighter_dataset_transformation(df):
    df = drop_unnamed(df)
    df = drop_columns(df)  # removes Promoter, Ceiling, Action, Trainer

    # 1. Fix name column — ensure it is exactly "Boxer"
    name_col = get_boxer_name_column(df)  # returns "Boxer"
    df = df.rename(columns={name_col: "Boxer"})

    # 2. Clean boxer names so they match fight dataset
    df["Boxer"] = (
        df["Boxer"]
        .str.replace(",", "") # remove commas
        .str.strip()
        .str.title()  # make consistent casing
    )

    # 3. Convert Weight lbs → kg (your data uses lbs)
    df["Weight"] = pd.to_numeric(df["Weight"], errors="coerce") * 0.45359237

    # 4. Assign weight class
    df["Weight_Class"] = df["Weight"].apply(assign_weight_class_fighter)

    # 5. Build final cleaned fighter dataset
    fighter_clean = df[[
        "Boxer",
        "Sex",
        "Country",
        "Weight",
        "Weight_Class",
        "Rating"
    ]]

    return fighter_clean

if __name__ == "__main__":
    df_raw = pd.read_csv(os.path.join(raw_directory, raw_file_name))
    second_df = pd.read_csv(os.path.join(processed_data_directory, second_clean_file))

    # Transform fight dataset
    df_clean = boxer_dataset_transformation(df_raw.copy())
    df_clean.to_csv(os.path.join(processed_data_directory, processed_file_name), index=False)

    print("Transformation complete. Cleaned files saved!")



