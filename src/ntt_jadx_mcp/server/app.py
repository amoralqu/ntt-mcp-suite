from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ntt_jadx_mcp.tools.registry import register_all


def create_app() -> FastMCP:
    mcp = FastMCP("ntt-jadx-mcp")
    register_all(mcp)
    return mcp
