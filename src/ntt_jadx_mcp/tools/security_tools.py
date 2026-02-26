"""
NTT JADX MCP - Security Analysis Tools

This module provides specialized MCP tools for security analysis of Android applications,
including vulnerability detection, dangerous API usage, and security pattern detection.

These tools work with the actual capabilities of JADX 1.5.0 by using code search
instead of trying to access resources that aren't available.
"""

from ntt_jadx_mcp.tools.client import get_from_jadx
from typing import List, Dict


# Patrones de vulnerabilidades comunes en Android
SECURITY_PATTERNS = {
    "crypto_weak": [
        "DES", "MD5", "SHA1", "ECB", "javax.crypto.Cipher",
        "MessageDigest", "SecretKeySpec"
    ],
    "hardcoded_secrets": [
        "password", "passwd", "pwd", "secret", "api_key",
        "apikey", "token", "auth", "credential"
    ],
    "insecure_network": [
        "http://", "ALLOW_ALL_HOSTNAME_VERIFIER", "TrustAllCerts",
        "setHostnameVerifier", "X509TrustManager"
    ],
    "sql_injection": [
        "execSQL", "rawQuery", "SELECT", "INSERT", "UPDATE", "DELETE"
    ],
    "webview_vulnerabilities": [
        "setJavaScriptEnabled", "addJavascriptInterface",
        "setAllowFileAccess", "setAllowContentAccess"
    ],
    "path_traversal": [
        "FileInputStream", "FileOutputStream", "openFileOutput",
        "../", "getExternalStorage"
    ],
    "intent_vulnerabilities": [
        "setComponent", "PendingIntent", "exported=\"true\"",
        "startActivity", "sendBroadcast"
    ],
    "debug_logging": [
        "Log.d", "Log.v", "Log.i", "System.out.println", "printStackTrace"
    ],
    "root_detection": [
        "su", "/system/xbin", "Superuser.apk", "RootTools"
    ],
    "dangerous_permissions": [
        "READ_EXTERNAL_STORAGE", "WRITE_EXTERNAL_STORAGE",
        "CAMERA", "RECORD_AUDIO", "ACCESS_FINE_LOCATION",
        "READ_CONTACTS", "READ_SMS", "SEND_SMS"
    ]
}


async def analyze_security_vulnerabilities(categories: List[str] = None) -> dict:
    """
    Analiza el APK buscando patrones de vulnerabilidades de seguridad comunes.
    
    Args:
        categories: Lista de categorías a analizar. Si es None, analiza todas.
                   Categorías disponibles: crypto_weak, hardcoded_secrets,
                   insecure_network, sql_injection, webview_vulnerabilities,
                   path_traversal, intent_vulnerabilities, debug_logging,
                   root_detection, dangerous_permissions
    
    Returns:
        dict: Resultados agrupados por categoría con clases afectadas
    
    MCP Tool: analyze_security_vulnerabilities
    Description: Realiza un análisis completo de seguridad buscando vulnerabilidades comunes.
    """
    if categories is None:
        categories = list(SECURITY_PATTERNS.keys())
    
    results = {
        "summary": {
            "total_categories_analyzed": len(categories),
            "categories_with_findings": 0,
            "total_findings": 0
        },
        "findings": {}
    }
    
    for category in categories:
        if category not in SECURITY_PATTERNS:
            continue
            
        patterns = SECURITY_PATTERNS[category]
        category_findings = []
        
        for pattern in patterns:
            try:
                # Buscar el patrón en el código
                search_result = await get_from_jadx(
                    "search-classes-by-keyword",
                    {"search_term": pattern, "count": "50"}
                )
                
                if search_result.get("classes"):
                    category_findings.append({
                        "pattern": pattern,
                        "classes": search_result["classes"][:10],  # Limitar a 10 clases por patrón
                        "total_matches": search_result.get("total", len(search_result["classes"]))
                    })
            except Exception as e:
                continue
        
        if category_findings:
            results["findings"][category] = category_findings
            results["summary"]["categories_with_findings"] += 1
            results["summary"]["total_findings"] += len(category_findings)
    
    return results


