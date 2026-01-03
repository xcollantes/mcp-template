"""MCP server object."""

from functools import lru_cache

from mcp.server.fastmcp import FastMCP


@lru_cache(maxsize=1)
def get_mcp_server() -> FastMCP:
    mcp: FastMCP = FastMCP(__name__)
    return mcp
