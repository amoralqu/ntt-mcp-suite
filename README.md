# NTT MCP Suite (Model Context Protocol Servers)

## 📌 Descripción general

**NTT MCP Suite** es un proyecto interno cuyo objetivo es **integrar, estandarizar y gobernar múltiples servidores MCP (Model Context Protocol)** para que el **equipo de Hacking** pueda **automatizar pruebas, orquestar herramientas y apoyarse en IA** durante actividades de análisis dinámico, reversing y seguridad.

La idea central del proyecto **no es un MCP concreto**, sino crear una **plataforma común** donde:

* 🧠 La IA (Copilot u otros clientes MCP) pueda interactuar con herramientas técnicas.
* 🔐 El código sea **100% de autoría propia**, protegiendo información de clientes.
* 🧩 Se puedan integrar **múltiples MCPs especializados** (Frida, tooling interno, análisis estático, etc.).
* 🚀 El proyecto pueda crecer sin rehacer arquitectura ni romper compatibilidad.

Actualmente, el repositorio incluye **tres MCPs funcionales** como casos de uso iniciales:

* **`ntt-frida-mcp`** → MCP para interactuar con **Frida** (local, emuladores y dispositivos USB).
* **`ntt-jadx-mcp`** → MCP para análisis estático, extracción y refactor de apps Android vía **Jadx**.
* **`ntt-objection-mcp`** → MCP para exploración y análisis de aplicaciones móviles mediante **Objection**.

Estos MCPs no son el objetivo final del proyecto, sino los primeros MCPs integrados dentro de NTT MCP Suite.

---

## 🧱 Arquitectura del proyecto

```text
ntt-mcp-suite/
├── .vscode/
│   └── mcp.json
├── scripts/
│   └── manual_mcp_test_client.py
├── src/
│   ├── ntt_frida_mcp/
│   │   ├── server/
│   │   └── tools/
│   ├── ntt_jadx_mcp/
│   │   ├── server/
│   │   └── tools/
│   └── (futuros MCPs)
│       └── ntt_<otro>_mcp/
├── pyproject.toml
├── requirements.txt
└── README.md
```

### Principios de arquitectura

* 🧩 Cada MCP vive en su propio paquete (`ntt_<nombre>_mcp`).
* 🧠 Cada MCP expone herramientas MCP independientes.
* 🔌 El proyecto actúa como **contenedor de MCPs**, no como una herramienta única.
* 🧱 MCPs pueden añadirse sin modificar los existentes.

---

## ⚙️ Requisitos del proyecto NTT MCPS

Estos requisitos aplican **al proyecto base**, independientemente de los MCPs que se integren.

* Python **3.10+**
* Git
* VSCode (recomendado)
* GitHub Copilot (opcional, recomendado para uso en modo Agent)

---

## 🚀 Instalación del proyecto base

### 1️⃣ Crear entorno virtual

```bash
python -m venv .venv
```

Activar:

* **Windows**

```powershell
.\.venv\Scripts\Activate.ps1
```

* **Linux / macOS**

```bash
source .venv/bin/activate
```

### 2️⃣ Instalar dependencias base

```bash
pip install -r requirements.txt
```

> El proyecto se instala en modo editable para facilitar el desarrollo e integración de MCPs.

---

## ▶️ Ejecución de MCPs

### VSCode + GitHub Copilot (modo Agent)

1. Abrir el proyecto en VSCode.
2. Verificar `.vscode/mcp.json`.
3. Iniciar Copilot Chat en **modo Agent**.
4. Copilot levantará automáticamente los MCPs configurados.

### Ejecución manual de un MCP

```bash
.\.venv\Scripts\python.exe -m <paquete_mcp>.server.main
```

Ejemplo:

```bash
.\.venv\Scripts\python.exe -m ntt_frida_mcp.server.main
```
```bash
.\.venv\Scripts\python.exe -m ntt_jadx_mcp.server.main
```

---

## 🧪 Script de verificación manual (proyecto)

El script:

```text
scripts/manual_mcp_test_client.py
```

Permite verificar que **el framework MCP funciona correctamente**, sin depender de Copilot:

* Descubrimiento de dispositivos
* Selección automática de device (Android si existe, si no local)
* Creación de sesión MCP
* Ejecución de JavaScript
* Cierre limpio de sesión

Ejecutar:

