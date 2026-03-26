# src/ntt_burp_mcp/tools/scanner.py
from __future__ import annotations

from typing import Any, Dict, List, Optional
from .client import get_burp_client


def start_scan(target_url: str, scan_type: str = "crawl_and_audit") -> Dict[str, Any]:
    """
    Inicia un escaneo en Burp Suite.
    
    Args:
        target_url: URL del objetivo a escanear
        scan_type: Tipo de escaneo (crawl_and_audit, crawl, audit)
    
    Returns:
        Dict con la información del escaneo iniciado
    """
    client = get_burp_client()
    payload = {
        "urls": [target_url],
        "scan_type": scan_type
    }
    return client.post("/v0.1/scan", json=payload)


def get_scan_status(scan_id: str) -> Dict[str, Any]:
    """
    Obtiene el estado de un escaneo.
    
    Args:
        scan_id: ID del escaneo
    
    Returns:
        Dict con el estado del escaneo
    """
    client = get_burp_client()
    return client.get(f"/v0.1/scan/{scan_id}")


def get_scan_issues(scan_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Obtiene las vulnerabilidades encontradas.
    
    Args:
        scan_id: ID del escaneo (opcional, si no se proporciona devuelve todos)
    
    Returns:
        Lista de vulnerabilidades encontradas
    """
    client = get_burp_client()
    endpoint = f"/v0.1/scan/{scan_id}/issues" if scan_id else "/v0.1/scan/issues"
    result = client.get(endpoint)
    return result.get("issues", []) if isinstance(result, dict) else result


def stop_scan(scan_id: str) -> Dict[str, Any]:
    """
    Detiene un escaneo en curso.
    
    Args:
        scan_id: ID del escaneo
    
    Returns:
        Dict con la confirmación de detención
    """
    client = get_burp_client()
    return client.delete(f"/v0.1/scan/{scan_id}")


def get_scan_metrics(scan_id: str) -> Dict[str, Any]:
    """
    Obtiene métricas de un escaneo.
    
    Args:
        scan_id: ID del escaneo
    
    Returns:
        Dict con las métricas del escaneo
    """
    client = get_burp_client()
    return client.get(f"/v0.1/scan/{scan_id}/metrics")
