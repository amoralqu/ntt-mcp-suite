# Script de verificación para Burp Suite Docker + MCP
# Ejecutar desde PowerShell: .\scripts\verify_burp_docker_setup.ps1

Write-Host "=== Verificación de Burp Suite Docker + MCP ===" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar Docker
Write-Host "[1/6] Verificando Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker instalado: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker no está instalado o no está en PATH" -ForegroundColor Red
    Write-Host "    Instala Docker Desktop: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

# 2. Verificar Docker Compose
Write-Host "[2/6] Verificando Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version
    Write-Host "✓ Docker Compose instalado: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Compose no está disponible" -ForegroundColor Red
    exit 1
}

# 3. Verificar si Docker daemon está corriendo
Write-Host "[3/6] Verificando Docker daemon..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✓ Docker daemon está corriendo" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker daemon no está corriendo" -ForegroundColor Red
    Write-Host "    Abre Docker Desktop y espera a que inicie" -ForegroundColor Yellow
    exit 1
}

# 4. Verificar contenedor de Burp
Write-Host "[4/6] Verificando contenedor de Burp Suite..." -ForegroundColor Yellow
$burpContainer = docker ps --filter "name=burp" --format "{{.Names}}"
if ($burpContainer) {
    Write-Host "✓ Contenedor de Burp encontrado: $burpContainer" -ForegroundColor Green
    
    # Verificar puertos
    $ports = docker port $burpContainer
    Write-Host "  Puertos mapeados:" -ForegroundColor Cyan
    Write-Host "  $ports" -ForegroundColor White
} else {
    Write-Host "⚠ No se encontró contenedor de Burp corriendo" -ForegroundColor Yellow
    Write-Host "    Ejecuta: cd <ruta_burp2025> && docker-compose up -d" -ForegroundColor Cyan
}

# 5. Verificar REST API de Burp
Write-Host "[5/6] Verificando REST API de Burp Suite..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:1337/v0.1/" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✓ REST API de Burp está respondiendo" -ForegroundColor Green
    Write-Host "  Status: $($response.StatusCode)" -ForegroundColor White
} catch {
    Write-Host "✗ No se puede conectar a la REST API de Burp" -ForegroundColor Red
    Write-Host "    Verifica que:" -ForegroundColor Yellow
    Write-Host "    1. El contenedor esté corriendo (docker ps)" -ForegroundColor Yellow
    Write-Host "    2. El puerto 1337 esté mapeado en docker-compose.yml" -ForegroundColor Yellow
    Write-Host "    3. La REST API esté habilitada en Burp Suite" -ForegroundColor Yellow
}

# 6. Verificar entorno Python y servidor MCP
Write-Host "[6/6] Verificando servidor MCP..." -ForegroundColor Yellow
if (Test-Path ".\.venv\Scripts\python.exe") {
    Write-Host "✓ Entorno virtual Python encontrado" -ForegroundColor Green
    
    # Verificar que el módulo existe
    if (Test-Path ".\src\ntt_burp_mcp\server\main.py") {
        Write-Host "✓ Servidor MCP de Burp encontrado" -ForegroundColor Green
    } else {
        Write-Host "✗ Servidor MCP de Burp no encontrado" -ForegroundColor Red
    }
} else {
    Write-Host "⚠ Entorno virtual Python no encontrado" -ForegroundColor Yellow
    Write-Host "    Crea el entorno: python -m venv .venv" -ForegroundColor Cyan
}

# Resumen
Write-Host ""
Write-Host "=== Resumen ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para iniciar Burp Suite:" -ForegroundColor White
Write-Host "  cd C:\Users\amoralqu\Downloads\burp2025" -ForegroundColor Gray
Write-Host "  docker-compose up -d" -ForegroundColor Gray
Write-Host ""
Write-Host "Para probar el servidor MCP:" -ForegroundColor White
Write-Host "  .\.venv\Scripts\activate" -ForegroundColor Gray
Write-Host "  python scripts\manual_mcp_test_client_burp.py" -ForegroundColor Gray
Write-Host ""
Write-Host "Para ver logs de Burp:" -ForegroundColor White
Write-Host "  docker-compose logs -f" -ForegroundColor Gray
Write-Host ""
Write-Host "Documentación completa: docs\BURP_DOCKER_SETUP.md" -ForegroundColor Cyan
