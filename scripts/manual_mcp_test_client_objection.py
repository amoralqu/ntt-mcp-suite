#!/usr/bin/env python3
"""
Script de prueba manual para el servidor MCP de Objection.
Permite probar las funcionalidades del servidor sin necesidad de un cliente MCP completo.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ntt_objection_mcp.tools import devices, applications, exploration


def print_separator():
    print("\n" + "="*80 + "\n")


def test_enumerate_devices():
    """Prueba la enumeración de dispositivos."""
    print("🔍 TEST: Enumerar dispositivos")
    print_separator()
    
    result = devices.enumerate_devices()
    print(f"Resultado: {result}")
    
    if isinstance(result, list):
        print(f"\n✅ Dispositivos encontrados: {len(result)}")
        for i, device in enumerate(result, 1):
            print(f"  {i}. {device.get('name')} (ID: {device.get('id')}, Tipo: {device.get('type')})")
    else:
        print(f"\n❌ Error: {result}")
    
    return result


def test_get_device(device_id=None):
    """Prueba obtener información de un dispositivo."""
    print("🔍 TEST: Obtener información de dispositivo")
    print_separator()
    
    result = devices.get_device(device_id)
    print(f"Resultado: {result}")
    
    if result.get('success'):
        print(f"\n✅ Dispositivo: {result.get('name')}")
        print(f"   ID: {result.get('id')}")
        print(f"   Tipo: {result.get('type')}")
    else:
        print(f"\n❌ Error: {result.get('error')}")
    
    return result


def test_list_applications(device_id=None):
    """Prueba listar aplicaciones."""
    print("🔍 TEST: Listar aplicaciones")
    print_separator()
    
    result = applications.list_applications(device_id)
    print(f"Tipo de resultado: {type(result)}")
    
    if isinstance(result, list):
        print(f"\n✅ Aplicaciones encontradas: {len(result)}")
        # Mostrar solo las primeras 10
        for i, app in enumerate(result[:10], 1):
            print(f"  {i}. {app.get('name')} ({app.get('identifier')})")
        if len(result) > 10:
            print(f"  ... y {len(result) - 10} más")
    else:
        print(f"\n❌ Error: {result}")
    
    return result


def test_get_frontmost_application(device_id=None):
    """Prueba obtener la aplicación en primer plano."""
    print("🔍 TEST: Obtener aplicación en primer plano")
    print_separator()
    
    result = applications.get_frontmost_application(device_id)
    print(f"Resultado: {result}")
    
    if result.get('success'):
        print(f"\n✅ Aplicación en primer plano:")
        print(f"   Nombre: {result.get('name')}")
        print(f"   Identificador: {result.get('identifier')}")
        print(f"   PID: {result.get('pid')}")
    else:
        print(f"\n⚠️  {result.get('error')}")
    
    return result


def test_explore_classes(app_identifier, device_id=None, pattern=None):
    """Prueba explorar clases de una aplicación."""
    print("🔍 TEST: Explorar clases")
    print_separator()
    print(f"App: {app_identifier}")
    if pattern:
        print(f"Patrón: {pattern}")
    
    result = exploration.explore_classes(app_identifier, device_id, pattern)
    print(f"\nTipo de resultado: {type(result)}")
    
    if result.get('success'):
        classes = result.get('classes', [])
        print(f"\n✅ Clases encontradas: {len(classes)}")
        # Mostrar solo las primeras 20
        for i, cls in enumerate(classes[:20], 1):
            print(f"  {i}. {cls}")
        if len(classes) > 20:
            print(f"  ... y {len(classes) - 20} más")
    else:
        print(f"\n❌ Error: {result.get('error')}")
    
    return result


def test_explore_activities(app_identifier, device_id=None):
    """Prueba explorar Activities de una aplicación Android."""
    print("🔍 TEST: Explorar Activities")
    print_separator()
    print(f"App: {app_identifier}")
    
    result = exploration.explore_activities(app_identifier, device_id)
    print(f"\nResultado: {result}")
    
    if result.get('success'):
        activities = result.get('activities', [])
        print(f"\n✅ Activities encontradas: {len(activities)}")
        for i, activity in enumerate(activities, 1):
            print(f"  {i}. {activity}")
    else:
        print(f"\n❌ Error: {result.get('error')}")
    
    return result


def main():
    """Función principal para ejecutar las pruebas."""
    print("\n" + "="*80)
    print("  PRUEBAS MANUALES - NTT OBJECTION MCP SERVER")
    print("="*80 + "\n")
    
    try:
        # 1. Enumerar dispositivos
        devices_result = test_enumerate_devices()
        input("\nPresiona Enter para continuar...")
        
        # 2. Obtener información del dispositivo local
        test_get_device()
        input("\nPresiona Enter para continuar...")
        
        # 3. Intentar obtener dispositivo USB (puede fallar si no hay uno conectado)
        print("🔍 TEST: Obtener dispositivo USB")
        print_separator()
        usb_result = devices.get_usb_device(timeout=3)
        print(f"Resultado: {usb_result}")
        input("\nPresiona Enter para continuar...")
        
        # 4. Listar aplicaciones
        print("\n¿Quieres listar aplicaciones de un dispositivo?")
        print("1. Dispositivo local")
        print("2. Dispositivo USB (si está conectado)")
        print("3. Saltar esta prueba")
        choice = input("Elige una opción (1-3): ").strip()
        
        if choice == "1":
            test_list_applications()
        elif choice == "2":
            if usb_result.get('success'):
                test_list_applications(usb_result.get('id'))
            else:
                print("❌ No hay dispositivo USB disponible")
        
        input("\nPresiona Enter para continuar...")
        
        # 5. Obtener aplicación en primer plano (requiere dispositivo real)
        print("\n¿Quieres obtener la aplicación en primer plano?")
        print("NOTA: Esto requiere un dispositivo real con una app en ejecución")
        if input("Continuar? (s/n): ").lower() == 's':
            test_get_frontmost_application()
        
        input("\nPresiona Enter para continuar...")
        
        # 6. Explorar clases (requiere app específica)
        print("\n¿Quieres explorar clases de una aplicación?")
        print("NOTA: Necesitas el identificador de la app y que esté en ejecución")
        if input("Continuar? (s/n): ").lower() == 's':
            app_id = input("Identificador de la aplicación (ej: com.android.settings): ").strip()
            if app_id:
                pattern = input("Patrón de búsqueda (opcional, Enter para todas): ").strip()
                test_explore_classes(app_id, pattern=pattern if pattern else None)
        
        input("\nPresiona Enter para continuar...")
        
        # 7. Explorar Activities
        print("\n¿Quieres explorar Activities de una aplicación Android?")
        if input("Continuar? (s/n): ").lower() == 's':
            app_id = input("Identificador de la aplicación: ").strip()
            if app_id:
                test_explore_activities(app_id)
        
        print_separator()
        print("✅ Pruebas completadas!")
        print_separator()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
