# 🎯 NTT JADX MCP Plugin - Resumen

## 📋 ¿Qué Construimos?

Un **plugin para JADX GUI** que expone una API REST para que GitHub Copilot pueda analizar automáticamente aplicaciones Android (APKs) mediante el **protocolo MCP (Model Context Protocol)**.

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  GitHub Copilot │ ◄─MCP──►│  MCP Server      │ ◄─HTTP─►│  JADX Plugin    │
│   (VS Code)     │         │  (Python)        │         │  (Java)         │
└─────────────────┘         └──────────────────┘         └─────────────────┘
        │                            │                            │
        │                            │                            │
    Usuario                     FastMCP                     JADX GUI
   pregunta                   47 herramientas              Puerto 8650
                             organizadas                 API REST local
```

---

## 🔧 Componentes Principales

### 1️⃣ **Plugin JADX (Java)** 
📁 `src/ntt_jadx_mcp_plugin/`

**Archivos principales:**
- `NttJadxMcpPlugin.java` - Punto de entrada del plugin
- `NttMcpServer.java` - Servidor HTTP embebido (puerto 8650)
- `NttApiHandler.java` - Maneja 15 endpoints REST

**Función:**
- Se ejecuta **dentro de JADX GUI**
- Expone las clases descompiladas del APK vía API REST
- Inicia automáticamente al cargar JADX

**Herramientas de construcción:**
- ✅ Gradle 9.3.1
- ✅ Java 11+
- ✅ JADX API 1.5.0

---

### 2️⃣ **MCP Server (Python)**
📁 `src/ntt_jadx_mcp/`

**Archivos principales:**
- `server/main.py` - Servidor MCP con FastMCP
- `tools/registry.py` - Registro de 47 herramientas
- `tools/security_tools.py` - 7 herramientas de análisis de seguridad
- `tools/class_tools.py` - Análisis de clases
- `tools/search_tools.py` - Búsqueda en código

**Función:**
- Traduce peticiones de GitHub Copilot a llamadas HTTP al plugin
- Procesa y estructura las respuestas
- Expone herramientas especializadas de análisis

**Herramientas utilizadas:**
- ✅ Python 3.10+
- ✅ FastMCP (framework de Anthropic)
- ✅ httpx (cliente HTTP)

---

## 🔄 Flujo de Interacción

### Ejemplo: Usuario pregunta sobre vulnerabilidades

```
1. Usuario escribe en VS Code:
   "@ntt-jadx-mcp busca vulnerabilidades en el APK"

2. GitHub Copilot detecta el comando MCP

3. MCP Server recibe la solicitud y ejecuta:
   - scan_for_common_vulnerabilities()
   - analyze_crypto_usage()
   - detect_hardcoded_credentials()

4. MCP Server hace peticiones HTTP al plugin:
   GET http://localhost:8650/search-classes-by-keyword?search_term=password

5. Plugin JADX busca en las clases descompiladas

6. Plugin responde con JSON:
   {
     "classes": ["com.app.Login", "com.app.Config"],
     "total": 2
   }

7. MCP Server procesa y estructura la respuesta

8. GitHub Copilot presenta resultados al usuario:
   "🔍 Encontré 2 posibles credenciales hardcodeadas..."
```

---

## 📊 Capacidades del Sistema

### **47 Herramientas MCP Disponibles**

#### 🔍 Análisis de Clases (10 herramientas)
- Listar todas las clases del APK
- Obtener código fuente de una clase
- Analizar métodos y campos
- Obtener código Smali

#### 🔎 Búsqueda (3 herramientas)
- Buscar por palabra clave en código
- Buscar métodos por nombre
- Búsqueda con filtros de paquete

#### 🔒 Análisis de Seguridad (7 herramientas) ⭐ **DESTACADO**
- `scan_for_common_vulnerabilities` - Top 10 vulnerabilidades
- `analyze_permissions_usage` - Permisos peligrosos
- `analyze_crypto_usage` - Algoritmos criptográficos
- `detect_hardcoded_credentials` - Secrets en código
- `find_dangerous_api_usage` - APIs peligrosas
- `find_exported_components` - Componentes expuestos
- `analyze_security_vulnerabilities` - Análisis por categorías

#### 📦 Recursos (4 herramientas)
- Obtener strings.xml
- Listar archivos de recursos
- Obtener contenido de recursos

#### 🔗 Referencias Cruzadas (3 herramientas)
- Xrefs a clases, métodos y campos

#### 🛠️ Refactorización (5 herramientas)
- Renombrar clases, métodos, campos, paquetes

#### 🐛 Debug (3 herramientas)
- Stack frames, threads, variables

---

## 🎨 Innovaciones Técnicas

### 1. **Análisis de Seguridad sin AndroidManifest.xml**
**Problema:** JADX 1.5.0 no expone el manifest fácilmente

**Solución:** Búsqueda de patrones en código descompilado
- En vez de leer permisos del manifest
- Buscamos uso de APIs que requieren permisos
- Ejemplo: Encontrar `LocationManager` = usa permisos de ubicación

### 2. **Servidor HTTP Embebido en Plugin**
- No requiere servidor externo
- Auto-inicia con JADX
- Puerto fijo (8650) para compatibilidad

### 3. **Integración con GitHub Copilot**
- Lenguaje natural → Herramientas MCP → API REST → Resultados
- Usuario no necesita saber sintaxis de API

---

## 📈 Estadísticas del Proyecto

```
📦 Plugin Java:
   - 3 clases principales
   - 15 endpoints REST
   - ~600 líneas de código

