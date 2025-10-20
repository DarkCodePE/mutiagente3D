"""
AGENTE MONSTRUO
Implementación del agente reflejo simple para monstruos
"""

import random
from typing import TYPE_CHECKING

from .ontology import Posicion

if TYPE_CHECKING:
    from .environment import EntornoHexaedrico


class AgenteMonstruo:
    """
    Agente reflejo simple
    - Movimiento aleatorio cada K iteraciones con probabilidad p
    - Sin memoria ni objetivos
    """
    
    def __init__(self, id: int, posicion: Posicion, entorno: 'EntornoHexaedrico', K: int = 3, p: float = 0.7):
        self.id = id
        self.posicion = posicion
        self.entorno = entorno
        self.K = K  # Frecuencia de operación
        self.p = p  # Probabilidad de movimiento
        self.vivo = True
    
    def ejecutar_ciclo(self, iteracion: int):
        """
        Lógica reflejo simple:
        Si (iteracion % K == 0) y random() < p → Mover aleatoriamente
        """
        if not self.vivo:
            return
        
        # Condición: cada K iteraciones
        if iteracion % self.K != 0:
            return
        
        # Acción: movimiento aleatorio con probabilidad p
        if random.random() < self.p:
            vecinos = self.entorno.obtener_vecinos(self.posicion)
            vecinos_validos = [v for v in vecinos if self.entorno.es_posicion_valida(v)]
            
            if vecinos_validos:
                nueva_pos = random.choice(vecinos_validos)
                self.posicion = nueva_pos
