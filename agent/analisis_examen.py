"""
ANÁLISIS PARA EXAMEN MIA-103
Módulo específico para análisis de racionalidad, episodios y cumplimiento de requisitos
"""

from typing import Dict, List, Tuple
import numpy as np
from .ontology import Posicion, Orientacion
from .robot_agent import AgenteRobot
from .monster_agent import AgenteMonstruo


class AnalizadorExamen:
    """
    Analizador específico para cumplir con los requisitos del examen MIA-103
    """
    
    def __init__(self, entorno):
        self.entorno = entorno
        self.historial_analisis = []
    
    def analizar_racionalidad_agente(self, robot: AgenteRobot) -> Dict:
        """
        Análisis detallado de racionalidad del agente robot
        Cumple con requisito: "Defina una medida de racionalidad del agente robot"
        """
        racionalidad = robot.calcular_racionalidad()
        
        # Análisis de componentes de racionalidad
        movimientos_exitosos = robot.memoria.metricas_racionalidad.get('movimientos_exitosos', 0)
        colisiones = robot.memoria.metricas_racionalidad.get('colisiones', 0)
        total_movimientos = movimientos_exitosos + colisiones
        
        efectividad = movimientos_exitosos / max(total_movimientos, 1) if total_movimientos > 0 else 0
        eficiencia_caza = robot.memoria.metricas_racionalidad.get('acciones_caza', 0) / max(len(robot.memoria.percepciones_acciones), 1)
        adaptabilidad = len(robot.memoria.reglas_aprendidas) / 10.0
        comunicacion = robot.memoria.metricas_racionalidad.get('comunicaciones_exitosas', 0) / max(len(robot.memoria.percepciones_acciones), 1)
        
        return {
            'racionalidad_total': racionalidad,
            'efectividad_movimiento': efectividad,
            'eficiencia_caza': eficiencia_caza,
            'adaptabilidad': min(adaptabilidad, 1.0),
            'eficiencia_comunicacion': comunicacion,
            'reglas_aprendidas': len(robot.memoria.reglas_aprendidas),
            'total_acciones': len(robot.memoria.percepciones_acciones),
            'monstruos_destruidos': robot.monstruos_destruidos,
            'puntuacion': robot.puntuacion
        }
    
    def analizar_episodico(self, robot: AgenteRobot, ventana: int = 15) -> Dict:
        """
        Análisis de si el agente es episódico
        Cumple con requisito: "¿Entra a bucle infinito?"
        """
        en_bucle = robot.detectar_bucle_infinito(ventana)
        
        # Análisis más detallado de patrones
        percepciones_acciones = robot.memoria.percepciones_acciones
        if len(percepciones_acciones) < ventana:
            return {
                'es_episodico': True,
                'en_bucle_infinito': False,
                'patrones_detectados': 0,
                'variabilidad_acciones': 1.0,
                'razon': 'Datos insuficientes'
            }
        
        # Obtener últimas acciones
        ultimas_acciones = [accion for _, accion in percepciones_acciones[-ventana:]]
        
        # Calcular variabilidad de acciones
        acciones_unicas = len(set(ultimas_acciones))
        variabilidad = acciones_unicas / len(ultimas_acciones)
        
        # Detectar patrones repetitivos
        patrones = {}
        for i in range(len(ultimas_acciones) - 2):
            patron = tuple(ultimas_acciones[i:i+3])
            patrones[patron] = patrones.get(patron, 0) + 1
        
        patrones_repetidos = sum(1 for count in patrones.values() if count >= 2)
        
        # Determinar si es episódico
        es_episodico = not en_bucle and variabilidad > 0.3
        
        return {
            'es_episodico': es_episodico,
            'en_bucle_infinito': en_bucle,
            'patrones_detectados': patrones_repetidos,
            'variabilidad_acciones': variabilidad,
            'razon': 'Bucle detectado' if en_bucle else ('Baja variabilidad' if variabilidad <= 0.3 else 'Episódico normal')
        }
    
    def analizar_ambiente_por_agente(self) -> Dict:
        """
        Análisis del ambiente según criterios AIMA
        Cumple con requisito: "Según los criterios dados por el AIMA, describa el ambiente por cada agente"
        """
        return {
            'robot': {
                'accesible': False,  # No puede ver todo el mundo
                'no_accesible': True,  # Solo percibe localmente
                'determinista': False,  # Monstruos se mueven aleatoriamente
                'no_determinista': True,
                'episodico': self._verificar_episodico_robot(),
                'no_episodico': not self._verificar_episodico_robot(),
                'estatico': False,  # Monstruos se mueven
                'dinamico': True,
                'discreto': True,  # Posiciones discretas
                'continuo': False
            },
            'monstruo': {
                'accesible': False,  # No percibe nada
                'no_accesible': True,
                'determinista': True,  # Solo se mueve aleatoriamente
                'no_determinista': False,
                'episodico': True,  # Cada movimiento es independiente
                'no_episodico': False,
                'estatico': False,  # Se mueve
                'dinamico': True,
                'discreto': True,
                'continuo': False
            }
        }
    
    def _verificar_episodico_robot(self) -> bool:
        """Verifica si el robot es episódico analizando todos los robots vivos"""
        robots_vivos = [r for r in self.entorno.robots if r.vivo]
        if not robots_vivos:
            return True
        
        # Si al menos un robot no está en bucle, el sistema es episódico
        for robot in robots_vivos:
            if not robot.detectar_bucle_infinito():
                return True
        return False
    
    def generar_tabla_percepcion_accion(self, robot: AgenteRobot) -> List[Dict]:
        """
        Genera tabla percepción-acción del agente
        Cumple con requisito: "Defina la tabla percepción-acción de cada agente"
        """
        tabla = []
        percepciones_acciones = robot.memoria.percepciones_acciones
        
        for i, (percepcion, accion) in enumerate(percepciones_acciones):
            entrada = {
                'iteracion': i + 1,
                'orientacion': percepcion.orientacion.name,
                'monstruo_cercano': percepcion.monstruo_cercano,
                'monstruo_en_celda': percepcion.monstruo_en_celda,
                'robot_delante': percepcion.robot_delante,
                'colision_zona_vacia': percepcion.colision_zona_vacia,
                'accion_ejecutada': accion,
                'efectividad': robot._evaluar_efectividad_accion(percepcion, accion)
            }
            tabla.append(entrada)
        
        return tabla
    
    def analizar_mapeo_percepcion_accion(self, robot: AgenteRobot) -> Dict:
        """
        Análisis del mapeo percepción-acción
        Cumple con requisito: "Precise de qué forma puede usar el agente esta información"
        """
        percepciones_acciones = robot.memoria.percepciones_acciones
        
        if not percepciones_acciones:
            return {
                'total_entradas': 0,
                'patrones_identificados': 0,
                'reglas_aprendidas': 0,
                'efectividad_promedio': 0.0,
                'uso_memoria': 'Ninguna'
            }
        
        # Analizar patrones en el mapeo
        patrones = {}
        efectividades = []
        
        for percepcion, accion in percepciones_acciones:
            clave = f"{percepcion.monstruo_cercano}_{percepcion.robot_delante}_{percepcion.monstruo_en_celda}_{percepcion.colision_zona_vacia}"
            patrones[clave] = patrones.get(clave, 0) + 1
            efectividad = robot._evaluar_efectividad_accion(percepcion, accion)
            efectividades.append(efectividad)
        
        return {
            'total_entradas': len(percepciones_acciones),
            'patrones_identificados': len(patrones),
            'reglas_aprendidas': len(robot.memoria.reglas_aprendidas),
            'efectividad_promedio': sum(efectividades) / len(efectividades),
            'uso_memoria': 'Aprendizaje activo' if robot.memoria.reglas_aprendidas else 'Solo almacenamiento'
        }
    
    def generar_reporte_completo(self) -> Dict:
        """
        Genera reporte completo para el examen
        Incluye todos los análisis requeridos
        """
        reporte = {
            'resumen_general': self.entorno.estadisticas(),
            'analisis_racionalidad': {},
            'analisis_episodico': {},
            'analisis_ambiente': self.analizar_ambiente_por_agente(),
            'tablas_percepcion_accion': {},
            'mapeo_percepcion_accion': {}
        }
        
        # Análisis por cada robot
        for robot in self.entorno.robots:
            if robot.vivo:
                robot_id = f"robot_{robot.id}"
                reporte['analisis_racionalidad'][robot_id] = self.analizar_racionalidad_agente(robot)
                reporte['analisis_episodico'][robot_id] = self.analizar_episodico(robot)
                reporte['tablas_percepcion_accion'][robot_id] = self.generar_tabla_percepcion_accion(robot)
                reporte['mapeo_percepcion_accion'][robot_id] = self.analizar_mapeo_percepcion_accion(robot)
        
        return reporte
    
    def imprimir_reporte_examen(self):
        """
        Imprime reporte formateado para el examen
        """
        reporte = self.generar_reporte_completo()
        
        print("\n" + "="*80)
        print("REPORTE DE ANÁLISIS PARA EXAMEN MIA-103")
        print("="*80)
        
        # Resumen general
        print("\n1. RESUMEN GENERAL DEL ENTORNO:")
        print("-" * 40)
        stats = reporte['resumen_general']
        print(f"Iteraciones totales: {stats['iteracion']}")
        print(f"Robots vivos: {stats['robots_vivos']}")
        print(f"Monstruos vivos: {stats['monstruos_vivos']}")
        print(f"Monstruos destruidos: {stats['monstruos_destruidos']}")
        
        # Análisis de racionalidad
        print("\n2. ANÁLISIS DE RACIONALIDAD DE AGENTES:")
        print("-" * 40)
        for robot_id, analisis in reporte['analisis_racionalidad'].items():
            print(f"\n{robot_id.upper()}:")
            print(f"  Racionalidad total: {analisis['racionalidad_total']:.3f}")
            print(f"  Efectividad movimiento: {analisis['efectividad_movimiento']:.3f}")
            print(f"  Eficiencia caza: {analisis['eficiencia_caza']:.3f}")
            print(f"  Adaptabilidad: {analisis['adaptabilidad']:.3f}")
            print(f"  Reglas aprendidas: {analisis['reglas_aprendidas']}")
        
        # Análisis episódico
        print("\n3. ANÁLISIS EPISÓDICO:")
        print("-" * 40)
        for robot_id, analisis in reporte['analisis_episodico'].items():
            print(f"\n{robot_id.upper()}:")
            print(f"  Es episódico: {analisis['es_episodico']}")
            print(f"  En bucle infinito: {analisis['en_bucle_infinito']}")
            print(f"  Variabilidad acciones: {analisis['variabilidad_acciones']:.3f}")
            print(f"  Razón: {analisis['razon']}")
        
        # Análisis de ambiente
        print("\n4. ANÁLISIS DE AMBIENTE (CRITERIOS AIMA):")
        print("-" * 40)
        ambiente = reporte['analisis_ambiente']
        print("ROBOT:")
        for criterio, valor in ambiente['robot'].items():
            print(f"  {criterio}: {valor}")
        print("MONSTRUO:")
        for criterio, valor in ambiente['monstruo'].items():
            print(f"  {criterio}: {valor}")
        
        print("\n" + "="*80)
        print("FIN DEL REPORTE")
        print("="*80)



