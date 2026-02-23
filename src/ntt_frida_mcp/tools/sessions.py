# src/ntt_frida_mcp/tools/sessions.py
from __future__ import annotations

from typing import Any, Dict, Optional
import os
import threading
import time

import frida

from . import state


# TTL por defecto (1h). Se puede ajustar por env var sin meter config extra.
SESSION_TIMEOUT_SECONDS = int(os.environ.get("NTT_SESSION_TIMEOUT", "3600"))
_CLEANUP_INTERVAL_SECONDS = int(os.environ.get("NTT_SESSION_CLEANUP_INTERVAL", "300"))

_cleaner_started = False
_cleaner_lock = threading.Lock()


def _get_device(device_id: Optional[str] = None) -> frida.core.Device:
    return frida.get_device(device_id) if device_id else frida.get_local_device()


def _start_cleaner_once() -> None:
    """
    Lanza un thread daemon que limpia sesiones expiradas cada X segundos.
    """
    global _cleaner_started
    if _cleaner_started:
        return

    with _cleaner_lock:
        if _cleaner_started:
            return

        def _run():
            while True:
                try:
                    state.cleanup_expired(timeout_seconds=SESSION_TIMEOUT_SECONDS)
                except Exception:
                    # no matamos el thread por fallos puntuales
                    pass
                time.sleep(_CLEANUP_INTERVAL_SECONDS)

        t = threading.Thread(target=_run, name="ntt_frida_session_cleaner", daemon=True)
        t.start()
        _cleaner_started = True


def create_interactive_session(process_id: int, device_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Crea una sesión interactiva contra un proceso en el device indicado.
    Guarda session+script en state para reuso con execute_in_session.

    Nota: esta sesión se limpia automáticamente si queda inactiva (TTL),
    o se puede cerrar explícitamente con close_interactive_session.
    """
    _start_cleaner_once()

    device = _get_device(device_id)

    try:
        sess = device.attach(process_id)
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "message": f"Failed to attach to process {process_id}: {e}"}

    # Script base: solo expone un canal de logs. La evaluación ocurre vía script.exports.
    # Mantenerlo simple y compatible.
    base_js = r"""
        rpc.exports = {
            evaljs: function(code) {
                try {
                    // Eval controlado por el usuario; devuelve resultado serializable
                    var r = eval(code);
                    // Normalizamos a string si es objeto
                    if (typeof r === 'object') {
                        try { return JSON.stringify(r); } catch (e) { return String(r); }
                    }
                    return String(r);
                } catch (e) {
                    throw new Error(String(e));
                }
            }
        };

        // Canal opcional de logs
        console.log("[*] Interactive session script loaded");
    """

    messages = []

    try:
        script = sess.create_script(base_js)

        def on_message(message, data):  # noqa: ARG001
            # guardamos todo lo que llegue
            state.add_message(session_id, message)

        session_id = f"session_{process_id}_{int(time.time())}"
        script.on("message", on_message)
        script.load()

        # Guardar referencias para poder reusar/cerrar
        state.sessions[session_id] = sess
        state.scripts[session_id] = script
        state.touch_session(session_id)

        return {
            "status": "success",
            "process_id": process_id,
            "session_id": session_id,
            "message": f"Interactive session created for process {process_id}. Use execute_in_session to run JavaScript commands.",
        }

    except Exception as e:  # noqa: BLE001
        # cleanup si falla a mitad
        try:
            sess.detach()
        except Exception:
            pass
        return {"status": "error", "message": f"Failed to create interactive session: {e}"}


def execute_in_session(session_id: str, javascript_code: str) -> Dict[str, Any]:
    """
    Ejecuta JS dentro de una sesión interactiva creada previamente.
    Devuelve result + logs (mensajes capturados por send/console).
    """
    script = state.scripts.get(session_id)
    if script is None:
        return {"status": "error", "message": f"Session '{session_id}' not found (expired or closed)."}

    state.touch_session(session_id)

    try:
        # Frida RPC export
        result = script.exports.evaljs(javascript_code)
        logs = state.pop_messages(session_id)
        return {"status": "success", "result": result, "logs": logs}
    except Exception as e:  # noqa: BLE001
        logs = state.pop_messages(session_id)
        return {"status": "error", "message": str(e), "logs": logs}


def close_interactive_session(session_id: str) -> Dict[str, Any]:
    """
    Cierra explícitamente una sesión interactiva y libera recursos.
    """
    if session_id not in state.scripts and session_id not in state.sessions:
        return {"status": "error", "message": f"Session '{session_id}' not found (already closed/expired)."}

    info = state.close_session(session_id)
    return {"status": "success", "closed": info}
