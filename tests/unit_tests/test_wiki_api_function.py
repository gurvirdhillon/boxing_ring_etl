import pandas as pd
from unittest.mock import patch, MagicMock
from src.streamlit.pages.boxer_portfolio import get_wikipedia_image


def test_get_wikipedia_image_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "thumbnail": {"source": "http://test.me/image.jpg"}
    }

    with patch("requests.get", return_value=mock_response):
        url = get_wikipedia_image("Test Boxer")
        assert url == "http://test.me/image.jpg"
