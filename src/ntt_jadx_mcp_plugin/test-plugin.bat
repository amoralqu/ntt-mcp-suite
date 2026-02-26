@echo off
echo ========================================
echo  Test de Conectividad - NTT JADX MCP Plugin
echo ========================================
echo.

echo [1/3] Verificando si el servidor esta corriendo...
curl -s http://localhost:8650/health
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Servidor HTTP respondiendo en puerto 8650
) else (
    echo.
    echo [ERROR] No se puede conectar al puerto 8650
    echo.
    echo Posibles causas:
    echo  - JADX GUI no esta abierto
    echo  - El plugin no esta instalado
    echo  - No hay un APK cargado en JADX
    echo  - El puerto 8650 esta ocupado por otra aplicacion
)

echo.
echo [2/3] Verificando instalacion del plugin...
set JADX_PLUGINS_DIR=%USERPROFILE%\.local\share\jadx\plugins
if exist "%JADX_PLUGINS_DIR%\ntt_jadx_mcp_plugin-1.0.0.jar" (
    echo [OK] Plugin encontrado en: %JADX_PLUGINS_DIR%
) else (
    echo [ADVERTENCIA] Plugin no encontrado en: %JADX_PLUGINS_DIR%
    echo Ejecute: instalar.bat
)

echo.
echo [3/3] Verificando puerto 8650...
netstat -ano | findstr :8650
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Puerto 8650 esta en uso
) else (
    echo [INFO] Puerto 8650 esta libre (el servidor no esta corriendo)
)

echo.
echo ========================================
echo  INSTRUCCIONES
echo ========================================
echo.
echo Si el servidor no responde:
echo  1. Abre JADX GUI
echo  2. Carga un archivo APK
echo  3. Verifica en la consola: "[NTT MCP Plugin] Escuchando en http://localhost:8650"
echo  4. Ejecuta nuevamente: test-plugin.bat
echo.
pause
