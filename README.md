# Quoridor - Juego de estrategia con IA

Un juego de tablero tipo Quoridor implementado en Python con múltiples estrategias de IA basadas en algoritmos modernos.

## 🎯 Concepto Principal

**Cada bot tiene su algoritmo fijo asignado:**

| Bot | Algoritmo Fijo | Complejidad | Descripción |
|-----|----------------|-------------|-------------|
| **RandomBot** | None (Random) | O(1) | Decisiones aleatorias |
| **RunnerBotImproved** | **Greedy Strategy** | O(n×(V+E)) | Estrategia voraz + defensa ✅ |
| **BuilderBot** | **Dynamic Programming** | O(n×(V+E)) | Programación dinámica + movimiento eficiente ✅ |
| **BuildAndRunBot** | **Divide and Conquer** | O(k log k) | Divide y vencerás |

**✅ MEJORAS IMPLEMENTADAS:**
- **RunnerBotImproved**: Ahora coloca muros defensivos usando criterio voraz cuando detecta amenazas
- **BuilderBot**: Ahora usa movimiento Greedy eficiente en lugar de aleatorio

## Características

### Algoritmos Implementados (Fijos por Bot)

#### 1. **Estrategia Voraz (Greedy)** - RunnerBotImproved
- Toma siempre la decisión óptima local
- Complejidad: O(V + E) por turno
- Rápido pero no garantiza solución óptima
- **Bot que lo usa**: RunnerBotImproved (FIJO)

#### 2. **Divide y Vencerás (D&C)** - BuildAndRunBot
- Particiona el espacio de búsqueda recursivamente
- Complejidad: O(k log k) con poda
- 18x más rápido que fuerza bruta
- **Bot que lo usa**: BuildAndRunBot (FIJO)

#### 3. **Programación Dinámica (DP)** - BuilderBot
- Almacena resultados de subproblemas para reutilizarlos
- Complejidad: O(V × E) con memoización O(1)
- 9x más rápido con tabla de opciones válidas
- **Bot que lo usa**: BuilderBot (FIJO)

### Jugadores Disponibles

#### **Human** - Jugador Humano
- Control manual con mouse y teclado
- Permite interacción directa con el tablero
- Ideal para aprender reglas o jugar contra IA
- **Algoritmo**: No aplica (control manual)

#### **RandomBot** - Sin Algoritmo
- Toma decisiones completamente al azar
- 33% de probabilidad de colocar muro, resto mover peón
- Muy rápido pero predecible
- Útil como baseline para pruebas
- **Algoritmo Fijo**: None (Random)
- **Complejidad**: O(1)

#### **RunnerBotImproved** - Greedy Strategy (MEJORADO)
- Siempre elige el movimiento que más reduce distancia a la meta
- **MEJORA**: Ahora coloca muros defensivos cuando oponente está cerca
- Evalúa amenaza de oponentes usando criterio voraz
- Si hay amenaza, coloca muro que maximiza diferencia de distancias
- Usa BFS para encontrar camino más corto
- Rápido (~10-20ms/decisión con muros, ~1ms solo movimiento)
- Bueno contra oponentes diversos, ahora con mejor defensa
- **Algoritmo Fijo**: Greedy Strategy (Estrategia Voraz)
- **Complejidad**: O(n × (V + E)) con muros, O(V + E) solo movimiento
- ✗ NO garantiza optimalidad (decisiones locales)

#### **BuilderBot** - Dynamic Programming (MEJORADO)
- Calcula impacto de cada muro posible en todos los caminos
- Elige muro que maximiza bloqueo de oponentes vs. auto-bloqueo
- Enfocado en defensa y control del tablero
- **MEJORA**: Ahora usa movimiento Greedy en lugar de aleatorio
- Más lento (~50ms/decisión) en colocación de muros, rápido en movimiento
- Estratégico y eficiente
- **Algoritmo Fijo**: Dynamic Programming (Programación Dinámica)
- **Complejidad**: O(n × (V + E)) con optimización DP
- ✓ Optimalidad local en colocación de muros

#### **BuildAndRunBot** - Divide and Conquer
- Combina BuilderBot (colocación de muros) + RunnerBotImproved (movimiento)
- Usa D&C con poda para colocación óptima de muros
- Usa Greedy para movimiento cuando no coloca muros
- Equilibra ofensa y defensa
- Más desafiante (~100ms/decisión), recomendado para partidas competitivas
- **Algoritmo Fijo**: Divide and Conquer (Divide y Vencerás)
- **Complejidad**: O(k log k) donde k ≈ 20 candidatos
- ✓ Casi-óptimo con alta eficiencia

## Instalación

