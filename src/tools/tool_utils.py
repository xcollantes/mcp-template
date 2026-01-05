"""TODO: Example tool helper functions.

Example tool definition in main.py:

```python
@mcp.tool(
    name="todo_example_tool",
    title="A tool to complete a task.",
    description="A tool to complete a task.",
)
def todo_example_tool(task: Annotated[str, "A task to complete."]) -> str:

    # Perform some action.

    return "Task completed successfully."
```
"""

import logging
import textwrap
from typing import Any

import httpx


logger: logging.Logger = logging.getLogger(__name__)


def format_alert(feature: dict[str, Any]) -> str:
    props = feature["properties"]
    return textwrap.dedent(
        f"""
    Event: {props.get("event", "Unknown")}
    Area: {props.get("areaDesc", "Unknown")}
    Severity: {props.get("severity", "Unknown")}
    Description: {props.get("description", "No description available")}
    Instructions: {props.get("instruction", "No specific instructions provided")}
    """
    )


async def _make_request(url: str, user_agent: str) -> Any:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                headers={
                    "User-Agent": user_agent,
                    "Accept": "application/geo+json",
                },
                timeout=10,
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error("HTTP error occurred: %s", e)
            raise e


def get_weather(location: str, api_key: str, weather_api_base: str) -> dict[str, Any]:
    """Get weather forecast data for a location."""

    response: httpx.Response = httpx.get(
        f"{weather_api_base}/points/{location}/forecast",
        params={"apikey": api_key},
    )
    response.raise_for_status()
    return response.json()


def get_alerts(state: str, api_key: str, weather_api_base: str) -> dict[str, Any]:
    """Get active weather alerts for a U.S. state."""

    response: httpx.Response = httpx.get(
        f"{weather_api_base}/alerts/active/area/{state}",
        params={"apikey": api_key},
    )
    response.raise_for_status()
    return response.json()


async def get_forecast(
    latitude: float,
    longitude: float,
    api_key: str,
    user_agent: str,
    weather_api_base: str,
) -> str:
    """Get detailed weather forecast for a specific location."""

    # First get the forecast grid endpoint.
    points_url: str = f"{weather_api_base}/points/{latitude},{longitude}"
    points_data: dict[str, Any] = await _make_request(points_url, user_agent)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response.
    forecast_url: str = points_data["properties"]["forecast"]
    forecast_data: dict[str, Any] = await _make_request(forecast_url, user_agent)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast.
    periods: list[dict[str, Any]] = forecast_data["properties"]["periods"]
    forecasts: list[str] = []
    for period in periods[:5]:  # Only show next 5 periods.
        forecast: str = textwrap.dedent(
            f"""
        {period["name"]}:
        Temperature: {period["temperature"]}°{period["temperatureUnit"]}
        Wind: {period["windSpeed"]} {period["windDirection"]}
        Forecast: {period["detailedForecast"]}
        """
        )
        forecasts.append(forecast)

    return "\n".join(forecasts)
