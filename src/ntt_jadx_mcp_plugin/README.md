# ntt_jadx_mcp_plugin

Plugin para JADX GUI que expone una API REST local para el MCP Server de análisis de vulnerabilidades de NTT.

## Estructura del proyecto

```
ntt_jadx_mcp_plugin/
├── build.gradle.kts
├── settings.gradle.kts
└── src/main/
    ├── java/com/ntt/jadxmcp/
    │   ├── NttJadxMcpPlugin.java   ← Punto de entrada del plugin
    │   ├── NttMcpServer.java       ← Servidor HTTP en puerto 37860
    │   └── NttApiHandler.java      ← Endpoints de la API REST
    └── resources/
        └── jadx-plugin.properties  ← Declaración del plugin
```

## Endpoints disponibles

| Endpoint | Parámetros | Descripción |
|---|---|---|
| `GET /list-classes` | — | Lista todas las clases del APK |
| `GET /get-current-class` | — | Clase activa en el editor de JADX GUI |
| `GET /get-class-code` | `?name=<className>` | Código descompilado de una clase |
| `GET /get-method` | `?class=<className>&method=<methodName>` | Código de un método específico |
| `GET /search` | `?q=<term>` | Busca un término en el código |

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Windows - Recomendado)
```bash
compilar-e-instalar.bat
```

Este script hará todo automáticamente:
- ✅ Verificar dependencias (Java, Gradle)
- ✅ Compilar el plugin
- ✅ Instalar en JADX
- ✅ Verificar la instalación

### Opción 2: Scripts Separados (Windows)
```bash
# Paso 1: Compilar
compilar.bat

# Paso 2: Instalar
instalar.bat
```

### Opción 3: Comandos Manuales

**Compilar:**
```bash
# Si tienes Gradle Wrapper:
gradlew.bat jar  # Windows
./gradlew jar    # Linux/macOS

# Si usas Gradle directamente:
gradle jar
```

El JAR se genera en: `build/libs/ntt_jadx_mcp_plugin-1.0.0.jar`

**Instalar:**
```bash
# Windows
mkdir %APPDATA%\jadx\plugins
copy build\libs\ntt_jadx_mcp_plugin-1.0.0.jar %APPDATA%\jadx\plugins\

# Linux / macOS
mkdir -p ~/.jadx/plugins
cp build/libs/ntt_jadx_mcp_plugin-1.0.0.jar ~/.jadx/plugins/
```

**Reiniciar JADX GUI** tras la instalación.

## 📋 Requisitos Previos

- **Java JDK 11+** - [Descargar](https://adoptium.net/)
- **Gradle** - [Descargar](https://gradle.org/releases/) o instalar con:
  - Chocolatey: `choco install gradle`
  - Scoop: `scoop install gradle`
- **JADX GUI** instalado

📖 **Guía detallada:** Ver [INSTALACION.md](INSTALACION.md) para instrucciones completas y solución de problemas.

## Versión JADX requerida

Ajusta la dependencia en `build.gradle.kts` a la versión exacta de JADX que tengas instalada:

```kotlin
compileOnly("io.github.skylot:jadx-core:1.5.0") // <- cambia aquí
```
