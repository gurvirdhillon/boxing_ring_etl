import pandas as pd
from src.transform.clean_boxing_data import drop_unnamed, drop_columns, clean_weight


def test_drop_unnamed_columns():
    df = pd.DataFrame({"Unnamed: 0": [1], "real_col": [2]})
    cleaned = drop_unnamed(df)
    assert "Unnamed: 0" not in cleaned.columns


def test_drop_columns():
    df = pd.DataFrame({"Promoter": [1], "Trainer": [2], "Action": [3]})
    cleaned = drop_columns(df)
    assert "Promoter" not in cleaned.columns
    assert "Trainer" not in cleaned.columns
    assert "Action" not in cleaned.columns



