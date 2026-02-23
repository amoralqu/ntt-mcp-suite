import asyncio
import json
import os
from pathlib import Path
from typing import Any, Optional

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


# -------------------------
# Helpers MCP (robustos)
# -------------------------
def _pick_text(result) -> str:
    if not getattr(result, "content", None):
        return ""
    first = result.content[0]
    if isinstance(first, types.TextContent):
        return first.text
    return str(first)


def _structured(result) -> Any:
    # Compatibilidad entre versiones (camelCase vs snake_case)
    if hasattr(result, "structuredContent"):
        return result.structuredContent
    if hasattr(result, "structured_content"):
        return result.structured_content
    return None


def _unwrap_result(value: Any) -> Any:
    """
    Muchos tools responden {"result": ...} o directamente algo.
    Normalizamos.
    """
    if isinstance(value, dict) and "result" in value and len(value) == 1:
        return value["result"]
    return value


async def call_tool(session: ClientSession, name: str, args: dict) -> Any:
    res = await session.call_tool(name, arguments=args)

    sc = _structured(res)
    if sc is not None:
        return _unwrap_result(sc)

    txt = _pick_text(res)
    try:
        return _unwrap_result(json.loads(txt))
    except Exception:
        return txt


def _pp(title: str, data: Any) -> None:
    print(f"\n== {title} ==")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(str(data))


def _is_error(obj: Any) -> bool:
    """
    Detecta errores tanto si vienen como dict {"error": ...}
    como si el cliente devuelve un string "Error executing tool ...".
    """
    if isinstance(obj, dict):
        return ("error" in obj) or (obj.get("ok") is False)
    if isinstance(obj, str):
        s = obj.strip().lower()
        return (
            s.startswith("error executing tool")
            or "server error" in s
            or "500 server error" in s
            or "http error" in s
            or "traceback" in s
        )
    return False


def _extract_class_name(fetch_current: Any) -> Optional[str]:
    """
    El plugin puede devolver varios formatos. Intentamos:
    - {"class_name": "..."} / {"className": "..."} / {"name": "..."} / {"class": "..."}
    - o anidado.
    """
    if not isinstance(fetch_current, dict):
        return None

    for key in ("class_name", "className", "name", "class", "fullName", "full_name"):
        v = fetch_current.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()

    c = fetch_current.get("class")
    if isinstance(c, dict):
        for key in ("name", "class_name", "className", "fullName", "full_name"):
            v = c.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()

    return None


def _extract_items_list(paginated: Any) -> list[str]:
    """
    Soporta:
    - formato PaginationUtils: {"items":[...], ...}
    - formato raw: {"classes":[...]} o {"files":[...]}
    """
    if not isinstance(paginated, dict):
        return []

    for key in ("items", "classes", "files"):
        v = paginated.get(key)
        if isinstance(v, list):
            return [x for x in v if isinstance(x, str) and x.strip()]

    return []


# -------------------------
# Selección de resource "seguro"
# -------------------------
_TEXT_EXTS = (
    ".xml", ".json", ".txt", ".properties", ".js", ".html", ".htm", ".css",
    ".proto", ".md", ".csv", ".yml", ".yaml"
)

_DENY_PREFIXES = (
    "meta-inf/",
    "lib/",
)

_DENY_CONTAINS = (
    "/dexopt/",      # baseline.prof, etc.
    "global-metadata.dat",
)

_DENY_EXTS = (
    ".dex",
    ".so",
    ".prof",
    ".bin",
    ".dat",
    ".arsc",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
)


def _is_good_resource(path: str) -> bool:
    p = path.strip()
    if not p:
        return False
    low = p.replace("\\", "/").lower()

    for pref in _DENY_PREFIXES:
        if low.startswith(pref):
            return False

    for token in _DENY_CONTAINS:
        if token in low:
            return False

    for ext in _DENY_EXTS:
        if low.endswith(ext):
            return False

    # Evitar clases*.dex explícitamente aunque ya cae en .dex
    if low.startswith("classes") and low.endswith(".dex"):
        return False

    # Aceptar res/* siempre, y assets/* solo si es texto
    if low.startswith("res/"):
        return True
    if low.startswith("assets/"):
        return low.endswith(_TEXT_EXTS)

    # Otros archivos sueltos (ej: billing.properties, *.proto) -> permitir si texto
    return low.endswith(_TEXT_EXTS)


def _pick_preferred_resource(paths: list[str]) -> Optional[str]:
    """
    Prioridad:
    1) res/*
    2) assets/* (texto)
    3) otros archivos de texto (p.ej. *.properties, *.proto) fuera de META-INF/lib
    """
    if not paths:
        return None

    # 1) res/*
    for p in paths:
        if p.lower().startswith("res/") and _is_good_resource(p):
            return p

    # 2) assets/*
    for p in paths:
        if p.lower().startswith("assets/") and _is_good_resource(p):
            return p

    # 3) cualquier texto permitido
    for p in paths:
        if _is_good_resource(p):
            return p

    return None


