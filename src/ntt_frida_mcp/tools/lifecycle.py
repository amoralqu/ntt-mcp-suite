# src/ntt_frida_mcp/tools/lifecycle.py
from typing import Any, Dict, List, Optional
import frida


def spawn_process(
    program: str,
    args: Optional[List[str]] = None,
    device_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Spawn a program on the given device (or local)."""
    try:
        device = frida.get_device(device_id) if device_id else frida.get_local_device()
        pid = device.spawn(program, args=args or [])
        return {"pid": pid}
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Failed to spawn {program}: {e}") from e


def resume_process(pid: int, device_id: Optional[str] = None) -> Dict[str, Any]:
    """Resume a process by ID."""
    try:
        device = frida.get_device(device_id) if device_id else frida.get_local_device()
        device.resume(pid)
        return {"success": True, "pid": pid}
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Failed to resume process {pid}: {e}") from e


def kill_process(pid: int, device_id: Optional[str] = None) -> Dict[str, Any]:
    """Kill a process by ID."""
    try:
        device = frida.get_device(device_id) if device_id else frida.get_local_device()
        device.kill(pid)
        return {"success": True, "pid": pid}
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Failed to kill process {pid}: {e}") from e
