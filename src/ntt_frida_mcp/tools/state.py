# src/ntt_frida_mcp/tools/state.py
from __future__ import annotations

from typing import Any, Dict, List, Optional
import threading
import time

# ---- Estado de sesiones interactivas ----
# Guardamos tanto la sesión como el script para poder descargar + detach
sessions: Dict[str, Any] = {}          # session_id -> frida.Session
scripts: Dict[str, Any] = {}           # session_id -> frida.Script

# Mensajes por sesión (send(...) desde JS)
script_messages: Dict[str, List[Any]] = {}   # session_id -> [message...]
message_locks: Dict[str, threading.Lock] = {}  # session_id -> Lock

# Último acceso para TTL cleanup
_last_access: Dict[str, float] = {}     # session_id -> timestamp


def touch_session(session_id: str) -> None:
    _last_access[session_id] = time.time()


def ensure_lock(session_id: str) -> threading.Lock:
    lock = message_locks.get(session_id)
    if lock is None:
        lock = threading.Lock()
        message_locks[session_id] = lock
    return lock


def add_message(session_id: str, message: Any) -> None:
    lock = ensure_lock(session_id)
    with lock:
        script_messages.setdefault(session_id, []).append(message)
    touch_session(session_id)


def pop_messages(session_id: str) -> List[Any]:
    lock = ensure_lock(session_id)
    with lock:
        msgs = script_messages.get(session_id, [])
        script_messages[session_id] = []
    return msgs


def remove_session(session_id: str) -> None:
    """
    Elimina referencias del estado (no hace unload/detach).
    Para cierre completo usar close_session().
    """
    sessions.pop(session_id, None)
    scripts.pop(session_id, None)
    script_messages.pop(session_id, None)
    message_locks.pop(session_id, None)
    _last_access.pop(session_id, None)


def close_session(session_id: str) -> Dict[str, Any]:
    """
    Cierre completo: unload script + detach session + limpiar estado.
    Devuelve dict con información del cierre.
    """
    info: Dict[str, Any] = {"session_id": session_id, "unloaded": False, "detached": False}

    script = scripts.get(session_id)
    sess = sessions.get(session_id)

    # Descargar script primero
    try:
        if script is not None:
            script.unload()
            info["unloaded"] = True
    except Exception as e:  # noqa: BLE001
        info["script_unload_error"] = str(e)

    # Detach de sesión
    try:
        if sess is not None:
            sess.detach()
            info["detached"] = True
    except Exception as e:  # noqa: BLE001
        info["session_detach_error"] = str(e)

    remove_session(session_id)
    return info


def cleanup_expired(timeout_seconds: int = 3600) -> Dict[str, Any]:
    """
    Cierra sesiones inactivas (TTL).
    """
    now = time.time()
    expired = [sid for sid, ts in list(_last_access.items()) if (now - ts) > timeout_seconds]

    closed: List[Dict[str, Any]] = []
    for sid in expired:
        closed.append(close_session(sid))

    return {"timeout_seconds": timeout_seconds, "expired_count": len(expired), "closed": closed}