async def find_dangerous_api_usage() -> dict:
    """
    Busca el uso de APIs peligrosas de Android en el código.
    
    Returns:
        dict: Lista de APIs peligrosas encontradas y dónde se usan
    
    MCP Tool: find_dangerous_api_usage
    Description: Identifica el uso de APIs de Android consideradas peligrosas.
    """
    dangerous_apis = [
        "Runtime.exec",
        "ProcessBuilder",
        "System.load",
        "System.loadLibrary",
        "Class.forName",
        "URLClassLoader",
        "DexClassLoader",
        "PathClassLoader"
    ]
    
    findings = []
    
    for api in dangerous_apis:
        try:
            result = await get_from_jadx(
                "search-classes-by-keyword",
                {"search_term": api, "count": "20"}
            )
            
            if result.get("classes"):
                findings.append({
                    "api": api,
                    "risk_level": "HIGH" if api in ["Runtime.exec", "ProcessBuilder"] else "MEDIUM",
                    "classes": result["classes"][:5],
                    "total_occurrences": result.get("total", len(result["classes"]))
                })
        except Exception:
            continue
    
    return {
        "total_dangerous_apis_found": len(findings),
        "findings": findings
    }


async def detect_hardcoded_credentials() -> dict:
    """
    Detecta posibles credenciales hardcodeadas en el código.
    
    Returns:
        dict: Clases que contienen posibles credenciales hardcodeadas
    
    MCP Tool: detect_hardcoded_credentials
    Description: Busca patrones comunes de credenciales hardcodeadas.
    """
    credential_patterns = [
        "password =",
        "passwd =",
        "api_key =",
        "apiKey =",
        "secret =",
        "token =",
        "auth =",
        "bearer",
        "authorization"
    ]
    
    findings = []
    
    for pattern in credential_patterns:
        try:
            result = await get_from_jadx(
                "search-classes-by-keyword",
                {"search_term": pattern, "count": "20"}
            )
            
            if result.get("classes"):
                findings.append({
                    "pattern": pattern,
                    "classes": result["classes"][:5],
                    "total_matches": result.get("total", len(result["classes"]))
                })
        except Exception:
            continue
    
    return {
        "total_patterns_found": len(findings),
        "findings": findings,
        "recommendation": "Verificar manualmente cada clase para confirmar si contiene credenciales reales"
    }


async def analyze_crypto_usage() -> dict:
    """
    Analiza el uso de criptografía en la aplicación.
    
    Returns:
        dict: Análisis del uso de criptografía, incluyendo algoritmos débiles
    
    MCP Tool: analyze_crypto_usage
    Description: Identifica uso de criptografía y detecta algoritmos débiles.
    """
    crypto_patterns = {
        "weak_algorithms": ["DES", "MD5", "SHA1", "RC4"],
        "strong_algorithms": ["AES", "RSA", "SHA256", "SHA512"],
        "crypto_classes": ["javax.crypto", "java.security", "Cipher", "KeyGenerator"]
    }
    
    results = {
        "weak_crypto": [],
        "strong_crypto": [],
        "general_crypto_usage": []
    }
    
    # Buscar algoritmos débiles
    for algo in crypto_patterns["weak_algorithms"]:
        try:
            result = await get_from_jadx(
                "search-classes-by-keyword",
                {"search_term": algo, "count": "20"}
            )
            if result.get("classes"):
                results["weak_crypto"].append({
                    "algorithm": algo,
                    "risk": "HIGH",
                    "classes": result["classes"][:5]
                })
        except Exception:
            continue
    
    # Buscar algoritmos fuertes
    for algo in crypto_patterns["strong_algorithms"]:
        try:
            result = await get_from_jadx(
                "search-classes-by-keyword",
                {"search_term": algo, "count": "10"}
            )
            if result.get("classes"):
                results["strong_crypto"].append({
                    "algorithm": algo,
                    "classes": result["classes"][:3]
                })
        except Exception:
            continue
    
    return {
        "summary": {
            "weak_algorithms_found": len(results["weak_crypto"]),
            "strong_algorithms_found": len(results["strong_crypto"])
        },
        "details": results,
        "recommendation": "Reemplazar algoritmos débiles (DES, MD5, SHA1) con alternativas seguras (AES, SHA256)"
    }


async def find_exported_components() -> dict:
    """
    Busca componentes exportados que podrían ser vulnerables.
    
    Returns:
        dict: Componentes que parecen estar exportados
    
    MCP Tool: find_exported_components
    Description: Identifica activities, services y receivers exportados.
    """
    component_keywords = [
        "exported",
        "Activity",
        "Service", 
        "BroadcastReceiver",
        "ContentProvider"
    ]
    
    findings = []
    
    for keyword in component_keywords:
        try:
            result = await get_from_jadx(
                "search-classes-by-keyword",
                {"search_term": keyword, "count": "30"}
            )
            
            if result.get("classes"):
                findings.append({
                    "component_type": keyword,
                    "classes": result["classes"][:10],
                    "total": result.get("total", len(result["classes"]))
                })
        except Exception:
            continue
    
    return {
        "total_components_found": len(findings),
        "findings": findings,
        "recommendation": "Verificar que los componentes exportados requieran permisos apropiados"
    }


