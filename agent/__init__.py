"""
SISTEMA MULTI-AGENTE 3D: ROBOTS MONSTRUICIDAS
Paquete modularizado para el examen parcial de Fundamentos de IA

Módulos:
- ontology: Definiciones conceptuales y estructuras de datos
- environment: Entorno hexaédrico 3D
- robot_agent: Agente robot con memoria interna
- monster_agent: Agente monstruo reflejo simple
- simulator: Controlador de simulación y visualización
- main: Módulo principal que orquesta todo el sistema
"""

from .ontology import (
    TipoCelda,
    Orientacion,
    Posicion,
    Percepcion,
    MemoriaRobot
)

from .environment import EntornoHexaedrico
from .robot_agent import AgenteRobot
from .monster_agent import AgenteMonstruo
from .simulator import Simulador
from .visualizacion_pygame import VisualizadorPygame
from .analisis_examen import AnalizadorExamen
from .main import ejecutar_simulacion, crear_experimento_personalizado

__version__ = "1.0.0"
__author__ = "Agente Racional Supremo (ARS-103)"

__all__ = [
    # Ontología
    'TipoCelda',
    'Orientacion', 
    'Posicion',
    'Percepcion',
    'MemoriaRobot',
    
    # Entorno
    'EntornoHexaedrico',
    
    # Agentes
    'AgenteRobot',
    'AgenteMonstruo',
    
    # Simulación
    'Simulador',
    'VisualizadorPygame',
    'AnalizadorExamen',
    
    # Funciones principales
    'ejecutar_simulacion',
    'crear_experimento_personalizado'
]
