# src/ntt_frida_mcp/tools/devices.py
from __future__ import annotations

from typing import Any, Dict, List, Optional

import frida


def _get_device(device_id: Optional[str] = None) -> frida.core.Device:
    """
    Devuelve el device de Frida a usar.
    - Si device_id es None -> local device
    - Si device_id viene -> frida.get_device(device_id)
    """
    return frida.get_device(device_id) if device_id else frida.get_local_device()


def enumerate_devices() -> List[Dict[str, Any]]:
    """
    Lista dispositivos visibles por Frida.

    Retorna una lista de dicts con:
    - id
    - name
    - type
    """
    devices = frida.enumerate_devices()
    return [{"id": d.id, "name": d.name, "type": d.type} for d in devices]


def get_device(device_id: str) -> Dict[str, Any]:
    """
    Obtiene metadata de un device por id.
    """
    try:
        d = frida.get_device(device_id)
        return {"id": d.id, "name": d.name, "type": d.type}
    except Exception as e:  # noqa: BLE001
        return {"success": False, "error": str(e), "device_id": device_id}


def get_usb_device(timeout: int = 5) -> Dict[str, Any]:
    """
    Obtiene el dispositivo USB por defecto (si existe).
    """
    try:
        d = frida.get_usb_device(timeout=timeout)
        return {"id": d.id, "name": d.name, "type": d.type}
    except Exception as e:  # noqa: BLE001
        return {"success": False, "error": str(e), "timeout": timeout}


def enumerate_processes(device_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Enumera procesos en un device.

    - device_id=None -> local
    - device_id=<id> -> ese device (USB/remoto)
    """
    device = _get_device(device_id)
    procs = device.enumerate_processes()
    return [{"pid": p.pid, "name": p.name} for p in procs]


def list_processes(device_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Alias de enumerate_processes para mantener compatibilidad.
    IMPORTANTE: ahora acepta device_id, igual que el resto de tools.

    Retorna lista de {pid, name}.
    """
    return enumerate_processes(device_id=device_id)
