# src/ntt_objection_mcp/config.py
from __future__ import annotations
import logging
import os

# Nombre del servidor MCP (usado por FastMCP)
MCP_SERVER_NAME: str = os.environ.get("NTT_OBJECTION_MCP_NAME", "ntt-objection-mcp")

# Timeouts / configuración
SESSION_TIMEOUT_SECONDS: int = int(os.environ.get("NTT_SESSION_TIMEOUT", "3600"))
OBJECTION_DEFAULT_DEVICE: str | None = os.environ.get("OBJECTION_DEVICE_ID", None)

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("ntt_objection_mcp")
