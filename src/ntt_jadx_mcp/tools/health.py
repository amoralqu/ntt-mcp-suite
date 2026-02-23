from __future__ import annotations

from typing import Any, Dict

from ntt_jadx_mcp.tools.client import health_ping


async def health_check() -> Dict[str, Any]:
    """
    Health check del MCP (y del plugin si está disponible).
    """
    plugin = await health_ping()
    if plugin.get("ok"):
        return {"status": "ok", "server": "ntt-jadx-mcp", "plugin": plugin}
    return {"status": "degraded", "server": "ntt-jadx-mcp", "plugin": plugin}
