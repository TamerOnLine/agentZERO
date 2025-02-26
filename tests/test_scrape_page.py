TEXT_LIMIT = 1000

URL = "https://www.sciencedirect.com/"

import pytest
import requests
from bs4 import BeautifulSoup
from unittest.mock import patch, Mock

def scrape_page(url, text_limit=TEXT_LIMIT):
    """Extract text from a web page."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().strip()
        return text[:text_limit] if len(text) > text_limit else text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>Test Content</p></body></html>"
        mock_get.return_value = mock_response
        yield mock_get

def test_scrape_page_success(mock_requests_get):
    result = scrape_page(URL)
    result = scrape_page(URL)
    assert "Test Content" in result

def test_scrape_page_error():
    with patch("requests.get", side_effect=requests.exceptions.RequestException("Network error")):
        invalid_url = "http://invalid-url.com"
        result = scrape_page(invalid_url)
        result = scrape_page(URL)
        assert "Error: Network error" in result

if __name__ == "__main__":
    pytest.main()
