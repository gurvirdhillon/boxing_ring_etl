import pandas as pd
import random as rd
import numpy as np
import os

# the file in its raw messy form yet to be transformed
# raw_directory = "../../data/raw/"
# raw_file_name = "boxing_matches_messy_data.csv"

# when the process of cleaning is complete this will be where it is uploaded
# processed_data_directory = "../../data/processed/"
# processed_file_name = "boxing_match.csv"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

raw_directory = os.path.join(BASE_DIR, "data", "raw/")
processed_data_directory = os.path.join(BASE_DIR, "data", "processed/")

raw_file_name = "boxing_matches_messy_data.csv"
processed_file_name = "boxing_match.csv"

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
    return df['reach_A'], df['reach_B']

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
    
    df['won_A'] = df['won_A'].round().astype(int)
    df['won_B'] = df['won_B'].round().astype(int)
    
    df.loc[df['won_A'] > 70, 'won_A'] = np.random.randint(1, 51, size=df[df['won_A'] > 70].shape[0])
    df.loc[df['won_B'] > 70, 'won_B'] = np.random.randint(1, 51, size=df[df['won_B'] > 70].shape[0])
    
    return df
    

def clean_lost(df):
    df['lost_A'] = df['lost_A'].abs()
    df['lost_B'] = df['lost_B'].abs()
    
    df['lost_A'] = df['lost_A'].round().astype(int)
    df['lost_B'] = df['lost_B'].round().astype(int)
    
    df.loc[df['lost_A'] > 130, 'lost_A'] = np.random.randint(1, 120, size=df[df['lost_A'] > 130].shape[0])
    df.loc[df['lost_B'] > 130, 'lost_B'] = np.random.randint(1, 120, size=df[df['lost_B'] > 130].shape[0])
    
    return df
    


def clean_draws(df):
    df['drawn_A'] = df['drawn_A'].apply(lambda x: np.nan if x < 0 or x > 20 else x)
    df['drawn_B'] = df['drawn_B'].apply(lambda x: np.nan if x < 0 or x > 20 else x)
    
    df['drawn_A'] = df['drawn_A'].fillna(df['drawn_A'].median())
    df['drawn_B'] = df['drawn_B'].fillna(df['drawn_B'].median())
    
    df['drawn_A'] = df['drawn_A'].astype(int)
    df['drawn_B'] = df['drawn_B'].astype(int)
    
    return df


def clean_kos(df):
    df['lost_A'] = df['lost_A'].abs()
    df['lost_B'] = df['lost_B'].abs()
    
    df['kos_A'] = df['kos_A'].apply(lambda x: x if pd.notna(x) and 0 <= x <= 70 else np.nan)
    df['kos_B'] = df['kos_B'].apply(lambda x: x if pd.notna(x) and 0 <= x <= 70 else np.nan)
    
    df['kos_A'] = df.apply(lambda row: min(row['kos_A'], row['won_A']) if pd.notna(row['kos_A']) else np.nan, axis=1)
    df['kos_B'] = df.apply(lambda row: min(row['kos_B'], row['won_B']) if pd.notna(row['kos_B']) else np.nan, axis=1)
    
    
    df['kos_A'] = df['kos_A'].astype('float')
    df['won_A'] = df['won_A'].astype('float')
    df['kos_B'] = df['kos_B'].astype('float')
    df['won_B'] = df['won_B'].astype('float')
    
    avg_ko_ratio = (df['kos_A'] / df['won_A']).mean()

    df['kos_A'] = df.apply(
    lambda row: round(row['won_A'] * avg_ko_ratio)
    if pd.isna(row['kos_A']) and pd.notna(row['won_A']) and row['won_A'] > 0
    else row['kos_A'],
    axis=1)

    df['kos_B'] = df.apply(lambda row: round(row['won_B'] * avg_ko_ratio)
    if pd.isna(row['kos_B']) and pd.notna(row['won_B']) and row['won_B'] > 0
        else row['kos_B'], axis=1)
    
    df['kos_A'] = df['kos_A'].round().astype('Int64')
    df['kos_B'] = df['kos_B'].round().astype('Int64')
    
    return df