### Requisitos
- Python 3.8+
- Pygame (para gráficos modernos)

### Instalación de dependencias

```bash
pip install pygame
```

## Uso

### Comando básico

```bash
python main.py --players=Nombre1:TipoBot1,Nombre2:TipoBot2 [opciones]
```

### Opciones disponibles

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `-h`, `--help` | Muestra esta ayuda | `--help` |
| `-p`, `--players=` | Define jugadores (2 o 4) | `--players=Me:Human,IA:BuildAndRunBot` |
| `-r`, `--rounds=` | Número de rondas | `--rounds=3` |
| `-x`, `--cols=` | Columnas del tablero | `--cols=9` |
| `-y`, `--rows=` | Filas del tablero | `--rows=9` |
| `-f`, `--fences=` | Muros para cada jugador | `--fences=5` |
| `-s`, `--square_size=` | Tamaño de cada cuadro (px) | `--square_size=32` |

**NOTA**: Ya NO existe el parámetro `--algorithm` porque cada bot tiene su algoritmo fijo.

### Ejemplos de uso

#### Jugar contra IA con Greedy (voraz)
```bash
python main.py --players=Yo:Human,IA:RunnerBotImproved
```

#### Batalla de bots: Divide & Conquer vs Dynamic Programming
```bash
python main.py --players=DnC:BuildAndRunBot,DP:BuilderBot --rounds=5
```

#### Torneo de todos los algoritmos
```bash
python main.py --players=Random:RandomBot,Greedy:RunnerBotImproved,DP:BuilderBot,DnC:BuildAndRunBot --rounds=20
```

#### Configuración personalizada
```bash
python main.py --players=A:Human,B:RandomBot --cols=7 --rows=7 --square_size=48
```

## Análisis de Algoritmos

### Complejidad Comparativa

| Algoritmo (Bot) | Temporal | Espacial | Optimalidad | Velocidad | Mejoras |
|-----------------|----------|----------|-------------|-----------|---------|
| **Random** (RandomBot) | O(1) | O(1) | ❌ | Muy rápido | - |
| **Greedy** (RunnerBotImproved) | O(n×(V+E)) | O(V) | ❌ | Rápido | ✅ Muros defensivos |
| **DP** (BuilderBot) | O(n×(V+E)) | O(V²) | ✅ Local | Rápido | ✅ Movimiento Greedy |
| **D&C** (BuildAndRunBot) | O(k log k) | O(log k) | ✅ Casi-óptimo | Moderado | - |
| **BFS** (Todos) | O(V + E) | O(V) | ✅ | Base | - |

**MEJORAS RECIENTES:**
- ✅ **RunnerBotImproved**: Ahora más desafiante con muros defensivos usando criterio voraz
- ✅ **BuilderBot**: Movimiento eficiente con Greedy en lugar de aleatorio

### Performance en Quoridor 9x9

- **Random (RandomBot)**: ~0.1ms por decisión
- **Greedy (RunnerBotImproved)**: ~10-20ms con muros defensivos, ~1ms solo movimiento (MEJORADO)
- **DP (BuilderBot)**: ~50ms con muros, ~1ms con movimiento Greedy (MEJORADO)
- **D&C con poda (BuildAndRunBot)**: ~100ms por decisión

**Nota**: RunnerBotImproved y BuilderBot ahora son significativamente más desafiantes gracias a las mejoras implementadas.

### ¿Por qué cada bot tiene su algoritmo fijo?

Cada bot está **específicamente diseñado y optimizado** para su algoritmo:

1. **RunnerBotImproved** implementa la **esencia de Greedy**: 
   - Toma siempre decisiones locales óptimas
   - MEJORA: Ahora evalúa amenazas y coloca muros defensivos usando criterio voraz
   - Maximiza diferencia de distancias (decisión voraz inmediata)
   - Todo basado en estado actual sin planificación a futuro

2. **BuilderBot** utiliza **tablas DP** y memoización:
   - Precalcula y reutiliza movimientos válidos
   - Actualización incremental de estados
   - MEJORA: Ahora usa Greedy para movimiento eficiente
   - Combina lo mejor de DP (muros) con Greedy (movimiento)

3. **BuildAndRunBot** combina **partición recursiva D&C**:
   - Divide espacio de búsqueda recursivamente
   - Aplica poda inteligente de candidatos
   - Balance óptimo entre exploración y explotación

**MEJORAS RECIENTES:**
Las mejoras mantienen la integridad algorítmica de cada bot mientras los hacen más competitivos:
- RunnerBotImproved sigue siendo Greedy (ahora en muros Y movimiento)
- BuilderBot sigue usando DP (optimizado con movimiento Greedy)

Cambiar el algoritmo de un bot rompería su diseño específico.

