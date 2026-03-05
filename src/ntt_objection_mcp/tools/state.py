# src/ntt_objection_mcp/tools/state.py
from __future__ import annotations
from typing import Dict, Any, Optional
from objection.state.connection import StateConnection

# Estado global para mantener la sesión de Objection
_objection_state: Dict[str, Any] = {
    "connection": None,
    "device_id": None,
    "app_identifier": None,
}


def get_state() -> Dict[str, Any]:
    """Retorna el estado actual de la sesión de Objection."""
    return _objection_state


def set_connection(connection: Optional[StateConnection]) -> None:
    """Establece la conexión de Objection."""
    _objection_state["connection"] = connection


def get_connection() -> Optional[StateConnection]:
    """Obtiene la conexión activa de Objection."""
    return _objection_state.get("connection")


def set_device_id(device_id: Optional[str]) -> None:
    """Establece el ID del dispositivo."""
    _objection_state["device_id"] = device_id


def get_device_id() -> Optional[str]:
    """Obtiene el ID del dispositivo."""
    return _objection_state.get("device_id")


def set_app_identifier(app_identifier: Optional[str]) -> None:
    """Establece el identificador de la aplicación."""
    _objection_state["app_identifier"] = app_identifier


def get_app_identifier() -> Optional[str]:
    """Obtiene el identificador de la aplicación."""
    return _objection_state.get("app_identifier")


def clear_state() -> None:
    """Limpia el estado de la sesión."""
    _objection_state["connection"] = None
    _objection_state["device_id"] = None
    _objection_state["app_identifier"] = None