```bash
.\.venv\Scripts\python.exe .\scripts\manual_mcp_test_client.py
```

---

# 🧠 MCP: ntt-frida-mcp

## ¿Qué es?

`ntt-frida-mcp` es **uno de los MCPs integrados en NTT MCPS**. Su propósito es exponer **Frida** como un conjunto de herramientas MCP para que la IA pueda interactuar con procesos y dispositivos durante pruebas de seguridad.

Este MCP **no define el proyecto**, sino que **demuestra cómo integrar tooling técnico real dentro del ecosistema MCP**.

---

## 🎯 ¿Qué permite hacer?

* Enumerar dispositivos Frida (local, emuladores, USB).
* Enumerar procesos.
* Adjuntarse a procesos.
* Crear sesiones interactivas persistentes.
* Ejecutar JavaScript dentro del proceso target.
* Instalar hooks simples (best-effort).
* Limpiar sesiones automáticamente.

---

## ⚙️ Requisitos específicos de ntt-frida-mcp

Estos requisitos **solo aplican si se usa este MCP**:

* Frida instalado en el host
* Frida compatible con el target
* Para Android:

  * Emulador o dispositivo físico
  * `frida-server` ejecutándose en el dispositivo

---

## 🧰 Herramientas expuestas por ntt-frida-mcp

### 🔹 Dispositivos y procesos

* `enumerate_devices`
* `get_device`
* `get_usb_device`
* `enumerate_processes(device_id=None)`
* `list_processes(device_id=None)`
* `get_process_by_name(name, device_id=None)`

### 🔹 Ciclo de vida de procesos

* `spawn_process(program, args, device_id=None)`
* `resume_process(pid, device_id=None)`
* `kill_process(pid, device_id=None)`

### 🔹 Sesiones interactivas

* `create_interactive_session(process_id, device_id=None)`
* `execute_in_session(session_id, javascript_code)`
* `close_interactive_session(session_id)`

### 🔹 Hooks simples (best-effort)

* `create_simple_hook(process_id, hook_type, device_id=None)`

  * `hook_type`: `network`, `file`, `memory`

> ⚠️ Los hooks dependen de la plataforma y del proceso. Si no aplican, el MCP devuelve errores claros (`installed: false`).

---

## 💬 Ejemplos de prompts (Copilot Agent)

### Enumerar dispositivos

> "Enumera los dispositivos disponibles usando el MCP."

### Enumerar procesos en Android

> "Enumera los procesos del dispositivo USB disponible."

### Crear sesión interactiva

> "Crea una sesión interactiva contra el proceso system_server."

### Ejecutar JavaScript

> "En la sesión activa, ejecuta JavaScript para mostrar Process.id y Process.platform."

### Cerrar sesión

> "Cierra la sesión interactiva actual."

---

## 🧹 Limpieza y estabilidad

* Las sesiones interactivas tienen **TTL automático**.
* Existe un **cleaner daemon** que libera sesiones inactivas.
* Se recomienda cerrar sesiones explícitamente cuando ya no se usen.

---

## 🔐 Seguridad y buenas prácticas

* Los MCPs se ejecutan por `stdio` (no exponen red por defecto).
* El JavaScript ejecutado dentro de procesos es responsabilidad del usuario.
* Evitar ejecutar scripts no auditados en procesos sensibles.

---

# 🧠 MCP: ntt-jadx-mcp

## ¿Qué es?

`ntt-jadx-mcp` es otro MCP integrado en NTT MCPS. Su propósito es exponer capacidades avanzadas de análisis estático, extracción de información y refactorización sobre APKs Android mediante **Jadx**.

---

## 🎯 ¿Qué permite hacer?

* Extraer y listar clases, métodos y fields de una APK Android.
* Obtener código fuente Java/Smali y recursos.
* Buscar clases/métodos/fields por nombre o keyword.
* Consultar strings y recursos de la app.
* Refactorizar: renombrar clases, métodos, paquetes o variables.
* Operaciones de depuración sobre simbolización estática (stack frames, threads, variables).
* Descubrir clases principales o actividades (AndroidManifest, main activity).

---

## ⚙️ Requisitos específicos de ntt-jadx-mcp

Estos requisitos **solo aplican si se usa este MCP**:

* Jadx GUI instalado.
* Plugin ntt_jadx_mcp_plugin instalado en el Jadx GUI  `ntt_jadx_mcp_plugin/README.md`.
* Tener la APK objetivo cargada/anotada para análisis.

