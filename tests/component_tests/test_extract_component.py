import pandas as pd
import pytest

from src.transform.clean_boxing_data import (
    clean_boxing_dataset,
    clean_age_col,
    remove_duplicates
)

@pytest.fixture
def sample_raw_data():
    return pd.DataFrame({
        "age_A": [29, -31],
        "age_B": [-28, 30],
        "result": ["KO", "UD"],
        "Boxer_A": ["Mohammad Ali", "Mike Tyson"],
        "Boxer_B": ["Evander Holyfield", "George Foreman"]
    })


def test_full_cleaning_pipeline(sample_raw_data):
    """
    Component test verifying that the real transform pipeline behaves
    correctly when handling duplicated fighters but non-duplicated rows.
    """

    # Step 1: remove exact-duplicate rows (should not remove any here)
    cleaned = remove_duplicates(sample_raw_data)
    assert len(cleaned) == 2  # FIXED: correct expectation

    # Step 2: clean age columns (negative values become positive)
    cleaned = clean_age_col(cleaned)
    assert all(cleaned["age_A"] >= 0)
    assert all(cleaned["age_B"] >= 0)

    # Step 3: run entire cleaning pipeline
    final_output = clean_boxing_dataset(cleaned)

    assert isinstance(final_output, pd.DataFrame)
    assert "age_A" in final_output.columns
    assert "age_B" in final_output.columns
    assert len(final_output) == 2  # still two rows
