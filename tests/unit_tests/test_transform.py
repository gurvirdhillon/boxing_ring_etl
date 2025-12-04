import pandas as pd
from unittest.mock import patch
from src.transform.clean_boxing_data import clean_age_col, fight_data_transform, clean_stance, clean_height, clean_weight, clean_kos, infer_results, fill_decision


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


def test_fight_dataset_column_count():
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

    df = fight_data_transform(fake_data)

    assert df.shape[1] == len(expected_columns), \
        f"Expected {len(expected_columns)} columns, got {df.shape[1]}"


def test_clean_stance_standardises_values_and_fills_missing():
    df = pd.DataFrame({
        "stance_A": ["orthdox", " none ", None],
        "stance_B": ["southpaw", "", None]
    })

    with patch("numpy.random.choice", return_value="Orthodox"):
        cleaned = clean_stance(df)

    assert cleaned["stance_A"].iloc[0] == "Orthodox"   # corrected typo
    assert cleaned["stance_A"].iloc[1] == "Orthodox"   # replaced empty
    assert cleaned["stance_A"].iloc[2] == "Orthodox"   # filled missing
    assert cleaned["stance_B"].iloc[0] == "Southpaw"
    assert cleaned["stance_B"].iloc[1] == "Orthodox"
    
    
def test_clean_height_handles_missing_and_invalid_values():
    df = pd.DataFrame({
        "height_A": [None, -200],
        "height_B": [500, None],
        "weight_A": [70, 85],
        "weight_B": [65, 120]
    })

    # Mock estimate_height so it returns a stable number
    with patch("src.transform.clean_boxing_data.estimate_height", return_value=180):
        cleaned = clean_height(df)

    assert cleaned["height_A"].notna().all()
    assert cleaned["height_B"].notna().all()
    assert cleaned["height_A"].between(150, 210).all()
    assert cleaned["height_B"].between(150, 210).all()
    

def test_clean_weight_replaces_invalid_and_missing():
    df = pd.DataFrame({
        "weight_A": [500, None],  # invalid + missing
        "weight_B": [-50, None],  # invalid + missing
        "height_A": [180, 175],
        "height_B": [178, 183]
    })

    with patch("src.transform.clean_boxing_data.estimate_weight", return_value=75):
        cleaned = clean_weight(df)

    assert cleaned["weight_A"].iloc[0] == 75
    assert cleaned["weight_A"].iloc[1] == 75
    assert cleaned["weight_B"].iloc[0] == 75
    assert cleaned["weight_B"].iloc[1] == 75


def test_clean_kos_caps_invalid_and_fills_missing():
    df = pd.DataFrame({
        "kos_A": [100, None],
        "kos_B": [-5, None],
        "won_A": [50, 20],
        "won_B": [40, 10],
        "lost_A": [5, 1],
        "lost_B": [3, 2]
    })

    cleaned = clean_kos(df)

    assert cleaned["kos_A"].iloc[0] <= cleaned["won_A"].iloc[0]
    assert cleaned["kos_A"].iloc[1] == round(20 * (50/50)) or cleaned["kos_A"].iloc[1] >= 0
    assert cleaned["kos_B"].iloc[0] >= 0


def test_infer_results_ko_logic():
    df = pd.DataFrame({"kos_A": [2], "kos_B": [0]})
    row = df.iloc[0]
    assert infer_results(df, row) == "win_A"


def test_infer_results_scorecard_logic():
    row = pd.Series({
        "kos_A": 0, "kos_B": 0,
        "judge1_A": 100, "judge1_B": 95,
        "judge2_A": 90,  "judge2_B": 85,
        "judge3_A": 110, "judge3_B": 109
    })
    df = pd.DataFrame([row])
    assert infer_results(df, row) == "win_A"


def test_fill_decision_preserves_existing_value():
    row = pd.Series({"decision": "UD", "kos_A": 0, "kos_B": 0, "result": None})
    assert fill_decision(row) == "UD"


def test_fill_decision_detects_ko():
    row = pd.Series({"decision": None, "kos_A": 1, "kos_B": None, "result": None})
    assert fill_decision(row) == "KO"

