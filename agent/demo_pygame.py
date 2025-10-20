"""
DEMO PYGAME - Sistema Multi-Agente 3D
Demostración interactiva con visualización en tiempo real
"""

import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import EntornoHexaedrico, VisualizadorPygame


def demo_basico():
    """Demo básico con configuración estándar"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   SISTEMA MULTI-AGENTE 3D: ROBOTS MONSTRUICIDAS             ║
    ║   Demo Pygame - Visualización Interactiva                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Crear entorno
    entorno = EntornoHexaedrico(
        N=5,              # Mundo 5x5x5
        pfree=0.7,        # 70% zonas libres
        pvacio=0.3,       # 30% zonas vacías
        n_robots=3,       # 3 robots
        n_monstruos=5,    # 5 monstruos
        seed=42
    )
    
    # Crear visualizador
    visualizador = VisualizadorPygame(entorno, ancho=1200, alto=800)
    
    print("\n" + "="*60)
    print("CONTROLES:")
    print("="*60)
    print("  ESPACIO       - Pausar/Reanudar simulación")
    print("  ← →          - Rotar vista horizontal")
    print("  ↑ ↓          - Rotar vista vertical")
    print("  + -          - Zoom in/out")
    print("  ESC          - Salir")
    print("="*60)
    print("\nIniciando visualización...")
    
    # Ejecutar con visualización
    stats = visualizador.ejecutar_con_visualizacion(max_iteraciones=300)
    
    # Mostrar estadísticas finales
    print("\n" + "="*60)
    print("ESTADÍSTICAS FINALES")
    print("="*60)
    print(f"Iteraciones:          {stats['iteracion']}")
    print(f"Robots vivos:         {stats['robots_vivos']}")
    print(f"Monstruos vivos:      {stats['monstruos_vivos']}")
    print(f"Monstruos destruidos: {stats['monstruos_destruidos']}")
    print(f"Puntuación total:     {stats['puntuacion_total']}")
    print("="*60)


def demo_mundo_grande():
    """Demo con mundo más grande"""
    print("\n=== DEMO: MUNDO GRANDE 7x7x7 ===\n")
    
    entorno = EntornoHexaedrico(
        N=7,
        pfree=0.75,
        pvacio=0.25,
        n_robots=5,
        n_monstruos=8,
        seed=123
    )
    
    visualizador = VisualizadorPygame(entorno, ancho=1400, alto=900)
    visualizador.ejecutar_con_visualizacion(max_iteraciones=500)


def demo_mundo_pequeño():
    """Demo con mundo pequeño para ver detalles"""
    print("\n=== DEMO: MUNDO PEQUEÑO 3x3x3 ===\n")
    
    entorno = EntornoHexaedrico(
        N=3,
        pfree=0.8,
        pvacio=0.2,
        n_robots=2,
        n_monstruos=3,
        seed=789
    )
    
    visualizador = VisualizadorPygame(entorno, ancho=1000, alto=700)
    visualizador.zoom = 1.5  # Zoom inicial mayor para mundo pequeño
    visualizador.ejecutar_con_visualizacion(max_iteraciones=200)


def demo_muchos_agentes():
    """Demo con muchos robots y monstruos"""
    print("\n=== DEMO: MUCHOS AGENTES ===\n")
    
    entorno = EntornoHexaedrico(
        N=8,
        pfree=0.85,
        pvacio=0.15,
        n_robots=10,
        n_monstruos=15,
        seed=456
    )
    
    visualizador = VisualizadorPygame(entorno, ancho=1400, alto=900)
    visualizador.velocidad = 300  # Más rápido
    visualizador.ejecutar_con_visualizacion(max_iteraciones=1000)


def menu_principal():
    """Menú de selección de demos"""
    while True:
        print("\n" + "="*60)
        print("SISTEMA MULTI-AGENTE 3D - MENU PRINCIPAL")
        print("="*60)
        print("1. Demo Básico (5x5x5, 3 robots, 5 monstruos)")
        print("2. Demo Mundo Grande (7x7x7, 5 robots, 8 monstruos)")
        print("3. Demo Mundo Pequeño (3x3x3, 2 robots, 3 monstruos)")
        print("4. Demo Muchos Agentes (8x8x8, 10 robots, 15 monstruos)")
        print("0. Salir")
        print("="*60)
        
        try:
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                demo_basico()
            elif opcion == "2":
                demo_mundo_grande()
            elif opcion == "3":
                demo_mundo_pequeño()
            elif opcion == "4":
                demo_muchos_agentes()
            elif opcion == "0":
                print("\n¡Hasta luego!")
                break
            else:
                print("\n❌ Opción no válida. Intente nuevamente.")
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    # Si se pasa un argumento, ejecutar demo específico
    if len(sys.argv) > 1:
        demo_num = sys.argv[1]
        if demo_num == "1":
            demo_basico()
        elif demo_num == "2":
            demo_mundo_grande()
        elif demo_num == "3":
            demo_mundo_pequeño()
        elif demo_num == "4":
            demo_muchos_agentes()
        else:
            print(f"❌ Demo {demo_num} no existe")
    else:
        # Mostrar menú interactivo
        menu_principal()

