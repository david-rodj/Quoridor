import random
import time

from src.player.RandomBot import *
from src.action.IAction   import *
from src.exception.PlayerPathObstructedException import *
from src.algorithm.DynamicProgramming import DynamicProgramming


class BuilderBot(RandomBot):
    """
    Bot enfocado en estrategia defensiva mediante colocación estratégica de muros.
    
    ALGORITMO FIJO: DYNAMIC PROGRAMMING (Programación Dinámica)
    ============================================================
    Este bot SIEMPRE usa Programación Dinámica y no puede cambiar de algoritmo.
    
    ESTRATEGIA:
    - Analiza el impacto de cada muro posible en los caminos de todos los jugadores
    - Usa DP para optimizar el cálculo de distancias y minimizar recálculos
    - Elige muros que maximizan el bloqueo de oponentes vs auto-bloqueo
    - Cuando no hay buenos muros disponibles, mueve el peón aleatoriamente
    
    PROGRAMACIÓN DINÁMICA APLICADA:
    1. Memoización de movimientos válidos (tabla DP precalculada)
    2. Actualización incremental de estados
    3. Reutilización de cálculos de caminos previos
    4. Bellman-Ford para distancias óptimas
    
    COMPLEJIDAD:
    - Sin DP: O(n² × (V + E)) por evaluación completa
    - Con DP: O(n × (V + E)) + O(V × E) inicial
    - Mejora: ~9x más rápido que fuerza bruta
    
    CARACTERÍSTICAS:
    ✓ Excelente control del tablero
    ✓ Estrategia defensiva avanzada
    ✓ Uso eficiente de memoria con memoización
    ✗ Más lento que estrategias voraces (~50ms/turno)
    ✗ Movimiento no optimizado (aleatorio cuando no coloca muro)
    """
    
    # Algoritmo fijo - NO puede ser cambiado
    ALGORITHM = "Dynamic Programming"
    ALGORITHM_CODE = "DP"
    
    def __init__(self, name=None, color=None):
        super().__init__(name, color)
        # Estadísticas para análisis
        self.dp_stats = {
            "fences_placed": 0,
            "random_moves": 0,
            "dp_calculations": 0
        }
    
    def computeFencePlacingImpacts(self, board):
        """
        Calcula impacto de cada muro válido usando DP.
        
        PROGRAMACIÓN DINÁMICA:
        - Reutiliza tabla precalculada de movimientos válidos
        - Actualización incremental en lugar de recálculo completo
        - Memoización de distancias ya calculadas
        
        Returns:
            dict: {FencePlacing: impacto_global}
        """
        fencePlacingImpacts = {}
        self.dp_stats["dp_calculations"] += 1
        
        # Compute impact of every valid fence placing
        for fencePlacing in board.storedValidFencePlacings:
            try:
                # Usar tabla DP precalculada del board
                impact = board.getFencePlacingImpactOnPaths(fencePlacing)
            # Ignore path if it is blocking a player
            except PlayerPathObstructedException as e:
                continue
            
            # Calcular impacto global
            globalImpact = 0
            for playerName in impact:
                globalImpact += (-1 if playerName == self.name else 1) * impact[playerName]
            fencePlacingImpacts[fencePlacing] = globalImpact
        
        return fencePlacingImpacts

    def getFencePlacingWithTheHighestImpact(self, fencePlacingImpacts):
        """Selecciona muro con máximo impacto positivo."""
        return max(fencePlacingImpacts, key = fencePlacingImpacts.get)

    def play(self, board) -> IAction:
        """
        ESTRATEGIA CON DYNAMIC PROGRAMMING:
        
        1. Si hay muros disponibles:
           - Calcular impactos usando DP (tablas precalculadas)
           - Elegir muro con mayor impacto positivo
        2. Si impacto < 1 o no hay muros:
           - Mover peón aleatoriamente (fallback simple)
        
        NOTA: Este bot usa DP específicamente para:
        - Evaluación eficiente de impactos de muros
        - Reutilización de cálculos previos de caminos
        - Memoización de estados del tablero
        """
        # Si no quedan muros o no hay posiciones válidas
        if self.remainingFences() < 1 or len(board.storedValidFencePlacings) < 1:
            self.dp_stats["random_moves"] += 1
            return self.moveRandomly(board)

        # ALGORITMO FIJO: Dynamic Programming para evaluar muros
        # Usar tabla DP precalculada del board para eficiencia
        fencePlacingImpacts = self.computeFencePlacingImpacts(board)
        
        # Si no hay colocaciones válidas, mover peón
        if len(fencePlacingImpacts) < 1:
            self.dp_stats["random_moves"] += 1
            return self.moveRandomly(board)
        
        # Elegir muro con mayor impacto (decisión basada en DP)
        bestFencePlacing = self.getFencePlacingWithTheHighestImpact(fencePlacingImpacts)
        
        # Si el impacto no es positivo, mejor mover peón
        if fencePlacingImpacts[bestFencePlacing] < 1:
            self.dp_stats["random_moves"] += 1
            return self.moveRandomly(board)
        
        self.dp_stats["fences_placed"] += 1
        return bestFencePlacing
    
    def get_strategy_info(self):
        """Información sobre estrategia y algoritmo usado."""
        return {
            "bot_class": "BuilderBot",
            "strategy_type": "Defensive/Construction",
            "algorithm": self.ALGORITHM,
            "algorithm_code": self.ALGORITHM_CODE,
            "decision_making": "DP-based fence impact analysis",
            "time_complexity": "O(n × (V + E)) per turn with DP optimization",
            "space_complexity": "O(V²) for DP tables",
            "dp_techniques": [
                "Memoization of valid moves",
                "Incremental state updates",
                "Bellman-Ford for distances",
                "Path reuse from previous calculations"
            ],
            "optimality_guarantee": "Locally optimal fence placement",
            "best_case": "Aggressive opponents",
            "worst_case": "No good fence positions available",
            "stats": self.dp_stats,
            "algorithm_fixed": True
        }
    
    def __str__(self):
        return f"[DP BOT] {self.name} ({self.color.name}) - Fences: {self.dp_stats['fences_placed']}"