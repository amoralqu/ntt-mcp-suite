# src/ntt_adb_mcp/tools/packages.py
from __future__ import annotations

from typing import Any, Dict, List, Optional
from .devices import _run_adb_command


def list_packages(
    device_id: Optional[str] = None,
    filter_system: bool = False,
    filter_third_party: bool = False
) -> Dict[str, Any]:
    """
    Lista paquetes instalados en el dispositivo.
    
    Args:
        device_id: ID del dispositivo
        filter_system: Si True, solo muestra paquetes del sistema
        filter_third_party: Si True, solo muestra paquetes de terceros
    
    Returns:
        Dict con lista de paquetes
    """
    args = ["shell", "pm", "list", "packages"]
    
    if filter_system:
        args.append("-s")
    elif filter_third_party:
        args.append("-3")
    
    result = _run_adb_command(args, device_id)
    
    if not result["success"]:
        return result
    
    packages = []
    for line in result["stdout"].split("\n"):
        if line.startswith("package:"):
            packages.append(line.replace("package:", "").strip())
    
    return {
        "success": True,
        "packages": packages,
        "count": len(packages)
    }


def get_package_info(
    package_name: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Obtiene información detallada de un paquete.
    
    Args:
        package_name: Nombre del paquete
        device_id: ID del dispositivo
    
    Returns:
        Dict con información del paquete
    """
    result = _run_adb_command(
        ["shell", "dumpsys", "package", package_name],
        device_id
    )
    
    return {
        "success": result["success"],
        "package": package_name,
        "info": result["stdout"] if result["success"] else None
    }


def install_apk(
    apk_path: str,
    device_id: Optional[str] = None,
    reinstall: bool = False
) -> Dict[str, Any]:
    """
    Instala un APK en el dispositivo.
    
    Args:
        apk_path: Ruta local del APK
        device_id: ID del dispositivo
        reinstall: Si True, reinstala la aplicación
    
    Returns:
        Dict con resultado de la instalación
    """
    args = ["install"]
    if reinstall:
        args.append("-r")
    args.append(apk_path)
    
    result = _run_adb_command(args, device_id, timeout=60)
    
    return {
        "success": result["success"],
        "apk_path": apk_path,
        "output": result["stdout"]
    }


def uninstall_package(
    package_name: str,
    device_id: Optional[str] = None,
    keep_data: bool = False
) -> Dict[str, Any]:
    """
    Desinstala un paquete del dispositivo.
    
    Args:
        package_name: Nombre del paquete
        device_id: ID del dispositivo
        keep_data: Si True, mantiene los datos de la aplicación
    
    Returns:
        Dict con resultado de la desinstalación
    """
    args = ["uninstall"]
    if keep_data:
        args.append("-k")
    args.append(package_name)
    
    result = _run_adb_command(args, device_id)
    
    return {
        "success": result["success"],
        "package": package_name,
        "output": result["stdout"]
    }


def start_activity(
    package_name: str,
    activity_name: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Inicia una actividad específica de una aplicación.
    
    Args:
        package_name: Nombre del paquete
        activity_name: Nombre de la actividad
        device_id: ID del dispositivo
    
    Returns:
        Dict con resultado del inicio
    """
    component = f"{package_name}/{activity_name}"
    result = _run_adb_command(
        ["shell", "am", "start", "-n", component],
        device_id
    )
    
    return {
        "success": result["success"],
        "component": component,
        "output": result["stdout"]
    }


def stop_app(
    package_name: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Detiene una aplicación.
    
    Args:
        package_name: Nombre del paquete
        device_id: ID del dispositivo
    
    Returns:
        Dict con resultado
    """
    result = _run_adb_command(
        ["shell", "am", "force-stop", package_name],
        device_id
    )
    
    return {
        "success": result["success"],
        "package": package_name
    }


def clear_app_data(
    package_name: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Limpia los datos de una aplicación.
    
    Args:
        package_name: Nombre del paquete
        device_id: ID del dispositivo
    
    Returns:
        Dict con resultado
    """
    result = _run_adb_command(
        ["shell", "pm", "clear", package_name],
        device_id
    )
    
    return {
        "success": result["success"],
        "package": package_name,
        "output": result["stdout"]
    }
