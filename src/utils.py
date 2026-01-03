import logging
import textwrap
from typing import Any

import httpx


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


async def make_request(url: str, user_agent: str) -> Any:
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
            logging.error("HTTP error occurred: %s", e)
            raise e
