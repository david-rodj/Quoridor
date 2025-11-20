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
Controla la partida manualmente con el ratón:
- **Clic en cuadro adyacente**: Mover el peón a esa posición
- **Clic en línea/intersección**: Colocar muro vertical/horizontal
- **Escape**: Salir del juego

**Ventajas**: Control total, aprendizaje de estrategias
**Desventajas**: Requiere atención constante
**Algoritmos**: No soporta (control manual)

**Ejemplos de uso:**
```bash
# Básico contra RandomBot
python main.py --players=Tú:Human,IA:RandomBot

# Contra RunnerBot (desafiante)
python main.py --players=Tú:Human,IA:RunnerBotImproved

# Torneo con múltiples bots
python main.py --players=Tú:Human,Bot1:BuilderBot,Bot2:BuildAndRunBot --rounds=3
```

### 2. **RandomBot** - Movimientos Aleatorios
La IA toma decisiones completamente al azar:
- 33% de probabilidad de intentar colocar muro
- 67% de probabilidad de mover peón aleatoriamente
- Evita muros que bloquean completamente caminos

**Ventajas**: Muy rápido, impredecible
**Desventajas**: Sin estrategia, fácil de vencer
**Uso**: Baseline para pruebas, aprendizaje básico
**Algoritmos**: No soporta (acciones aleatorias)

**Ejemplos de uso:**
```bash
# Básico para aprender
python main.py --players=Yo:Human,Contrincante:RandomBot

# Torneo con múltiples RandomBots
python main.py --players=Bot1:RandomBot,Bot2:RandomBot,Bot3:RandomBot,Bot4:RandomBot --rounds=10

# Tablero pequeño para pruebas rápidas
python main.py --players=Yo:Human,IA:RandomBot --cols=5 --rows=5 --fences=5
```

### 3. **RunnerBotImproved** - Estrategia Voraz (Greedy)
Siempre elige el movimiento que más reduce la distancia a la meta:
- Usa BFS para calcular camino más corto
- Toma primer paso del camino óptimo
- Soporta algoritmos avanzados (DP para distancias)
- Tiene fallback a movimientos aleatorios si bloqueado

**Ventajas**: Rápido (~1ms/decisión), directo a la meta
**Desventajas**: No anticipa bloqueos, vulnerable a trampas
**Uso**: Bueno contra oponentes pasivos, desafiante pero predecible
**Algoritmos**: Greedy (por defecto), DynamicProgramming

**Ejemplos de uso:**
```bash
# Básico con estrategia voraz
python main.py --players=Yo:Human,IA:RunnerBotImproved

# Con algoritmo Greedy (por defecto)
python main.py --players=Yo:Human,IA:RunnerBotImproved --algorithm=Greedy

# Con Dynamic Programming para mejores cálculos de distancia
python main.py --players=Yo:Human,IA:RunnerBotImproved --algorithm=DynamicProgramming

# Torneo entre RunnerBots con diferentes algoritmos
python main.py --players=GreedyBot:RunnerBotImproved,DPBot:RunnerBotImproved --algorithm=DynamicProgramming --rounds=5
```

### 4. **BuilderBot** - Estrategia de Construcción
Se enfoca en colocar muros estratégicos:
- Calcula impacto de cada muro posible en todos los caminos
- Elige muro que maximiza bloqueo de oponentes vs. auto-bloqueo
- Soporta DivideAndConquer y DynamicProgramming
- Cuando no hay muros buenos, mueve aleatoriamente

**Ventajas**: Excelente defensa, controla el tablero
**Desventajas**: Más lento (~50ms/decisión), no agresivo en movimiento
**Uso**: Contra oponentes que avanzan directamente, estrategia defensiva
**Algoritmos**: DivideAndConquer (recomendado), DynamicProgramming, Greedy

**Ejemplos de uso:**
```bash
# Básico con estrategia de construcción
python main.py --players=Yo:Human,IA:BuilderBot

# Con Divide and Conquer (recomendado para BuilderBot)
python main.py --players=Yo:Human,IA:BuilderBot --algorithm=DivideAndConquer

# Con Dynamic Programming para análisis profundo
python main.py --players=Yo:Human,IA:BuilderBot --algorithm=DynamicProgramming

# Batalla entre BuilderBots con diferentes algoritmos
python main.py --players=DnC_Bot:BuilderBot,DP_Bot:BuilderBot --algorithm=DivideAndConquer --rounds=3
```

### 5. **BuildAndRunBot** - Estrategia Combinada
Mejor bot disponible, combina ofensa y defensa:
- **Con muros**: Usa BuilderBot para colocar estratégicamente
- **Sin muros**: Usa RunnerBotImproved para avanzar eficientemente
- Soporta todos los algoritmos avanzados
- Equilibra construcción de muros con progreso hacia meta

**Ventajas**: Completo, desafiante (~100ms/decisión), adaptable
**Desventajas**: Más lento que bots especializados
**Uso**: Partidas competitivas, desafíos, mejor experiencia de juego
**Algoritmos**: DivideAndConquer (recomendado), DynamicProgramming, Greedy

