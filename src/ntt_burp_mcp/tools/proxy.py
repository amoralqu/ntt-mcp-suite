# src/ntt_burp_mcp/tools/proxy.py
from __future__ import annotations

from typing import Any, Dict, List, Optional
from .client import get_burp_client


def get_proxy_history(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Obtiene el historial de peticiones del proxy.
    
    Args:
        limit: Número máximo de peticiones a devolver
    
    Returns:
        Lista de peticiones del historial
    """
    client = get_burp_client()
    result = client.get(f"/v0.1/proxy/history?limit={limit}")
    return result.get("history", []) if isinstance(result, dict) else result


def get_proxy_item(item_id: int) -> Dict[str, Any]:
    """
    Obtiene los detalles de un item específico del proxy.
    
    Args:
        item_id: ID del item en el historial del proxy
    
    Returns:
        Dict con los detalles del item
    """
    client = get_burp_client()
    return client.get(f"/v0.1/proxy/history/{item_id}")


def send_to_repeater(item_id: int) -> Dict[str, Any]:
    """
    Envía un item del proxy al Repeater.
    
    Args:
        item_id: ID del item en el historial del proxy
    
    Returns:
        Dict con la confirmación del envío
    """
    client = get_burp_client()
    return client.post(f"/v0.1/proxy/history/{item_id}/send_to_repeater")


def send_to_intruder(item_id: int) -> Dict[str, Any]:
    """
    Envía un item del proxy al Intruder.
    
    Args:
        item_id: ID del item en el historial del proxy
    
    Returns:
        Dict con la confirmación del envío
    """
    client = get_burp_client()
    return client.post(f"/v0.1/proxy/history/{item_id}/send_to_intruder")


def get_proxy_config() -> Dict[str, Any]:
    """
    Obtiene la configuración actual del proxy.
    
    Returns:
        Dict con la configuración del proxy
    """
    client = get_burp_client()
    return client.get("/v0.1/proxy/config")


def update_proxy_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Actualiza la configuración del proxy.
    
    Args:
        config: Configuración del proxy a actualizar
    
    Returns:
        Dict con la confirmación de actualización
    """
    client = get_burp_client()
    return client.put("/v0.1/proxy/config", json=config)
