# 🚀 Guía Rápida - NTT JADX MCP Plugin

## Instalación en 3 pasos

### 1️⃣ Verificar requisitos
```bash
java -version    # Debe mostrar Java 11 o superior
gradle -v        # Debe mostrar Gradle instalado
```

Si falta algo:
- **Java:** https://adoptium.net/
- **Gradle:** `choco install gradle` (Windows con Chocolatey)

### 2️⃣ Compilar e instalar
```bash
compilar-e-instalar.bat
```

### 3️⃣ Reiniciar JADX
- Cierra JADX GUI completamente
- Ábrelo de nuevo
- Verifica en: `Plugins → Installed Plugins`

---

## ✅ Verificar que funciona

### En JADX GUI
1. Abre un APK en JADX
2. Ve a: `Plugins → Installed Plugins`
3. Debes ver: **NTT JADX MCP Plugin v1.0.0**

### Probar la API
```bash
# Opción 1: En el navegador
http://localhost:37860/list-classes

# Opción 2: Con curl
curl http://localhost:37860/list-classes
```

---

## 📡 Endpoints API

| Endpoint | Uso |
|----------|-----|
| `/list-classes` | Lista todas las clases del APK |
| `/get-current-class` | Obtiene la clase activa en el editor |
| `/get-class-code?name=com.example.MainActivity` | Código de una clase específica |
| `/get-method?class=com.example.MainActivity&method=onCreate` | Código de un método |
| `/search?q=password` | Busca "password" en todo el código |

---

## 🔧 Solución rápida de problemas

### El plugin no aparece en JADX
```bash
# Verificar que el JAR está instalado:
dir %APPDATA%\jadx\plugins\ntt_jadx_mcp_plugin-1.0.0.jar
```
- ✅ Archivo existe → Reinicia JADX completamente
- ❌ Archivo no existe → Ejecuta `instalar.bat`

### El servidor no responde
- ✅ JADX está abierto con un APK cargado?
- ✅ Verifica que el puerto 37860 no esté ocupado
- ✅ Revisa los logs en la consola de JADX

### Error de compilación
```bash
# Limpiar y recompilar:
gradlew.bat clean jar
```

---

## 📁 Ubicaciones importantes

| Item | Ruta Windows |
|------|--------------|
| Plugin compilado | `build\libs\ntt_jadx_mcp_plugin-1.0.0.jar` |
| Plugins JADX | `%APPDATA%\jadx\plugins\` |
| Ruta completa típica | `C:\Users\TU_USUARIO\AppData\Roaming\jadx\plugins\` |

---

## 🔄 Actualizar el plugin

```bash
# 1. Recompilar
compilar.bat

# 2. Cerrar JADX GUI

# 3. Reinstalar
instalar.bat

# 4. Abrir JADX GUI
```

---

## 💡 Uso típico con MCP Server

```
┌─────────────┐         HTTP          ┌──────────────┐
│ MCP Server  │ ←─ localhost:37860 ─→ │  JADX GUI    │
│ (Claude)    │                        │  + Plugin    │
└─────────────┘                        └──────────────┘
                                              │
                                              ↓
                                       ┌─────────────┐
                                       │   APK File  │
                                       └─────────────┘
```

El plugin permite que Claude (via MCP) analice el código del APK que tienes abierto en JADX.

---

## 📞 ¿Necesitas más ayuda?

- 📖 Guía completa: [INSTALACION.md](INSTALACION.md)
- 📝 README: [README.md](README.md)
- 🐛 Revisa los logs de JADX en la consola
