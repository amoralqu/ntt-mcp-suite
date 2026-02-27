@echo off
echo ========================================
echo  NTT JADX MCP Plugin - Script de Compilacion
echo ========================================
echo.

REM Verificar Java
echo [1/5] Verificando Java...
java -version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Java no esta instalado.
    echo Por favor instala Java JDK 11 o superior desde: https://adoptium.net/
    pause
    exit /b 1
)
echo [OK] Java encontrado
echo.

REM Verificar Gradle
echo [2/5] Verificando Gradle...
gradle -v >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Gradle no esta instalado.
    echo.
    echo Opciones de instalacion:
    echo   1. Chocolatey: choco install gradle
    echo   2. Scoop: scoop install gradle
    echo   3. Manual: https://gradle.org/releases/
    echo.
    pause
    exit /b 1
)
echo [OK] Gradle encontrado
echo.

REM Limpiar build anterior
echo [3/5] Limpiando build anterior...
if exist "build" (
    rmdir /S /Q build
    echo [OK] Build anterior eliminado
) else (
    echo [OK] No hay build anterior
)
echo.

REM Compilar
echo [4/5] Compilando plugin...
gradle clean jar
if errorlevel 1 (
    echo [ERROR] La compilacion fallo
    pause
    exit /b 1
)
echo [OK] Compilacion exitosa
echo.

REM Verificar JAR
echo [5/5] Verificando archivo JAR...
if exist "build\libs\ntt_jadx_mcp_plugin-1.0.0.jar" (
    echo [OK] Plugin compilado exitosamente:
    echo      build\libs\ntt_jadx_mcp_plugin-1.0.0.jar
    echo.
    echo ========================================
    echo  COMPILACION COMPLETADA
    echo ========================================
    echo.
    echo Siguiente paso: Instalar el plugin
    echo Ejecuta: instalar.bat
    echo.
) else (
    echo [ERROR] El archivo JAR no se genero
    pause
    exit /b 1
)

pause
