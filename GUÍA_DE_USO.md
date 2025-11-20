# Guía de Uso - Quoridor

Guía completa en español para jugar y configurar Quoridor con diferentes algoritmos.

## Requisitos

- Python 3.8 o superior
- Pygame instalado (`pip install pygame`)

## Inicio Rápido

### Forma más simple

```bash
python main.py --players=Yo:Human,IA:BuildAndRunBot
```

Esto abre una partida donde:
- Tú juegas como `Yo` (jugador humano)
- La IA juega como `IA` usando **Divide and Conquer** (algoritmo fijo del BuildAndRunBot)

## IMPORTANTE: Algoritmos Fijos por Bot

**CADA BOT TIENE SU ALGORITMO FIJO** que no puede ser cambiado:

| Bot | Algoritmo Fijo | Descripción |
|-----|----------------|-------------|
| **RandomBot** | Ninguno (Aleatorio) | Decisiones completamente aleatorias |
| **RunnerBotImproved** | **Greedy Strategy** | Estrategia voraz, siempre busca camino más corto |
| **BuilderBot** | **Dynamic Programming** | Programación dinámica para muros estratégicos |
| **BuildAndRunBot** | **Divide and Conquer** | Divide y vencerás, estrategia balanceada |

**Ya NO existe el parámetro `--algorithm`** porque cada bot está diseñado específicamente para usar un algoritmo particular.

## Tipos de Jugadores Disponibles

### 1. **Human** - Jugador Humano
Controla la partida manualmente con el ratón:
- **Clic en cuadro adyacente**: Mover el peón a esa posición
- **Clic en línea/intersección**: Colocar muro vertical/horizontal
- **Tecla P**: Mostrar/ocultar movimientos válidos
- **Tecla F**: Mostrar/ocultar posiciones de muros válidas
- **Escape**: Salir del juego

**Algoritmo**: No aplica (control manual)

**Ejemplos de uso:**
```bash
# Básico contra RandomBot
python main.py --players=Tú:Human,IA:RandomBot

# Contra RunnerBot (usa Greedy)
python main.py --players=Tú:Human,IA:RunnerBotImproved

# Torneo con múltiples bots
python main.py --players=Tú:Human,Bot1:BuilderBot,Bot2:BuildAndRunBot --rounds=3
```

### 2. **RandomBot** - Movimientos Aleatorios
La IA toma decisiones completamente al azar:
- 33% de probabilidad de intentar colocar muro
- 67% de probabilidad de mover peón aleatoriamente
- Evita muros que bloquean completamente caminos

**Algoritmo Fijo**: Ninguno (Random)
**Complejidad**: O(1) por decisión
**Ventajas**: Muy rápido, impredecible
**Desventajas**: Sin estrategia, fácil de vencer
**Uso**: Baseline para pruebas, aprendizaje básico

**Ejemplos de uso:**
```bash
# Básico para aprender
python main.py --players=Yo:Human,Contrincante:RandomBot

# Torneo con múltiples RandomBots
python main.py --players=Bot1:RandomBot,Bot2:RandomBot,Bot3:RandomBot,Bot4:RandomBot --rounds=10

# Tablero pequeño para pruebas rápidas
python main.py --players=Yo:Human,IA:RandomBot --cols=5 --rows=5 
```

### 3. **RunnerBotImproved** - Estrategia Voraz (Greedy)
**ALGORITMO FIJO: GREEDY STRATEGY (Estrategia Voraz)**

Siempre elige el movimiento que más reduce la distancia a la meta:
- Usa BFS para calcular camino más corto
- Toma primer paso del camino óptimo (decisión voraz)
- NO anticipa bloqueos futuros
- Tiene fallback a movimientos aleatorios si bloqueado

**Complejidad**: O(V + E) ≈ O(405) por decisión
**Ventajas**: Rápido (~1ms/decisión), directo a la meta
**Desventajas**: No anticipa bloqueos, vulnerable a trampas
**Uso**: Bueno contra oponentes pasivos, desafiante pero predecible

**Características del Algoritmo Voraz:**
- ✓ Toma decisión óptima local en cada paso
- ✓ No requiere backtracking
- ✗ NO garantiza solución óptima global
- ✗ Puede quedar atrapado en mínimos locales

