"""Main entry point for the MCP server."""

import logging

from mcp_server import get_mcp_server


logger: logging.Logger = logging.getLogger(__name__)



def main() -> None:
    logger.info("Starting MCP!")
    mcp_server = get_mcp_server()
    mcp_server.run(transport="stdio")


if __name__ == "__main__":
    main()
