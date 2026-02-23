# src/ntt_frida_mcp/tools/registry.py
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import devices
from . import lifecycle
from . import hooks
from . import processes
from . import sessions


def register_all(mcp: FastMCP) -> None:
    # Devices / processes enumeration
    mcp.tool()(devices.enumerate_devices)
    mcp.tool()(devices.get_device)
    mcp.tool()(devices.get_usb_device)

    # Consistencia: ambos aceptan device_id (si aplicaste Paso 1)
    mcp.tool()(devices.enumerate_processes)
    mcp.tool()(devices.list_processes)

    # Process helpers
    mcp.tool()(processes.get_process_by_name)
    mcp.tool()(processes.attach_to_process)

    # Lifecycle
    mcp.tool()(lifecycle.spawn_process)
    mcp.tool()(lifecycle.resume_process)
    mcp.tool()(lifecycle.kill_process)

    # Hooks
    mcp.tool()(hooks.create_simple_hook)

    # Sessions
    mcp.tool()(sessions.create_interactive_session)
    mcp.tool()(sessions.execute_in_session)
    mcp.tool()(sessions.close_interactive_session)