---

## 🧰 Herramientas expuestas por ntt-jadx-mcp

### 🔹 Análisis de clases y código

* `get_all_classes`, `get_class_source`, `get_methods_of_class`, `get_fields_of_class`
* `get_smali_of_class`, `get_main_application_classes_code`
* `get_main_activity_class`, `get_main_application_classes_names`

### 🔹 Recursos y strings

* `get_android_manifest`
* `get_strings`
* `get_all_resource_file_names`, `get_resource_file`

### 🔹 Búsqueda y referencias cruzadas

* `search_classes_by_keyword`
* `search_method_by_name`
* `get_method_by_name`
* `get_xrefs_to_class`, `get_xrefs_to_method`, `get_xrefs_to_field`

### 🔹 Refactor y debug

* `rename_class`, `rename_method`, `rename_field`, `rename_package`, `rename_variable`
* `debug_get_stack_frames`, `debug_get_threads`, `debug_get_variables`

---

## 💬 Ejemplos de prompts (Copilot Agent)

### Listar clases y métodos de una APK

> "Lista todas las clases del APK cargado usando el MCP Jadx."

### Buscar por palabra clave

> "Busca clases relacionadas con 'login' en el APK vía Jadx MCP."

### Obtener y modificar código

> "Obtén el código smali de la clase MainActivity."
> "Renombra el método 'checkLogin' de la clase 'AuthManager' por 'verificarIngreso'."

---

## 🧹 Limpieza y estabilidad

* Las operaciones sobre la APK no persisten cambios sobre el archivo original.
* Refactorizaciones y búsquedas son in-memory hasta ser exportadas.

---

## 🔐 Seguridad y buenas prácticas

* El MCP solo procesa APKs testadas/autorizadas internamente.
* El análisis estático no ejecuta código malicioso ni toca dispositivos físicos.

---

# 🧠 MCP: ntt-objection-mcp

## ¿Qué es?

`ntt-objection-mcp` es otro MCP integrado en NTT MCPS. Su propósito es exponer **Objection** como un conjunto de herramientas MCP para facilitar la exploración y análisis de aplicaciones móviles (Android e iOS) mediante Frida, proporcionando una interfaz de alto nivel para tareas comunes de seguridad móvil.

---

## 🎯 ¿Qué permite hacer?

* Enumerar dispositivos disponibles (local, USB, remotos).
* Listar aplicaciones instaladas en dispositivos.
* Obtener información detallada de aplicaciones específicas.
* Identificar la aplicación en primer plano.
* Explorar clases Java/Objective-C con filtrado por patrones.
* Explorar métodos de clases específicas.
* Listar Activities de aplicaciones Android.
* Listar Services de aplicaciones Android.

---

## ⚙️ Requisitos específicos de ntt-objection-mcp

Estos requisitos **solo aplican si se usa este MCP**:

* Frida instalado en el host
* Objection instalado (`pip install objection`)
* Para Android:

  * Emulador o dispositivo físico
  * `frida-server` ejecutándose en el dispositivo

* Para iOS:

  * Dispositivo con jailbreak
  * `frida-server` instalado en el dispositivo

---

## 🧰 Herramientas expuestas por ntt-objection-mcp

### 🔹 Gestión de dispositivos

* `enumerate_devices`
* `get_device(device_id=None)`
* `get_usb_device(timeout=5)`

### 🔹 Gestión de aplicaciones

* `list_applications(device_id=None)`
* `get_frontmost_application(device_id=None)`
* `get_application_info(app_identifier, device_id=None)`

### 🔹 Exploración de aplicaciones

* `explore_classes(app_identifier, device_id=None, pattern=None)`
* `explore_methods(app_identifier, class_name, device_id=None)`
* `explore_activities(app_identifier, device_id=None)`
* `explore_services(app_identifier, device_id=None)`

---

## 💬 Ejemplos de prompts (Copilot Agent)

### Enumerar dispositivos

> "Lista los dispositivos disponibles usando ntt-objection-mcp."

### Listar aplicaciones en dispositivo USB

> "Muestra todas las aplicaciones instaladas en el dispositivo USB."

### Obtener aplicación en primer plano

> "¿Qué aplicación está actualmente en primer plano en el dispositivo?"

