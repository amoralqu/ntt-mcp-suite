# src/ntt_nuclei_mcp/config.py
from __future__ import annotations
import logging
import os

# Nombre del servidor MCP (usado por FastMCP)
MCP_SERVER_NAME: str = os.environ.get("NTT_NUCLEI_MCP_NAME", "ntt-nuclei-mcp")

# Configuración de Nuclei
NUCLEI_PATH: str = os.environ.get("NUCLEI_PATH", "nuclei")
NUCLEI_TEMPLATES_PATH: str | None = os.environ.get("NUCLEI_TEMPLATES_PATH", None)
NUCLEI_TIMEOUT: int = int(os.environ.get("NUCLEI_TIMEOUT", "300"))

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("ntt_nuclei_mcp")
