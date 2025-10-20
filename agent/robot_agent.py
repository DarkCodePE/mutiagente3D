"""
AGENTE ROBOT MONSTRUICIDA
Implementación del agente con memoria interna para robots
"""

import random
from typing import TYPE_CHECKING

from .ontology import Posicion, Orientacion, Percepcion, MemoriaRobot

if TYPE_CHECKING:
    from .environment import EntornoHexaedrico


class AgenteRobot:
    """
    Agente con memoria interna (basado en modelo)
    - Mantiene creencias sobre el mundo
    - Usa historial percepción-acción
    - Aplica reglas jerárquicas
    """
    
    def __init__(self, id: int, posicion: Posicion, orientacion: Orientacion, entorno: 'EntornoHexaedrico'):
        self.id = id
        self.posicion = posicion
        self.orientacion = orientacion
        self.entorno = entorno
        self.vivo = True
        
        # Memoria interna
        self.memoria = MemoriaRobot()
        self.memoria.posicion_relativa = Posicion(0, 0, 0)
        self.memoria.ultima_posicion = posicion
        
        # Métricas de rendimiento
        self.puntuacion = 0
        self.monstruos_destruidos = 0
        self.movimientos = 0
        self.colisiones = 0
    
    def percibir(self) -> Percepcion:
        """
        Obtiene percepciones del entorno usando sensores
        """
        # Giroscopio: orientación actual
        orientacion_actual = self.orientacion
        
        # Energómetro Espectral: monstruo en mi celda
        monstruo_en_celda = self.entorno.hay_monstruo_en(self.posicion)
        
        # Monstroscopio: monstruo en 5 lados (sin parte posterior)
        monstruo_cercano = False
        pos_adelante = self._calcular_posicion_adelante()
        vecinos = self.entorno.obtener_vecinos(self.posicion)
        
        # Excluir la parte posterior
        pos_atras = self._calcular_posicion_atras()
        vecinos_visibles = [v for v in vecinos if v != pos_atras]
        
        for vecino in vecinos_visibles:
            if self.entorno.es_posicion_valida(vecino) and self.entorno.hay_monstruo_en(vecino):
                monstruo_cercano = True
                break
        
        # Roboscanner: robot delante
        robot_delante = (self.entorno.es_posicion_valida(pos_adelante) and 
                        self.entorno.hay_robot_en(pos_adelante))
        
        # Vacuscopio: se activa cuando choca (lo detectaremos en la acción)
        colision_zona_vacia = False
        
        return Percepcion(
            orientacion=orientacion_actual,
            monstruo_cercano=monstruo_cercano,
            colision_zona_vacia=colision_zona_vacia,
            monstruo_en_celda=monstruo_en_celda,
            robot_delante=robot_delante,
            iteracion=self.entorno.iteracion
        )
    
    def decidir_accion(self, percepcion: Percepcion) -> str:
        """
        Lógica de decisión con reglas jerárquicas
        
        JERARQUÍA DE REGLAS:
        1. Si monstruo en celda → VACUUMATOR (destruir)
        2. Si robot delante → COMUNICAR_EVADIR (protocolo coordinado)
        3. Si monstruo cercano → EXPLORAR_MONSTRUO (caza)
        4. Si memoria indica zona peligrosa → EVITAR
        5. Si no → EXPLORAR (búsqueda sistemática)
        """
        
        # REGLA 1: Destruir monstruo (PRIORIDAD MÁXIMA)
        if percepcion.monstruo_en_celda:
            return "VACUUMATOR"
        
        # REGLA 2: Protocolo de evasión con otro robot
        if percepcion.robot_delante:
            return self._protocolo_comunicacion_robot()
        
        # REGLA 3: Caza de monstruo cercano
        if percepcion.monstruo_cercano:
            # Explorar las 5 direcciones visibles
            return self._estrategia_caza()
        
        # REGLA 4: Exploración sistemática
        return self._estrategia_exploracion()
    
    def _protocolo_comunicacion_robot(self) -> str:
        """
        Protocolo de comunicación robot-robot según especificaciones del examen:
        - Ambos rotan 90° O
        - Uno continúa de frente y el otro rota 90° a algún lado
        """
        # Obtener robot delante
        pos_adelante = self._calcular_posicion_adelante()
        robot_delante = None
        for robot in self.entorno.robots:
            if robot.vivo and robot.posicion == pos_adelante and robot.id != self.id:
                robot_delante = robot
                break
        
        if not robot_delante:
            return "ROTAR_90"  # Fallback
        
        # Protocolo basado en ID para consistencia
        if self.id < robot_delante.id:
            # Robot con ID menor: continúa de frente
            return "MOVER_ADELANTE"
        else:
            # Robot con ID mayor: rota 90°
            return "ROTAR_90"
    
    def _estrategia_caza(self) -> str:
        """Estrategia cuando hay monstruo cercano"""
        # Intentar moverse hacia direcciones no exploradas
        pos_adelante = self._calcular_posicion_adelante()
        
        if pos_adelante not in self.memoria.zonas_vacias_conocidas:
            if self.entorno.es_posicion_valida(pos_adelante):
                return "MOVER_ADELANTE"
        
        # Si adelante no es viable, rotar para explorar
        return "ROTAR_90"
    
    def _estrategia_exploracion(self) -> str:
        """Estrategia de exploración cuando no hay monstruos cerca"""
        pos_adelante = self._calcular_posicion_adelante()
        
        # Evitar zonas vacías conocidas
        if pos_adelante in self.memoria.zonas_vacias_conocidas:
            return "ROTAR_90"
        
        # Preferir moverse a zonas no visitadas
        if pos_adelante not in self.memoria.mapa_creencias:
            return "MOVER_ADELANTE"
        
        # Si ya visitamos esa celda, explorar otra dirección
        if random.random() < 0.3:
            return "ROTAR_90"
        
        return "MOVER_ADELANTE"
    
    def ejecutar_accion(self, accion: str, percepcion: Percepcion):
        """Ejecuta la acción decidida y actualiza el mundo"""
        
        if accion == "VACUUMATOR":
            # Destruir monstruo y autodestruirse
            for monstruo in self.entorno.monstruos:
                if monstruo.posicion == self.posicion and monstruo.vivo:
                    monstruo.vivo = False
                    self.monstruos_destruidos += 1
                    self.puntuacion += 1000
                    print(f"  🎯 Robot-{self.id} destruyó Monstruo-{monstruo.id} en {self.posicion}")
                    break
            
            # El robot también se destruye
            self.vivo = False
            self.puntuacion -= 1000
            print(f"  💀 Robot-{self.id} se autodestruyó")
        
        elif accion == "MOVER_ADELANTE":
            pos_adelante = self._calcular_posicion_adelante()
            
            if self.entorno.es_posicion_valida(pos_adelante):
                # Actualizar posición relativa en memoria
                dx, dy, dz = self.orientacion.value
                self.memoria.posicion_relativa.x += dx
                self.memoria.posicion_relativa.y += dy
                self.memoria.posicion_relativa.z += dz
                
                self.memoria.ultima_posicion = self.posicion
                self.posicion = pos_adelante
                self.movimientos += 1
                self.puntuacion -= 10
                
                # Actualizar creencias: marcar como visitado
                self.memoria.mapa_creencias[pos_adelante] = "visitado"
            else:
                # Colisión con Zona Vacía (Vacuscopio activado)
                self.memoria.zonas_vacias_conocidas.add(pos_adelante)
                self.memoria.mapa_creencias[pos_adelante] = "zona_vacia"
                self.colisiones += 1
                self.puntuacion -= 50
                percepcion.colision_zona_vacia = True
        
        elif accion == "ROTAR_90":
            # Rotar a uno de los 4 lados
            lado = random.randint(0, 3)
            self.orientacion = self.orientacion.rotar_90(lado)
            self.puntuacion -= 10
        
        elif accion == "ESPERAR":
            pass  # No hacer nada esta iteración
    
    def actualizar_memoria(self, percepcion: Percepcion, accion: str):
        """Actualiza la memoria interna del agente"""
        # Registrar percepción-acción
        self.memoria.percepciones_acciones.append((percepcion, accion))
        
        # Actualizar creencias sobre zonas vacías
        if percepcion.colision_zona_vacia:
            pos_adelante = self._calcular_posicion_adelante()
            self.memoria.zonas_vacias_conocidas.add(pos_adelante)
        
        # Aprender nuevas reglas basadas en experiencias
        self._aprender_reglas(percepcion, accion)
        
        # Actualizar métricas de racionalidad
        self._actualizar_metricas_racionalidad(percepcion, accion)
    
    def ejecutar_ciclo(self):
        """Ciclo percepción-decisión-acción-aprendizaje"""
        if not self.vivo:
            return
        
        # 1. Percibir
        percepcion = self.percibir()
        
        # 2. Decidir
        accion = self.decidir_accion(percepcion)
        
        # 3. Actuar
        self.ejecutar_accion(accion, percepcion)
        
        # 4. Aprender (actualizar memoria)
        self.actualizar_memoria(percepcion, accion)
    
    def _calcular_posicion_adelante(self) -> Posicion:
        """Calcula la posición adelante según orientación"""
        dx, dy, dz = self.orientacion.value
        return Posicion(self.posicion.x + dx, self.posicion.y + dy, self.posicion.z + dz)
    
    def _calcular_posicion_atras(self) -> Posicion:
        """Calcula la posición atrás (opuesta a orientación)"""
        dx, dy, dz = self.orientacion.value
        return Posicion(self.posicion.x - dx, self.posicion.y - dy, self.posicion.z - dz)
    
    def _aprender_reglas(self, percepcion: Percepcion, accion: str):
        """Aprende nuevas reglas basadas en experiencias exitosas"""
        # Crear clave de regla basada en percepción
        clave_regla = f"{percepcion.monstruo_cercano}_{percepcion.robot_delante}_{percepcion.monstruo_en_celda}_{percepcion.colision_zona_vacia}"
        
        # Evaluar efectividad de la acción
        efectividad = self._evaluar_efectividad_accion(percepcion, accion)
        
        # Actualizar confianza en la regla
        if clave_regla in self.memoria.reglas_aprendidas:
            # Promedio ponderado con factor de olvido
            confianza_actual = self.memoria.reglas_aprendidas[clave_regla]
            self.memoria.reglas_aprendidas[clave_regla] = 0.9 * confianza_actual + 0.1 * efectividad
        else:
            self.memoria.reglas_aprendidas[clave_regla] = efectividad
    
    def _evaluar_efectividad_accion(self, percepcion: Percepcion, accion: str) -> float:
        """Evalúa la efectividad de una acción (0-1)"""
        if accion == "VACUUMATOR" and percepcion.monstruo_en_celda:
            return 1.0  # Acción perfecta
        elif accion == "MOVER_ADELANTE" and not percepcion.colision_zona_vacia:
            return 0.8  # Movimiento exitoso
        elif accion == "ROTAR_90" and percepcion.robot_delante:
            return 0.7  # Evasión exitosa
        elif accion == "MOVER_ADELANTE" and percepcion.colision_zona_vacia:
            return 0.1  # Colisión
        else:
            return 0.5  # Neutral
    
    def _actualizar_metricas_racionalidad(self, percepcion: Percepcion, accion: str):
        """Actualiza métricas de racionalidad del agente"""
        # Eficiencia de movimiento
        if accion == "MOVER_ADELANTE":
            if not percepcion.colision_zona_vacia:
                self.memoria.metricas_racionalidad['movimientos_exitosos'] = \
                    self.memoria.metricas_racionalidad.get('movimientos_exitosos', 0) + 1
            else:
                self.memoria.metricas_racionalidad['colisiones'] = \
                    self.memoria.metricas_racionalidad.get('colisiones', 0) + 1
        
        # Efectividad en caza
        if percepcion.monstruo_cercano and accion in ["MOVER_ADELANTE", "ROTAR_90"]:
            self.memoria.metricas_racionalidad['acciones_caza'] = \
                self.memoria.metricas_racionalidad.get('acciones_caza', 0) + 1
        
        # Comunicación efectiva
        if percepcion.robot_delante and accion in ["MOVER_ADELANTE", "ROTAR_90"]:
            self.memoria.metricas_racionalidad['comunicaciones_exitosas'] = \
                self.memoria.metricas_racionalidad.get('comunicaciones_exitosas', 0) + 1
    
    def calcular_racionalidad(self) -> float:
        """
        Calcula medida de racionalidad del agente (0-1)
        Basado en efectividad, eficiencia y adaptabilidad
        """
        total_acciones = len(self.memoria.percepciones_acciones)
        if total_acciones == 0:
            return 0.0
        
        # Factor 1: Efectividad general (30%)
        movimientos_exitosos = self.memoria.metricas_racionalidad.get('movimientos_exitosos', 0)
        colisiones = self.memoria.metricas_racionalidad.get('colisiones', 0)
        total_movimientos = movimientos_exitosos + colisiones
        efectividad = movimientos_exitosos / max(total_movimientos, 1)
        
        # Factor 2: Eficiencia en caza (25%)
        acciones_caza = self.memoria.metricas_racionalidad.get('acciones_caza', 0)
        eficiencia_caza = min(acciones_caza / max(total_acciones, 1), 1.0)
        
        # Factor 3: Adaptabilidad (25%)
        reglas_aprendidas = len(self.memoria.reglas_aprendidas)
        confianza_promedio = sum(self.memoria.reglas_aprendidas.values()) / max(reglas_aprendidas, 1)
        adaptabilidad = min(reglas_aprendidas / 10.0, 1.0) * confianza_promedio
        
        # Factor 4: Comunicación (20%)
        comunicaciones = self.memoria.metricas_racionalidad.get('comunicaciones_exitosas', 0)
        eficiencia_comunicacion = min(comunicaciones / max(total_acciones, 1), 1.0)
        
        # Puntuación final ponderada
        racionalidad = (0.30 * efectividad + 
                       0.25 * eficiencia_caza + 
                       0.25 * adaptabilidad + 
                       0.20 * eficiencia_comunicacion)
        
        return min(max(racionalidad, 0.0), 1.0)
    
    def detectar_bucle_infinito(self, ventana: int = 10) -> bool:
        """
        Detecta si el agente está en un bucle infinito
        Analiza patrones repetitivos en las últimas acciones
        """
        if len(self.memoria.percepciones_acciones) < ventana * 2:
            return False
        
        # Obtener últimas acciones
        ultimas_acciones = [accion for _, accion in self.memoria.percepciones_acciones[-ventana:]]
        
        # Detectar patrones repetitivos
        patrones = {}
        for i in range(len(ultimas_acciones) - 2):
            patron = tuple(ultimas_acciones[i:i+3])
            patrones[patron] = patrones.get(patron, 0) + 1
        
        # Si hay un patrón que se repite más de 2 veces, es un bucle
        max_repeticiones = max(patrones.values()) if patrones else 0
        return max_repeticiones >= 3
