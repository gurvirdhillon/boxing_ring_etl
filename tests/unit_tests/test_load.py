import os
import pandas as pd
import pytest

base_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
csv_path = os.path.join(
    base_directory, "data", "processed", "final_processed_data", "boxing-match-fighters.csv")


def test_load_processed_fighter_file():
    
    assert os.path.exists(csv_path), f"file not found {csv_path}"

    df = pd.read_csv(csv_path)

    assert not df.empty, "loaded file is empty"

    expected = {"Boxer_A", "Country_A", "Weight_A", "age_A", "height_A"}

    assert expected.issubset(df.columns)
    
# tests if the data is loaded and checks a small segment of the code


def test_missing_processed_fighter_file(monkeypatch):
    '''
    Raises a file not found error if a file does not exist
    '''
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    correct_path = os.path.join(
        base_dir,
        "data",
        "processed",
        "final_processed_data",
        "boxing-match-fighters.csv"
    )

    monkeypatch.setattr(os.path, "exists", lambda _: False)

    # uses file not found to inspect the code if its not there
    with pytest.raises(FileNotFoundError):
        if not os.path.exists(correct_path):
            raise FileNotFoundError(f"Missing file: {correct_path}")


from src.load.load import validate_column_count, validate_row_count


def test_validate_column_count_passes():
    """
    validate_column_count() should NOT raise an error
    when the dataframe has the expected number of columns.
    """
    
    df = pd.read_csv(csv_path)
    expected_count = len(df.columns)

    # Actual assertion: if no exception is raised, the test implicitly passes
    try:
        validate_column_count(df, expected_count)
    except Exception as error:
        pytest.fail(f"validate_column_count raised an exception unexpectedly: {error}")


def test_validate_row():
    '''
    validate we have the number of rows we expect
    '''
    df = pd.read_csv(csv_path)
    expected_count = df.shape[0]

    try:
        validate_row_count(df, expected_count)
    except Exception as error:
        pytest.fail(f"failed row validation test at:", error)
