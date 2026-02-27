# 🔒 Análisis de Seguridad - NTT JADX MCP

Este documento explica las herramientas de análisis de seguridad disponibles en el NTT JADX MCP Server.

## 🎯 Herramientas Disponibles

### 1. `scan_for_common_vulnerabilities`
**Escaneo rápido de vulnerabilidades comunes**

Realiza un análisis rápido de las 10 vulnerabilidades más comunes en aplicaciones Android.

**Uso con GitHub Copilot:**
```
@ntt-jadx-mcp escanea vulnerabilidades comunes en el APK
```

**Detecta:**
- SQL Injection
- WebView XSS
- Criptografía insegura
- Contraseñas hardcodeadas
- Debug habilitado
- Conexiones HTTP inseguras
- Detección de root
- Path traversal
- Componentes exportados
- Algoritmos de hash débiles

---

### 2. `analyze_security_vulnerabilities`
**Análisis detallado por categorías**

Analiza el APK buscando patrones específicos de vulnerabilidades agrupados por categoría.

**Uso con GitHub Copilot:**
```
@ntt-jadx-mcp analiza todas las vulnerabilidades de seguridad
@ntt-jadx-mcp busca vulnerabilidades de criptografía débil
```

**Categorías disponibles:**
- `crypto_weak` - Algoritmos criptográficos débiles (DES, MD5, SHA1)
- `hardcoded_secrets` - Secretos hardcodeados
- `insecure_network` - Configuraciones de red inseguras
- `sql_injection` - Vulnerabilidades de SQL injection
- `webview_vulnerabilities` - Problemas de WebView
- `path_traversal` - Vulnerabilidades de path traversal
- `intent_vulnerabilities` - Problemas con Intents
- `debug_logging` - Logs de debug en producción
- `root_detection` - Detección/bypass de root
- `dangerous_permissions` - Uso de permisos peligrosos

---

### 3. `analyze_permissions_usage`
**Análisis de permisos peligrosos**

Busca en el código el uso de APIs que requieren permisos peligrosos de Android.

**Uso con GitHub Copilot:**
```
@ntt-jadx-mcp analiza el uso de permisos peligrosos
@ntt-jadx-mcp qué permisos usa esta aplicación
```

**Permisos analizados:**
- CAMERA - Uso de cámara
- LOCATION - Acceso a ubicación
- STORAGE - Acceso a almacenamiento externo
- CONTACTS - Acceso a contactos
- SMS - Envío/lectura de SMS
- PHONE - Información del teléfono
- MICROPHONE - Grabación de audio
- CALENDAR - Acceso al calendario

---

### 4. `analyze_crypto_usage`
**Análisis de uso criptográfico**

Identifica el uso de criptografía en la aplicación y detecta algoritmos débiles.

**Uso con GitHub Copilot:**
```
@ntt-jadx-mcp analiza el uso de criptografía
@ntt-jadx-mcp qué algoritmos criptográficos usa el APK
```

**Identifica:**
- ❌ Algoritmos débiles: DES, MD5, SHA1, RC4
- ✅ Algoritmos seguros: AES, RSA, SHA256, SHA512
- Clases de Java Crypto API utilizadas

---

### 5. `find_dangerous_api_usage`
**Detección de APIs peligrosas**

Busca el uso de APIs de Android consideradas peligrosas.

**Uso con GitHub Copilot:**
```
@ntt-jadx-mcp busca APIs peligrosas en el código
@ntt-jadx-mcp encuentra uso de Runtime.exec
```

**APIs detectadas:**
- `Runtime.exec` - Ejecución de comandos (HIGH)
- `ProcessBuilder` - Construcción de procesos (HIGH)
- `System.load/loadLibrary` - Carga de bibliotecas nativas (MEDIUM)
- `Class.forName` - Carga dinámica de clases (MEDIUM)
- `DexClassLoader` - Carga dinámica de DEX (MEDIUM)

---

### 6. `detect_hardcoded_credentials`
**Detección de credenciales hardcodeadas**

Busca patrones comunes de credenciales hardcodeadas en el código.

