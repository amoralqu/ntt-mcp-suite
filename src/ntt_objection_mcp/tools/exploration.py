# src/ntt_objection_mcp/tools/exploration.py
from __future__ import annotations
from typing import Any, Dict, List, Optional
import frida
from ..config import logger
from . import state


def explore_classes(
    app_identifier: str,
    device_id: Optional[str] = None,
    pattern: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lista las clases disponibles en la aplicación.
    
    Args:
        app_identifier: Bundle identifier de la aplicación
        device_id: ID del dispositivo. Si es None, usa el dispositivo actual
        pattern: Patrón opcional para filtrar clases (ej: "com.example.*")
    
    Returns:
        Lista de clases encontradas
    """
    try:
        # Obtener dispositivo
        if device_id:
            device = frida.get_device(device_id)
        else:
            saved_device_id = state.get_device_id()
            device = frida.get_device(saved_device_id) if saved_device_id else frida.get_local_device()
        
        # Script para listar clases
        script_code = """
        Java.perform(function() {
            var classes = [];
            var pattern = %s;
            
            Java.enumerateLoadedClasses({
                onMatch: function(className) {
                    if (!pattern || className.indexOf(pattern) !== -1) {
                        classes.push(className);
                    }
                },
                onComplete: function() {
                    send({type: 'classes', data: classes});
                }
            });
        });
        """ % (f"'{pattern}'" if pattern else "null")
        
        # Crear sesión
        session = device.attach(app_identifier)
        script = session.create_script(script_code)
        
        result = {"classes": []}
        
        def on_message(message, data):
            if message['type'] == 'send':
                if message['payload']['type'] == 'classes':
                    result['classes'] = message['payload']['data']
        
        script.on('message', on_message)
        script.load()
        
        # Dar tiempo para que el script se ejecute
        import time
        time.sleep(2)
        
        session.detach()
        
        return {
            "success": True,
            "app_identifier": app_identifier,
            "pattern": pattern,
            "classes": result['classes']
        }
        
    except Exception as e:
        logger.error(f"Error exploring classes: {e}")
        return {"success": False, "error": str(e)}


def explore_methods(
    app_identifier: str,
    class_name: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lista los métodos de una clase específica.
    
    Args:
        app_identifier: Bundle identifier de la aplicación
        class_name: Nombre completo de la clase
        device_id: ID del dispositivo. Si es None, usa el dispositivo actual
    
    Returns:
        Lista de métodos de la clase
    """
    try:
        # Obtener dispositivo
        if device_id:
            device = frida.get_device(device_id)
        else:
            saved_device_id = state.get_device_id()
            device = frida.get_device(saved_device_id) if saved_device_id else frida.get_local_device()
        
        # Script para listar métodos
        script_code = """
        Java.perform(function() {
            try {
                var targetClass = Java.use('%s');
                var methods = [];
                
                var methodsArray = targetClass.class.getDeclaredMethods();
                for (var i = 0; i < methodsArray.length; i++) {
                    methods.push(methodsArray[i].toString());
                }
                
                send({type: 'methods', data: methods});
            } catch(e) {
                send({type: 'error', data: e.toString()});
            }
        });
        """ % class_name
        
        # Crear sesión
        session = device.attach(app_identifier)
        script = session.create_script(script_code)
        
        result = {"methods": [], "error": None}
        
        def on_message(message, data):
            if message['type'] == 'send':
                payload = message['payload']
                if payload['type'] == 'methods':
                    result['methods'] = payload['data']
                elif payload['type'] == 'error':
                    result['error'] = payload['data']
        
        script.on('message', on_message)
        script.load()
        
        # Dar tiempo para que el script se ejecute
        import time
        time.sleep(2)
        
        session.detach()
        
        if result['error']:
            return {
                "success": False,
                "error": result['error']
            }
        
        return {
            "success": True,
            "app_identifier": app_identifier,
            "class_name": class_name,
            "methods": result['methods']
        }
        
    except Exception as e:
        logger.error(f"Error exploring methods: {e}")
        return {"success": False, "error": str(e)}


def explore_activities(
    app_identifier: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lista las Activities de una aplicación Android.
    
    Args:
        app_identifier: Bundle identifier de la aplicación
        device_id: ID del dispositivo. Si es None, usa el dispositivo actual
    
    Returns:
        Lista de Activities encontradas
    """
    try:
        # Obtener dispositivo
        if device_id:
            device = frida.get_device(device_id)
        else:
            saved_device_id = state.get_device_id()
            device = frida.get_device(saved_device_id) if saved_device_id else frida.get_local_device()
        
        # Script para listar Activities
        script_code = """
        Java.perform(function() {
            try {
                var ActivityThread = Java.use('android.app.ActivityThread');
                var app = ActivityThread.currentApplication();
                var packageManager = app.getPackageManager();
                var packageInfo = packageManager.getPackageInfo(app.getPackageName(), 1); // GET_ACTIVITIES = 1
                
                var activities = [];
                var activityInfoArray = packageInfo.activities;
                
                if (activityInfoArray) {
                    for (var i = 0; i < activityInfoArray.length; i++) {
                        activities.push(activityInfoArray[i].name.value);
                    }
                }
                
                send({type: 'activities', data: activities});
            } catch(e) {
                send({type: 'error', data: e.toString()});
            }
        });
        """
        
        # Crear sesión
        session = device.attach(app_identifier)
        script = session.create_script(script_code)
        
        result = {"activities": [], "error": None}
        
        def on_message(message, data):
            if message['type'] == 'send':
                payload = message['payload']
                if payload['type'] == 'activities':
                    result['activities'] = payload['data']
                elif payload['type'] == 'error':
                    result['error'] = payload['data']
        
        script.on('message', on_message)
        script.load()
        
        # Dar tiempo para que el script se ejecute
        import time
        time.sleep(2)
        
        session.detach()
        
        if result['error']:
            return {
                "success": False,
                "error": result['error']
            }
        
        return {
            "success": True,
            "app_identifier": app_identifier,
            "activities": result['activities']
        }
        
    except Exception as e:
        logger.error(f"Error exploring activities: {e}")
        return {"success": False, "error": str(e)}


def explore_services(
    app_identifier: str,
    device_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lista los Services de una aplicación Android.
    
    Args:
        app_identifier: Bundle identifier de la aplicación
        device_id: ID del dispositivo. Si es None, usa el dispositivo actual
    
    Returns:
        Lista de Services encontrados
    """
    try:
        # Obtener dispositivo
        if device_id:
            device = frida.get_device(device_id)
        else:
            saved_device_id = state.get_device_id()
            device = frida.get_device(saved_device_id) if saved_device_id else frida.get_local_device()
        
        # Script para listar Services
        script_code = """
        Java.perform(function() {
            try {
                var ActivityThread = Java.use('android.app.ActivityThread');
                var app = ActivityThread.currentApplication();
                var packageManager = app.getPackageManager();
                var packageInfo = packageManager.getPackageInfo(app.getPackageName(), 4); // GET_SERVICES = 4
                
                var services = [];
                var serviceInfoArray = packageInfo.services;
                
                if (serviceInfoArray) {
                    for (var i = 0; i < serviceInfoArray.length; i++) {
                        services.push(serviceInfoArray[i].name.value);
                    }
                }
                
                send({type: 'services', data: services});
            } catch(e) {
                send({type: 'error', data: e.toString()});
            }
        });
        """
        
        # Crear sesión
        session = device.attach(app_identifier)
        script = session.create_script(script_code)
        
        result = {"services": [], "error": None}
        
        def on_message(message, data):
            if message['type'] == 'send':
                payload = message['payload']
                if payload['type'] == 'services':
                    result['services'] = payload['data']
                elif payload['type'] == 'error':
                    result['error'] = payload['data']
        
        script.on('message', on_message)
        script.load()
        
        # Dar tiempo para que el script se ejecute
        import time
        time.sleep(2)
        
        session.detach()
        
        if result['error']:
            return {
                "success": False,
                "error": result['error']
            }
        
        return {
            "success": True,
            "app_identifier": app_identifier,
            "services": result['services']
        }
        
    except Exception as e:
        logger.error(f"Error exploring services: {e}")
        return {"success": False, "error": str(e)}
