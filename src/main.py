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
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr,  # Use stderr to avoid corrupting stdout (used for MCP protocol)
    )


def main() -> None:
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(
        description="MCP Weather Server - Provides weather tools for LLM clients"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--help", action="help", help="Show this help message and exit")

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.debug)

    try:
        logger.info("Starting MCP Weather server...")
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error("Error starting MCP server: %s", e)


if __name__ == "__main__":
    main()
