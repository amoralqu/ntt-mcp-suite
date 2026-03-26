#!/usr/bin/env python3
"""
Script de prueba manual para el servidor MCP de Burp Suite.
"""
import asyncio
import sys
from pathlib import Path

# Añadir el directorio src al path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Función principal de prueba."""
    print("=== Test Manual: NTT Burp Suite MCP ===\n")
    
    # Parámetros del servidor
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "ntt_burp_mcp.server.main"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar la sesión
            await session.initialize()
            
            print("✓ Servidor MCP de Burp Suite iniciado correctamente\n")
            
            # Listar herramientas disponibles
            tools = await session.list_tools()
            print(f"Herramientas disponibles ({len(tools.tools)}):")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()
            
            # Test 1: Health check
            print("--- Test 1: Health Check ---")
            try:
                result = await session.call_tool("health_check", {})
                print(f"✓ Health check: {result.content}")
            except Exception as e:
                print(f"✗ Error en health check: {e}")
            print()
            
            # Test 2: Obtener configuración del proxy
            print("--- Test 2: Obtener configuración del proxy ---")
            try:
                result = await session.call_tool("get_proxy_config", {})
                print(f"✓ Configuración del proxy obtenida")
                print(f"  Respuesta: {result.content}")
            except Exception as e:
                print(f"✗ Error al obtener configuración del proxy: {e}")
            print()
            
            # Test 3: Obtener historial del proxy (limitado)
            print("--- Test 3: Obtener historial del proxy ---")
            try:
                result = await session.call_tool("get_proxy_history", {"limit": 10})
                print(f"✓ Historial del proxy obtenido")
                print(f"  Respuesta: {result.content}")
            except Exception as e:
                print(f"✗ Error al obtener historial del proxy: {e}")
            print()
            
            # Nota: Los siguientes tests requieren que Burp Suite esté ejecutándose
            # con la API REST habilitada
            print("\n=== Notas ===")
            print("• Para utilizar completamente este servidor MCP, necesitas:")
            print("  1. Burp Suite Professional con la REST API habilitada")
            print("  2. Configurar BURP_API_URL (por defecto: http://127.0.0.1:1337)")
            print("  3. Configurar BURP_API_KEY si es necesario")
            print("\n• Herramientas disponibles:")
            print("  - Scanner: start_scan, get_scan_status, get_scan_issues, stop_scan, get_scan_metrics")
            print("  - Proxy: get_proxy_history, get_proxy_item, send_to_repeater, send_to_intruder")
            print("  - Config: get_proxy_config, update_proxy_config")


if __name__ == "__main__":
    asyncio.run(main())
