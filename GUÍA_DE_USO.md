# Guía de Uso - Quoridor

Guía completa en español para jugar y configurar Quoridor con diferentes algoritmos.

## Requisitos

- Python 3.8 o superior
- Pygame instalado (`pip install pygame`)

## Inicio Rápido

### Forma más simple

```bash
python main.py --players=Yo:Human,IA:BuilderBot
```

Esto abre una partida donde:
- Tú juegas como `Yo` (jugador humano)
- La IA juega como `IA` (estrategia de construcción)

## Tipos de Jugadores Disponibles

### 1. **Human** - Jugador Humano
Controla la partida con el ratón:
- **Clic en cuadro**: Mover el peón
- **Clic en línea/intersección**: Colocar muro

```bash
python main.py --players=Tú:Human,IA:RandomBot
```

### 2. **RandomBot** - Movimientos Aleatorios
La IA elige movimientos al azar (sin estrategia).

```bash
python main.py --players=Yo:Human,Contrincante:RandomBot
```

### 3. **RunnerBotImproved** - Estrategia Voraz (Greedy)
Algoritmo rápido que siempre intenta acercarse a la meta.

```bash
python main.py --players=Yo:Human,IA:RunnerBotImproved
```

### 4. **BuilderBot** - Estrategia de Construcción
Coloca muros para bloquear a los oponentes.

```bash
python main.py --players=Yo:Human,IA:BuilderBot
```

### 5. **BuildAndRunBot** - Estrategia Combinada
Combina construcción de muros + movimiento estratégico.

```bash
python main.py --players=Yo:Human,IA:BuildAndRunBot
```

## Algoritmos Disponibles

### Opción: `--algorithm=Greedy`
Usa estrategia voraz (rápida pero no garantiza óptimo).

```bash
python main.py --players=Yo:Human,IA:BuildAndRunBot --algorithm=Greedy
```

### Opción: `--algorithm=DivideAndConquer`
Usa divide y vencerás (más lento pero mejor decisiones).

```bash
python main.py --players=Yo:Human,IA:BuildAndRunBot --algorithm=DivideAndConquer
```

### Opción: `--algorithm=DynamicProgramming`
Usa programación dinámica (preciso pero más lento).

```bash
python main.py --players=Yo:Human,IA:BuildAndRunBot --algorithm=DynamicProgramming
```

## Ejemplos de Partidas

### Partida: Tú vs BuilderBot (Greedy)
```bash
python main.py --players=Yo:Human,IA:BuilderBot --algorithm=Greedy
```

### Partida: 4 Jugadores (todos bots)
```bash
python main.py --players=Bot1:RandomBot,Bot2:RunnerBotImproved,Bot3:BuilderBot,Bot4:BuildAndRunBot --rounds=1
```

### Partida: Múltiples Rondas
```bash
python main.py --players=Yo:Human,IA:BuildAndRunBot --rounds=5
```

Esto juega 5 rondas y muestra el ganador final.

### Partida: Tablero Personalizado (7x7)
```bash
python main.py --players=Yo:Human,IA:BuilderBot --cols=7 --rows=7 --square_size=48
```

### Partida: Con más muros (30 en lugar de 20)
```bash
python main.py --players=Yo:Human,IA:BuildAndRunBot --fences=30
```

## Comparativa de Estrategias

### 1. RandomBot
- Muy rápido
- Movimientos aleatorios
- Predecible
- Bueno para aprender

### 2. RunnerBotImproved (Greedy)
- Muy rápido (~1ms/decisión)
- Va hacia la meta
- Vulnerable a bloqueos
- Desafiante

### 3. BuilderBot
- Rápido (~50ms/decisión)
- Bloquea oponentes
- Buena defensa
- No muy agresivo

### 4. BuildAndRunBot
- Rápido (~100ms/decisión)
- Equilibrado ofensa/defensa
- Desafiante
- Recomendado

## Modo Torneo

Juega varias rondas para ver quién gana más:

```bash
python main.py --players=Humano:Human,IA1:BuildAndRunBot,IA2:RunnerBotImproved,IA3:BuilderBot --rounds=10
```

