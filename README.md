# 🤖 Sistema Multi-Agente 3D: Robots Monstruicidas

Sistema modularizado para el examen parcial de Fundamentos de IA (MIA-103). Implementa un entorno hexaédrico 3D donde robots con memoria interna cazan monstruos usando agentes reflejo simples.

## 🚀 Inicio Rápido

### Instalación

```bash
# Clonar o descargar el proyecto
cd examen-fundamentos

# Instalar dependencias
pip install -r requirements.txt

```

### Ejecutar el Juego

```bash
# Demo interactivo con Pygame (RECOMENDADO)
python agent/demo_pygame.py

# Simulación en consola
python agent/main.py
```

## 🎮 Controles Pygame

| Tecla | Función |
|-------|---------|
| **ESPACIO** | Pausar/Reanudar |
| **← →** | Rotar vista horizontal |
| **↑ ↓** | Rotar vista vertical |
| **+ -** | Zoom in/out |
| **ESC** | Salir |

## 📁 Estructura del Proyecto

```
examen-fundamentos/
├── agent/                          # Módulo principal
│   ├── __init__.py                # Paquete principal
│   ├── ontology.py                # Definiciones conceptuales
│   ├── environment.py             # Entorno hexaédrico 3D
│   ├── robot_agent.py             # Agente robot con memoria
│   ├── monster_agent.py           # Agente monstruo reflejo
│   ├── simulator.py               # Simulador (matplotlib)
│   ├── visualizacion_pygame.py    # Visualizador pygame
│   ├── main.py                    # Main consola
│   ├── demo_pygame.py             # Main pygame
│   └── README.md                  # Documentación del módulo
├── docs/                          # Documentación
│   ├── MIA 103 examen parcial 2025-2.docx.md
│   ├── PYGAME_IMPLEMENTADO.md
│   └── README_PYGAME.md
├── requirements.txt               # Dependencias
├── setup.py                      # Instalación del paquete
├── .gitignore                    # Archivos a ignorar
└── README.md                     # Este archivo
```

## 🎯 Características

### Agentes Implementados
- **Agente Robot**: Con memoria interna y lógica de decisión jerárquica
- **Agente Monstruo**: Reflejo simple con movimiento aleatorio

### Sensores del Robot
- **Giroscopio**: Orientación en el espacio
- **Monstroscopio**: Detección de monstruos en 5 lados
- **Vacuscopio**: Detección de colisiones con zonas vacías
- **Energómetro Espectral**: Detección de monstruos en la celda actual
- **Roboscanner**: Detección de otros robots

### Efectores del Robot
- **Propulsor Direccional**: Movimiento hacia adelante
- **Reorientador**: Rotación de 90 grados
- **Vacuumator**: Destrucción de monstruos (y autodestrucción)

### Visualización
- **Modo Consola**: Simulación con matplotlib para análisis
- **Modo Interactivo**: Visualización 3D con pygame para demos

## 🎮 Demos Disponibles

```bash
python agent/demo_pygame.py 1  # Básico (5x5x5)
python agent/demo_pygame.py 2  # Grande (7x7x7)
python agent/demo_pygame.py 3  # Pequeño (3x3x3)
python agent/demo_pygame.py 4  # Muchos agentes (8x8x8)
```

## 💻 Uso Programático

```python
from agent import EntornoHexaedrico, VisualizadorPygame

# Crear entorno personalizado
entorno = EntornoHexaedrico(
    N=5,              # Tamaño del mundo
    pfree=0.7,        # 70% zonas libres
    pvacio=0.3,       # 30% zonas vacías
    n_robots=3,       # Número de robots
    n_monstruos=5,    # Número de monstruos
    seed=42           # Semilla (opcional)
)

# Visualizar con pygame
visualizador = VisualizadorPygame(entorno)
stats = visualizador.ejecutar_con_visualizacion(max_iteraciones=300)
```

## 📊 Requisitos del Sistema

- **Python**: 3.8 o superior
- **Dependencias**: Ver `requirements.txt`
- **Memoria RAM**: ~100MB para mundos medianos
- **GPU**: No requerida (CPU rendering)

## 🎓 Para el Examen

### Presentación
1. **Demo en vivo**: Usar `python agent/demo_pygame.py`
2. **Explicación técnica**: Mostrar arquitectura modular
3. **Análisis de resultados**: Usar reportes de simulación

### Documentación
- `agent/README.md` - Documentación técnica completa
- `docs/README_PYGAME.md` - Guía de visualización pygame
- `docs/PYGAME_IMPLEMENTADO.md` - Detalles de implementación

## 🔧 Desarrollo

### Instalar en modo desarrollo
```bash
pip install -e .
```

### Ejecutar tests
```bash
python verificar_sistema.py
```

### Formatear código (opcional)
```bash
pip install black
black agent/
```

## 📈 Arquitectura

El sistema sigue principios de arquitectura limpia:

- **Capa de Dominio**: `ontology.py` (entidades y reglas de negocio)
- **Capa de Aplicación**: `robot_agent.py`, `monster_agent.py` (lógica de agentes)
- **Capa de Infraestructura**: `environment.py`, `simulator.py`, `visualizacion_pygame.py`
- **Capa de Presentación**: `main.py`, `demo_pygame.py` (interfaces)
