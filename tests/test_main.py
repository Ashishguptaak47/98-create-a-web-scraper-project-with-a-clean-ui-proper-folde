import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app
from scraper.models import ScrapeResponse

client = TestClient(app)

def test_ui_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "Web Scraper Studio" in response.text

def test_api_scrape_mocked():
    mock_result = ScrapeResponse(
        url="https://example.com",
        status_code=200,
        elapsed_seconds=0.12,
        total_items=2,
        data={"Title": ["Example Domain"], "Links": ["https://iana.org"]},
        title="Example Domain"
    )

    with patch("main.scrape_target", new=AsyncMock(return_value=mock_result)):
        payload = {
            "url": "https://example.com",
            "preset": "custom",
            "rules": [
                {"name": "Title", "selector": "h1"},
                {"name": "Links", "selector": "a", "attribute": "href"}
            ]
        }
        response = client.post("/api/scrape", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Example Domain"
        assert data["total_items"] == 2
        assert "Title" in data["data"]
        assert data["data"]["Title"] == ["Example Domain"]
