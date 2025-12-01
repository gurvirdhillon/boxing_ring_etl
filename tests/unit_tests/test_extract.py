import pandas as pd
from unittest.mock import patch


@patch("src.extract.extract.get_file_path") # @patch to replace functions with mock versions
@patch("src.extract.extract.get_file_path")
@patch("pandas.read_csv")
def test_extract_raw_data(mock_read_csv, mock_get_path, mock_exists):
    mock_get_path.return_value = "fake/path.csv"
    mock_exists.return_value = True
    mock_read_csv.return_value = pd.DataFrame({"col1":[1], "col2":[2]})
    
    from src.extract.extract import extract_data
    df = extract_data("boxing_match_messy_data.csv")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["col1", "col2"]

# this tests if the extract process has occurred^


