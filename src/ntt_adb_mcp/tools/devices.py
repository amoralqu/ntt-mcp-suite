# src/ntt_adb_mcp/tools/devices.py
from __future__ import annotations

from typing import Any, Dict, List, Optional
import subprocess
from ..config import ADB_PATH, COMMAND_TIMEOUT_SECONDS, logger


def _run_adb_command(
    args: List[str],
    device_id: Optional[str] = None,
    timeout: int = COMMAND_TIMEOUT_SECONDS
) -> Dict[str, Any]:
    """
    Ejecuta un comando ADB y retorna el resultado.
    
    Args:
        args: Lista de argumentos para el comando ADB
        device_id: ID del dispositivo (opcional)
        timeout: Timeout en segundos
    
    Returns:
        Dict con success, stdout, stderr
    """
    cmd = [ADB_PATH]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(args)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Command timed out after {timeout} seconds",
            "command": " ".join(cmd)
        }
    except Exception as e:
        logger.error(f"Error executing ADB command: {e}")
        return {
            "success": False,
            "error": str(e),
            "command": " ".join(cmd)
        }


def list_devices() -> Dict[str, Any]:
    """
    Lista todos los dispositivos conectados via ADB.
    
    Returns:
        Dict con lista de dispositivos y su estado
    """
    result = _run_adb_command(["devices", "-l"])
    
    if not result["success"]:
        return result
    
    devices = []
    lines = result["stdout"].split("\n")[1:]  # Skip "List of devices attached"
    
    for line in lines:
        if line.strip():
            parts = line.split()
            if len(parts) >= 2:
                device_info = {
                    "id": parts[0],
                    "state": parts[1]
                }
                # Parse additional info (model, device, etc.)
                for part in parts[2:]:
                    if ":" in part:
                        key, value = part.split(":", 1)
                        device_info[key] = value
                devices.append(device_info)
    
    return {
        "success": True,
        "devices": devices,
        "count": len(devices)
    }


def get_device_info(device_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Obtiene información detallada de un dispositivo.
    
    Args:
        device_id: ID del dispositivo (opcional, usa el primero si no se especifica)
    
    Returns:
        Dict con información del dispositivo
    """
    # Obtener propiedades importantes del dispositivo
    properties = [
        "ro.product.model",
        "ro.product.manufacturer",
        "ro.build.version.release",
        "ro.build.version.sdk",
        "ro.product.cpu.abi",
        "ro.serialno"
    ]
    
    device_info = {"device_id": device_id}
    
    for prop in properties:
        result = _run_adb_command(["shell", "getprop", prop], device_id)
        if result["success"]:
            key = prop.split(".")[-1]
            device_info[key] = result["stdout"]
    
    return {"success": True, "info": device_info}


def get_device_state(device_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Obtiene el estado de un dispositivo.
    
    Args:
        device_id: ID del dispositivo
    
    Returns:
        Dict con el estado del dispositivo
    """
    result = _run_adb_command(["get-state"], device_id)
    return {
        "success": result["success"],
        "state": result["stdout"] if result["success"] else None,
        "device_id": device_id
    }