**Ejemplos de uso:**
```bash
# Básico con estrategia voraz (fija)
python main.py --players=Yo:Human,IA:RunnerBotImproved

# Torneo entre RunnerBots
python main.py --players=Greedy1:RunnerBotImproved,Greedy2:RunnerBotImproved --rounds=5

# Comparar Greedy vs otros algoritmos
python main.py --players=Greedy:RunnerBotImproved,DP:BuilderBot,DnC:BuildAndRunBot --rounds=10
```

### 4. **BuilderBot** - Programación Dinámica
**ALGORITMO FIJO: DYNAMIC PROGRAMMING (Programación Dinámica)**

Se enfoca en colocar muros estratégicos:
- Calcula impacto de cada muro posible en todos los caminos
- Usa memoización y tablas DP para eficiencia
- Elige muro que maximiza bloqueo de oponentes vs. auto-bloqueo
- Actualización incremental de estados (no recalcula todo)
- Cuando no hay muros buenos, mueve aleatoriamente

**Complejidad**: O(n × (V + E)) con optimización DP (vs O(n²) sin DP)
**Ventajas**: Excelente defensa, controla el tablero, ~9x más rápido con DP
**Desventajas**: Más lento que Greedy (~50ms/decisión), no agresivo en movimiento
**Uso**: Contra oponentes que avanzan directamente, estrategia defensiva

**Características de Dynamic Programming:**
- ✓ Memoización de subproblemas
- ✓ Reutilización de cálculos previos
- ✓ Actualización incremental eficiente
- ✓ Garantiza optimalidad en colocación de muros

**Ejemplos de uso:**
```bash
# Básico con estrategia DP (fija)
python main.py --players=Yo:Human,IA:BuilderBot

# Batalla entre BuilderBots (ambos usan DP)
python main.py --players=DP_Bot1:BuilderBot,DP_Bot2:BuilderBot --rounds=3

# Comparar DP vs Greedy
python main.py --players=DP:BuilderBot,Greedy:RunnerBotImproved --rounds=10
```

### 5. **BuildAndRunBot** - Divide y Vencerás
**ALGORITMO FIJO: DIVIDE AND CONQUER (Divide y Vencerás)**

Mejor bot disponible, combina ofensa y defensa:
- **Con muros**: Usa D&C con poda para colocar estratégicamente
- **Sin muros**: Usa Greedy para avanzar eficientemente
- Particiona espacio de búsqueda recursivamente
- Aplica poda de candidatos prometedores
- Equilibra construcción de muros con progreso hacia meta

**Complejidad**: O(k log k) donde k ≈ 20 candidatos (vs O(n²) fuerza bruta)
**Ventajas**: Completo, desafiante (~100ms/decisión), adaptable, ~18x más rápido con D&C
**Desventajas**: Más lento que bots especializados
**Uso**: Partidas competitivas, desafíos, mejor experiencia de juego

**Características de Divide and Conquer:**
- ✓ Partición recursiva del espacio de búsqueda
- ✓ Poda de candidatos no prometedores
- ✓ Complejidad logarítmica
- ✓ Casi-óptimo con alta eficiencia

**Ejemplos de uso:**
```bash
# Básico - el bot más equilibrado (usa D&C fijo)
python main.py --players=Yo:Human,IA:BuildAndRunBot

# Torneo entre BuildAndRunBots (todos usan D&C)
python main.py --players=DnC1:BuildAndRunBot,DnC2:BuildAndRunBot --rounds=5

# Máxima dificultad
python main.py --players=Yo:Human,IA1:BuildAndRunBot,IA2:BuildAndRunBot --rounds=3
```

### 6. **MyBot** - Plantilla Personalizada
Clase base vacía para implementar tu propia estrategia:
- Hereda de IBot
- Método `play(board)` vacío para lógica custom
- Permite experimentación con algoritmos propios

**Algoritmo**: Depende de implementación (por defecto ninguno)
**Uso**: Desarrollo de nuevas estrategias de IA

**Ejemplos de uso:**
```bash
# Usar la plantilla base (no hace nada)
python main.py --players=Yo:Human,MyBot:MyBot

# Después de implementar lógica custom
python main.py --players=MiEstrategia:MyBot,Oponente:RandomBot
```

