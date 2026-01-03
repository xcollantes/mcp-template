"""Main entry point for the MCP server."""

import logging
import textwrap

import httpx
from mcp.server.fastapi import FastMCP

logger: logging.Logger = logging.getLogger(__name__)

mcp: FastMCP = FastMCP(__name__)

WEATHER_API_BASE = "https://api.weather.gov"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
USER_AGENT = "weather-app/1.0"


def main() -> None:
    logger.info("Starting MCP!")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