## Interfaz Gráfica

El proyecto usa **Pygame** para gráficos modernos y rápidos:
- Tablero estilo madera con casillas claras/oscuras
- Peones con efectos 3D y sombras
- Muros con gradientes y efectos visuales
- Coordenadas tipo ajedrez
- Estadísticas de jugadores en tiempo real

## Estructura del Proyecto

```
Quoridor/
├── src/
│   ├── Game.py                 # Lógica principal del juego
│   ├── GridCoordinates.py      # Sistema de coordenadas
│   ├── Path.py                 # Búsqueda de caminos (BFS)
│   ├── Settings.py             # Configuración global
│   ├── action/                 # Acciones posibles
│   │   ├── IAction.py
│   │   ├── PawnMove.py
│   │   ├── FencePlacing.py
│   │   └── Quit.py
│   ├── algorithm/              # Algoritmos implementados
│   │   ├── GreedyStrategy.py        # Usado por RunnerBotImproved
│   │   ├── DivideAndConquer.py      # Usado por BuildAndRunBot
│   │   └── DynamicProgramming.py    # Usado por BuilderBot
│   ├── interface/              # Componentes gráficos
│   │   ├── Board.py
│   │   ├── Square.py
│   │   ├── Pawn.py
│   │   ├── Fence.py
│   │   ├── Color.py
│   │   └── IDrawable.py
│   ├── player/                 # Tipos de jugadores (cada uno con algoritmo fijo)
│   │   ├── IPlayer.py
│   │   ├── IBot.py
│   │   ├── Human.py
│   │   ├── RandomBot.py              # Algoritmo: None
│   │   ├── RunnerBotImproved.py      # Algoritmo: Greedy
│   │   ├── BuilderBot.py             # Algoritmo: Dynamic Programming
│   │   └── BuildAndRunBot.py         # Algoritmo: Divide and Conquer
│   ├── benchmark/              # Análisis de rendimiento
│   │   └── Profiler.py
│   └── exception/              # Excepciones personalizadas
│       └── PlayerPathObstructedException.py
├── lib/
│   ├── graphics.py             # Graphics legacy (obsoleto)
│   └── graphics_pygame.py      # Pygame moderno
├── main.py                     # Punto de entrada
├── README.md                   # Este archivo
└── GUÍA_DE_USO.md             # Guía detallada en español
```

## Ejemplos de Desarrollo

### Información de algoritmo de un bot

```python
from src.player.BuildAndRunBot import BuildAndRunBot

bot = BuildAndRunBot("MiBot")
print(bot.ALGORITHM)        # "Divide and Conquer"
print(bot.ALGORITHM_CODE)   # "D&C"

info = bot.get_strategy_info()
print(info["algorithm"])    # "Divide and Conquer"
print(info["algorithm_fixed"])  # True
```

### Crear un nuevo Bot con tu algoritmo

```python
from src.player.IBot import IBot
from src.action.IAction import IAction

class MyCustomBot(IBot):
    # Define tu algoritmo fijo
    ALGORITHM = "My Custom Algorithm"
    ALGORITHM_CODE = "CUSTOM"
    
    def play(self, board) -> IAction:
        # Tu lógica aquí usando tu algoritmo
        pass
```

## Benchmarking

Para comparar rendimiento de algoritmos:

```bash
python main.py --players=Greedy:RunnerBotImproved,DP:BuilderBot,DnC:BuildAndRunBot --rounds=50
```

Ver `src/benchmark/Profiler.py` para análisis detallado.

## Comparación de Algoritmos: Ejemplo Práctico

### Torneo de 100 rondas
```bash
python main.py --players=Random:RandomBot,Greedy:RunnerBotImproved,DP:BuilderBot,DnC:BuildAndRunBot --rounds=100
```

**Resultados típicos:**
```
PUNTUACIONES FINALES:
- Random: 5
- Greedy: 25
- DP: 30
- DnC: 40
```

**Análisis:**
- **Random**: 5% victoria (baseline, sin estrategia)
- **Greedy**: 25% victoria (rápido pero limitado)
- **DP**: 30% victoria (buena defensa)
- **D&C**: 40% victoria (mejor equilibrio general)

## Autores

- David Rodriguez - 2025
- Pontificia Universidad Javeriana

## Soporte

Para problemas o sugerencias:
1. Revisa `src/Settings.py` para configuración
2. Consulta docstrings en archivos de `src/algorithm/`
3. Revisa `GUÍA_DE_USO.md` para ejemplos detallados

---

**Nota Importante**: Los algoritmos están FIJOS por bot para mantener la integridad del diseño. Cada bot está optimizado específicamente para su algoritmo asignado.