async def list_tools(session: ClientSession) -> list[str]:
    tools = await session.list_tools()
    names = [t.name for t in tools.tools]  # type: ignore[attr-defined]
    print("\n== TOOLS DISPONIBLES ==")
    for n in names:
        print(f"- {n}")
    return names


# -------------------------
# Main test flow
# -------------------------
async def main() -> int:
    """
    Contexto asumido:
    - JADX GUI abierto con un APK cargado
    - Plugin JADX AI MCP Server activo y escuchando en 127.0.0.1:8650
    - Validamos tools críticas: get_class_source y get_resource_file
    """
    repo_root = Path(__file__).resolve().parents[1]
    venv_python = repo_root / ".venv" / "Scripts" / "python.exe"

    env = os.environ.copy()
    env.setdefault("NTT_JADX_PORT", "8650")

    server_params = StdioServerParameters(
        command=str(venv_python),
        args=["-m", "ntt_jadx_mcp.server.main"],
        env=env,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            await list_tools(session)

            # 1) Health check (server + plugin)
            hc = await call_tool(session, "health_check", {})
            _pp("health_check", hc)

            plugin_ok = isinstance(hc, dict) and hc.get("plugin", {}).get("ok") is True
            if not plugin_ok:
                print(
                    "\n[ERROR] El plugin de JADX no parece accesible.\n"
                    "Asegúrate de que:\n"
                    "- JADX GUI está abierto\n"
                    "- el plugin JADX AI MCP Server está activo\n"
                    "- puerto correcto (NTT_JADX_PORT=8650)\n"
                )
                return 2

            # 2) fetch_current_class (puede ser clase o resource abierto en GUI)
            current = await call_tool(session, "fetch_current_class", {})
            _pp("fetch_current_class", current)

            class_name = _extract_class_name(current)
            if not class_name:
                print(
                    "\n[WARN] No pude extraer el nombre de clase desde fetch_current_class "
                    "(name vacío o formato distinto). Haré fallback a get_all_classes."
                )

                classes = await call_tool(session, "get_all_classes", {"offset": 0, "count": 50})
                _pp("get_all_classes (offset=0,count=50)", classes)

                class_candidates = _extract_items_list(classes)
                if not class_candidates:
                    print(
                        "\n[ERROR] No pude obtener clases desde get_all_classes.\n"
                        "Asegúrate de que el APK esté completamente cargado y decompilado."
                    )
                    return 3

                class_name = class_candidates[0]

            print(f"\n== TARGET CLASS PARA PRUEBAS ==\n{class_name}")

            # 3) get_class_source (tool crítica)
            src = await call_tool(session, "get_class_source", {"class_name": class_name})
            _pp("get_class_source", src)

            if _is_error(src):
                print(
                    "\n[ERROR] get_class_source falló.\n"
                    "Diagnóstico sugerido:\n"
                    "- mismatch de versión del plugin (endpoint/params)\n"
                    "- decompilación aún no completa\n"
                )
                return 4

            # 4) List resources (y escoger uno "seguro" en vez de META-INF)
            resources = await call_tool(session, "get_all_resource_file_names", {"offset": 0, "count": 500})
            _pp("get_all_resource_file_names (offset=0,count=500)", resources)

            resource_candidates = _extract_items_list(resources)
            if not resource_candidates:
                print(
                    "\n[WARN] get_all_resource_file_names devolvió 0 items.\n"
                    "No es fatal, pero no puedo validar get_resource_file."
                )
                return 0

            resource_name = _pick_preferred_resource(resource_candidates)
            if not resource_name:
                print(
                    "\n[WARN] No encontré un resource de texto 'seguro' para probar get_resource_file.\n"
                    "Esto suele pasar si el APK no tiene res/ visibles o assets de texto."
                )
                return 0

            print(f"\n== TARGET RESOURCE PARA PRUEBAS ==\n{resource_name}")

            # 5) get_resource_file (tool crítica)
            rf = await call_tool(session, "get_resource_file", {"resource_name": resource_name})
            _pp("get_resource_file", rf)

            if _is_error(rf):
                print(
                    "\n[ERROR] get_resource_file falló incluso con un resource de texto seleccionado.\n"
                    "Esto sí sugiere revisar:\n"
                    "- compatibilidad endpoint/param en el plugin\n"
                    "- errores internos del plugin para ese file\n"
                )
                return 5

            print("\n[OK] Validación completada: get_class_source y get_resource_file funcionan.")
            return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