🐍 MCP Server Python:
   - 47 herramientas MCP
   - 10 módulos organizados
   - ~2,000 líneas de código

📋 Patrones de Seguridad:
   - 10 categorías de vulnerabilidades
   - 50+ patrones de búsqueda
   - 8 tipos de permisos peligrosos
```

---

## 🚀 Ventajas del Sistema

✅ **Automatización** - Análisis de seguridad automático con IA  
✅ **Integrado** - Funciona directamente en VS Code  
✅ **Extensible** - Fácil agregar nuevas herramientas  
✅ **Sin dependencias externas** - Todo local en localhost  
✅ **Multiplataforma** - Windows, Linux, macOS  
✅ **Open Source** - Basado en protocolos abiertos (MCP)  

---

## 🛠️ Tecnologías Utilizadas

### Backend (Plugin)
- **Java 11+** - Lenguaje del plugin
- **Gradle** - Build system
- **JADX API** - Acceso a clases descompiladas
- **Java HttpServer** - Servidor HTTP embebido

### Middleware (MCP Server)
- **Python 3.10+** - Lenguaje del servidor
- **FastMCP** - Framework MCP de Anthropic
- **httpx** - Cliente HTTP asíncrono
- **asyncio** - Programación asíncrona

### Frontend (Cliente)
- **GitHub Copilot** - IA conversacional
- **VS Code** - IDE con MCP integrado
- **MCP Protocol** - Comunicación estandarizada

---

## 📝 Comandos de Ejemplo

```bash
# Análisis general
@ntt-jadx-mcp lista todas las clases del APK
@ntt-jadx-mcp muestra el código de la clase MainActivity

# Análisis de seguridad
@ntt-jadx-mcp escanea vulnerabilidades comunes
@ntt-jadx-mcp analiza permisos peligrosos
@ntt-jadx-mcp busca credenciales hardcodeadas
@ntt-jadx-mcp qué algoritmos criptográficos usa

# Búsquedas específicas
@ntt-jadx-mcp busca uso de LocationManager
@ntt-jadx-mcp encuentra todas las Activities exportadas
```

---

## 🎓 Casos de Uso

1. **Auditorías de Seguridad**
   - Análisis automatizado de APKs
   - Detección de vulnerabilidades comunes
   - Identificación de malas prácticas

2. **Ingeniería Inversa**
   - Exploración de código descompilado
   - Búsqueda de funcionalidad específica
   - Análisis de estructura de la app

3. **Investigación de Malware**
   - Búsqueda de comportamiento sospechoso
   - Identificación de técnicas de evasión
   - Análisis de APIs maliciosas

4. **Educación**
   - Enseñanza de seguridad en Android
   - Análisis de apps de ejemplo
   - Demostración de vulnerabilidades

---

## 🎯 Conclusión

Construimos un **puente inteligente** entre:
- 🤖 **GitHub Copilot** (IA conversacional)
- 🔧 **JADX** (descompilador Android)
- 🔒 **Análisis de seguridad** (automatizado)

**Resultado:** Análisis de aplicaciones Android usando lenguaje natural, sin necesidad de conocer APIs o comandos complejos.

---

## 📞 Datos Técnicos Clave

- **Puerto:** 8650
- **Protocolo:** MCP (Model Context Protocol)
- **Formato:** REST API + JSON
- **Lenguajes:** Java + Python
- **Frameworks:** Gradle + FastMCP
- **Total herramientas:** 47
- **Herramientas de seguridad:** 7
- **Patrones detectados:** 50+
