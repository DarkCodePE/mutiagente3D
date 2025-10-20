"""
SIMULADOR Y VISUALIZACIÓN
Controlador de simulación y herramientas de visualización
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, TYPE_CHECKING

from .ontology import TipoCelda

if TYPE_CHECKING:
    from .environment import EntornoHexaedrico


class Simulador:
    """Controlador de la simulación"""
    
    def __init__(self, entorno: 'EntornoHexaedrico'):
        self.entorno = entorno
        self.historial_estadisticas = []
    
    def ejecutar(self, max_iteraciones: int = 100, verbose: bool = True):
        """Ejecuta la simulación"""
        print(f"\n{'='*60}")
        print(f"INICIANDO SIMULACIÓN - Máximo {max_iteraciones} iteraciones")
        print(f"{'='*60}\n")
        
        for i in range(max_iteraciones):
            # Condición de parada: todos los monstruos destruidos o robots muertos
            stats = self.entorno.estadisticas()
            self.historial_estadisticas.append(stats)
            
            if verbose and i % 10 == 0:
                print(f"Iter {stats['iteracion']:3d} | Robots: {stats['robots_vivos']} | "
                      f"Monstruos: {stats['monstruos_vivos']} | "
                      f"Destruidos: {stats['monstruos_destruidos']} | "
                      f"Puntuación: {stats['puntuacion_total']}")
            
            if stats['monstruos_vivos'] == 0:
                print(f"\n🎉 ¡MISIÓN CUMPLIDA! Todos los monstruos destruidos en {stats['iteracion']} iteraciones")
                break
            
            if stats['robots_vivos'] == 0:
                print(f"\n💀 MISIÓN FALLIDA: Todos los robots destruidos. Quedan {stats['monstruos_vivos']} monstruos")
                break
            
            # Actualizar entorno
            self.entorno.actualizar()
        
        return self.generar_reporte()
    
    def generar_reporte(self) -> Dict:
        """Genera reporte final con métricas"""
        stats_final = self.entorno.estadisticas()
        
        # Calcular métricas de racionalidad
        racionalidad_robots = []
        bucles_detectados = 0
        
        for robot in self.entorno.robots:
            if robot.vivo:
                racionalidad = robot.calcular_racionalidad()
                racionalidad_robots.append(racionalidad)
                
                if robot.detectar_bucle_infinito():
                    bucles_detectados += 1
        
        racionalidad_promedio = sum(racionalidad_robots) / max(len(racionalidad_robots), 1)
        
        reporte = {
            'iteraciones_totales': stats_final['iteracion'],
            'monstruos_destruidos': stats_final['monstruos_destruidos'],
            'tasa_exito': stats_final['monstruos_destruidos'] / len(self.entorno.monstruos) * 100,
            'robots_supervivientes': stats_final['robots_vivos'],
            'puntuacion_final': stats_final['puntuacion_total'],
            'eficiencia': stats_final['monstruos_destruidos'] / max(stats_final['iteracion'], 1),
            'racionalidad_promedio': racionalidad_promedio,
            'bucles_infinitos_detectados': bucles_detectados,
            'es_episodico': bucles_detectados == 0
        }
        
        print(f"\n{'='*60}")
        print("REPORTE FINAL")
        print(f"{'='*60}")
        for key, value in reporte.items():
            if isinstance(value, float):
                print(f"{key:.<40} {value:.3f}")
            else:
                print(f"{key:.<40} {value}")
        print(f"{'='*60}\n")
        
        # Reporte detallado de racionalidad por robot
        print("ANÁLISIS DE RACIONALIDAD POR ROBOT:")
        print("-" * 50)
        for i, robot in enumerate(self.entorno.robots):
            if robot.vivo:
                racionalidad = robot.calcular_racionalidad()
                en_bucle = robot.detectar_bucle_infinito()
                reglas_aprendidas = len(robot.memoria.reglas_aprendidas)
                print(f"Robot-{robot.id}: Racionalidad={racionalidad:.3f}, "
                      f"Reglas={reglas_aprendidas}, Bucle={'Sí' if en_bucle else 'No'}")
        print("-" * 50)
        
        return reporte
    
    def visualizar_corte_2d(self, z: int = 0):
        """Visualiza un corte 2D del mundo en el plano Z"""
        fig, ax = plt.subplots(figsize=(10, 10))
        N = self.entorno.N
        
        # Crear matriz de visualización
        visual = np.zeros((N, N, 3))
        
        for x in range(N):
            for y in range(N):
                if self.entorno.grid[x, y, z] == TipoCelda.ZONA_VACIA.value:
                    visual[y, x] = [0.2, 0.2, 0.2]  # Gris para vacío
                else:
                    visual[y, x] = [1, 1, 1]  # Blanco para libre
        
        # Agregar robots (azul)
        for robot in self.entorno.robots:
            if robot.vivo and robot.posicion.z == z:
                visual[robot.posicion.y, robot.posicion.x] = [0, 0, 1]
        
        # Agregar monstruos (rojo)
        for monstruo in self.entorno.monstruos:
            if monstruo.vivo and monstruo.posicion.z == z:
                visual[monstruo.posicion.y, monstruo.posicion.x] = [1, 0, 0]
        
        ax.imshow(visual)
        ax.set_title(f'Corte Z={z} | Iter={self.entorno.iteracion} | '
                     f'Robots={sum(1 for r in self.entorno.robots if r.vivo)} | '
                     f'Monstruos={sum(1 for m in self.entorno.monstruos if m.vivo)}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        plt.grid(True, alpha=0.3)
        plt.show()
