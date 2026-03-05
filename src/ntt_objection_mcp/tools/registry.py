# src/ntt_objection_mcp/tools/registry.py
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import devices
from . import applications
from . import exploration


def register_all(mcp: FastMCP) -> None:
    """
    Registra todas las herramientas de Objection en el servidor MCP.
    """
    # Dispositivos
    mcp.tool()(devices.enumerate_devices)
    mcp.tool()(devices.get_device)
    mcp.tool()(devices.get_usb_device)
    
    # Aplicaciones
    mcp.tool()(applications.list_applications)
    mcp.tool()(applications.get_frontmost_application)
    mcp.tool()(applications.get_application_info)
    
    # Exploración
    mcp.tool()(exploration.explore_classes)
    mcp.tool()(exploration.explore_methods)
    mcp.tool()(exploration.explore_activities)
    mcp.tool()(exploration.explore_services)
