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


@mcp.tool()
def get_weather(location: str) -> dict:
    """Get weather by state."""

    response = httpx.get(
        f"{WEATHER_API_BASE}/points/{location}/forecast",
        params={"apikey": WEATHER_API_KEY},
    )
    response.raise_for_status()
    return response.json()


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a state."""

    url: str = f"{WEATHER_API_BASE}/alerts/active/area/{state}"

    data = await make_request(url, USER_AGENT)
    if not data or data.get("features") is None:
        return "Cannot get alerts or no alerts found."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
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
