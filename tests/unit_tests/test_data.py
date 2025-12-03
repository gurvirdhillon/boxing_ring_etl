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
