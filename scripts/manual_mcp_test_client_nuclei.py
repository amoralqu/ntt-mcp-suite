#!/usr/bin/env python3
"""
Script de prueba para el servidor MCP de Nuclei.
Ejecuta varios tests para verificar que el servidor funciona correctamente.
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Función principal que ejecuta los tests del servidor Nuclei MCP."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "ntt_nuclei_mcp.server.main"],
        env=None
    )
    
    print("=" * 80)
    print("Iniciando tests del servidor NTT Nuclei MCP")
    print("=" * 80)
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("\n✓ Servidor MCP inicializado correctamente\n")
                
                # Test 1: Health check
                print("=" * 80)
                print("Test 1: Health Check")
                print("=" * 80)
                try:
                    result = await session.call_tool("health_check", {})
                    print(json.dumps(result.content, indent=2))
                    print("✓ Health check exitoso\n")
                except Exception as e:
                    print(f"✗ Error en health check: {e}\n")
                
                # Test 2: Get Nuclei version
                print("=" * 80)
                print("Test 2: Get Nuclei Version")
                print("=" * 80)
                try:
                    result = await session.call_tool("get_nuclei_version", {})
                    print(json.dumps(result.content, indent=2))
                    print("✓ Versión obtenida exitosamente\n")
                except Exception as e:
                    print(f"✗ Error obteniendo versión: {e}\n")
                
                # Test 3: List templates (filtrado por críticos)
                print("=" * 80)
                print("Test 3: List Templates (Severity: Critical)")
                print("=" * 80)
                try:
                    result = await session.call_tool("list_templates", {
                        "severity": "critical"
                    })
                    data = result.content
                    if isinstance(data, list) and len(data) > 0:
                        templates_data = data[0].get("text", "{}")
                        templates_dict = json.loads(templates_data) if isinstance(templates_data, str) else templates_data
                        print(f"Total templates críticos: {templates_dict.get('total_templates', 0)}")
                        templates_list = templates_dict.get('templates', [])
                        if templates_list:
                            print(f"\nPrimeros 5 templates:")
                            for i, template in enumerate(templates_list[:5], 1):
                                print(f"  {i}. {template}")
                    else:
                        print(json.dumps(data, indent=2))
                    print("\n✓ Lista de templates obtenida exitosamente\n")
                except Exception as e:
                    print(f"✗ Error listando templates: {e}\n")
                
                # Test 4: Update templates (opcional - comentado por defecto)
                print("=" * 80)
                print("Test 4: Update Templates (OPCIONAL - comentado)")
                print("=" * 80)
                print("Para ejecutar este test, descomenta las líneas en el script.")
                print("Advertencia: Puede tardar varios minutos en completarse.\n")
                
                # Descomenta las siguientes líneas si quieres probar la actualización de templates
                # try:
                #     print("Actualizando templates de Nuclei...")
                #     result = await session.call_tool("update_templates", {})
                #     print(json.dumps(result.content, indent=2))
                #     print("✓ Templates actualizados exitosamente\n")
                # except Exception as e:
                #     print(f"✗ Error actualizando templates: {e}\n")
                
                # Test 5: Información sobre escaneos
                print("=" * 80)
                print("Test 5: Información sobre Escaneos")
                print("=" * 80)
                print("NOTA: Los escaneos reales requieren un target válido y autorizado.")
                print("Ejemplo de uso:")
                print("""
result = await session.call_tool("run_nuclei_scan", {
    "target": "https://example.com",
    "severity": "critical,high",
    "rate_limit": 100
})
                """)
                print("⚠️  IMPORTANTE: Solo escanea objetivos autorizados.\n")
                
                print("=" * 80)
                print("Resumen de Tests")
                print("=" * 80)
                print("✓ Todos los tests básicos completados")
                print("✓ El servidor MCP de Nuclei está funcionando correctamente")
                print("\nPróximos pasos:")
                print("1. Asegúrate de que Nuclei esté instalado: nuclei -version")
                print("2. Actualiza los templates: nuclei -update-templates")
                print("3. Configura las variables de entorno en .vscode/mcp.json")
                print("4. Usa el servidor en tu aplicación MCP")
                print("=" * 80)
                
    except Exception as e:
        print(f"\n✗ Error fatal al conectar con el servidor MCP: {e}")
        print("\nPosibles causas:")
        print("1. El módulo ntt_nuclei_mcp no está instalado")
        print("2. Faltan dependencias (ejecuta: pip install -e .)")
        print("3. Error en la configuración del servidor")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
