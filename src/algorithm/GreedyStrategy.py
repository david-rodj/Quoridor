#
# GreedyStrategy.py
#
# Implementación y documentación EXPLÍCITA de Estrategia Voraz (Greedy)
# usada por RunnerBot
#
# @author    Sistema Quoridor
# @date      2025.01
# @version   1.0
#

from src.action.IAction import *
from src.Path import *


class GreedyStrategy:
    """
    Estrategia VORAZ (Greedy) para Quoridor.
    
    DEFINICIÓN DE ALGORITMO VORAZ:
    Algoritmo que toma siempre la decisión ÓPTIMA LOCAL en cada paso,
    sin considerar consecuencias futuras, esperando llegar a un
    óptimo global.
    
    APLICACIÓN EN QUORIDOR:
    El RunnerBot implementa estrategia voraz:
    - En cada turno: elegir movimiento que MÁS REDUCE distancia al objetivo
    - Criterio: Camino más corto actual (BFS)
    - Decisión: Primer paso de ese camino
    
    CARACTERÍSTICAS VORAZ:
    ✓ Toma decisión inmediata sin backtracking
    ✓ Elección basada en criterio local (distancia)
    ✓ No considera estados futuros
    ✓ Complejidad baja: O(n) por decisión
    
    OPTIMALIDAD:
    ✗ NO garantiza solución óptima global
    ✓ Encuentra solución rápidamente
    ✓ Buena aproximación en muchos casos
    
    COMPLEJIDAD:
    - Por turno: O(V + E) para BFS = O(81 + 324) ≈ O(405)
    - Total partida: O(T × (V + E)) donde T = turnos
    """
    
    @staticmethod
    def greedyMove(board, player):
        """
        ALGORITMO VORAZ para seleccionar movimiento.
        
        PSEUDOCÓDIGO:
        1. Calcular camino más corto a objetivo (BFS)
        2. TOMAR PRIMER PASO de ese camino (decisión voraz)
        3. NO evaluar alternativas
        
        Esta es la ESENCIA de estrategia voraz: 
        elegir lo que parece mejor AHORA, sin mirar adelante.
        
        Args:
            board: Estado actual del tablero
            player: Jugador que debe mover
            
        Returns:
            PawnMove: Primer movimiento del camino más corto
            
        Complejidad: O(V + E) = O(405)
        Optimalidad: NO garantizada
        """
        # Paso 1: Calcular camino más corto (heurística voraz)
        path = Path.BreadthFirstSearch(
            board, 
            player.pawn.coord, 
            player.endPositions, 
            ignorePawns=False
        )
        
        # Si no hay camino directo, ignorar peones
        if path is None:
            path = Path.BreadthFirstSearch(
                board,
                player.pawn.coord,
                player.endPositions,
                ignorePawns=True
            )
        
        # Paso 2: DECISIÓN VORAZ - tomar primer paso
        # (No se evalúan otras opciones, no se mira el futuro)
        if path is not None:
            return path.firstMove()
        
        return None
    
    @staticmethod
    def greedyFencePlacing(board, player):
        """
        Variante voraz para colocar muros.
        
        CRITERIO VORAZ: Elegir muro con MÁXIMO IMPACTO INMEDIATO
        sobre longitud de caminos de oponentes.
        
        ALGORITMO:
        1. Para cada muro válido:
           - Calcular impacto: Δ distancia oponentes - Δ distancia propia
        2. ELEGIR muro con mayor impacto (decisión voraz)
        3. No considerar respuestas futuras del oponente
        
        Complejidad: O(n × (V + E)) donde n = muros válidos
        """
        best_fence = None
        best_score = -float('inf')
        
        for fence_placing in board.storedValidFencePlacings:
            try:
                impact = board.getFencePlacingImpactOnPaths(fence_placing)
                
                # FUNCIÓN VORAZ: impacto inmediato
                score = 0
                for player_name, distance_increase in impact.items():
                    if player_name == player.name:
                        score -= distance_increase  # Malo para mí
                    else:
                        score += distance_increase  # Bueno (bloquea rival)
                
                # DECISIÓN VORAZ: quedarse con el mejor hasta ahora
                if score > best_score:
                    best_score = score
                    best_fence = fence_placing
            
            except:
                continue
        
        return best_fence
    
    @staticmethod
    def compareWithOptimal(greedy_solution, optimal_solution):
        """
        Compara solución voraz vs solución óptima.
        
        ANÁLISIS DE OPTIMALIDAD:
        La estrategia voraz NO garantiza encontrar la solución óptima.
        
        EJEMPLO DONDE VORAZ FALLA:
        
        Tablero:   P = peón, X = oponente, # = muro, G = objetivo
        
        . . . G        Voraz elige: →
        . # . .        (reduce distancia inmediata)
        P X . .
        
        Resultado: ¡Trampa! X bloqueará camino
        
        Óptimo hubiera sido: ↓ (mayor distancia inicial pero evita bloqueo)
        
        RATIO DE APROXIMACIÓN:
        En casos simples: voraz encuentra óptimo
        En casos complejos: voraz puede ser 2-3x peor que óptimo
        
        Returns:
            dict: Métricas de comparación
        """
        return {
            "greedy_moves": len(greedy_solution) if greedy_solution else None,
            "optimal_moves": len(optimal_solution) if optimal_solution else None,
            "approximation_ratio": (
                len(greedy_solution) / len(optimal_solution)
                if greedy_solution and optimal_solution
                else None
            ),
            "is_optimal": (greedy_solution == optimal_solution),
            "note": "Greedy may find suboptimal solutions in complex scenarios"
        }
    
    @staticmethod
    def explainGreedyProperties():
        """
        Explica propiedades teóricas de algoritmos voraces.
        
        PROPIEDADES:
        
        1. ELECCIÓN VORAZ (Greedy Choice):
           - En cada paso: elegir lo que parece mejor localmente
           - No reconsiderar elecciones previas
           - No backtracking
        
        2. SUBESTRUCTURA ÓPTIMA:
           - Solución óptima contiene soluciones óptimas a subproblemas
           - En Quoridor: NO siempre se cumple
        
        3. MADUREZ (Matroid Property):
           - Quoridor NO es matroid
           - Por eso voraz no garantiza óptimo
        
        VENTAJAS:
        + Simple de implementar
        + Rápido: O(n) o O(n log n)
        + Bajo uso de memoria
        + Buenas soluciones en la práctica
        
        DESVENTAJAS:
        - No garantiza óptimo global
        - Puede quedar atrapado en mínimos locales
        - Sensible a orden de elecciones
        
        CUÁNDO USAR VORAZ:
        ✓ Cuando se necesita rapidez sobre optimalidad perfecta
        ✓ Cuando el problema tiene estructura especial (matroid)
        ✓ Como heurística para problemas NP-completos
        ✓ Para obtener cotas de aproximación
        """
        return {
            "strategy_type": "Greedy/Voraz",
            "decision_making": "Local optimum at each step",
            "backtracking": "No",
            "optimality_guarantee": "No (for Quoridor)",
            "time_complexity": "O(n) to O(n log n)",
            "space_complexity": "O(1) to O(n)",
            "use_cases": ["Fast approximations", "Matroid problems", "Heuristics"]
        }


class GreedyExamples:
    """
    Ejemplos clásicos de algoritmos voraces para comparación.
    """
    
    @staticmethod
    def coinChange(amount, coins):
        """
        Problema del cambio de monedas (voraz funciona para monedas USA).
        Ejemplo donde voraz SÍ encuentra óptimo.
        """
        coins = sorted(coins, reverse=True)
        result = []
        for coin in coins:
            while amount >= coin:
                result.append(coin)
                amount -= coin
        return result if amount == 0 else None
    
    @staticmethod
    def fractionalKnapsack(items, capacity):
        """
        Mochila fraccionaria (voraz encuentra óptimo).
        items = [(valor, peso), ...]
        """
        # Ordenar por valor/peso (decisión voraz)
        items = sorted(items, key=lambda x: x[0]/x[1], reverse=True)
        total_value = 0
        
        for value, weight in items:
            if capacity >= weight:
                total_value += value
                capacity -= weight
            else:
                total_value += value * (capacity / weight)
                break
        
        return total_value