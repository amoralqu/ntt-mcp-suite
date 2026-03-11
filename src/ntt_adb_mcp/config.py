# src/ntt_adb_mcp/config.py
from __future__ import annotations
import logging
import os

# Nombre del servidor MCP (usado por FastMCP)
MCP_SERVER_NAME: str = os.environ.get("NTT_ADB_MCP_NAME", "ntt-adb-mcp")

# Timeouts / configuración
COMMAND_TIMEOUT_SECONDS: int = int(os.environ.get("NTT_ADB_TIMEOUT", "30"))
ADB_PATH: str | None = os.environ.get("ADB_PATH", "adb")  # Default to 'adb' in PATH

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("ntt_adb_mcp")
