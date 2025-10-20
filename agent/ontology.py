"""
ONTOLOGÍA DEL SISTEMA MULTI-AGENTE 3D
Definiciones conceptuales y estructuras de datos base
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict


class TipoCelda(Enum):
    """Tipos de celdas en el entorno"""
    ZONA_LIBRE = 0
    ZONA_VACIA = 1


class Orientacion(Enum):
    """Orientación del robot en el espacio 3D"""
    NORTE = (0, 1, 0)    # +Y
    SUR = (0, -1, 0)     # -Y
    ESTE = (1, 0, 0)     # +X
    OESTE = (-1, 0, 0)   # -X
    ARRIBA = (0, 0, 1)   # +Z
    ABAJO = (0, 0, -1)   # -Z
    
    def rotar_90(self, eje_rotacion: int = 0):
        """Rota 90 grados en uno de los 4 lados del robot"""
        rotaciones = {
            0: Orientacion.ESTE,
            1: Orientacion.NORTE,
            2: Orientacion.OESTE,
            3: Orientacion.SUR
        }
        if self in [Orientacion.ARRIBA, Orientacion.ABAJO]:
            return rotaciones.get(eje_rotacion, Orientacion.NORTE)
        return rotaciones.get(eje_rotacion, self)


@dataclass
class Posicion:
    """Posición en el espacio 3D"""
    x: int
    y: int
    z: int
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def distancia(self, otra: 'Posicion') -> float:
        """Distancia Manhattan"""
        return abs(self.x - otra.x) + abs(self.y - otra.y) + abs(self.z - otra.z)


@dataclass
class Percepcion:
    """Percepciones del agente Robot"""
    orientacion: Orientacion  # Giroscopio
    monstruo_cercano: bool    # Monstroscopio (5 lados, sin parte posterior)
    colision_zona_vacia: bool # Vacuscopio
    monstruo_en_celda: bool   # Energómetro Espectral
    robot_delante: bool       # Roboscanner
    iteracion: int


@dataclass
class MemoriaRobot:
    """Memoria interna del agente Robot"""
    percepciones_acciones: List[Tuple[Percepcion, str]] = field(default_factory=list)
    mapa_creencias: Dict[Posicion, str] = field(default_factory=dict)
    posicion_relativa: Posicion = field(default_factory=lambda: Posicion(0, 0, 0))
    zonas_vacias_conocidas: set = field(default_factory=set)
    ultima_posicion: Optional[Posicion] = None
    comunicaciones_robots: List[Tuple[int, str, str]] = field(default_factory=list)  # (iteracion, robot_id, accion)
    reglas_aprendidas: Dict[str, float] = field(default_factory=dict)  # Regla -> confianza
    metricas_racionalidad: Dict[str, float] = field(default_factory=dict)  # Métricas de rendimiento
