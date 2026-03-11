# src/ntt_adb_mcp/tools/shell.py
from __future__ import annotations

from typing import Any, Dict, Optional
from .devices import _run_adb_command


def execute_shell_command(
    command: str,
    device_id: Optional[str] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Ejecuta un comando shell en el dispositivo.
    
    Args:
        command: Comando shell a ejecutar
        device_id: ID del dispositivo
        timeout: Timeout en segundos
    
    Returns:
        Dict con resultado del comando
    """
    result = _run_adb_command(
        ["shell", command],
        device_id,
        timeout=timeout
    )
    
    return {
        "success": result["success"],
        "command": command,
        "output": result["stdout"],
        "error": result.get("stderr", "")
    }


def pull_file(
    remote_path: str,
    local_path: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Descarga un archivo del dispositivo.
    
    Args:
        remote_path: Ruta del archivo en el dispositivo
        local_path: Ruta local donde guardar el archivo
        device_id: ID del dispositivo
    
    Returns:
        Dict con resultado de la operación
    """
    result = _run_adb_command(
        ["pull", remote_path, local_path],
        device_id,
        timeout=60
    )
    
    return {
        "success": result["success"],
        "remote_path": remote_path,
        "local_path": local_path,
        "output": result["stdout"]
    }


def push_file(
    local_path: str,
    remote_path: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Sube un archivo al dispositivo.
    
    Args:
        local_path: Ruta local del archivo
        remote_path: Ruta destino en el dispositivo
        device_id: ID del dispositivo
    
    Returns:
        Dict con resultado de la operación
    """
    result = _run_adb_command(
        ["push", local_path, remote_path],
        device_id,
        timeout=60
    )
    
    return {
        "success": result["success"],
        "local_path": local_path,
        "remote_path": remote_path,
        "output": result["stdout"]
    }


def list_directory(
    path: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lista el contenido de un directorio en el dispositivo.
    
    Args:
        path: Ruta del directorio
        device_id: ID del dispositivo
    
    Returns:
        Dict con lista de archivos
    """
    result = _run_adb_command(
        ["shell", "ls", "-la", path],
        device_id
    )
    
    return {
        "success": result["success"],
        "path": path,
        "content": result["stdout"] if result["success"] else None
    }


def get_logcat(
    device_id: Optional[str] = None,
    filter_tag: Optional[str] = None,
    max_lines: int = 100
) -> Dict[str, Any]:
    """
    Obtiene logs del dispositivo.
    
    Args:
        device_id: ID del dispositivo
        filter_tag: Tag para filtrar logs (opcional)
        max_lines: Número máximo de líneas
    
    Returns:
        Dict con logs
    """
    args = ["logcat", "-d", "-t", str(max_lines)]
    
    if filter_tag:
        args.append(f"{filter_tag}:*")
        args.append("*:S")  # Silencia otros tags
    
    result = _run_adb_command(args, device_id, timeout=10)
    
    return {
        "success": result["success"],
        "logs": result["stdout"] if result["success"] else None,
        "filter_tag": filter_tag
    }


def clear_logcat(device_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Limpia el buffer de logcat.
    
    Args:
        device_id: ID del dispositivo
    
    Returns:
        Dict con resultado
    """
    result = _run_adb_command(["logcat", "-c"], device_id)
    
    return {
        "success": result["success"]
    }


def reboot_device(
    device_id: Optional[str] = None,
    mode: Optional[str] = None
) -> Dict[str, Any]:
    """
    Reinicia el dispositivo.
    
    Args:
        device_id: ID del dispositivo
        mode: Modo de reinicio (bootloader, recovery, None para normal)
    
    Returns:
        Dict con resultado
    """
    args = ["reboot"]
    if mode:
        args.append(mode)
    
    result = _run_adb_command(args, device_id)
    
    return {
        "success": result["success"],
        "mode": mode or "normal"
    }


def take_screenshot(
    output_path: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Toma una captura de pantalla del dispositivo.
    
    Args:
        output_path: Ruta local donde guardar la captura
        device_id: ID del dispositivo
    
    Returns:
        Dict con resultado
    """
    remote_path = "/sdcard/screenshot.png"
    
    # Tomar captura
    result = _run_adb_command(
        ["shell", "screencap", "-p", remote_path],
        device_id
    )
    
    if not result["success"]:
        return result
    
    # Descargar captura
    pull_result = pull_file(remote_path, output_path, device_id)
    
    # Limpiar archivo temporal
    _run_adb_command(["shell", "rm", remote_path], device_id)
    
    return {
        "success": pull_result["success"],
        "output_path": output_path
    }
