# src/ntt_objection_mcp/tools/applications.py
from __future__ import annotations
from typing import Any, Dict, List, Optional
import frida
from ..config import logger
from . import state


def list_applications(device_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Lista todas las aplicaciones instaladas en el dispositivo.
    
    Args:
        device_id: ID del dispositivo. Si es None, usa el dispositivo actual o local.
    
    Returns:
        Lista de aplicaciones con su información básica.
    """
    try:
        # Obtener dispositivo
        if device_id:
            device = frida.get_device(device_id)
        else:
            # Intentar usar el dispositivo guardado en estado
            saved_device_id = state.get_device_id()
            if saved_device_id:
                device = frida.get_device(saved_device_id)
            else:
                device = frida.get_local_device()
        
        # Listar aplicaciones
        applications = device.enumerate_applications()
        
        result = []
        for app in applications:
            result.append({
                "identifier": app.identifier,
                "name": app.name,
                "pid": app.pid if hasattr(app, 'pid') else 0
            })
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing applications: {e}")
        return {"success": False, "error": str(e)}


def get_frontmost_application(device_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Obtiene la aplicación que está actualmente en primer plano.
    
    Args:
        device_id: ID del dispositivo. Si es None, usa el dispositivo actual o local.
    
    Returns:
        Información de la aplicación en primer plano.
    """
    try:
        # Obtener dispositivo
        if device_id:
            device = frida.get_device(device_id)
        else:
            saved_device_id = state.get_device_id()
            if saved_device_id:
                device = frida.get_device(saved_device_id)
            else:
                device = frida.get_local_device()
        
        # Obtener aplicación en primer plano
        app = device.get_frontmost_application()
        
        if app:
            return {
                "success": True,
                "identifier": app.identifier,
                "name": app.name,
                "pid": app.pid if hasattr(app, 'pid') else 0
            }
        else:
            return {
                "success": False,
                "error": "No frontmost application found"
            }
        
    except Exception as e:
        logger.error(f"Error getting frontmost application: {e}")
        return {"success": False, "error": str(e)}


def get_application_info(identifier: str, device_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Obtiene información detallada de una aplicación específica.
    
    Args:
        identifier: Bundle identifier de la aplicación (ej: com.example.app)
        device_id: ID del dispositivo. Si es None, usa el dispositivo actual o local.
    
    Returns:
        Información detallada de la aplicación.
    """
    try:
        # Obtener dispositivo
        if device_id:
            device = frida.get_device(device_id)
        else:
            saved_device_id = state.get_device_id()
            if saved_device_id:
                device = frida.get_device(saved_device_id)
            else:
                device = frida.get_local_device()
        
        # Buscar la aplicación
        applications = device.enumerate_applications()
        
        for app in applications:
            if app.identifier == identifier:
                return {
                    "success": True,
                    "identifier": app.identifier,
                    "name": app.name,
                    "pid": app.pid if hasattr(app, 'pid') else 0
                }
        
        return {
            "success": False,
            "error": f"Application '{identifier}' not found"
        }
        
    except Exception as e:
        logger.error(f"Error getting application info: {e}")
        return {"success": False, "error": str(e)}