## Comparativa de Algoritmos

### **Tabla Comparativa de Bots y Algoritmos**

| Bot | Algoritmo | Complejidad | Velocidad | Estrategia | Optimalidad |
|-----|-----------|-------------|-----------|------------|-------------|
| **RandomBot** | None (Random) | O(1) | Muy rápido | Ninguna | ✗ |
| **RunnerBotImproved** | Greedy | O(V+E) | Muy rápido | Voraz (local) | ✗ |
| **BuilderBot** | Dynamic Programming | O(n×(V+E)) | Rápido | Defensiva | ✓ (local) |
| **BuildAndRunBot** | Divide & Conquer | O(k log k) | Moderado | Híbrida | ✓ (casi-óptimo) |

### **Análisis de Algoritmos**

#### **1. Random - Sin Algoritmo**
- **Velocidad**: ~0.1ms/decisión
- **Estrategia**: Completamente aleatoria
- **Uso**: Baseline, pruebas, aprendizaje
- **Rendimiento**: Débil, predecible

#### **2. Greedy Strategy (RunnerBotImproved)**
- **Velocidad**: ~1ms/decisión
- **Estrategia**: Minimizar distancia inmediata
- **Ventaja**: Rápido, simple, directo
- **Desventaja**: No anticipa, vulnerable a trampas
- **Rendimiento**: Medio, bueno en tableros simples

#### **3. Dynamic Programming (BuilderBot)**
- **Velocidad**: ~50ms/decisión
- **Estrategia**: Memoización y reutilización de cálculos
- **Ventaja**: Defensa excelente, control de tablero
- **Desventaja**: Movimiento no optimizado
- **Rendimiento**: Alto en defensa, medio en ataque

#### **4. Divide and Conquer (BuildAndRunBot)**
- **Velocidad**: ~100ms/decisión
- **Estrategia**: Partición recursiva con poda
- **Ventaja**: Equilibrio perfecto ofensa/defensa
- **Desventaja**: Más lento que especializados
- **Rendimiento**: Muy alto, más desafiante

### **Recomendaciones por Nivel**

#### **Principiante - Aprender Reglas**
```bash
# Fácil de vencer, sin algoritmo
python main.py --players=Yo:Human,IA:RandomBot
```

#### **Intermedio - Entender Estrategia Voraz**
```bash
# Desafiante pero justo, usa Greedy
python main.py --players=Yo:Human,IA:RunnerBotImproved
```

#### **Avanzado - Enfrentar Programación Dinámica**
```bash
# Defensa fuerte con DP
python main.py --players=Yo:Human,IA:BuilderBot
```

#### **Experto - Máximo Desafío con D&C**
```bash
# Estrategia completa con Divide & Conquer
python main.py --players=Yo:Human,IA:BuildAndRunBot
```

#### **Investigación - Comparar Algoritmos**
```bash
# Torneo entre diferentes algoritmos
python main.py --players=Random:RandomBot,Greedy:RunnerBotImproved,DP:BuilderBot,DnC:BuildAndRunBot --rounds=20
```

## Ejemplos de Partidas

### Partida: Tú vs BuilderBot (Dynamic Programming)
```bash
python main.py --players=Yo:Human,IA:BuilderBot
```

### Partida: 4 Jugadores (todos los algoritmos)
```bash
python main.py --players=Random:RandomBot,Greedy:RunnerBotImproved,DP:BuilderBot,DnC:BuildAndRunBot --rounds=1
```

### Partida: Múltiples Rondas
```bash
python main.py --players=Yo:Human,IA:BuildAndRunBot --rounds=5
```

### Partida: Tablero Personalizado (7x7)
```bash
python main.py --players=Yo:Human,IA:BuilderBot --cols=7 --rows=7 --square_size=48
```

### Partida: Con más muros (10 en lugar de 5)
```bash
python main.py --players=Yo:Human,IA:BuildAndRunBot --fences=10
```

### Partida: Torneo de Algoritmos
```bash
# Ver cuál algoritmo es mejor en 50 rondas
python main.py --players=Greedy:RunnerBotImproved,DP:BuilderBot,DnC:BuildAndRunBot --rounds=50
```