def clean_score_cards(df):
    # clean judges data
    judge_columns = ['judge1_A', 'judge1_B', 'judge2_A', 'judge2_B', 'judge3_A', 'judge3_B']
    for col in judge_columns:
        df[col] = df[col].apply(lambda x: np.nan if x < 0 or x > 120 else x)

    df['judge1_A'] = df['judge1_A'].fillna(df[['judge1_A', 'judge2_A', 'judge3_A']].mean(axis=1))
    df['judge1_B'] = df['judge1_B'].fillna(df[['judge1_B', 'judge2_B', 'judge3_B']].mean(axis=1))
    
    judge_columns_A = ['judge1_A', 'judge2_A', 'judge3_A']
    judge_columns_B = ['judge1_B', 'judge2_B', 'judge3_B']

# Step 1: Remove invalid values (<0 or >120)
    for col in judge_columns_A + judge_columns_B:
        df[col] = df[col].apply(lambda x: np.nan if x < 0 or x > 120 else x)

# Step 2: Fill missing values row-wise using A-side averages
    df[judge_columns_A] = df[judge_columns_A].apply(
        lambda row: row.fillna(row.mean()), axis=1
    )

# Step 3: Fill missing values row-wise using B-side averages
    df[judge_columns_B] = df[judge_columns_B].apply(
        lambda row: row.fillna(row.mean()), axis=1
    )
    
    return df


def infer_results(df, row):
    if row['kos_A'] > 0: return 'win_A'
    if row['kos_B'] > 0: return 'win_B'

    a_score = (row['judge1_A'] + row['judge2_A'] + row['judge3_A']).fillna(0)
    b_score = (row['judge1_B'] + row['judge2_B'] + row['judge3_B']).fillna(0)

    if a_score.sum() > b_score.sum(): return 'win_A'
    if a_score.sum() < b_score.sum(): return 'win_B'

    df['decision'] = df['decision'].str.strip().str.upper().replace({
        'TECHNICAL KNOCKOUT': 'TKO',
        'KNOCKOUT': 'KO',
        'UNANIMOUS': 'UD',
        'SPLIT': 'SD',
        'MAJORITY': 'MD',
        'POINTS': 'UD',
        'DRAW ': 'DRAW',
        ' DQ': 'DQ'
    })
    
    return 'draw'


def fill_decision(df, row):
    # Keep existing decision
    if pd.notna(row['decision']):
        return row['decision']

    # Infer based on KO counts
    if pd.notna(row['kos_A']) and row['kos_A'] > 0:
        return 'KO'
    if pd.notna(row['kos_B']) and row['kos_B'] > 0:
        return 'KO'

    # If result exists, apply logic safely
    if pd.notna(row['result']):
        if row['result'] in ['win_A', 'win_B']:
            return 'UD'  # points win
        if row['result'] == 'draw':
            return 'DRAW'
    df['decision'] = df.apply(fill_decision, axis=1)
        
    return 'UNKNOWN'  # Fallback


def assign_weight_class(weight):
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
    df['class_A'] = df['weight_A'].apply(assign_weight_class)
    df['class_B'] = df['weight_B'].apply(assign_weight_class)
    
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

def boxer_dataset_transformation(df):
    clean_boxing_dataset(df)
    remove_duplicates(df)
    clean_age_col(df)
    clean_height(df)
    clean_draws(df)
    clean_kos(df)
    clean_lost(df)
    clean_reach(df)
    clean_stance(df)
    clean_weight(df)
    clean_won(df)
    clean_score_cards(df)
    infer_results(df)
    
    return df


if __name__ == "__main__":
    df_raw = pd.read_csv(os.path.join(raw_directory, raw_file_name))
    df_clean = boxer_dataset_transformation(df_raw.copy())
    df_clean.to_csv(os.path.join(processed_data_directory, processed_file_name), index=False)
    print("Transformation complete. Cleaned file saved!")
