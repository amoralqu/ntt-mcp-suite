# src/ntt_nuclei_mcp/tools/scanner.py
from __future__ import annotations

import subprocess
import json
from typing import Any, Dict, List, Optional

from ..config import NUCLEI_PATH, NUCLEI_TEMPLATES_PATH, NUCLEI_TIMEOUT, logger


def run_nuclei_scan(
    target: str,
    templates: Optional[str] = None,
    severity: Optional[str] = None,
    tags: Optional[str] = None,
    exclude_tags: Optional[str] = None,
    timeout: Optional[int] = None,
    rate_limit: Optional[int] = None,
    additional_args: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Ejecuta un escaneo con Nuclei contra un target.

    Args:
        target: URL o IP del objetivo
        templates: Templates específicos a usar (ej: 'cves/', 'vulnerabilities/')
        severity: Filtrar por severidad (info, low, medium, high, critical)
        tags: Filtrar por tags específicos
        exclude_tags: Excluir templates con estos tags
        timeout: Timeout en segundos
        rate_limit: Rate limit (requests por segundo)
        additional_args: Argumentos adicionales para nuclei

    Returns:
        Dict con resultados del escaneo o error
    """
    try:
        cmd = [NUCLEI_PATH, "-target", target, "-json"]
        
        if templates:
            cmd.extend(["-t", templates])
        elif NUCLEI_TEMPLATES_PATH:
            cmd.extend(["-t", NUCLEI_TEMPLATES_PATH])
        
        if severity:
            cmd.extend(["-severity", severity])
        
        if tags:
            cmd.extend(["-tags", tags])
        
        if exclude_tags:
            cmd.extend(["-exclude-tags", exclude_tags])
        
        if rate_limit:
            cmd.extend(["-rate-limit", str(rate_limit)])
        
        if additional_args:
            cmd.extend(additional_args)
        
        timeout_value = timeout or NUCLEI_TIMEOUT
        
        logger.info(f"Ejecutando: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_value,
            check=False,
            shell=True  # Necesario en Windows
        )
        
        # Parsear salida JSON
        findings = []
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        findings.append(json.loads(line))
                    except json.JSONDecodeError:
                        logger.warning(f"No se pudo parsear línea: {line}")
        
        return {
            "success": True,
            "target": target,
            "findings": findings,
            "total_findings": len(findings),
            "stderr": result.stderr if result.stderr else None,
            "return_code": result.returncode
        }
        
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout ejecutando nuclei en {target}")
        return {
            "success": False,
            "error": f"Timeout después de {timeout_value} segundos",
            "target": target
        }
    except Exception as e:
        logger.error(f"Error ejecutando nuclei: {e}")
        return {
            "success": False,
            "error": str(e),
            "target": target
        }


def list_templates(
    tags: Optional[str] = None,
    severity: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lista los templates disponibles en Nuclei.

    Args:
        tags: Filtrar por tags
        severity: Filtrar por severidad

    Returns:
        Dict con lista de templates
    """
    try:
        cmd = [NUCLEI_PATH, "-tl"]
        
        if tags:
            cmd.extend(["-tags", tags])
        
        if severity:
            cmd.extend(["-severity", severity])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
            shell=True
        )
        
        templates = []
        # En Windows, la salida puede estar en stdout o stderr
        output = result.stdout if result.stdout.strip() else result.stderr
        if output:
            templates = [t for t in output.strip().split('\n') if t.strip()]
        
        return {
            "success": True,
            "templates": templates,
            "total_templates": len(templates)
        }
        
    except Exception as e:
        logger.error(f"Error listando templates: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def update_templates() -> Dict[str, Any]:
    """
    Actualiza los templates de Nuclei.

    Returns:
        Dict con resultado de la actualización
    """
    try:
        cmd = [NUCLEI_PATH, "-update-templates"]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
            shell=True
        )
        
        # Combinar stdout y stderr para mostrar todo el output
        output = result.stdout if result.stdout.strip() else ""
        if result.stderr and result.stderr.strip():
            output += "\n" + result.stderr if output else result.stderr
        
        return {
            "success": result.returncode == 0,
            "output": output.strip(),
            "return_code": result.returncode
        }
        
    except Exception as e:
        logger.error(f"Error actualizando templates: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def get_nuclei_version() -> Dict[str, Any]:
    """
    Obtiene la versión de Nuclei instalada.

    Returns:
        Dict con información de versión
    """
    try:
        cmd = [NUCLEI_PATH, "-version"]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
            shell=True  # Necesario en Windows para algunos comandos
        )
        
        # En Windows, Nuclei puede enviar la salida a stderr
        version_output = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()
        
        return {
            "success": True,
            "version": version_output,
            "nuclei_path": NUCLEI_PATH,
            "raw_stdout": result.stdout,
            "raw_stderr": result.stderr
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo versión: {e}")
        return {
            "success": False,
            "error": str(e),
            "nuclei_path": NUCLEI_PATH
        }
