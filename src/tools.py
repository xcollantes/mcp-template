"""MCP tools."""

import os
import textwrap

import httpx
from mcp.server.fastmcp import FastMCP

from mcp_server import get_mcp_server
from utils import format_alert, make_request


WEATHER_API_BASE = "https://api.weather.gov"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
USER_AGENT = "weather-app/1.0"

mcp: FastMCP = get_mcp_server()


@mcp.tool(
    name="get_weather",
    title="Get weather forecast data for a location.",
    description="Retrieves weather forecast information from the National Weather Service API for the specified location. The location should be in the format of latitude,longitude (e.g., '47.7623,-122.2054').",
    parameters=["location"],
)
def get_weather(location: str) -> dict:
    """Get weather forecast data for a location.

    Retrieves weather forecast information from the National Weather Service API
    for the specified location. The location should be in the format of
    latitude,longitude (e.g., "47.7623,-122.2054").

    Args:
        location: Location coordinates in "latitude,longitude" format or location identifier.

    Returns:
        A dictionary containing the raw weather forecast data from the API.

    Raises:
        httpx.HTTPStatusError: If the API request fails or returns an error status.
    """
    response = httpx.get(
        f"{WEATHER_API_BASE}/points/{location}/forecast",
        params={"apikey": WEATHER_API_KEY},
    )
    response.raise_for_status()
    return response.json()


@mcp.tool(
    name="get_alerts",
    title="Get active weather alerts for a U.S. state.",
    description="Retrieves all currently active weather alerts, warnings, and advisories issued by the National Weather Service for the specified state. This includes severe weather warnings, flood advisories, winter weather alerts, and more.",
    parameters=["state"],
)
async def get_alerts(state: str) -> str:
    """Get active weather alerts for a U.S. state.

    Retrieves all currently active weather alerts, warnings, and advisories
    issued by the National Weather Service for the specified state. This includes
    severe weather warnings, flood advisories, winter weather alerts, and more.

    Args:
        state: Two-letter U.S. state code (e.g., "WA" for Washington, "CA" for California).

    Returns:
        A formatted string containing all active weather alerts for the state,
        with each alert separated by "---". Each alert includes event type, area,
        severity, description, and instructions. Returns a message if no alerts
        are found or if the request fails.
    """
    url: str = f"{WEATHER_API_BASE}/alerts/active/area/{state}"

    data = await make_request(url, USER_AGENT)
    if not data or data.get("features") is None:
        return "Cannot get alerts or no alerts found."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool(
    name="get_forecast",
    title="Get detailed weather forecast for a specific location.",
    description="Retrieves a multi-period weather forecast from the National Weather Service for the specified coordinates. The forecast includes temperature, wind conditions, and detailed descriptions for the next 5 forecast periods (typically covering the next 2-3 days).",
    parameters=["latitude", "longitude"],
)
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get detailed weather forecast for a specific location.

    Retrieves a multi-period weather forecast from the National Weather Service
    for the specified coordinates. The forecast includes temperature, wind conditions,
    and detailed descriptions for the next 5 forecast periods (typically covering
    the next 2-3 days).

    Args:
        latitude: Latitude coordinate of the location (e.g., 47.7623 for Bothell, WA).
        longitude: Longitude coordinate of the location (e.g., -122.2054 for Bothell, WA).

    Returns:
        A formatted string containing the weather forecast for the next 5 periods,
        with each period showing the period name, temperature, wind speed and direction,
        and a detailed forecast description. Returns an error message if the forecast
        cannot be retrieved for the specified location.
    """

    # First get the forecast grid endpoint
    points_url = f"{WEATHER_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_request(points_url, USER_AGENT)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_request(forecast_url, USER_AGENT)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods.
        forecast = textwrap.dedent(
            f"""
        {period["name"]}:
        Temperature: {period["temperature"]}°{period["temperatureUnit"]}
        Wind: {period["windSpeed"]} {period["windDirection"]}
        Forecast: {period["detailedForecast"]}
        """
        )
        forecasts.append(forecast)

    return "\n".join(forecasts)
