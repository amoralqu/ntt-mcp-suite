import asyncio
import json
from pathlib import Path
from typing import Any, Optional

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


# Procesos preferidos según plataforma
ANDROID_PROCESS_CANDIDATES = [
    "system_server",
    "zygote64",
    "zygote",
    "audioserver",
    "surfaceflinger",
    "servicemanager",
    "hwservicemanager",
    "logd",
]

LOCAL_PROCESS_BLACKLIST = {"idle", "system", "registry", "init"}


# -------------------------
# Helpers MCP
# -------------------------
def _pick_text(result) -> str:
    if not getattr(result, "content", None):
        return ""
    first = result.content[0]
    if isinstance(first, types.TextContent):
        return first.text
    return str(first)


def _structured(result) -> Any:
    if hasattr(result, "structuredContent"):
        return result.structuredContent
    if hasattr(result, "structured_content"):
        return result.structured_content
    return None


def _unwrap_result(value: Any) -> Any:
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


def pick_device(devices: list[dict]) -> dict:
    # Preferimos Android USB
    for d in devices:
        if d.get("type") == "usb":
            return d
    # Fallback a local
    for d in devices:
        if d.get("id") == "local":
            return d
    raise RuntimeError("No suitable device found")


def pick_process(processes: list[dict], is_android: bool) -> Optional[dict]:
    by_name = {}
    for p in processes:
        name = p.get("name")
        if name and name not in by_name:
            by_name[name] = p

    if is_android:
        for cand in ANDROID_PROCESS_CANDIDATES:
            if cand in by_name:
                return by_name[cand]

    # fallback genérico
    for p in processes:
        pid = p.get("pid")
        name = (p.get("name") or "").lower()
        if isinstance(pid, int) and pid > 1 and name not in LOCAL_PROCESS_BLACKLIST:
            return p

    return None


# -------------------------
# Main
# -------------------------
async def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    venv_python = repo_root / ".venv" / "Scripts" / "python.exe"

    server_params = StdioServerParameters(
        command=str(venv_python),
        args=["-m", "ntt_frida_mcp.server.main"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("\n== health_check ==")
            print(await call_tool(session, "health_check", {}))

            print("\n== enumerate_devices ==")
            devices = await call_tool(session, "enumerate_devices", {})
            print(json.dumps(devices, indent=2, ensure_ascii=False))

            device = pick_device(devices)
            device_id = device["id"]
            is_android = device["type"] == "usb"

            print(f"\n== USING DEVICE ==\nID: {device_id}\nTYPE: {device['type']}")

            print("\n== enumerate_processes ==")
            processes = await call_tool(
                session,
                "enumerate_processes",
                {"device_id": None if device_id == "local" else device_id},
            )
            print(json.dumps(processes[:20], indent=2, ensure_ascii=False))
            print(f"... total: {len(processes)}")

            target = pick_process(processes, is_android)
            if not target:
                raise RuntimeError("No suitable target process found")

            pid = target["pid"]
            name = target.get("name")
            print(f"\n== TARGET ==\nPID: {pid}\nNAME: {name}")

            print("\n== create_interactive_session ==")
            sess = await call_tool(
                session,
                "create_interactive_session",
                {"process_id": pid, "device_id": None if device_id == "local" else device_id},
            )
            print(json.dumps(sess, indent=2, ensure_ascii=False))

            session_id = sess["session_id"]

            print("\n== execute_in_session ==")
            result = await call_tool(
                session,
                "execute_in_session",
                {
                    "session_id": session_id,
                    "javascript_code": (
                        "JSON.stringify({"
                        "pid: Process.id, "
                        "platform: Process.platform, "
                        "arch: Process.arch"
                        "})"
                    ),
                },
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))

            print("\n== close_interactive_session ==")
            close = await call_tool(
                session,
                "close_interactive_session",
                {"session_id": session_id},
            )
            print(json.dumps(close, indent=2, ensure_ascii=False))

            print("\n[OK] Manual MCP test completed successfully.")
            return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
