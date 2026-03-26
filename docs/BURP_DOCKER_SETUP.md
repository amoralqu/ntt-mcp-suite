# Guía de Instalación: Burp Suite 2025 en Docker para Windows

Esta guía explica cómo instalar y configurar Burp Suite 2025 desde `burp2025.tar.gz` usando Docker en Windows, y cómo integrarlo con el servidor MCP.

## Requisitos Previos

### 1. Instalar Docker Desktop para Windows

**Descargar e instalar**:
1. Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop/
2. Ejecuta el instalador
3. Reinicia tu computadora cuando se te solicite
4. Abre Docker Desktop y espera a que inicie completamente

**Verificar instalación**:
```powershell
docker --version
docker-compose --version
```

### 2. Configurar WSL 2 (Windows Subsystem for Linux)

Docker Desktop en Windows usa WSL 2. Asegúrate de tenerlo habilitado:

```powershell
# Ejecutar PowerShell como Administrador
wsl --install
wsl --set-default-version 2
```

## Instalación de Burp Suite 2025

### Paso 1: Preparar el archivo

Supongamos que tienes `burp2025.tar.gz` en `C:\Users\amoralqu\Downloads\`

```powershell
# Navegar a la ubicación del archivo
cd C:\Users\amoralqu\Downloads\

# Descomprimir (puedes usar 7-Zip o tar en PowerShell)
tar -xvf burp2025.tar.gz
```

Esto creará una carpeta `burp2025` con los archivos necesarios.

### Paso 2: Revisar docker-compose.yml

```powershell
cd burp2025
notepad docker-compose.yml
```

**Verifica que el archivo incluya**:
- Mapeo de puertos para la API REST (puerto 1337)
- Mapeo de puertos para la UI web (si aplica)
- Configuración de red adecuada

**Ejemplo de configuración necesaria**:
```yaml
version: '3'
services:
  burp:
    image: burp2025:latest
    ports:
      - "8080:8080"   # Proxy HTTP
      - "1337:1337"   # REST API (IMPORTANTE para MCP)
      - "8000:8000"   # UI Web (si aplica)
    volumes:
      - ./data:/burp/data
    environment:
      - BURP_API_ENABLED=true
```

### Paso 3: Cargar la imagen Docker

Si el archivo incluye una imagen Docker (archivo .tar):

```powershell
# Listar imágenes actuales
docker images

# Si hay imágenes antiguas de Burp, eliminarlas
docker rmi burp2025:latest

# Cargar la nueva imagen (si hay un archivo .tar en la carpeta)
docker load -i burp2025.tar
```

### Paso 4: Iniciar Burp Suite

```powershell
# Desde la carpeta burp2025
docker-compose up
```

**Para ejecutar en segundo plano (detached mode)**:
```powershell
docker-compose up -d
```

**Ver logs en tiempo real**:
```powershell
docker-compose logs -f
```

### Paso 5: Detener Burp Suite

```powershell
# En la carpeta burp2025
docker-compose down
```

## Configuración de la REST API

### Verificar que la API esté activa

Una vez que el contenedor esté corriendo:

```powershell
# Probar la API
curl http://localhost:1337/v0.1/
```

Si obtienes una respuesta JSON, la API está funcionando.

### Si la API no está habilitada por defecto

Necesitarás acceder a la UI de Burp y habilitarla:

1. **Si hay UI web**: Abre `http://localhost:8000` en tu navegador
2. **Si es desktop app**: Conecta al contenedor
   ```powershell
   docker exec -it burp2025_burp_1 bash
   ```

3. Habilitar REST API:
   - Settings > Suite > REST API
   - Enable service ✓
   - Listen on all interfaces: 0.0.0.0:1337

## Configuración del Servidor MCP

### Actualizar mcp.json

El servidor MCP ya está configurado en `.vscode/mcp.json`, pero verifica la URL:

```json
{
  "servers": {
    "ntt-burp-mcp": {
      "type": "stdio",
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
      "args": ["-m", "ntt_burp_mcp.server.main"],
      "env": {
        "BURP_API_URL": "http://localhost:1337",
        "BURP_API_KEY": ""
      }
    }
  }
}
```

### Probar la conexión

```powershell
# Activar el entorno virtual
.\.venv\Scripts\activate

# Ejecutar el script de prueba
python scripts/manual_mcp_test_client_burp.py
```

## Solución de Problemas

### Error: "Cannot connect to the Docker daemon"

**Solución**: Asegúrate de que Docker Desktop esté corriendo.

```powershell
# Iniciar Docker Desktop manualmente o:
"C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

### Error: "Port is already allocated"

**Solución**: Otro servicio está usando el puerto.

```powershell
# Ver qué está usando el puerto 1337
netstat -ano | findstr :1337

# Matar el proceso (reemplaza PID)
taskkill /PID <PID> /F
```

### No puedo conectarme a la API desde Windows

**Posibles causas**:
1. La API no está habilitada en Burp
2. El puerto no está mapeado en docker-compose.yml
3. Firewall de Windows bloqueando la conexión

**Solución**:
```powershell
# Verificar que el contenedor esté corriendo
docker ps

# Verificar logs
docker-compose logs burp

# Probar conectividad
Test-NetConnection localhost -Port 1337
```

### El contenedor se detiene inmediatamente

**Solución**: Ver los logs para identificar el error

```powershell
docker-compose logs
```

## Comandos Útiles

```powershell
# Ver contenedores corriendo
docker ps

# Ver todos los contenedores (incluso detenidos)
docker ps -a

# Ver imágenes
docker images

# Entrar al contenedor
docker exec -it burp2025_burp_1 bash

# Ver uso de recursos
docker stats

# Limpiar contenedores detenidos
docker container prune

# Limpiar imágenes no usadas
docker image prune
```

## Workflow Diario

### Iniciar Burp Suite:
```powershell
cd C:\Users\amoralqu\Downloads\burp2025
docker-compose up -d
```

### Verificar que esté corriendo:
```powershell
docker ps
curl http://localhost:1337/v0.1/
```

### Usar el servidor MCP:
```powershell
cd c:\AND\CiberSeguridad\MCP\mcp-server\ntt-mcp-suite
.\.venv\Scripts\activate
python scripts/manual_mcp_test_client_burp.py
```

### Detener Burp Suite:
```powershell
cd C:\Users\amoralqu\Downloads\burp2025
docker-compose down
```

## Notas Importantes

1. **Docker Desktop debe estar corriendo** antes de usar docker-compose
2. **La REST API debe estar habilitada** en Burp Suite para que el servidor MCP funcione
3. **El puerto 1337 debe estar mapeado** en docker-compose.yml
4. **Desde Windows puedes acceder** al contenedor usando `localhost:1337`
5. **Los datos persisten** si tienes volúmenes configurados en docker-compose.yml

## Próximos Pasos

Una vez que tengas Burp Suite corriendo:

1. Verifica la API: `curl http://localhost:1337/v0.1/`
2. Ejecuta el test del MCP: `python scripts/manual_mcp_test_client_burp.py`
3. Usa las herramientas del MCP desde tu cliente preferido

## Recursos Adicionales

- [Docker Desktop Documentation](https://docs.docker.com/desktop/windows/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Burp Suite REST API Documentation](https://portswigger.net/burp/documentation/desktop/tools/rest-api)
