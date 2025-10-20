"""
ENTORNO HEXAEDRICO 3D
Gestión del mundo de operación para robots y monstruos
"""

import random
import numpy as np
from typing import List, Dict, TYPE_CHECKING

from .ontology import TipoCelda, Posicion

if TYPE_CHECKING:
    from .robot_agent import AgenteRobot
    from .monster_agent import AgenteMonstruo


class EntornoHexaedrico:
    """
    Entorno de operación 3D
    - Mundo NxNxN con zonas libres y vacías
    - Rodeado por zona vacía impenetrable
    """
    
    def __init__(self, N: int, pfree: float, pvacio: float, 
                 n_robots: int, n_monstruos: int, seed: int = None):
        if seed:
            random.seed(seed)
            np.random.seed(seed)
        
        self.N = N
        self.pfree = pfree
        self.pvacio = pvacio
        self.iteracion = 0
        
        # Crear grid 3D (0=libre, 1=vacío)
        self.grid = np.zeros((N, N, N), dtype=int)
        
        # Generar zonas vacías aleatoriamente
        total_celdas = N * N * N
        n_vacias = int(total_celdas * pvacio)
        
        posiciones_todas = [(x, y, z) for x in range(N) for y in range(N) for z in range(N)]
        posiciones_vacias = random.sample(posiciones_todas, n_vacias)
        
        for x, y, z in posiciones_vacias:
            self.grid[x, y, z] = TipoCelda.ZONA_VACIA.value
        
        # Inicializar agentes
        self.robots: List['AgenteRobot'] = []
        self.monstruos: List['AgenteMonstruo'] = []
        
        # Colocar robots
        posiciones_libres = [(x, y, z) for x, y, z in posiciones_todas 
                             if self.grid[x, y, z] == TipoCelda.ZONA_LIBRE.value]
        
        # Importar aquí para evitar importaciones circulares
        from .ontology import Orientacion
        from .robot_agent import AgenteRobot
        from .monster_agent import AgenteMonstruo
        
        for i in range(n_robots):
            if not posiciones_libres:
                break
            pos = random.choice(posiciones_libres)
            posiciones_libres.remove(pos)
            
            orientacion = random.choice(list(Orientacion))
            robot = AgenteRobot(i, Posicion(*pos), orientacion, self)
            self.robots.append(robot)
        
        # Colocar monstruos
        for i in range(n_monstruos):
            if not posiciones_libres:
                break
            pos = random.choice(posiciones_libres)
            posiciones_libres.remove(pos)
            
            monstruo = AgenteMonstruo(i, Posicion(*pos), self)
            self.monstruos.append(monstruo)
        
        print(f"✓ Entorno creado: {N}x{N}x{N}")
        print(f"  - Zonas vacías: {n_vacias} ({pvacio*100:.1f}%)")
        print(f"  - Robots: {len(self.robots)}")
        print(f"  - Monstruos: {len(self.monstruos)}")
    
    def es_posicion_valida(self, pos: Posicion) -> bool:
        """Verifica si una posición está dentro de los límites y es zona libre"""
        if pos.x < 0 or pos.x >= self.N or pos.y < 0 or pos.y >= self.N or pos.z < 0 or pos.z >= self.N:
            return False  # Fuera del mundo (zona vacía impenetrable)
        return self.grid[pos.x, pos.y, pos.z] == TipoCelda.ZONA_LIBRE.value
    
    def obtener_vecinos(self, pos: Posicion) -> List[Posicion]:
        """Obtiene las 6 posiciones adyacentes (sin diagonales)"""
        vecinos = []
        for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
            nueva_pos = Posicion(pos.x + dx, pos.y + dy, pos.z + dz)
            vecinos.append(nueva_pos)
        return vecinos
    
    def hay_monstruo_en(self, pos: Posicion) -> bool:
        """Verifica si hay un monstruo en la posición"""
        return any(m.posicion == pos and m.vivo for m in self.monstruos)
    
    def hay_robot_en(self, pos: Posicion) -> bool:
        """Verifica si hay un robot en la posición"""
        return any(r.posicion == pos and r.vivo for r in self.robots)
    
    def actualizar(self):
        """Ejecuta una iteración del entorno"""
        self.iteracion += 1
        
        # Primero, todos los robots perciben y deciden
        for robot in [r for r in self.robots if r.vivo]:
            robot.ejecutar_ciclo()
        
        # Luego, los monstruos actúan según su frecuencia
        for monstruo in [m for m in self.monstruos if m.vivo]:
            monstruo.ejecutar_ciclo(self.iteracion)
    
    def estadisticas(self) -> Dict:
        """Retorna estadísticas del estado actual"""
        return {
            'iteracion': self.iteracion,
            'robots_vivos': sum(1 for r in self.robots if r.vivo),
            'monstruos_vivos': sum(1 for m in self.monstruos if m.vivo),
            'monstruos_destruidos': sum(r.monstruos_destruidos for r in self.robots),
            'puntuacion_total': sum(r.puntuacion for r in self.robots)
        }
