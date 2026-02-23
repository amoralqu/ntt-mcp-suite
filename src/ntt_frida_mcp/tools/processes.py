# src/ntt_frida_mcp/tools/processes.py
from typing import Any, Dict, Optional
import frida


def get_process_by_name(name: str, device_id: Optional[str] = None) -> Dict[str, Any]:
    """Find a process by name (substring match, case-insensitive)."""
    device = frida.get_device(device_id) if device_id else frida.get_local_device()
    for proc in device.enumerate_processes():
        if name.lower() in proc.name.lower():
            return {"pid": proc.pid, "name": proc.name, "found": True}
    return {"found": False, "error": f"Process '{name}' not found"}


def attach_to_process(pid: int, device_id: Optional[str] = None) -> Dict[str, Any]:
    """Attach to a process by ID."""
    try:
        device = frida.get_device(device_id) if device_id else frida.get_local_device()
        device.attach(pid)
        return {"pid": pid, "success": True, "is_detached": False}
    except Exception as e:  # noqa: BLE001
        return {"success": False, "error": str(e)}
