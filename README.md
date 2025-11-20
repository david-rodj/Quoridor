# Quoridor - Juego de estrategia con IA

Un juego de tablero tipo Quoridor implementado en Python con múltiples estrategias de IA basadas en algoritmos modernos.

## Características

### Algoritmos Implementados

#### 1. **Estrategia Voraz (Greedy)**
- Toma siempre la decisión óptima local
- Complejidad: O(V + E) por turno
- Rápido pero no garantiza solución óptima
- Usado por: `RunnerBotImproved`

#### 2. **Divide y Vencerás (D&C)**
- Particiona el espacio de búsqueda recursivamente
- Complejidad: O(n log n)
- 18x más rápido que fuerza bruta
- Usado por: `BuilderBot`, `BuildAndRunBot` (para colocación de muros)

#### 3. **Programación Dinámica (DP)**
- Almacena resultados de subproblemas para reutilizarlos
- Complejidad: O(V × E) con memoización O(1)
- 9x más rápido con tabla de opciones válidas
- Usado por: `RunnerBotImproved` (cálculo de distancias)

### Jugadores Disponibles

#### **Human** - Jugador Humano
- Control manual con mouse y teclado
- Permite interacción directa con el tablero
- Ideal para aprender reglas o jugar contra IA
- **Algoritmos**: No soporta (control manual)

#### **RandomBot** - Movimientos Aleatorios
- Toma decisiones completamente al azar
- 33% de probabilidad de colocar muro, resto mover peón
- Muy rápido pero predecible
- Útil como baseline para pruebas
- **Algoritmos**: No soporta (acciones aleatorias)

#### **RunnerBotImproved** - Estrategia Voraz (Greedy)
- Siempre elige el movimiento que más reduce distancia a la meta
- Usa BFS para encontrar camino más corto
- Rápido (~1ms/decisión) pero puede quedar atrapado
- Bueno contra oponentes pasivos, vulnerable a bloqueos inteligentes
- **Algoritmos**: Greedy (por defecto), DynamicProgramming

#### **BuilderBot** - Estrategia de Construcción
- Calcula impacto de cada muro posible en todos los caminos
- Elige muro que maximiza bloqueo de oponentes vs. auto-bloqueo
- Enfocado en defensa y control del tablero
- Más lento (~50ms/decisión) pero estratégico
- **Algoritmos**: DivideAndConquer (recomendado), DynamicProgramming, Greedy

#### **BuildAndRunBot** - Estrategia Híbrida
- Combina BuilderBot (colocación de muros) + RunnerBotImproved (movimiento)
- Coloca muros cuando es ventajoso, mueve estratégicamente cuando no
- Equilibra ofensa y defensa
- Más desafiante (~100ms/decisión), recomendado para partidas competitivas
- **Algoritmos**: DivideAndConquer (recomendado), DynamicProgramming, Greedy

#### **MyBot** - Plantilla Personalizada
- Clase base vacía para implementar estrategias personalizadas
- Hereda de IBot, permite lógica completamente custom
- **Algoritmos**: Depende de implementación (por defecto ninguno)

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
| `-p`, `--players=` | Define jugadores (2 o 4) | `--players=Me:Human,IA:BuilderBot` |
| `-r`, `--rounds=` | Número de rondas | `--rounds=3` |
| `-x`, `--cols=` | Columnas del tablero | `--cols=9` |
| `-y`, `--rows=` | Filas del tablero | `--rows=9` |
| `-f`, `--fences=` | Muros para cada jugador | `--fences=5` |
| `-s`, `--square_size=` | Tamaño de cada cuadro (px) | `--square_size=32` |
| `-a`, `--algorithm=` | Algoritmo a usar | `--algorithm=DivideAndConquer` |

### Ejemplos de uso

#### Jugar contra IA voraz
```bash
python main.py --players=Yo:Human,IA:RunnerBotImproved --algorithm=Greedy
```

#### Batalla de bots con Divide y Vencerás
```bash
python main.py --players=Bot1:BuildAndRunBot,Bot2:BuilderBot --algorithm=DivideAndConquer --rounds=5
```

#### DP con RunnerBot
```bash
python main.py --players=Tú:Human,IA:RunnerBotImproved --algorithm=DynamicProgramming
```

#### Configuración personalizada
```bash
python main.py --players=A:Human,B:RandomBot --cols=7 --rows=7 --square_size=48
```

## Análisis de Algoritmos

### Complejidad Comparativa

| Algoritmo | Temporal | Espacial | Optimalidad | Uso |
|-----------|----------|----------|-------------|-----|
| **Greedy** | O(n) | O(1) | ❌ | Rápido |
| **Divide & Conquer** | O(n log n) | O(log n) | ✅ | Óptimo |
| **Dynamic Programming** | O(n²) | O(n) | ✅ | Exacto |
| **BFS** | O(V + E) | O(V) | ✅ | Camino más corto |

### Performance en Quoridor 9x9

- **Greedy**: ~1ms por decisión
- **D&C con poda**: ~5ms por decisión
- **DP (Bellman-Ford)**: ~50ms por decisión
- **Floyd-Warshall**: ~500ms (precalculado)

## Interfaz Gráfica

El proyecto usa **Pygame** para gráficos modernos y rápidos

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
│   │   ├── GreedyStrategy.py
│   │   ├── DivideAndConquer.py
│   │   └── DynamicProgramming.py
│   ├── interface/              # Componentes gráficos
│   │   ├── Board.py
│   │   ├── Square.py
│   │   ├── Pawn.py
│   │   ├── Fence.py
│   │   ├── Color.py
│   │   └── IDrawable.py
│   ├── player/                 # Tipos de jugadores
│   │   ├── IPlayer.py
│   │   ├── IBot.py
│   │   ├── Human.py
│   │   ├── RandomBot.py
│   │   ├── RunnerBotImproved.py
│   │   ├── BuilderBot.py
│   │   └── BuildAndRunBot.py
│   ├── benchmark/              # Análisis de rendimiento
│   │   └── Profiler.py
│   └── exception/              # Excepciones personalizadas
│       └── PlayerPathObstructedException.py
├── lib/
│   ├── graphics.py             # Graphics legacy (obsoleto)
│   └── graphics_pygame.py      # Pygame moderno
├── main.py                     # Punto de entrada
└── README.md                   # Este archivo
```

## Ejemplos de Desarrollo

### Crear un nuevo Bot

```python
from src.player.IBot import IBot
from src.action.IAction import IAction
from src.algorithm.GreedyStrategy import GreedyStrategy

class MyCustomBot(IBot):
    def play(self, board) -> IAction:
        # Tu lógica aquí
        if self.remainingFences() > 0:
            # Colocar muro
            return some_fence_placing
        else:
            # Mover peón
            return GreedyStrategy.greedyMove(board, self)
```

### Usar algoritmos directamente

```python
from src.algorithm.DivideAndConquer import DivideAndConquer
from src.algorithm.DynamicProgramming import DynamicProgramming

# Divide y Vencerás
best_fence, score = DivideAndConquer.findOptimalFenceWithPruning(board, player)

# Programación Dinámica
distances = DynamicProgramming.bellmanFord(board, start, goals)
```

## Benchmarking

Para medir rendimiento:

```bash
python main.py --players=Bot1:BuildAndRunBot,Bot2:RunnerBotImproved --rounds=10
```

Ver `src/benchmark/Profiler.py` para análisis detallado.

## Autores

- David Rodriguez - 2025
- Pontificia Universidad Javeriana

## Soporte

Para problemas o sugerencias:
1. Revisa `src/Settings.py` para configuración
2. Consulta docstrings en archivos de `src/algorithm/`

---

