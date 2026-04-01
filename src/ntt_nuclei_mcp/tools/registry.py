# src/ntt_nuclei_mcp/tools/registry.py
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import scanner


def register_all(mcp: FastMCP) -> None:
    """Registra todas las herramientas de Nuclei en el servidor MCP."""
    
    # Scanner tools
    mcp.tool()(scanner.run_nuclei_scan)
    mcp.tool()(scanner.list_templates)
    mcp.tool()(scanner.update_templates)
    mcp.tool()(scanner.get_nuclei_version)
