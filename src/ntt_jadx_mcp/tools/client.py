from __future__ import annotations

import os
from typing import Any, Dict, Optional, Union

import httpx


DEFAULT_JADX_PORT = 8650
JADX_HOST = "127.0.0.1"  # 🔒 hardcoded local-only
DEFAULT_TIMEOUT_SECONDS = 60.0


def get_jadx_port() -> int:
    raw = os.environ.get("NTT_JADX_PORT", str(DEFAULT_JADX_PORT))
    try:
        port = int(raw)
    except ValueError as e:
        raise ValueError(f"NTT_JADX_PORT must be an int (got {raw!r})") from e
    if port <= 0 or port > 65535:
        raise ValueError(f"NTT_JADX_PORT out of range (got {port})")
    return port


def base_url(port: Optional[int] = None) -> str:
    p = port if port is not None else get_jadx_port()
    return f"http://{JADX_HOST}:{p}"


async def get_from_jadx(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    *,
    port: Optional[int] = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
) -> Union[Dict[str, Any], str]:
    """
    Llama a la API del plugin JADX (local-only) en http://127.0.0.1:<port>/<endpoint>.

    - endpoint: string como 'health', 'class-source', 'manifest', etc.
    - params: dict de query params
    """
    params = params or {}
    url = f"{base_url(port)}/{endpoint.lstrip('/')}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, timeout=timeout_seconds)
        resp.raise_for_status()
        # intentamos JSON, si no, devolvemos texto
        try:
            return resp.json()
        except Exception:
            return resp.text


async def health_ping(*, port: Optional[int] = None) -> Dict[str, Any]:
    """
    Comprueba conectividad con el plugin en /health.
    """
    try:
        res = await get_from_jadx("health", port=port)
        return {"ok": True, "response": res, "base_url": base_url(port)}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e), "base_url": base_url(port)}
