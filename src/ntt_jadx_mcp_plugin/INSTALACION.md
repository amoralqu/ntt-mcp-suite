# Guía de Compilación e Instalación - NTT JADX MCP Plugin

## Requisitos Previos

### 1. Java Development Kit (JDK)
Necesitas JDK 11 o superior instalado.

**Verificar instalación:**
```bash
java -version
javac -version
```

**Si no está instalado:**
- Descarga OpenJDK desde: https://adoptium.net/
- O instala usando Chocolatey (Windows): `choco install openjdk`

### 2. Gradle
Necesitas Gradle para compilar el proyecto.

**Verificar instalación:**
```bash
gradle -v
```

**Si no está instalado:**

**Opción A - Usando Chocolatey (Windows - Recomendado):**
```bash
choco install gradle
```

**Opción B - Descarga manual:**
1. Descarga Gradle desde: https://gradle.org/releases/
2. Descomprime en una carpeta (ej: `C:\gradle`)
3. Añade a la variable PATH: `C:\gradle\bin`

**Opción C - Usando Scoop (Windows):**
```bash
scoop install gradle
```

## Pasos de Compilación

### 1. Navegar al directorio del proyecto
```bash
cd c:/AND/CiberSeguridad/MCP/mcp-server/ntt-mcp-suite/src/ntt_jadx_mcp_plugin
```

### 2. Inicializar Gradle Wrapper (primera vez)
```bash
gradle wrapper --gradle-version 8.5
```

Este comando crea los archivos necesarios para que el proyecto sea auto-contenido.

### 3. Compilar el plugin
```bash
# Si creaste el wrapper:
gradlew.bat jar

# O si usas Gradle directamente:
gradle jar
```

### 4. Verificar la compilación
El archivo JAR debe generarse en:
```
build/libs/ntt_jadx_mcp_plugin-1.0.0.jar
```

## Instalación del Plugin en JADX

### Windows

**Paso 1: Crear directorio de plugins (si no existe)**
```bash
mkdir %APPDATA%\jadx\plugins
```

**Paso 2: Copiar el plugin**
```bash
copy build\libs\ntt_jadx_mcp_plugin-1.0.0.jar %APPDATA%\jadx\plugins\
```

**Ruta completa típica:**
```
C:\Users\TU_USUARIO\AppData\Roaming\jadx\plugins\ntt_jadx_mcp_plugin-1.0.0.jar
```

### Linux / macOS

**Paso 1: Crear directorio de plugins (si no existe)**
```bash
mkdir -p ~/.jadx/plugins
```

**Paso 2: Copiar el plugin**
```bash
cp build/libs/ntt_jadx_mcp_plugin-1.0.0.jar ~/.jadx/plugins/
```

## Verificación de la Instalación

### 1. Reiniciar JADX GUI
Cierra completamente JADX GUI y vuelve a abrirlo.

### 2. Verificar en JADX
- Ve a: **Plugins** → **Installed Plugins**
- Deberías ver: **NTT JADX MCP Plugin v1.0.0**

### 3. Verificar el servidor
Una vez que JADX esté abierto con un APK cargado, el servidor HTTP debería estar corriendo en:
```
http://localhost:37860
```

**Probar con curl (si está instalado):**
```bash
curl http://localhost:37860/list-classes
```

**O abre en un navegador:**
```
http://localhost:37860/list-classes
```

## Solución de Problemas

### Error: "plugin-id no coincide"
Verifica que el archivo `jadx-plugin.properties` tenga el plugin-id correcto.

### Error: "NoClassDefFoundError"
- Verifica que la versión de JADX en `build.gradle.kts` coincida con tu versión instalada
- Recompila el plugin después de cambiar la versión

### El servidor no inicia
- Verifica que el puerto 37860 no esté en uso
- Revisa los logs de JADX en la consola

### Plugin no aparece en JADX
- Verifica que el JAR esté en la carpeta correcta
- Verifica permisos del archivo
- Asegúrate de haber reiniciado JADX completamente

## Configuración Avanzada

### Cambiar versión de JADX
Edita `build.gradle.kts`:
```kotlin
compileOnly("io.github.skylot:jadx-core:1.5.0") // <- cambia la versión aquí
```

### Cambiar puerto del servidor
Edita `src/main/java/com/tudominio/jadxmcp/NttMcpServer.java` y busca el puerto 37860.

## Actualización del Plugin

Para actualizar a una nueva versión:

1. Recompila el proyecto
2. Detén JADX GUI
3. Reemplaza el JAR antiguo con el nuevo
4. Reinicia JADX GUI

## Endpoints API Disponibles

Una vez instalado, el plugin expone los siguientes endpoints:

| Endpoint | Método | Parámetros | Descripción |
|----------|--------|------------|-------------|
| `/list-classes` | GET | - | Lista todas las clases del APK |
| `/get-current-class` | GET | - | Obtiene la clase activa en el editor |
| `/get-class-code` | GET | `name=<className>` | Código descompilado de una clase |
| `/get-method` | GET | `class=<className>&method=<methodName>` | Código de un método específico |
| `/search` | GET | `q=<term>` | Busca un término en el código |

## Soporte

Para problemas o consultas, revisa:
- Los logs de JADX GUI
- La consola de Windows donde ejecutaste los comandos
- Verifica que todas las dependencias estén correctamente instaladas
