"""
VISUALIZACIÓN PYGAME PARA SISTEMA MULTI-AGENTE 3D
Visualizador interactivo en tiempo real con pygame
"""

import pygame
import math
from typing import TYPE_CHECKING, List, Tuple
import numpy as np

from .ontology import TipoCelda, Posicion

if TYPE_CHECKING:
    from .environment import EntornoHexaedrico


class VisualizadorPygame:
    """
    Visualizador 3D interactivo usando pygame
    - Muestra el entorno en tiempo real
    - Permite rotar la vista
    - Muestra estadísticas en pantalla
    """
    
    # Colores
    COLOR_FONDO = (20, 20, 30)
    COLOR_ZONA_LIBRE = (50, 50, 60)
    COLOR_ZONA_VACIA = (100, 30, 30)
    COLOR_ROBOT = (50, 150, 255)
    COLOR_MONSTRUO = (255, 50, 50)
    COLOR_GRID = (40, 40, 50)
    COLOR_TEXTO = (255, 255, 255)
    COLOR_PANEL = (30, 30, 40)
    
    def __init__(self, entorno: 'EntornoHexaedrico', ancho: int = 1200, alto: int = 800):
        """
        Inicializa el visualizador pygame
        
        Args:
            entorno: Entorno hexaédrico a visualizar
            ancho: Ancho de la ventana
            alto: Alto de la ventana
        """
        pygame.init()
        self.entorno = entorno
        self.ancho = ancho
        self.alto = alto
        
        # Crear ventana
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Sistema Multi-Agente 3D: Robots Monstruicidas")
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 36)
        self.fuente_info = pygame.font.Font(None, 24)
        self.fuente_pequeña = pygame.font.Font(None, 18)
        
        # Parámetros de vista 3D
        self.angulo_x = 30  # Rotación en X
        self.angulo_y = 45  # Rotación en Y
        self.zoom = 1.0
        self.offset_x = ancho // 2
        self.offset_y = alto // 2
        
        # Escala para visualización
        self.escala = min(ancho, alto) // (self.entorno.N * 2)
        
        # Control de simulación
        self.pausado = False
        self.velocidad = 500  # ms por iteración
        self.ultimo_tick = pygame.time.get_ticks()
        
        # Reloj para FPS
        self.clock = pygame.time.Clock()
        self.fps = 60
    
    def proyecto_3d_a_2d(self, x: float, y: float, z: float) -> Tuple[int, int]:
        """
        Proyección isométrica 3D a 2D
        
        Args:
            x, y, z: Coordenadas 3D
            
        Returns:
            Tupla con coordenadas 2D (x, y)
        """
        # Convertir ángulos a radianes
        rad_x = math.radians(self.angulo_x)
        rad_y = math.radians(self.angulo_y)
        
        # Rotación en Y
        x_rot = x * math.cos(rad_y) - z * math.sin(rad_y)
        z_rot = x * math.sin(rad_y) + z * math.cos(rad_y)
        
        # Rotación en X
        y_rot = y * math.cos(rad_x) - z_rot * math.sin(rad_x)
        z_final = y * math.sin(rad_x) + z_rot * math.cos(rad_x)
        
        # Proyección isométrica simple
        screen_x = int(self.offset_x + (x_rot * self.escala * self.zoom))
        screen_y = int(self.offset_y - (y_rot * self.escala * self.zoom))
        
        return screen_x, screen_y
    
    def dibujar_cubo(self, x: int, y: int, z: int, color: Tuple[int, int, int], alpha: int = 255):
        """
        Dibuja un cubo en la posición especificada
        
        Args:
            x, y, z: Coordenadas del cubo
            color: Color RGB del cubo
            alpha: Transparencia (0-255)
        """
        # Calcular vértices del cubo
        vertices = []
        for dx in [0, 1]:
            for dy in [0, 1]:
                for dz in [0, 1]:
                    vx, vy = self.proyecto_3d_a_2d(x + dx, y + dy, z + dz)
                    vertices.append((vx, vy))
        
        # Definir caras del cubo (índices de vértices)
        caras = [
            [0, 1, 3, 2],  # Cara frontal
            [4, 5, 7, 6],  # Cara trasera
            [0, 1, 5, 4],  # Cara inferior
            [2, 3, 7, 6],  # Cara superior
            [0, 2, 6, 4],  # Cara izquierda
            [1, 3, 7, 5],  # Cara derecha
        ]
        
        # Dibujar caras con transparencia
        superficie = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        
        for cara in caras:
            puntos = [vertices[i] for i in cara]
            # Calcular color con sombreado simple
            color_cara = tuple(int(c * 0.7) for c in color)
            pygame.draw.polygon(superficie, (*color_cara, alpha // 2), puntos)
            pygame.draw.polygon(superficie, color, puntos, 2)
        
        self.screen.blit(superficie, (0, 0))
    
    def dibujar_esfera(self, x: float, y: float, z: float, color: Tuple[int, int, int], radio: int = 10):
        """
        Dibuja una esfera (robot o monstruo) en la posición especificada
        
        Args:
            x, y, z: Coordenadas de la esfera
            color: Color RGB
            radio: Radio de la esfera
        """
        screen_x, screen_y = self.proyecto_3d_a_2d(x + 0.5, y + 0.5, z + 0.5)
        pygame.draw.circle(self.screen, color, (screen_x, screen_y), radio)
        pygame.draw.circle(self.screen, (255, 255, 255), (screen_x, screen_y), radio, 2)
    
    def dibujar_entorno(self):
        """Dibuja el entorno completo"""
        # Dibujar grid y zonas
        for x in range(self.entorno.N):
            for y in range(self.entorno.N):
                for z in range(self.entorno.N):
                    tipo = self.entorno.grid[x, y, z]
                    
                    if tipo == TipoCelda.ZONA_VACIA.value:
                        # Dibujar zonas vacías con color rojo oscuro
                        self.dibujar_cubo(x, y, z, self.COLOR_ZONA_VACIA, alpha=150)
                    else:
                        # Dibujar grid para zonas libres (solo bordes)
                        color_grid = self.COLOR_GRID
                        vertices = []
                        for dx in [0, 1]:
                            for dy in [0, 1]:
                                for dz in [0, 1]:
                                    vx, vy = self.proyecto_3d_a_2d(x + dx, y + dy, z + dz)
                                    vertices.append((vx, vy))
                        
                        # Dibujar aristas del cubo
                        aristas = [
                            (0, 1), (0, 2), (0, 4), (1, 3), (1, 5),
                            (2, 3), (2, 6), (3, 7), (4, 5), (4, 6),
                            (5, 7), (6, 7)
                        ]
                        for i, j in aristas:
                            pygame.draw.line(self.screen, color_grid, vertices[i], vertices[j], 1)
    
    def dibujar_agentes(self):
        """Dibuja robots y monstruos"""
        # Dibujar monstruos
        for monstruo in self.entorno.monstruos:
            if monstruo.vivo:
                self.dibujar_esfera(
                    monstruo.posicion.x,
                    monstruo.posicion.y,
                    monstruo.posicion.z,
                    self.COLOR_MONSTRUO,
                    radio=12
                )
        
        # Dibujar robots
        for robot in self.entorno.robots:
            if robot.vivo:
                self.dibujar_esfera(
                    robot.posicion.x,
                    robot.posicion.y,
                    robot.posicion.z,
                    self.COLOR_ROBOT,
                    radio=15
                )
                
                # Dibujar dirección del robot
                dx, dy, dz = robot.orientacion.value
                end_x = robot.posicion.x + 0.5 + dx * 0.7
                end_y = robot.posicion.y + 0.5 + dy * 0.7
                end_z = robot.posicion.z + 0.5 + dz * 0.7
                
                start_x, start_y = self.proyecto_3d_a_2d(
                    robot.posicion.x + 0.5,
                    robot.posicion.y + 0.5,
                    robot.posicion.z + 0.5
                )
                end_screen_x, end_screen_y = self.proyecto_3d_a_2d(end_x, end_y, end_z)
                
                pygame.draw.line(self.screen, (255, 255, 0), 
                               (start_x, start_y), (end_screen_x, end_screen_y), 3)
    
    def dibujar_panel_info(self):
        """Dibuja panel de información"""
        # Fondo del panel
        panel_rect = pygame.Rect(10, 10, 350, 200)
        pygame.draw.rect(self.screen, self.COLOR_PANEL, panel_rect)
        pygame.draw.rect(self.screen, self.COLOR_TEXTO, panel_rect, 2)
        
        # Título
        titulo = self.fuente_titulo.render("ROBOTS MONSTRUICIDAS", True, self.COLOR_TEXTO)
        self.screen.blit(titulo, (20, 20))
        
        # Estadísticas
        stats = self.entorno.estadisticas()
        y_pos = 60
        
        info_lineas = [
            f"Iteración: {stats['iteracion']}",
            f"Robots vivos: {stats['robots_vivos']}",
            f"Monstruos vivos: {stats['monstruos_vivos']}",
            f"Monstruos destruidos: {stats['monstruos_destruidos']}",
            f"Puntuación total: {stats['puntuacion_total']}",
        ]
        
        for linea in info_lineas:
            texto = self.fuente_info.render(linea, True, self.COLOR_TEXTO)
            self.screen.blit(texto, (20, y_pos))
            y_pos += 25
        
        # Controles
        y_pos += 10
        estado = "PAUSADO" if self.pausado else "EJECUTANDO"
        texto_estado = self.fuente_pequeña.render(f"Estado: {estado}", True, 
                                                  (255, 255, 0) if self.pausado else (0, 255, 0))
        self.screen.blit(texto_estado, (20, y_pos))
    
    def dibujar_controles(self):
        """Dibuja información de controles"""
        controles = [
            "CONTROLES:",
            "ESPACIO - Pausar/Reanudar",
            "← → - Rotar vista horizontal",
            "↑ ↓ - Rotar vista vertical",
            "+ - - Zoom in/out",
            "ESC - Salir"
        ]
        
        y_pos = self.alto - 150
        panel_rect = pygame.Rect(10, y_pos - 10, 250, 140)
        pygame.draw.rect(self.screen, self.COLOR_PANEL, panel_rect)
        pygame.draw.rect(self.screen, self.COLOR_TEXTO, panel_rect, 1)
        
        for i, linea in enumerate(controles):
            texto = self.fuente_pequeña.render(linea, True, self.COLOR_TEXTO)
            self.screen.blit(texto, (20, y_pos + i * 20))
    
    def manejar_eventos(self) -> bool:
        """
        Maneja eventos de pygame
        
        Returns:
            False si se debe cerrar la ventana, True en caso contrario
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                elif evento.key == pygame.K_SPACE:
                    self.pausado = not self.pausado
                elif evento.key == pygame.K_LEFT:
                    self.angulo_y -= 5
                elif evento.key == pygame.K_RIGHT:
                    self.angulo_y += 5
                elif evento.key == pygame.K_UP:
                    self.angulo_x = max(0, self.angulo_x - 5)
                elif evento.key == pygame.K_DOWN:
                    self.angulo_x = min(90, self.angulo_x + 5)
                elif evento.key == pygame.K_PLUS or evento.key == pygame.K_EQUALS:
                    self.zoom = min(2.0, self.zoom + 0.1)
                elif evento.key == pygame.K_MINUS:
                    self.zoom = max(0.5, self.zoom - 0.1)
        
        return True
    
    def renderizar_frame(self):
        """Renderiza un frame completo"""
        # Limpiar pantalla
        self.screen.fill(self.COLOR_FONDO)
        
        # Dibujar elementos
        self.dibujar_entorno()
        self.dibujar_agentes()
        self.dibujar_panel_info()
        self.dibujar_controles()
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def ejecutar_con_visualizacion(self, max_iteraciones: int = 200):
        """
        Ejecuta la simulación con visualización en tiempo real
        
        Args:
            max_iteraciones: Número máximo de iteraciones
        """
        ejecutando = True
        
        while ejecutando:
            # Manejar eventos
            ejecutando = self.manejar_eventos()
            
            # Actualizar simulación si no está pausada
            if not self.pausado:
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - self.ultimo_tick >= self.velocidad:
                    stats = self.entorno.estadisticas()
                    
                    # Verificar condiciones de parada
                    if stats['monstruos_vivos'] == 0:
                        print(f"\n🎉 ¡MISIÓN CUMPLIDA! Todos los monstruos destruidos")
                        self.pausado = True
                    elif stats['robots_vivos'] == 0:
                        print(f"\n💀 MISIÓN FALLIDA: Todos los robots destruidos")
                        self.pausado = True
                    elif stats['iteracion'] >= max_iteraciones:
                        print(f"\n⏱️ Tiempo agotado después de {max_iteraciones} iteraciones")
                        self.pausado = True
                    else:
                        # Actualizar entorno
                        self.entorno.actualizar()
                        self.ultimo_tick = tiempo_actual
            
            # Renderizar frame
            self.renderizar_frame()
            
            # Limitar FPS
            self.clock.tick(self.fps)
        
        # Cerrar pygame
        pygame.quit()
        
        # Retornar estadísticas finales
        return self.entorno.estadisticas()

