# NTT Burp Suite MCP Server

Servidor MCP (Model Context Protocol) para interactuar con Burp Suite Professional a través de su REST API.

⚠️ **IMPORTANTE**: Este servidor requiere **Burp Suite Professional o Enterprise Edition**. La REST API NO está disponible en Burp Suite Community Edition.

## Características

Este servidor MCP proporciona herramientas para:

### Scanner
- `start_scan`: Inicia un escaneo de seguridad en una URL objetivo
- `get_scan_status`: Obtiene el estado actual de un escaneo
- `get_scan_issues`: Lista las vulnerabilidades encontradas
- `stop_scan`: Detiene un escaneo en curso
- `get_scan_metrics`: Obtiene métricas detalladas de un escaneo

### Proxy
- `get_proxy_history`: Obtiene el historial de peticiones interceptadas
- `get_proxy_item`: Obtiene detalles de una petición específica
- `send_to_repeater`: Envía una petición al Repeater
- `send_to_intruder`: Envía una petición al Intruder
- `get_proxy_config`: Obtiene la configuración actual del proxy
- `update_proxy_config`: Actualiza la configuración del proxy

## Requisitos

- **Burp Suite Professional o Enterprise Edition** (la REST API NO está disponible en Community Edition)
- REST API de Burp Suite habilitada
- Python 3.8 o superior
- Paquete `requests` instalado

### ¿Por qué no funciona con Burp Suite Community?

Burp Suite Community Edition no incluye la REST API. Esta es una característica exclusiva de las versiones Professional y Enterprise. Si solo tienes acceso a Community Edition, considera:

1. **Usar Burp Suite Professional**: Versión de pago con todas las características (incluye trial de 30 días)
2. **ZAP Proxy**: Alternativa gratuita con API REST completa
3. **Extensiones personalizadas**: Desarrollo más complejo para Community Edition

## Configuración

### Variables de Entorno

El servidor se puede configurar mediante las siguientes variables de entorno:

```bash
# URL de la API REST de Burp Suite (por defecto: http://127.0.0.1:1337)
BURP_API_URL=http://127.0.0.1:1337

# API Key de Burp Suite (opcional)
BURP_API_KEY=tu_api_key_aqui

# Nombre del servidor MCP (por defecto: ntt-burp-mcp)
NTT_BURP_MCP_NAME=ntt-burp-mcp

# Timeout para peticiones HTTP en segundos (por defecto: 30)
NTT_REQUEST_TIMEOUT=30

# Nivel de logging (por defecto: INFO)
LOG_LEVEL=INFO
```

### Configuración en mcp.json

El servidor ya está configurado en `.vscode/mcp.json`:

```json
{
  "servers": {
    "ntt-burp-mcp": {
      "type": "stdio",
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
      "args": ["-m", "ntt_burp_mcp.server.main"],
      "env": {
        "BURP_API_URL": "http://127.0.0.1:1337",
        "BURP_API_KEY": ""
      }
    }
  }
}
```

## Instalación con Docker (Recomendado)

Si tienes Burp Suite 2025 en formato Docker (`burp2025.tar.gz`):

### Requisitos
- Docker Desktop instalado en Windows
- WSL 2 habilitado

### Pasos Rápidos

```powershell
# 1. Descomprimir el archivo
cd C:\Users\amoralqu\Downloads
tar -xvf burp2025.tar.gz

# 2. Iniciar Burp Suite
cd burp2025
docker-compose up -d

# 3. Verificar que esté corriendo
docker ps
curl http://localhost:1337/v0.1/
```

**📖 Guía completa**: Ver `docs/BURP_DOCKER_SETUP.md` para instrucciones detalladas

**🔍 Script de verificación**: Ejecuta `.\scripts\verify_burp_docker_setup.ps1` para verificar toda la configuración

## Habilitar REST API en Burp Suite Professional

⚠️ **Nota**: Estos pasos solo funcionan en Burp Suite Professional o Enterprise Edition.

### Instalación Local
1. Abre Burp Suite Professional
2. Ve a `Settings` (o `User options` en versiones antiguas) > `Suite` > `REST API`
   - En versiones antiguas: `User options` > `Misc` > `REST API`
3. Marca la opción `Enable service`
4. Configura el puerto (por defecto: 1337)
5. Configura la dirección de escucha (por defecto: 127.0.0.1)
6. Opcionalmente, configura una API Key para mayor seguridad en `Keys`

### Instalación Docker
Si usas la versión Docker, asegúrate de:
1. El puerto 1337 esté mapeado en `docker-compose.yml`
2. La REST API esté habilitada (puede estar preconfigurada)
3. El contenedor escuche en `0.0.0.0:1337` para acceso desde el host

**Verificar que la API está activa**:
```bash
curl http://localhost:1337/v0.1/
```

Si obtienes una respuesta JSON, la API está funcionando correctamente.

## Uso

### Prueba Manual

Ejecuta el script de prueba para verificar que el servidor funciona correctamente:

```bash
python scripts/manual_mcp_test_client_burp.py
```

### Ejemplo de Uso

```python
# Iniciar un escaneo
result = await session.call_tool("start_scan", {
    "target_url": "https://example.com",
    "scan_type": "crawl_and_audit"
})

# Obtener el estado del escaneo
status = await session.call_tool("get_scan_status", {
    "scan_id": "scan_id_aqui"
})

# Obtener vulnerabilidades encontradas
issues = await session.call_tool("get_scan_issues", {
    "scan_id": "scan_id_aqui"
})

# Obtener historial del proxy
history = await session.call_tool("get_proxy_history", {
    "limit": 50
})
```

## Arquitectura

```
ntt_burp_mcp/
├── __init__.py              # Inicialización del paquete
├── config.py                # Configuración y variables de entorno
├── README.md                # Este archivo
├── server/
│   ├── __init__.py
│   ├── app.py              # Aplicación FastMCP principal
│   └── main.py             # Punto de entrada del servidor
└── tools/
    ├── __init__.py
    ├── client.py           # Cliente HTTP para la API de Burp
    ├── scanner.py          # Herramientas del scanner
    ├── proxy.py            # Herramientas del proxy
    └── registry.py         # Registro de todas las herramientas
```

## Notas y Limitaciones

- ⚠️ **CRÍTICO**: Este servidor requiere Burp Suite Professional o Enterprise Edition. La REST API NO está disponible en Community Edition
- Asegúrate de que Burp Suite esté ejecutándose antes de usar el servidor MCP
- La API REST de Burp Suite puede variar según la versión, consulta la documentación oficial para más detalles
- Si necesitas una solución gratuita, considera usar ZAP Proxy que tiene API REST sin restricciones

## Alternativas Gratuitas

Si no tienes acceso a Burp Suite Professional, considera:

### OWASP ZAP (Zed Attack Proxy)
- **Gratuito y Open Source**
- API REST completa y documentada
- Funcionalidad similar a Burp Suite
- Descarga: https://www.zaproxy.org/

¿Te gustaría que cree un servidor MCP para ZAP en su lugar?

## Documentación Adicional

- [Burp Suite REST API Documentation](https://portswigger.net/burp/documentation/desktop/tools/rest-api)
- [Model Context Protocol](https://modelcontextprotocol.io/)
