import pandas as pd
from unittest.mock import patch, MagicMock
from src.streamlit.pages.boxer_portfolio import get_wikipedia_image
from src.extract.request import get_wikipedia_image


def test_get_wikipedia_image_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "thumbnail": {"source": "http://test.me/image.jpg"}
    }

    with patch("requests.get", return_value=mock_response):
        url = get_wikipedia_image("Test Boxer")
        assert url == "http://test.me/image.jpg"


def test_get_wikipedia_image_no_thumbnail():
    """Test when Wikipedia returns valid data but no thumbnail exists."""

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}

    with patch("requests.get", return_value=mock_response):
        result = get_wikipedia_image("Unknown Fighter")

    assert result is None


def test_get_wikipedia_image_failure_status():
    """Test when Wikipedia returns a non-200 HTTP status."""

    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch("requests.get", return_value=mock_response):
        result = get_wikipedia_image("Bad Page Name")

    assert result is None
