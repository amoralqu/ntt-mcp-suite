# src/ntt_objection_mcp/tools/devices.py
from __future__ import annotations
from typing import Any, Dict, List, Optional
import frida
from ..config import logger


def enumerate_devices() -> List[Dict[str, Any]]:
    """
    Lista dispositivos visibles por Frida (usado por Objection).
    
    Retorna una lista de dicts con:
    - id: ID del dispositivo
    - name: Nombre del dispositivo
    - type: Tipo de dispositivo (local, usb, remote)
    """
    try:
        devices = frida.enumerate_devices()
        return [
            {
                "id": d.id,
                "name": d.name,
                "type": d.type
            }
            for d in devices
        ]
    except Exception as e:
        logger.error(f"Error enumerating devices: {e}")
        return {"success": False, "error": str(e)}


def get_device(device_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Obtiene información de un dispositivo específico.
    
    Args:
        device_id: ID del dispositivo. Si es None, usa el dispositivo local.
    
    Returns:
        Dict con información del dispositivo o error.
    """
    try:
        if device_id:
            device = frida.get_device(device_id)
        else:
            device = frida.get_local_device()
        
        return {
            "success": True,
            "id": device.id,
            "name": device.name,
            "type": device.type
        }
    except Exception as e:
        logger.error(f"Error getting device: {e}")
        return {"success": False, "error": str(e)}


def get_usb_device(timeout: int = 5) -> Dict[str, Any]:
    """
    Obtiene el dispositivo USB conectado.
    
    Args:
        timeout: Tiempo de espera en segundos.
    
    Returns:
        Dict con información del dispositivo USB o error.
    """
    try:
        device = frida.get_usb_device(timeout=timeout)
        return {
            "success": True,
            "id": device.id,
            "name": device.name,
            "type": device.type
        }
    except Exception as e:
        logger.error(f"Error getting USB device: {e}")
        return {"success": False, "error": str(e), "timeout": timeout}
