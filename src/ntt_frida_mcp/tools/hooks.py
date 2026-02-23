# src/ntt_frida_mcp/tools/hooks.py
from __future__ import annotations

from typing import Any, Dict, List, Optional
import time

import frida


# Scripts JS simples (algunos hooks son Linux/Android-centric).
# Paso 3: guard por plataforma con mensajes claros.
# Paso "extra compartible": network hook con fallback Android/Linux a libc.so.
_HOOK_SCRIPTS: Dict[str, str] = {
    "memory": r"""
        console.log("[*] Memory allocation hooks loaded");

        // Guard por plataforma: este hook no es portable a Windows tal cual.
        if (Process.platform === 'windows') {
            send({
                type: 'error',
                message: "Hook 'memory' (malloc) is not supported on Windows targets with this implementation. Use Android/Linux or implement a Windows-specific allocator hook."
            });
        } else {
            var mallocPtr = Module.findExportByName(null, 'malloc');
            if (!mallocPtr) {
                send({type: 'error', message: "malloc export not found on this target. Hook not installed."});
            } else {
                Interceptor.attach(mallocPtr, {
                    onEnter: function (args) {
                        send({type: 'malloc', size: args[0].toInt32()});
                    }
                });
                send({type: 'status', message: 'Memory hooks installed'});
            }
        }
    """,
    "network": r"""
        console.log("[*] Network hooks loaded");

        function resolveConnect() {
            // 1) Intento genérico (puede funcionar en algunos targets)
            var p = null;
            try { p = Module.findExportByName(null, 'connect'); } catch (e) { p = null; }
            if (p) return p;

            // 2) Fallback Android/Linux: suele estar en libc.so
            if (Process.platform === 'linux') {
                try { p = Module.findExportByName('libc.so', 'connect'); } catch (e) { p = null; }
                if (p) return p;
            }

            // 3) Fallback adicional (algunos entornos usan libc.so.6)
            if (Process.platform === 'linux') {
                try { p = Module.findExportByName('libc.so.6', 'connect'); } catch (e) { p = null; }
                if (p) return p;
            }

            return null;
        }

        var connectPtr = resolveConnect();

        if (!connectPtr) {
            send({type: 'error', message: "connect export not found on this target. Hook not installed."});
        } else {
            // Validación defensiva: si por alguna razón no es un NativePointer válido
            try {
                Interceptor.attach(connectPtr, {
                    onEnter: function (args) {
                        // args[1] apunta a sockaddr, pero no parseamos aquí: solo validamos hook
                        send({type: 'connect', message: 'connect() called'});
                    }
                });
                send({type: 'status', message: 'Network hooks installed'});
            } catch (e) {
                send({type: 'error', message: "Failed to attach to connect(): " + String(e)});
            }
        }
    """,
    "file": r"""
        console.log("[*] File hooks loaded");

        // Guard por plataforma: este hook está pensado para Android/Linux (libc.so open/openat).
        if (Process.platform === 'windows') {
            send({
                type: 'error',
                message: "Hook 'file' (open/openat in libc.so) is not supported on Windows targets with this implementation. Use Android/Linux or implement CreateFileW/NtCreateFile hooks for Windows."
            });
        } else {
            var candidates = ['open', 'open64', 'openat', 'openat64'];
            var openPtr = null;

            for (var i = 0; i < candidates.length; i++) {
                try {
                    openPtr = Module.findExportByName('libc.so', candidates[i]);
                    if (openPtr) break;
                } catch (e) {
                    // ignore
                }
            }

            if (!openPtr) {
                send({type: 'error', message: "No suitable open/openat export found in libc.so. Hook not installed."});
            } else {
                try {
                    Interceptor.attach(openPtr, {
                        onEnter: function (args) {
                            try {
                                var path = Memory.readCString(args[0]);
                                send({type: 'file_open', path: path});
                            } catch (e) {
                                send({type: 'file_open', path: '<unreadable>'});
                            }
                        }
                    });
                    send({type: 'status', message: 'File hooks installed'});
                } catch (e) {
                    send({type: 'error', message: "Failed to attach to open/openat: " + String(e)});
                }
            }
        }
    """,
}


def _get_device(device_id: Optional[str]) -> frida.core.Device:
    return frida.get_device(device_id) if device_id else frida.get_local_device()


def _pid_name(device: frida.core.Device, pid: int) -> Optional[str]:
    try:
        for p in device.enumerate_processes():
            if p.pid == pid:
                return p.name
    except Exception:
        return None
    return None


def _detect_install_error(messages: List[Dict[str, Any]]) -> Optional[str]:
    """
    Determina si el script reportó error (payload.type == 'error') o si Frida envió un error.
    Devuelve un string con el error si existe.
    """
    for m in messages:
        # Errores del runtime de Frida
        if m.get("type") == "error":
            return m.get("description") or m.get("error") or "Unknown Frida script error"

        # Mensajes enviados desde send(...)
        if m.get("type") == "send":
            payload = m.get("payload", {})
            if isinstance(payload, dict) and payload.get("type") == "error":
                return payload.get("message") or "Hook script reported an error"

    return None


def create_simple_hook(
    process_id: int,
    hook_type: str,
    device_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Crea un hook sencillo en un proceso usando Frida.

    Semántica:
    - success/installed = True sólo si el hook quedó instalado (no basta con que el script cargue).
    - Si el hook no aplica (p.ej. Windows), se devuelve un mensaje claro.
    """
    if hook_type not in _HOOK_SCRIPTS:
        return {
            "success": False,
            "installed": False,
            "error": f"Unsupported hook_type '{hook_type}'. Supported: {sorted(_HOOK_SCRIPTS.keys())}",
        }

    device = _get_device(device_id)

    diag: Dict[str, Any] = {
        "process_id": process_id,
        "device_id": device_id,
        "hook_type": hook_type,
    }

    try:
        procs = device.enumerate_processes()
        diag["enumerate_count"] = len(procs)
        diag["pid_found_in_enumerate"] = any(p.pid == process_id for p in procs)
        diag["pid_name"] = _pid_name(device, process_id)
    except Exception:
        diag["enumerate_count"] = None
        diag["pid_found_in_enumerate"] = None
        diag["pid_name"] = None

    session = None
    script = None
    messages: List[Dict[str, Any]] = []

    try:
        session = device.attach(process_id)
        diag["attach_ok"] = True
    except Exception as e:  # noqa: BLE001
        diag["attach_ok"] = False
        return {"success": False, "installed": False, "error": str(e), "diagnostic": diag}

    try:
        js = _HOOK_SCRIPTS[hook_type]
        script = session.create_script(js)

        def on_message(message, data):  # noqa: ARG001
            messages.append(message)

        script.on("message", on_message)
        script.load()

        # pequeño delay para recibir mensajes inmediatos (status/error)
        time.sleep(0.20)

        diag["messages_after_load"] = messages

        install_error = _detect_install_error(messages)
        installed = install_error is None
        success = installed

        result: Dict[str, Any] = {
            "success": success,
            "installed": installed,
            "messages": messages,
            "diagnostic": diag,
        }
        if install_error:
            result["error"] = install_error

        return {"result": result}

    except Exception as e:  # noqa: BLE001
        return {
            "result": {
                "success": False,
                "installed": False,
                "error": str(e),
                "messages": messages,
                "diagnostic": diag,
            }
        }
    finally:
        try:
            if script is not None:
                script.unload()
        except Exception:
            pass
        try:
            if session is not None:
                session.detach()
        except Exception:
            pass
