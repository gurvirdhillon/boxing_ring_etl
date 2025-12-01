import pytest
from unittest.mock import patch
from config.env_config import setup_env


@patch("os.path.exists")
@patch("config.env_config.load_dotenv")
def test_setup_env_loads_file(mock_load, mock_exists):
    mock_exists.return_value = True

    setup_env("dev")

    mock_exists.assert_called_with(".env.dev")
    mock_load.assert_called_with(".env.dev")


@patch("os.path.exists")
def test_setup_env_file_not_found(mock_exists, capsys): 
    mock_exists.return_value = False

    setup_env("prod")

    captured = capsys.readouterr().out #prints the output of what is captured.
    assert "Environment .env.prod not found." in captured
