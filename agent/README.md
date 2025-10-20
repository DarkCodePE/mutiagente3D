# Sistema Multi-Agente 3D: Robots Monstruicidas

## Descripción

Sistema modularizado para el examen parcial de Fundamentos de IA (MIA-103). Implementa un entorno hexaédrico 3D donde robots con memoria interna cazan monstruos usando agentes reflejo simples.

## Estructura Modular

```
agent/
├── __init__.py          # Paquete principal con exports
├── ontology.py          # Definiciones conceptuales y estructuras de datos
├── environment.py       # Entorno hexaédrico 3D
├── robot_agent.py       # Agente robot con memoria interna
├── monster_agent.py     # Agente monstruo reflejo simple
├── simulator.py         # Controlador de simulación y visualización
├── main.py             # Módulo principal que orquesta todo
├── ejemplo_uso.py      # Ejemplos de uso del sistema modularizado
└── README.md           # Este archivo
```

## Módulos

### 1. `ontology.py`
- **Propósito**: Definiciones conceptuales del dominio
- **Contenido**: Enums, clases de datos, estructuras base
- **Clases principales**:
  - `TipoCelda`: Tipos de celdas (libre/vacía)
  - `Orientacion`: Orientaciones 3D del robot
  - `Posicion`: Coordenadas 3D
  - `Percepcion`: Datos de sensores del robot
  - `MemoriaRobot`: Memoria interna del agente

### 2. `environment.py`
- **Propósito**: Gestión del mundo de operación
- **Clase principal**: `EntornoHexaedrico`
- **Funcionalidades**:
  - Creación del grid 3D
  - Validación de posiciones
  - Gestión de agentes
  - Actualización del entorno

### 3. `robot_agent.py`
- **Propósito**: Implementación del agente robot
- **Clase principal**: `AgenteRobot`
- **Características**:
  - Memoria interna con historial percepción-acción
  - Lógica de decisión jerárquica
  - Sensores: Giroscopio, Monstroscopio, Vacuscopio, etc.
  - Efectores: Propulsor, Reorientador, Vacuumator

### 4. `monster_agent.py`
- **Propósito**: Implementación del agente monstruo
- **Clase principal**: `AgenteMonstruo`
- **Características**:
  - Agente reflejo simple
  - Movimiento aleatorio cada K iteraciones
  - Sin memoria ni objetivos complejos

### 5. `simulator.py`
- **Propósito**: Control de simulación y visualización
- **Clase principal**: `Simulador`
- **Funcionalidades**:
  - Ejecución de simulaciones
  - Generación de reportes
  - Visualización 2D del entorno

### 6. `main.py`
- **Propósito**: Punto de entrada principal
- **Funciones principales**:
  - `ejecutar_simulacion()`: Función principal
  - `crear_experimento_personalizado()`: Experimentos con parámetros

## Uso

### Uso Básico
```python
from agent import ejecutar_simulacion

# Ejecutar con configuración por defecto
reporte = ejecutar_simulacion()
```

### Uso Personalizado
```python
from agent import crear_experimento_personalizado

# Experimentos con parámetros específicos
reporte = crear_experimento_personalizado(
    N=7,              # Mundo 7x7x7
    n_robots=5,       # 5 robots
    n_monstruos=8,    # 8 monstruos
    seed=123
)
```

### Uso Modular
```python
from agent import EntornoHexaedrico, Simulador

# Crear componentes individualmente
entorno = EntornoHexaedrico(N=5, pfree=0.7, pvacio=0.3, 
                           n_robots=3, n_monstruos=5)
sim = Simulador(entorno)
reporte = sim.ejecutar(max_iteraciones=100)
```

## Ventajas de la Modularización

1. **Separación de Responsabilidades**: Cada módulo tiene una función específica
2. **Mantenibilidad**: Código más fácil de mantener y debuggear
3. **Reutilización**: Componentes pueden usarse independientemente
4. **Testabilidad**: Cada módulo puede probarse por separado
5. **Escalabilidad**: Fácil agregar nuevas funcionalidades
6. **Legibilidad**: Código más organizado y comprensible

## Arquitectura

El sistema sigue principios de arquitectura limpia:

- **Capa de Dominio**: `ontology.py` (entidades y reglas de negocio)
- **Capa de Aplicación**: `robot_agent.py`, `monster_agent.py` (lógica de agentes)
- **Capa de Infraestructura**: `environment.py`, `simulator.py` (entorno y herramientas)
- **Capa de Presentación**: `main.py` (interfaz principal)

## Ejecución

### Modo Consola (Matplotlib)
```bash
# Ejecutar sistema completo
python agent/main.py

# Ejecutar ejemplos
python agent/ejemplo_uso.py
```

### Modo Interactivo (Pygame)
```bash
# Demo interactivo con menú
python agent/demo_pygame.py

# Demo directo
python agent/demo_pygame.py 1  # Demo básico
```

**Ver [README_PYGAME.md](README_PYGAME.md) para más información sobre visualización interactiva.**

## Dependencias

- `numpy`: Operaciones matemáticas
- `matplotlib`: Visualización estática
- `pygame`: Visualización interactiva en tiempo real (opcional)
- `random`: Generación de números aleatorios
- `typing`: Anotaciones de tipos
- `dataclasses`: Estructuras de datos
- `enum`: Enumeraciones

## Instalación

```bash
pip install numpy matplotlib pygame
```