**Ejemplos de uso:**
```bash
# Básico - el bot más equilibrado
python main.py --players=Yo:Human,IA:BuildAndRunBot

# Con Divide and Conquer (recomendado para máxima dificultad)
python main.py --players=Yo:Human,IA:BuildAndRunBot --algorithm=DivideAndConquer

# Con Dynamic Programming para análisis completo
python main.py --players=Yo:Human,IA:BuildAndRunBot --algorithm=DynamicProgramming

# Con Greedy para velocidad
python main.py --players=Yo:Human,IA:BuildAndRunBot --algorithm=Greedy

# Torneo entre BuildAndRunBots con diferentes algoritmos
python main.py --players=DnC:BuildAndRunBot,DP:BuildAndRunBot,Greedy:BuildAndRunBot --algorithm=DivideAndConquer --rounds=5
```

### 6. **MyBot** - Plantilla Personalizada
Clase base vacía para implementar tu propia estrategia:
- Hereda de IBot
- Método `play(board)` vacío para lógica custom
- Permite experimentación con algoritmos propios

**Uso**: Desarrollo de nuevas estrategias de IA
**Algoritmos**: Depende de implementación (por defecto ninguno)

**Ejemplos de uso:**
```bash
# Usar la plantilla base (no hace nada)
python main.py --players=Yo:Human,MyBot:MyBot

# Después de implementar lógica custom
python main.py --players=MiEstrategia:MyBot,Oponente:RandomBot
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

### Partida: Con más muros (10 en lugar de 5)
```bash
python main.py --players=Yo:Human,IA:BuildAndRunBot --fences=10
```

## Comparativa de Estrategias

### **Diferencias Clave entre Bots**

| Característica | RandomBot | RunnerBotImproved | BuilderBot | BuildAndRunBot |
|----------------|-----------|-------------------|------------|----------------|
| **Velocidad** | Muy rápido | Muy rápido | Rápido | Moderado |
| **Complejidad** | O(1) | O(V+E) | O(n×caminos) | O(n×caminos + V+E) |
| **Estrategia** | Ninguna | Voraz (meta) | Bloqueo | Híbrida |
| **Fortaleza** | Débil | Media | Alta (defensa) | Muy alta |
| **Debilidad** | Predecible | Trampas | Movimiento | Complejidad |

### **Análisis Detallado**

#### **1. RandomBot - Baseline Simple**
- **Modo de juego**: 33% colocar muro aleatorio, 67% mover peón aleatoriamente
- **Ventajas**: Instantáneo, no requiere cálculo
- **Desventajas**: Completamente predecible, fácil de vencer
- **Cuándo usar**: Pruebas, aprendizaje de reglas, contra principiantes
- **Rendimiento**: ~0.1ms/decisión

#### **2. RunnerBotImproved (Greedy) - Movimiento Directo**
- **Modo de juego**: Siempre toma primer paso del camino más corto (BFS)
- **Ventajas**: Rápido, eficiente en espacios abiertos, directo a objetivo
- **Desventajas**: No anticipa bloqueos, vulnerable a "trampas", puede quedar atrapado
- **Cuándo usar**: Contra oponentes pasivos, tableros simples, velocidad máxima
- **Rendimiento**: ~1ms/decisión

#### **3. BuilderBot - Estrategia Defensiva**
- **Modo de juego**: Calcula impacto de muros en caminos de todos los jugadores
- **Ventajas**: Excelente bloqueo, controla flujo del juego, defensivo fuerte
- **Desventajas**: Movimiento aleatorio cuando no construye, puede auto-bloquearse
- **Cuándo usar**: Contra bots agresivos, control de tablero, estrategia paciente
- **Rendimiento**: ~50ms/decisión

#### **4. BuildAndRunBot - IA Completa**
- **Modo de juego**: BuilderBot + RunnerBotImproved combinados
- **Ventajas**: Equilibra ofensa/defensa, adapta a situación, muy desafiante
- **Desventajas**: Más lento, complejo de optimizar
- **Cuándo usar**: Partidas serias, desafíos, mejor experiencia de juego
- **Rendimiento**: ~100ms/decisión

### **Recomendaciones por Nivel**

#### **Principiante**
```bash
# Fácil de vencer, aprender mecánicas
python main.py --players=Yo:Human,IA:RandomBot
```

#### **Intermedio**
```bash
# Desafiante pero justo
python main.py --players=Yo:Human,IA:RunnerBotImproved --algorithm=Greedy
```

#### **Avanzado**
```bash
# Estrategia completa
python main.py --players=Yo:Human,IA:BuildAndRunBot --algorithm=DivideAndConquer
```

#### **Experto**
```bash
# Máxima dificultad
python main.py --players=IA1:BuildAndRunBot,IA2:BuildAndRunBot --algorithm=DynamicProgramming
```

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
python main.py --players=Yo:Human,IA:RandomBot --cols=5 --rows=5 --fences=5

# Tablero grande y desafiante (11x11)
python main.py --players=Yo:Human,IA:BuildAndRunBot --cols=11 --rows=11 --fences=10

# Tablero grande en pantalla pequeña
python main.py --players=Yo:Human,IA:BuilderBot --square_size=24 --fences=5
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
