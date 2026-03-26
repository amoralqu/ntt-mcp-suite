# src/ntt_burp_mcp/tools/registry.py
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import scanner
from . import proxy


def register_all(mcp: FastMCP) -> None:
    """Registra todas las herramientas de Burp Suite en el servidor MCP."""
    
    # Scanner tools
    mcp.tool()(scanner.start_scan)
    mcp.tool()(scanner.get_scan_status)
    mcp.tool()(scanner.get_scan_issues)
    mcp.tool()(scanner.stop_scan)
    mcp.tool()(scanner.get_scan_metrics)
    
    # Proxy tools
    mcp.tool()(proxy.get_proxy_history)
    mcp.tool()(proxy.get_proxy_item)
    mcp.tool()(proxy.send_to_repeater)
    mcp.tool()(proxy.send_to_intruder)
    mcp.tool()(proxy.get_proxy_config)
    mcp.tool()(proxy.update_proxy_config)
