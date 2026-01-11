"""Shared pytest fixtures for mcp-template tests."""

from typing import Any
from unittest.mock import patch

import pytest


@pytest.fixture
def sample_weather_response() -> dict[str, Any]:
    """Create a sample weather API response for testing."""
    return {
        "properties": {
            "periods": [
                {
                    "name": "Tonight",
                    "temperature": 45,
                    "temperatureUnit": "F",
                    "windSpeed": "5 mph",
                    "windDirection": "NW",
                    "detailedForecast": "Partly cloudy with a low around 45.",
                },
                {
                    "name": "Saturday",
                    "temperature": 62,
                    "temperatureUnit": "F",
                    "windSpeed": "10 mph",
                    "windDirection": "W",
                    "detailedForecast": "Sunny with a high near 62.",
                },
            ]
        }
    }


@pytest.fixture
def sample_alerts_response() -> dict[str, Any]:
    """Create a sample alerts API response for testing."""
    return {
        "features": [
            {
                "properties": {
                    "event": "Winter Storm Warning",
                    "areaDesc": "Seattle Metro Area",
                    "severity": "Severe",
                    "description": "Heavy snow expected.",
                    "instruction": "Stay indoors if possible.",
                }
            },
            {
                "properties": {
                    "event": "Wind Advisory",
                    "areaDesc": "Puget Sound",
                    "severity": "Moderate",
                    "description": "Strong winds expected.",
                    "instruction": "Secure loose objects.",
                }
            },
        ]
    }


@pytest.fixture
def sample_points_response() -> dict[str, Any]:
    """Create a sample points API response for testing."""
    return {
        "properties": {
            "forecast": "https://api.weather.gov/gridpoints/SEW/124,67/forecast"
        }
    }


@pytest.fixture
def mock_httpx_get():
    """Mock httpx.get for testing synchronous HTTP requests."""
    with patch("httpx.get") as mock:
        yield mock


@pytest.fixture
def mock_httpx_async_client():
    """Mock httpx.AsyncClient for testing async HTTP requests."""
    with patch("httpx.AsyncClient") as mock:
        yield mock


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for testing CLI commands."""
    with patch("subprocess.run") as mock:
        yield mock
