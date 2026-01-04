"""Main entry point for the MCP server.

Point your LLM client to this file to use the MCP server.
"""

import argparse
import logging
import sys

from server import mcp

logger: logging.Logger = logging.getLogger(__name__)


def setup_logging(debug: bool = False) -> None:
    """Configure logging for the MCP server."""
    level: int = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s]%(name)s:%(levelname)s: %(message)s",
        # Use stderr to avoid corrupting stdout (used for MCP protocol).
        # https://modelcontextprotocol.io/docs/develop/build-server#logging-in-mcp-servers
        stream=sys.stderr,
    )


def main() -> None:
    """Main entry point for the MCP server."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="MCP Weather Server: Provides weather tools for LLM clients."
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument(
        "--help", action="help", help="Show this help message and exit."
    )

    args: argparse.Namespace = parser.parse_args()

    setup_logging(args.debug)

    logger.info("Starting MCP Weather server...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
