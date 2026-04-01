# NTT Nuclei MCP Server

Servidor MCP para la herramienta de escaneo de vulnerabilidades Nuclei.

## Requisitos Previos

- Python 3.8 o superior
- Nuclei instalado en el sistema
- Conexión a Internet (para actualizar templates)

## Instalación de Nuclei

### Opción 1: Instalación con Go (Recomendada)

Si tienes Go instalado:

```cmd
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

El binario se instalará en `%USERPROFILE%\go\bin\nuclei.exe`

### Opción 2: Descarga Directa

1. Ve a la página de releases de Nuclei:
   https://github.com/projectdiscovery/nuclei/releases/latest

2. Descarga el archivo para Windows:
   `nuclei_3.x.x_windows_amd64.zip`

3. Extrae el archivo y mueve `nuclei.exe` a una ubicación en tu PATH, por ejemplo:
   - `C:\Program Files\nuclei\nuclei.exe`
   - `C:\tools\nuclei\nuclei.exe`

4. Agrega la ubicación al PATH de Windows:
   ```cmd
   setx PATH "%PATH%;C:\Program Files\nuclei"
   ```

### Opción 3: Usando Chocolatey (si lo tienes instalado)

```cmd
choco install nuclei
```

### Verificar Instalación

Abre una nueva terminal y ejecuta:

```cmd
nuclei -version
```

Deberías ver algo como:
```
Nuclei Engine Version: v3.x.x
```

## Configuración Inicial de Nuclei

### 1. Actualizar Templates

Después de instalar Nuclei, actualiza los templates:

```cmd
nuclei -update-templates
```

Esto descargará los templates oficiales en:
`%USERPROFILE%\.nuclei-templates\`

### 2. Verificar Templates

Lista los templates disponibles:

```cmd
nuclei -tl
```

## Configuración del MCP Server

### 1. Instalar Dependencias del Proyecto

Asegúrate de estar en el directorio del proyecto y tener el entorno virtual activado:

```cmd
cd c:\AND\CiberSeguridad\MCP\mcp-server\ntt-mcp-suite
.venv\Scripts\activate
pip install -e .
```

### 2. Configurar Variables de Entorno en mcp.json

Edita `.vscode/mcp.json` y ajusta las variables según tu instalación:

```json
{
  "servers": {
    "ntt-nuclei-mcp": {
      "type": "stdio",
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
      "args": ["-m", "ntt_nuclei_mcp.server.main"],
      "env": {
        "NUCLEI_PATH": "nuclei",
        "NUCLEI_TEMPLATES_PATH": "",
        "NUCLEI_TIMEOUT": "300"
      }
    }
  }
}
```

#### Variables de Entorno Disponibles:

- **NUCLEI_PATH**: Ruta al ejecutable de nuclei
  - Si está en el PATH: `"nuclei"`
  - Ruta completa: `"C:\\Program Files\\nuclei\\nuclei.exe"`
  - Con Go: `"C:\\Users\\TuUsuario\\go\\bin\\nuclei.exe"`

- **NUCLEI_TEMPLATES_PATH**: (Opcional) Ruta a templates personalizados
  - Por defecto usa los templates oficiales
  - Ejemplo: `"C:\\custom-templates\\"`

- **NUCLEI_TIMEOUT**: Timeout en segundos para los escaneos
  - Por defecto: `300` (5 minutos)
  - Ajusta según tus necesidades

### 3. Probar el Servidor MCP

Crea un script de prueba `scripts/manual_mcp_test_client_nuclei.py`:

```python
#!/usr/bin/env python3
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "ntt_nuclei_mcp.server.main"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test 1: Health check
            print("\n=== Test 1: Health Check ===")
            result = await session.call_tool("health_check", {})
            print(json.dumps(result.content, indent=2))
            
            # Test 2: Get Nuclei version
            print("\n=== Test 2: Get Nuclei Version ===")
            result = await session.call_tool("get_nuclei_version", {})
            print(json.dumps(result.content, indent=2))
            
            # Test 3: List templates (primeros 10)
            print("\n=== Test 3: List Templates ===")
            result = await session.call_tool("list_templates", {
                "severity": "critical"
            })
            print(json.dumps(result.content, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
```

Ejecuta el script:

```cmd
python scripts\manual_mcp_test_client_nuclei.py
```

## Herramientas Disponibles

### 1. run_nuclei_scan

Ejecuta un escaneo con Nuclei:

```python
result = await session.call_tool("run_nuclei_scan", {
    "target": "https://example.com",
    "severity": "critical,high",
    "tags": "cve",
    "rate_limit": 150
})
```

Parámetros:
- `target` (requerido): URL o IP del objetivo
- `templates` (opcional): Templates específicos (ej: "cves/", "vulnerabilities/")
- `severity` (opcional): Filtrar por severidad (info, low, medium, high, critical)
- `tags` (opcional): Filtrar por tags
- `exclude_tags` (opcional): Excluir templates con estos tags
- `timeout` (opcional): Timeout en segundos
- `rate_limit` (opcional): Límite de requests por segundo
- `additional_args` (opcional): Lista de argumentos adicionales

### 2. list_templates

Lista templates disponibles:

```python
result = await session.call_tool("list_templates", {
    "severity": "high",
    "tags": "wordpress"
})
```

### 3. update_templates

Actualiza los templates de Nuclei:

```python
result = await session.call_tool("update_templates", {})
```

### 4. get_nuclei_version

Obtiene información de la versión instalada:

```python
result = await session.call_tool("get_nuclei_version", {})
```

## Ejemplos de Uso

### Escaneo Básico

```python
# Escanear un sitio web con templates por defecto
result = await session.call_tool("run_nuclei_scan", {
    "target": "https://testsite.com"
})
```

### Escaneo por Severidad

```python
# Solo vulnerabilidades críticas y altas
result = await session.call_tool("run_nuclei_scan", {
    "target": "https://testsite.com",
    "severity": "critical,high"
})
```

### Escaneo de CVEs

```python
# Buscar CVEs conocidos
result = await session.call_tool("run_nuclei_scan", {
    "target": "https://testsite.com",
    "templates": "cves/",
    "rate_limit": 100
})
```

### Escaneo con Tags Específicos

```python
# Escanear vulnerabilidades de Apache
result = await session.call_tool("run_nuclei_scan", {
    "target": "https://testsite.com",
    "tags": "apache",
    "severity": "medium,high,critical"
})
```

## Troubleshooting

### Error: "nuclei: command not found"

**Solución**: Asegúrate de que nuclei esté en el PATH o especifica la ruta completa en `NUCLEI_PATH`:

```json
"env": {
    "NUCLEI_PATH": "C:\\Program Files\\nuclei\\nuclei.exe"
}
```

### Error: "Failed to update templates"

**Solución**: 
1. Verifica tu conexión a Internet
2. Actualiza manualmente desde la terminal:
   ```cmd
   nuclei -update-templates
   ```

### Timeout en Escaneos

**Solución**: Aumenta el timeout en la configuración:

```json
"env": {
    "NUCLEI_TIMEOUT": "600"
}
```

O especifica el timeout en la llamada:

```python
result = await session.call_tool("run_nuclei_scan", {
    "target": "https://testsite.com",
    "timeout": 600
})
```

### Rate Limiting

Si recibes errores de rate limiting del servidor objetivo:

```python
result = await session.call_tool("run_nuclei_scan", {
    "target": "https://testsite.com",
    "rate_limit": 50  # Reducir requests por segundo
})
```

## Consideraciones de Seguridad

⚠️ **IMPORTANTE**:
- Solo escanea objetivos autorizados
- Nuclei puede generar mucho tráfico de red
- Algunos escaneos pueden ser detectados por WAFs/IDS
- Respeta los términos de servicio de los sitios web
- Usa rate limiting apropiado para evitar sobrecargar objetivos

## Recursos Adicionales

- [Documentación oficial de Nuclei](https://docs.projectdiscovery.io/tools/nuclei/overview)
- [Templates de Nuclei](https://github.com/projectdiscovery/nuclei-templates)
- [Comunidad de ProjectDiscovery](https://discord.gg/projectdiscovery)

## Logs y Debugging

Para ver logs detallados, configura el nivel de log:

```json
"env": {
    "LOG_LEVEL": "DEBUG"
}
```

Los logs se mostrarán en la salida estándar del servidor MCP.
