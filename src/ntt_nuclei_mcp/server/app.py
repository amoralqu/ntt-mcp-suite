# src/ntt_nuclei_mcp/server/app.py
from mcp.server.fastmcp import FastMCP
from ..config import MCP_SERVER_NAME, logger
from ..tools.registry import register_all
import signal
import sys

mcp = FastMCP(MCP_SERVER_NAME)

# Registrar todas las tools
register_all(mcp)

# Health-check simple
@mcp.tool()
def health_check() -> dict:
    """Health check for the MCP server."""
    return {"status": "ok", "server": MCP_SERVER_NAME}

def _graceful_shutdown(signum, frame):
    logger.info("Received signal %s, shutting down MCP server...", signum)
    try:
        mcp.stop()  # if FastMCP exposes stop()
    except Exception:
        pass
    sys.exit(0)

signal.signal(signal.SIGINT, _graceful_shutdown)
signal.signal(signal.SIGTERM, _graceful_shutdown)