### Explorar clases de una aplicación

> "Explora las clases de la aplicación com.example.app que contengan 'Auth' en su nombre."

### Explorar métodos de una clase

> "Muestra todos los métodos de la clase com.example.app.MainActivity."

### Listar Activities de Android

> "Lista todas las Activities de la aplicación com.android.settings."

---

## 🧹 Limpieza y estabilidad

* Las sesiones de exploración tienen **timeout de 2 segundos por defecto** para scripts Frida.
* Se recomienda que la aplicación objetivo esté en ejecución para operaciones de exploración.
* Las operaciones de listado de aplicaciones funcionan sin necesidad de que las apps estén activas.

---

## 🔐 Seguridad y buenas prácticas

* Los MCPs se ejecutan por `stdio` (no exponen red por defecto).
* Las operaciones de exploración requieren permisos de instrumentación en el dispositivo.
* Evitar explorar aplicaciones no autorizadas o en dispositivos no controlados.
* Los scripts Frida ejecutados son controlados y limitados en alcance.

---

# 🧠 MCP: ntt-adb-mcp

## ¿Qué es?

`ntt-adb-mcp` es otro MCP integrado en NTT MCPS. Su propósito es exponer **Android Debug Bridge (ADB)** como un conjunto de herramientas MCP para facilitar la gestión de dispositivos Android, instalación de aplicaciones, ejecución de comandos y operaciones de archivos durante pruebas de seguridad.

---

## 🎯 ¿Qué permite hacer?

* Enumerar dispositivos Android conectados (emuladores y dispositivos físicos).
* Obtener información detallada de dispositivos.
* Listar aplicaciones instaladas en dispositivos.
* Instalar y desinstalar APKs.
* Iniciar y detener aplicaciones.
* Ejecutar comandos shell en dispositivos.
* Transferir archivos entre el host y dispositivos (pull/push).
* Capturar logs del sistema (logcat).
* Tomar capturas de pantalla.
* Reiniciar dispositivos.

---

## ⚙️ Requisitos específicos de ntt-adb-mcp

Estos requisitos **solo aplican si se usa este MCP**:

* Android SDK Platform-Tools instalado (adb debe estar en PATH).
* Para dispositivos físicos:

  * Depuración USB habilitada en el dispositivo.
  * Drivers USB apropiados instalados.

* Para emuladores:

  * Android Emulator en ejecución.

---

## 🧰 Herramientas expuestas por ntt-adb-mcp

### 🔹 Gestión de dispositivos

* `list_devices`
* `get_device_info(device_id=None)`
* `get_device_state(device_id=None)`

### 🔹 Gestión de aplicaciones

* `list_packages(device_id=None, filter=None)`
* `get_package_info(package_name, device_id=None)`
* `install_apk(apk_path, device_id=None)`
* `uninstall_package(package_name, device_id=None)`
* `start_activity(package_name, activity_name, device_id=None)`
* `stop_app(package_name, device_id=None)`
* `clear_app_data(package_name, device_id=None)`

### 🔹 Operaciones de shell y archivos

* `execute_shell_command(command, device_id=None)`
* `pull_file(remote_path, local_path, device_id=None)`
* `push_file(local_path, remote_path, device_id=None)`
* `list_directory(path, device_id=None)`
* `get_logcat(filter=None, device_id=None)`
* `clear_logcat(device_id=None)`
* `reboot_device(device_id=None)`
* `take_screenshot(output_path, device_id=None)`

---

## 💬 Ejemplos de prompts (Copilot Agent)

### Listar dispositivos

> "Lista todos los dispositivos Android conectados usando ntt-adb-mcp."

### Instalar una APK

> "Instala la APK ubicada en /path/to/app.apk en el dispositivo conectado."

### Listar aplicaciones instaladas

> "Muestra todas las aplicaciones instaladas en el dispositivo."

### Ejecutar comando shell

> "Ejecuta el comando 'pm list packages -3' en el dispositivo para listar apps de terceros."

### Obtener logs de la aplicación

> "Obtén los logs de logcat filtrados por 'MyApp'."

### Capturar pantalla

> "Toma una captura de pantalla y guárdala en /path/to/screenshot.png."

---

## 🧹 Limpieza y estabilidad

* Los comandos de ADB tienen timeout configurable para evitar bloqueos.
* Las operaciones de archivo verifican la existencia de rutas antes de ejecutar.
* Se recomienda verificar el estado del dispositivo antes de operaciones críticas.