async def analyze_permissions_usage() -> dict:
    """
    Analiza el uso de permisos peligrosos en el código de la aplicación.
    
    Returns:
        dict: Clases que usan permisos peligrosos y su contexto
    
    MCP Tool: analyze_permissions_usage
    Description: Busca en el código el uso de APIs que requieren permisos peligrosos.
    """
    dangerous_permissions_apis = {
        "CAMERA": ["Camera", "camera", "takePicture", "SurfaceTexture"],
        "LOCATION": ["LocationManager", "getLastKnownLocation", "requestLocationUpdates", "GPS"],
        "STORAGE": ["getExternalStorageDirectory", "Environment.getExternalStorage", "WRITE_EXTERNAL"],
        "CONTACTS": ["ContactsContract", "getContentResolver", "Contacts"],
        "SMS": ["SmsManager", "sendTextMessage", "sendMultipartTextMessage"],
        "PHONE": ["TelephonyManager", "getDeviceId", "getLine1Number", "getSimSerialNumber"],
        "MICROPHONE": ["MediaRecorder", "AudioRecord", "RECORD_AUDIO"],
        "CALENDAR": ["CalendarContract", "CalendarProvider"]
    }
    
    findings = {}
    total_findings = 0
    
    for permission, apis in dangerous_permissions_apis.items():
        permission_findings = []
        
        for api in apis:
            try:
                result = await get_from_jadx(
                    "search-classes-by-keyword",
                    {"search_term": api, "count": "20"}
                )
                
                if result.get("classes"):
                    permission_findings.append({
                        "api": api,
                        "classes": result["classes"][:5],
                        "total_usage": result.get("total", len(result["classes"]))
                    })
                    total_findings += 1
            except Exception:
                continue
        
        if permission_findings:
            findings[permission] = {
                "apis_found": permission_findings,
                "risk_level": "HIGH" if permission in ["CAMERA", "LOCATION", "SMS"] else "MEDIUM"
            }
    
    return {
        "summary": {
            "dangerous_permissions_detected": len(findings),
            "total_api_usages": total_findings
        },
        "findings": findings,
        "recommendation": "Verificar que estos permisos estén declarados en AndroidManifest.xml y se soliciten en runtime para Android 6.0+"
    }


async def scan_for_common_vulnerabilities() -> dict:
    """
    Escaneo rápido para las vulnerabilidades más comunes en Android.
    
    Returns:
        dict: Resumen ejecutivo de vulnerabilidades encontradas
    
    MCP Tool: scan_for_common_vulnerabilities
    Description: Escaneo rápido de las Top 10 vulnerabilidades en Android.
    """
    # Top vulnerabilidades a buscar
    quick_checks = [
        ("SQL Injection", "rawQuery"),
        ("WebView XSS", "addJavascriptInterface"),
        ("Insecure Crypto", "DES"),
        ("Hardcoded Password", "password"),
        ("Debug Enabled", "Log.d"),
        ("Insecure Network", "http://"),
        ("Root Detection", "su"),
        ("Path Traversal", "../"),
        ("Exported Components", "exported"),
        ("Weak Crypto Hash", "MD5")
    ]
    
    findings = []
    
    for vuln_name, pattern in quick_checks:
        try:
            result = await get_from_jadx(
                "search-classes-by-keyword",
                {"search_term": pattern, "count": "10"}
            )
            
            if result.get("classes"):
                findings.append({
                    "vulnerability": vuln_name,
                    "pattern": pattern,
                    "affected_classes": len(result["classes"]),
                    "sample_classes": result["classes"][:3],
                    "severity": "HIGH" if vuln_name in ["SQL Injection", "WebView XSS", "Insecure Crypto"] else "MEDIUM"
                })
        except Exception:
            continue
    
    # Clasificar por severidad
    high_severity = [f for f in findings if f["severity"] == "HIGH"]
    medium_severity = [f for f in findings if f["severity"] == "MEDIUM"]
    
    return {
        "summary": {
            "total_vulnerabilities_found": len(findings),
            "high_severity": len(high_severity),
            "medium_severity": len(medium_severity)
        },
        "high_severity_issues": high_severity,
        "medium_severity_issues": medium_severity,
        "recommendation": "Priorizar la corrección de vulnerabilidades de severidad HIGH"
    }
