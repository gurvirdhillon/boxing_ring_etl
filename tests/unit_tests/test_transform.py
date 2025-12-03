import pandas as pd
from src.transform.clean_boxing_data import clean_age_col, fighter_dataset_transformation


def test_valid_age():
    df = pd.DataFrame({
        # test invalid ages with fake data
        "age_A": [-29, 34],
        "age_B": [32, -45]
    })
    
    df = df.abs()
    
    clean_data = clean_age_col(df)
    
    assert(clean_data["age_A"] >= 18).all()
    assert(clean_data["age_B"] >= 18).all()


fake_data = pd.DataFrame({
        "Rating_A": [1],
        "Boxer_A": ["Test A"],
        "Country_A": ["US"],
        "Weight_A": [150],
        "age_A": [25],
        "height_A": [70],
        "reach_A": [72],
        "stance_A": ["Orthodox"],
        "won_A": [10],
        "lost_A": [2],
        "drawn_A": [1],
        "kos_A": [5],
        "judge1_A": [98],
        "judge2_A": [99],
        "judge3_A": [97],
        "class_A": ["A"],
        "rank_A": [1],

        "Rating_B": [1],
        "Boxer_B": ["Test B"],
        "Country_B": ["GB"],
        "Weight_B": [160],
        "age_B": [27],
        "height_B": [71],
        "reach_B": [73],
        "stance_B": ["Southpaw"],
        "won_B": [12],
        "lost_B": [3],
        "drawn_B": [0],
        "kos_B": [7],
        "judge1_B": [98],
        "judge2_B": [99],
        "judge3_B": [97],
        "class_B": ["A"],
        "rank_B": [2],

        "Sex": ["M"],
        "Weight_Class": ["Middleweight"],
        "decision": ["KO"],
        "class_diff": [0],
        "result": ["A"],
        "Fight_Date": ["2024-01-01"],
    })


def test_columns_present():
    df = fighter_dataset_transformation(fake_data)
    expected_columns = {
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
    
    actual_columns = set(df.columns)
    missing = expected_columns - actual_columns
    assert not missing, f"missing columns {missing}"