## Configuración Avanzada

### Tableros de Diferentes Tamaños

```bash
# Tablero pequeño y rápido (5x5)
python main.py --players=Yo:Human,IA:RandomBot --cols=5 --rows=5 --fences=5

# Tablero grande y desafiante (11x11)
python main.py --players=Yo:Human,IA:BuildAndRunBot --cols=11 --rows=11 --fences=10

# Tablero grande en pantalla pequeña
python main.py --players=Yo:Human,IA:BuilderBot --square_size=24 --fences=5
```

## Modo Torneo

Juega varias rondas para ver cuál algoritmo gana más:

```bash
python main.py --players=Random:RandomBot,Greedy:RunnerBotImproved,DP:BuilderBot,DnC:BuildAndRunBot --rounds=10
```

Resultado después de 10 rondas:
```
CONFIGURACIÓN DE JUGADORES Y ALGORITMOS
========================================
  Random (RandomBot) → Algoritmo: None (Random)
  Greedy (RunnerBotImproved) → Algoritmo: Greedy Strategy
  DP (BuilderBot) → Algoritmo: Dynamic Programming
  DnC (BuildAndRunBot) → Algoritmo: Divide and Conquer
========================================

Ronda #1: El jugador DnC ganó
Ronda #2: El jugador DP ganó
...
PUNTUACIONES FINALES:
- Random: 0
- Greedy: 2
- DP: 3
- DnC: 5
¡El jugador DnC ganó con 5 victorias!
```

## Controles del Juego

### Con Jugador Human

**Mover peón:**
1. Presiona **P** para mostrar movimientos válidos
2. Haz clic en un cuadro resaltado

**Colocar muro:**
1. Presiona **F** para mostrar posiciones de muros válidas (si tienes muros)
2. Haz clic en una línea resaltada entre cuadros

**Salir:**
- Presiona **Escape** o cierra la ventana

## Optimización de Rendimiento

### Para juego más rápido (Greedy o Random):
```bash
# Algoritmos rápidos
python main.py --players=Bot1:RunnerBotImproved,Bot2:RandomBot --cols=5 --rows=5
```

### Para mejor IA (D&C o DP):
```bash
# Algoritmos avanzados
python main.py --players=Yo:Human,IA:BuildAndRunBot
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

# O usa bots más rápidos (Greedy o Random)
python main.py --players=Yo:Human,IA:RunnerBotImproved
```

### "La IA es muy fácil/difícil"
```bash
# Demasiado fácil: usa BuildAndRunBot (D&C)
python main.py --players=Yo:Human,IA:BuildAndRunBot

# Demasiado difícil: usa RandomBot
python main.py --players=Yo:Human,IA:RandomBot

# Intermedio: usa RunnerBotImproved (Greedy)
python main.py --players=Yo:Human,IA:RunnerBotImproved
```

## Análisis de Rendimiento

Ver estadísticas de tiempo de ejecución:

```bash
python main.py --players=DnC:BuildAndRunBot,Greedy:RunnerBotImproved --rounds=5
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

### Ver implementación de algoritmos:
- **Greedy Strategy**: `src/algorithm/GreedyStrategy.py`
- **Divide & Conquer**: `src/algorithm/DivideAndConquer.py`
- **Dynamic Programming**: `src/algorithm/DynamicProgramming.py`

### Ver uso en bots:
- **RunnerBotImproved** (Greedy): `src/player/RunnerBotImproved.py`
- **BuilderBot** (DP): `src/player/BuilderBot.py`
- **BuildAndRunBot** (D&C): `src/player/BuildAndRunBot.py`

### Comparar algoritmos empíricamente:
```bash
# Torneo largo para estadísticas
python main.py --players=Greedy:RunnerBotImproved,DP:BuilderBot,DnC:BuildAndRunBot --rounds=100
```

## Referencias

- Cada bot implementa un algoritmo específico de manera fija
- Los algoritmos NO son intercambiables entre bots
- Cada bot está optimizado para su algoritmo particular

---

**¿Necesitas ayuda?** Revisa los docstrings en el código o ejecuta:
```bash
python main.py -h
```

¡Que disfrutes jugando Quoridor y comparando algoritmos!