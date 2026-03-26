# src/ntt_burp_mcp/config.py
from __future__ import annotations
import logging
import os

# Nombre del servidor MCP (usado por FastMCP)
MCP_SERVER_NAME: str = os.environ.get("NTT_BURP_MCP_NAME", "ntt-burp-mcp")

# Configuración de Burp Suite
BURP_API_URL: str = os.environ.get("BURP_API_URL", "http://127.0.0.1:1337")
BURP_API_KEY: str | None = os.environ.get("BURP_API_KEY", None)

# Timeouts / configuración
REQUEST_TIMEOUT_SECONDS: int = int(os.environ.get("NTT_REQUEST_TIMEOUT", "30"))

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("ntt_burp_mcp")
