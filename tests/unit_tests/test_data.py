import pandas as pd
from src.transform.clean_boxing_data import boxer_dataset_transformation


def test_transformed_data_types(real_raw_fight_df):
    df = boxer_dataset_transformation(real_raw_fight_df)

    expected_types = {
        "won_A": "int64",
        "won_B": "int64",
        "lost_A": "int64",
        "lost_B": "int64",
        "drawn_A": "int64",
        "drawn_B": "int64",
        "kos_A": "int64",
        "kos_B": "int64",

        "weight_A": "float",
        "weight_B": "float",
        "height_A": "float",
        "height_B": "float",
        "reach_A": "float",
        "reach_B": "float",

        "stance_A": "object",
        "stance_B": "object",
        "class_A": "object",
        "class_B": "object",

        "Fight_Date": "datetime64[ns]",
    }

    for col, dtype in expected_types.items():
        assert col in df.columns, f"Missing column: {col}"
        assert pd.api.types.is_dtype_equal(df[col].dtype, dtype), \
            f"Column {col} has wrong dtype: {df[col].dtype}, expected {dtype}"


def test_value_ranges(real_raw_fight_df):
    df = boxer_dataset_transformation(real_raw_fight_df)

    assert (df["height_A"].between(150, 210)).all()
    assert (df["height_B"].between(150, 210)).all()

    assert (df["reach_A"].between(150, 220)).all()
    assert (df["reach_B"].between(150, 220)).all()

    assert (df["weight_A"].between(40, 130)).all()
    assert (df["weight_B"].between(40, 130)).all()

    assert (df["won_A"] >= 0).all()
    assert (df["won_B"] >= 0).all()
    assert (df["lost_A"] >= 0).all()
    assert (df["lost_B"] >= 0).all()
    assert (df["drawn_A"] >= 0).all()
    assert (df["drawn_B"] >= 0).all()
    assert (df["kos_A"] >= 0).all()
    assert (df["kos_B"] >= 0).all()

    assert (df["class_diff"] <= 1).all()