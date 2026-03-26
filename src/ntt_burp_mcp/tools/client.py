# src/ntt_burp_mcp/tools/client.py
from __future__ import annotations

import requests
from typing import Any, Dict, Optional
from ..config import BURP_API_URL, BURP_API_KEY, REQUEST_TIMEOUT_SECONDS, logger


class BurpClient:
    """Cliente para interactuar con la API de Burp Suite."""
    
    def __init__(self, api_url: str = BURP_API_URL, api_key: Optional[str] = BURP_API_KEY):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Realiza una petición HTTP a la API de Burp."""
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault("headers", {}).update(self.headers)
        kwargs.setdefault("timeout", REQUEST_TIMEOUT_SECONDS)
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {"success": True}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en petición a Burp API: {e}")
            return {"success": False, "error": str(e)}
    
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Realiza una petición GET."""
        return self._request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Realiza una petición POST."""
        return self._request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Realiza una petición PUT."""
        return self._request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Realiza una petición DELETE."""
        return self._request("DELETE", endpoint, **kwargs)


# Instancia global del cliente
_burp_client: Optional[BurpClient] = None


def get_burp_client() -> BurpClient:
    """Obtiene o crea una instancia del cliente de Burp."""
    global _burp_client
    if _burp_client is None:
        _burp_client = BurpClient()
    return _burp_client
