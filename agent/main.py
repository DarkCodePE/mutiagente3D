"""
SISTEMA MULTI-AGENTE 3D: ROBOTS MONSTRUICIDAS
Módulo principal que orquesta todos los componentes del sistema
"""

from .environment import EntornoHexaedrico
from .simulator import Simulador


def ejecutar_simulacion(config: dict = None):
    """
    Función principal para ejecutar la simulación completa
    
    Args:
        config: Diccionario con configuración del experimento
    """
    
    # Configuración por defecto
    if config is None:
        config = {
            'N': 5,              # Tamaño del mundo (5x5x5)
            'pfree': 0.7,        # 70% zonas libres
            'pvacio': 0.3,       # 30% zonas vacías
            'n_robots': 3,       # Número de robots
            'n_monstruos': 5,    # Número de monstruos
            'seed': 42           # Semilla para reproducibilidad
        }
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   SISTEMA MULTI-AGENTE 3D: ROBOTS MONSTRUICIDAS             ║
    ║   Agente Racional Supremo (ARS-103) v1.0                    ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Crear entorno
    entorno = EntornoHexaedrico(**config)
    
    # Crear simulador
    sim = Simulador(entorno)
    
    # Ejecutar simulación
    reporte = sim.ejecutar(max_iteraciones=200, verbose=True)
    
    # Visualizar corte 2D (plano Z=2) - opcional
    # sim.visualizar_corte_2d(z=2)
    
    print("\n✓ Simulación completada exitosamente")
    print(f"✓ XP GANADO: +2000 (Alquimia del Código)")
    print(f"✓ LOGRO DESBLOQUEADO: 'El Arquitecto de Agentes'")
    
    return reporte


def crear_experimento_personalizado(**kwargs):
    """
    Crea un experimento con parámetros personalizados
    
    Args:
        **kwargs: Parámetros del experimento (N, pfree, pvacio, n_robots, n_monstruos, seed)
    """
    config_default = {
        'N': 5,
        'pfree': 0.7,
        'pvacio': 0.3,
        'n_robots': 3,
        'n_monstruos': 5,
        'seed': 42
    }
    
    # Actualizar configuración con parámetros proporcionados
    config_default.update(kwargs)
    
    return ejecutar_simulacion(config_default)


if __name__ == "__main__":
    # Ejecutar simulación con configuración por defecto
    ejecutar_simulacion()