**Uso con GitHub Copilot:**
```
@ntt-jadx-mcp busca credenciales hardcodeadas
@ntt-jadx-mcp encuentra contraseñas en el código
```

**Patrones buscados:**
- `password =`, `passwd =`
- `api_key =`, `apiKey =`
- `secret =`, `token =`
- `auth =`, `bearer`
- `authorization`

---

### 7. `find_exported_components`
**Análisis de componentes exportados**

Identifica activities, services, broadcast receivers y content providers que podrían estar exportados.

**Uso con GitHub Copilot:**
```
@ntt-jadx-mcp busca componentes exportados
@ntt-jadx-mcp encuentra activities exportadas
```

---

## 📊 Ejemplos de Uso

### Análisis Completo de Seguridad
```
@ntt-jadx-mcp realiza un análisis completo de seguridad del APK
```

Este comando ejecutará múltiples herramientas para dar un panorama completo.

### Búsqueda Específica
```
@ntt-jadx-mcp busca vulnerabilidades de SQL injection
@ntt-jadx-mcp qué algoritmos de encriptación usa el APK
@ntt-jadx-mcp encuentra el uso de permisos de ubicación
```

### Análisis de Riesgo
```
@ntt-jadx-mcp identifica vulnerabilidades de alta severidad
@ntt-jadx-mcp muestra los mayores riesgos de seguridad
```

---

## 🔍 Cómo Funcionan las Herramientas

Estas herramientas utilizan **búsqueda de código** en lugar de análisis estático del manifest, ya que el plugin de JADX 1.5.0 tiene limitaciones para acceder a recursos.

**Proceso:**
1. Buscan patrones específicos en el código descompilado
2. Identifican clases que contienen esos patrones
3. Clasifican los hallazgos por severidad
4. Proporcionan recomendaciones de remediación

**Ventajas:**
- ✅ Funciona con cualquier APK cargado en JADX
- ✅ No depende del acceso al AndroidManifest.xml
- ✅ Encuentra uso real en código, no solo declaraciones
- ✅ Identifica código ofuscado que contenga patrones

**Limitaciones:**
- ⚠️ No puede acceder directamente al AndroidManifest.xml
- ⚠️ Los resultados pueden incluir falsos positivos
- ⚠️ Requiere verificación manual de los hallazgos

---

## 🛠️ Integración con GitHub Copilot

GitHub Copilot puede usar estas herramientas automáticamente cuando preguntes sobre seguridad:

**Ejemplos de preguntas naturales:**
- "¿Esta app tiene vulnerabilidades?"
- "¿Qué permisos peligrosos usa?"
- "¿Hay contraseñas hardcodeadas?"
- "¿Usa algoritmos de encriptación débiles?"
- "¿Tiene componentes exportados sin protección?"

Copilot elegirá automáticamente las herramientas apropiadas para responder.

---

## 📝 Notas Importantes

### Falsos Positivos
Las herramientas de búsqueda pueden generar falsos positivos. Por ejemplo:
- Comentarios que mencionan "password"
- Strings que contienen "http://" pero no son URLs reales
- Uso legítimo de APIs marcadas como peligrosas

**Siempre verifica manualmente los resultados.**

### Complementar con Análisis Manual
Estas herramientas son un punto de partida. Para un análisis completo:
1. Usa estas herramientas para identificar áreas de riesgo
2. Examina manualmente el código de las clases identificadas
3. Verifica el AndroidManifest.xml externamente si es necesario
4. Realiza pruebas dinámicas en un entorno controlado

---

## 🚀 Mejoras Futuras

Posibles mejoras cuando JADX agregue más capacidades:
- [ ] Análisis directo del AndroidManifest.xml
- [ ] Detección de vulnerabilidades en recursos XML
- [ ] Análisis de flujo de datos
- [ ] Detección de configuraciones inseguras en assets
- [ ] Integración con bases de datos de CVEs

---

## 📚 Referencias

- [OWASP Mobile Security Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/)
- [Android Security Best Practices](https://developer.android.com/topic/security/best-practices)
- [CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/)
