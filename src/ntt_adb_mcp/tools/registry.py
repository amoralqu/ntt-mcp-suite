# src/ntt_adb_mcp/tools/registry.py
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import devices
from . import packages
from . import shell


def register_all(mcp: FastMCP) -> None:
    """Registra todas las herramientas ADB en el servidor MCP."""
    
    # Device management
    mcp.tool()(devices.list_devices)
    mcp.tool()(devices.get_device_info)
    mcp.tool()(devices.get_device_state)
    
    # Package management
    mcp.tool()(packages.list_packages)
    mcp.tool()(packages.get_package_info)
    mcp.tool()(packages.install_apk)
    mcp.tool()(packages.uninstall_package)
    mcp.tool()(packages.start_activity)
    mcp.tool()(packages.stop_app)
    mcp.tool()(packages.clear_app_data)
    
    # Shell and file operations
    mcp.tool()(shell.execute_shell_command)
    mcp.tool()(shell.pull_file)
    mcp.tool()(shell.push_file)
    mcp.tool()(shell.list_directory)
    mcp.tool()(shell.get_logcat)
    mcp.tool()(shell.clear_logcat)
    mcp.tool()(shell.reboot_device)
    mcp.tool()(shell.take_screenshot)
