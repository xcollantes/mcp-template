"""Main entry point for the MCP server.

Point your LLM client to this file to use the MCP server.
"""

import logging

from server import mcp

logger: logging.Logger = logging.getLogger("logger")


def main() -> None:
    try:
        logger.info("Starting MCP server.")
        mcp.run(transport="stdio")

    except Exception as e:
        logger.error("Error starting MCP server: %s", e)
        raise e


if __name__ == "__main__":
    main()
