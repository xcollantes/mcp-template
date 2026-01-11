"""Tests for tool_utils module."""

from typing import Any
from unittest.mock import MagicMock

from src.tools.tool_utils import format_alert, get_alerts, get_weather


def test_format_alert_with_all_fields() -> None:
    """Test formatting alert with all fields present."""
    feature: dict[str, Any] = {
        "properties": {
            "event": "Winter Storm Warning",
            "areaDesc": "Seattle Metro Area",
            "severity": "Severe",
            "description": "Heavy snow expected.",
            "instruction": "Stay indoors if possible.",
        }
    }

    result = format_alert(feature)

    assert "Winter Storm Warning" in result
    assert "Seattle Metro Area" in result
    assert "Severe" in result
    assert "Heavy snow expected." in result
    assert "Stay indoors if possible." in result


def test_get_weather_success(
    mock_httpx_get: MagicMock,
    sample_weather_response: dict[str, Any],
) -> None:
    """Test getting weather data successfully."""
    mock_response = MagicMock()
    mock_response.json.return_value = sample_weather_response
    mock_response.raise_for_status.return_value = None
    mock_httpx_get.return_value = mock_response

    result = get_weather(
        "47.7623,-122.2054",
        "test-api-key",
        "https://api.weather.gov",
    )

    assert result == sample_weather_response
    mock_httpx_get.assert_called_once()

    # Verify the URL contains the location.
    call_url = mock_httpx_get.call_args[0][0]
    assert "47.7623,-122.2054" in call_url


def test_get_alerts_success(
    mock_httpx_get: MagicMock,
    sample_alerts_response: dict[str, Any],
) -> None:
    """Test getting alerts successfully."""
    mock_response = MagicMock()
    mock_response.json.return_value = sample_alerts_response
    mock_response.raise_for_status.return_value = None
    mock_httpx_get.return_value = mock_response

    result = get_alerts("WA", "test-api-key", "https://api.weather.gov")

    assert result == sample_alerts_response
    assert len(result["features"]) == 2

    # Verify the URL contains the state.
    call_url = mock_httpx_get.call_args[0][0]
    assert "WA" in call_url