Resultado después de 10 rondas:
```
Ronda #1: El jugador IA1 ganó
Ronda #2: El jugador IA2 ganó
...
PUNTUACIONES FINALES:
- Humano: 3
- IA1: 4
- IA2: 2
- IA3: 1
¡El jugador IA1 ganó con 4 victorias!
```

## Configuración Avanzada

### Combinación: Algoritmo + Tipo de Bot

```bash
# BuildAndRunBot con Divide & Conquer
python main.py --players=Yo:Human,IA:BuildAndRunBot --algorithm=DivideAndConquer

# RunnerBot con Dynamic Programming
python main.py --players=Yo:Human,IA:RunnerBotImproved --algorithm=DynamicProgramming
```

### Configuración de Tablero

```bash
# Tablero pequeño y rápido (5x5)
python main.py --players=Yo:Human,IA:RandomBot --cols=5 --rows=5 --fences=10

# Tablero grande y desafiante (11x11)
python main.py --players=Yo:Human,IA:BuildAndRunBot --cols=11 --rows=11 --fences=30

# Tablero grande en pantalla pequeña
python main.py --players=Yo:Human,IA:BuilderBot --square_size=24 --fences=15
```

## Controles del Juego

### Con Jugador Human

**Mover peón:**
1. Haz clic en un cuadro adyacente a tu peón
2. Si hay oponente, se activa salto (si es posible)

**Colocar muro:**
1. Haz clic en las líneas entre cuadros (no en los cuadros)
2. El muro se coloca si es válido (no bloquea todos los caminos)

**Salir:**
- Cierra la ventana

## Optimización de Rendimiento

### Para juego más rápido:
```bash
# Tablero pequeño, algoritmo rápido
python main.py --players=Bot1:BuildAndRunBot,Bot2:RandomBot --cols=5 --rows=5 --algorithm=Greedy
```

### Para mejor IA:
```bash
# Tablero normal, algoritmo lento pero preciso
python main.py --players=Yo:Human,IA:BuildAndRunBot --algorithm=DynamicProgramming
```

## Solución de Problemas

### "No aparece la ventana"
```bash
# Verifica que INTERFACE = True en src/Settings.py
# Reinstala Pygame: pip install --upgrade pygame
```

### "El juego es muy lento"
```bash
# Reduce el tamaño del tablero
python main.py --players=Yo:Human,IA:BuilderBot --cols=7 --rows=7

# O usa algoritmo Greedy
python main.py --players=Yo:Human,IA:BuildAndRunBot --algorithm=Greedy
```

### "La IA es muy fácil/difícil"
```bash
# Demasiado fácil: usa BuildAndRunBot + DynamicProgramming
python main.py --players=Yo:Human,IA:BuildAndRunBot --algorithm=DynamicProgramming

# Demasiado difícil: usa RandomBot
python main.py --players=Yo:Human,IA:RandomBot
```

## Análisis de Rendimiento

Ver estadísticas de tiempo de ejecución:

```bash
python main.py --players=Bot1:BuildAndRunBot,Bot2:RunnerBotImproved --rounds=5
```

Al final verás:
```
Trazas (TRACE):
Path.BreadthFirstSearch: 240
Board.validPawnMoves: 120
Board.getFencePlacingImpactOnPaths: 50
...
```

## Aprender sobre Algoritmos

### Ver implementación:
- **Greedy**: `src/algorithm/GreedyStrategy.py`
- **Divide & Conquer**: `src/algorithm/DivideAndConquer.py`
- **Dynamic Programming**: `src/algorithm/DynamicProgramming.py`

### Ver uso en bots:
- **RunnerBotImproved**: `src/player/RunnerBotImproved.py`
- **BuilderBot**: `src/player/BuilderBot.py`
- **BuildAndRunBot**: `src/player/BuildAndRunBot.py`

## Referencias

- Análisis de algoritmos aplicados a juegos
- Estrategias de IA en tiempo real
- Optimización de pathfinding

---

**¿Necesitas ayuda?** Revisa los docstrings en el código o ejecuta:
```bash
python main.py -h
```

¡Que disfrutes jugando Quoridor! 