---

## 🔐 Seguridad y buenas prácticas

* Los MCPs se ejecutan por `stdio` (no exponen red por defecto).
* Los comandos shell ejecutados son responsabilidad del usuario.
* Evitar ejecutar comandos que puedan comprometer la estabilidad del dispositivo.
* Las operaciones de instalación/desinstalación requieren permisos apropiados en el dispositivo.

---

# 🧠 MCP: ntt-burp-mcp

## ¿Qué es?

`ntt-burp-mcp` es otro MCP integrado en NTT MCPS. Su propósito es exponer **Burp Suite Professional** como un conjunto de herramientas MCP para facilitar el análisis de seguridad de aplicaciones web, mediante la automatización de escaneos, gestión del proxy y análisis de vulnerabilidades.

---

## 🎯 ¿Qué permite hacer?

* Iniciar escaneos de seguridad automatizados (crawl y audit).
* Monitorear el estado y progreso de escaneos.
* Obtener vulnerabilidades detectadas con detalles completos.
* Detener escaneos en curso.
* Obtener métricas de escaneos realizados.
* Acceder al historial del proxy HTTP.
* Enviar peticiones al Repeater y al Intruder.
* Consultar y actualizar la configuración del proxy.

---

## ⚙️ Requisitos específicos de ntt-burp-mcp

Estos requisitos **solo aplican si se usa este MCP**:

* Burp Suite Professional con REST API habilitada.
* Python 3.8 o superior.
* Paquete `requests` instalado.
* Burp Suite en ejecución con la REST API configurada (puerto por defecto: 1337).

---

## 🧰 Herramientas expuestas por ntt-burp-mcp

### 🔹 Scanner

* `start_scan(target_url, scan_type)`
* `get_scan_status(scan_id)`
* `get_scan_issues(scan_id)`
* `stop_scan(scan_id)`
* `get_scan_metrics(scan_id)`

### 🔹 Proxy

* `get_proxy_history(limit=None)`
* `get_proxy_item(item_id)`
* `send_to_repeater(item_id)`
* `send_to_intruder(item_id)`
* `get_proxy_config()`
* `update_proxy_config(config)`

---

## 💬 Ejemplos de prompts (Copilot Agent)

### Iniciar un escaneo

> "Inicia un escaneo de seguridad completo en https://example.com usando Burp Suite."

### Consultar estado del escaneo

> "¿Cuál es el estado actual del escaneo con ID 'scan_123'?"

### Obtener vulnerabilidades

> "Muestra todas las vulnerabilidades encontradas en el escaneo 'scan_123'."

### Ver historial del proxy

> "Lista las últimas 50 peticiones interceptadas por el proxy de Burp."

### Enviar al Repeater

> "Envía la petición con ID 'item_456' al Repeater para análisis manual."

---

## 🧹 Limpieza y estabilidad

* Las peticiones a la REST API tienen timeout configurable (por defecto: 30 segundos).
* Los escaneos pueden detenerse en cualquier momento sin afectar otros procesos.
* Se recomienda monitorear el uso de recursos de Burp Suite durante escaneos extensos.

---

## 🔐 Seguridad y buenas prácticas

* Los MCPs se ejecutan por `stdio` (no exponen red por defecto).
* La REST API de Burp Suite puede protegerse con API Key.
* Solo escanear aplicaciones con autorización explícita.
* Configurar el proxy solo en entornos de prueba controlados.
* La REST API solo está disponible en Burp Suite Professional.

---

## 📈 Estado del proyecto

* ✅ Framework MCP estable para uso interno.
* ✅ `ntt-frida-mcp` validado en Android (emuladores y USB).
* ✅ `ntt-jadx-mcp` integrado y validado para análisis estático de APKs.
* ✅ `ntt-objection-mcp` integrado y validado para exploración de apps móviles.
* ✅ `ntt-adb-mcp` integrado y validado para gestión de dispositivos Android.
* ✅ `ntt-burp-mcp` integrado y validado para análisis de seguridad web con Burp Suite Professional.
* 🚧 Se integrarán nuevos MCPs según necesidades del equipo.

---

## 📬 Soporte

Para dudas, mejoras o propuestas de nuevos MCPs, contactar con el equipo responsable de **NTT MCP Suite**.
