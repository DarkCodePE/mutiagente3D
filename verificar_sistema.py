"""
SCRIPT DE VERIFICACIÓN DEL SISTEMA
Verifica que todos los componentes estén funcionando correctamente
"""

import sys
import os
import subprocess

# Agregar path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verificar_requirements():
    """Verifica que requirements.txt exista y sea válido"""
    print("="*60)
    print("TEST 0: Verificando requirements.txt...")
    print("="*60)
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt no encontrado")
        return False
    
    try:
        # Intentar instalar dependencias
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ requirements.txt válido y dependencias instaladas")
            return True
        else:
            print(f"❌ Error instalando dependencias: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error verificando requirements: {e}")
        return False


def verificar_importaciones():
    """Verifica que todas las importaciones funcionen"""
    print("\n" + "="*60)
    print("TEST 1: Verificando importaciones...")
    print("="*60)
    
    try:
        from agent import (
            TipoCelda,
            Orientacion,
            Posicion,
            Percepcion,
            MemoriaRobot,
            EntornoHexaedrico,
            AgenteRobot,
            AgenteMonstruo,
            Simulador,
            VisualizadorPygame,
            ejecutar_simulacion,
            crear_experimento_personalizado
        )
        print("✅ Todas las importaciones correctas")
        return True
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False


def verificar_creacion_entorno():
    """Verifica que se pueda crear el entorno"""
    print("\n" + "="*60)
    print("TEST 2: Verificando creación de entorno...")
    print("="*60)
    
    try:
        from agent import EntornoHexaedrico
        
        entorno = EntornoHexaedrico(
            N=3,
            pfree=0.7,
            pvacio=0.3,
            n_robots=2,
            n_monstruos=2,
            seed=42
        )
        
        print(f"✅ Entorno creado: {entorno.N}x{entorno.N}x{entorno.N}")
        print(f"✅ Robots: {len(entorno.robots)}")
        print(f"✅ Monstruos: {len(entorno.monstruos)}")
        return True
    except Exception as e:
        print(f"❌ Error creando entorno: {e}")
        return False


def verificar_simulacion():
    """Verifica que la simulación funcione"""
    print("\n" + "="*60)
    print("TEST 3: Verificando simulación...")
    print("="*60)
    
    try:
        from agent import EntornoHexaedrico, Simulador
        
        entorno = EntornoHexaedrico(
            N=3, pfree=0.7, pvacio=0.3,
            n_robots=2, n_monstruos=2, seed=42
        )
        
        sim = Simulador(entorno)
        
        # Ejecutar solo 10 iteraciones
        for i in range(10):
            entorno.actualizar()
        
        stats = entorno.estadisticas()
        print(f"✅ Simulación ejecutada: {stats['iteracion']} iteraciones")
        print(f"✅ Robots vivos: {stats['robots_vivos']}")
        print(f"✅ Monstruos vivos: {stats['monstruos_vivos']}")
        return True
    except Exception as e:
        print(f"❌ Error en simulación: {e}")
        return False


def verificar_pygame():
    """Verifica que pygame esté instalado"""
    print("\n" + "="*60)
    print("TEST 4: Verificando pygame...")
    print("="*60)
    
    try:
        import pygame
        print(f"✅ Pygame instalado: versión {pygame.version.ver}")
        
        from agent import VisualizadorPygame
        print("✅ VisualizadorPygame importado correctamente")
        return True
    except ImportError:
        print("❌ Pygame no instalado")
        print("   Ejecutar: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error verificando pygame: {e}")
        return False


def verificar_archivos():
    """Verifica que todos los archivos existan"""
    print("\n" + "="*60)
    print("TEST 5: Verificando archivos del proyecto...")
    print("="*60)
    
    archivos_requeridos = [
        "requirements.txt",
        "setup.py",
        ".gitignore",
        "README.md",
        "agent/__init__.py",
        "agent/ontology.py",
        "agent/environment.py",
        "agent/robot_agent.py",
        "agent/monster_agent.py",
        "agent/simulator.py",
        "agent/visualizacion_pygame.py",
        "agent/main.py",
        "agent/demo_pygame.py",
        "agent/README.md"
    ]
    
    todos_ok = True
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} NO ENCONTRADO")
            todos_ok = False
    
    return todos_ok


def verificar_demos():
    """Verifica que los demos funcionen"""
    print("\n" + "="*60)
    print("TEST 6: Verificando demos...")
    print("="*60)
    
    try:
        # Verificar que el demo pygame se puede importar
        import agent.demo_pygame
        print("✅ demo_pygame.py importable")
        
        # Verificar que el main se puede importar
        import agent.main
        print("✅ main.py importable")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando demos: {e}")
        return False


def main():
    """Ejecuta todas las verificaciones"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   VERIFICACIÓN DEL SISTEMA MULTI-AGENTE 3D                   ║
    ║   Robots Monstruicidas - Test Suite Completo                ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    resultados = []
    
    # Ejecutar tests
    resultados.append(("Requirements.txt", verificar_requirements()))
    resultados.append(("Importaciones", verificar_importaciones()))
    resultados.append(("Creación entorno", verificar_creacion_entorno()))
    resultados.append(("Simulación", verificar_simulacion()))
    resultados.append(("Pygame", verificar_pygame()))
    resultados.append(("Archivos", verificar_archivos()))
    resultados.append(("Demos", verificar_demos()))
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE VERIFICACIÓN")
    print("="*60)
    
    tests_ok = sum(1 for _, resultado in resultados if resultado)
    tests_total = len(resultados)
    
    for nombre, resultado in resultados:
        estado = "✅ PASS" if resultado else "❌ FAIL"
        print(f"{nombre:.<40} {estado}")
    
    print("="*60)
    print(f"RESULTADO: {tests_ok}/{tests_total} tests pasados")
    
    if tests_ok == tests_total:
        print("\n🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("✅ Listo para uso y evaluación")
        print("\n📋 COMANDOS PARA USAR:")
        print("   python agent/demo_pygame.py    # Demo interactivo")
        print("   python agent/main.py           # Simulación consola")
        print("   pip install -r requirements.txt # Instalar dependencias")
    else:
        print("\n⚠️ Algunos tests fallaron")
        print("Revisar los errores anteriores")
    
    print("="*60)
    
    return tests_ok == tests_total


if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)
