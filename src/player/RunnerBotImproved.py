from src.player.IBot import *
from src.action.IAction import *
from src.Path import *
from src.algorithm.GreedyStrategy import GreedyStrategy
from src.benchmark.Profiler import Profiler


class RunnerBotImproved(IBot):
    """
    Bot que implementa ESTRATEGIA VORAZ (Greedy) para Quoridor.
    
    ALGORITMO FIJO: GREEDY STRATEGY (Estrategia Voraz)
    =====================================================
    Este bot SIEMPRE usa estrategia voraz y no puede cambiar de algoritmo.
    
    ALGORITMO VORAZ MEJORADO:
    1. DEFENSA (si hay amenaza): Colocar muro que maximiza diferencia de distancias
    2. OFENSA (por defecto): Mover siempre hacia el camino más corto
    
    ESTRATEGIA:
    - Evalúa amenaza de oponentes (decisión voraz basada en distancias actuales)
    - Si oponente está muy cerca, coloca muro defensivo (maximiza diferencia inmediata)
    - Si no hay amenaza, mueve hacia objetivo (minimiza distancia inmediata)
    - Todas las decisiones son locales y voraces (no planifica múltiples turnos)
    
    CARACTERÍSTICAS:
    ✓ Decisiones rápidas: O(n × (V + E)) para muros, O(V + E) para movimiento
    ✓ Ahora tiene defensa táctica con muros
    ✓ Mantiene velocidad y simplicidad
    ✗ NO garantiza solución óptima
    ✗ Decisiones puramente locales (voraz)
    ✗ Vulnerable a estrategias complejas
    
    COMPLEJIDAD POR TURNO:
    - Con muros: O(n × (V + E)) donde n ≈ 30 muros evaluados
    - Solo movimiento: O(V + E) ≈ O(405)
    - Promedio: ~10-20ms/decisión
    
    OPTIMALIDAD:
    - NO garantizada (característica de algoritmos voraces)
    - Ratio de aproximación: Ilimitado
    - Mejor en tableros simples, vulnerable en complejos
    """
    
    # Algoritmo fijo - NO puede ser cambiado
    ALGORITHM = "Greedy Strategy"
    ALGORITHM_CODE = "GREEDY"
    
    def __init__(self, name=None, color=None):
        super().__init__(name, color)
        # Eliminar la posibilidad de cambiar el algoritmo
        self.move_count = 0
        self.greedy_stats = {
            "total_distance_reduced": 0,
            "moves_made": 0,
            "times_blocked": 0
        }
    
    @Profiler.profile
    def play(self, board) -> IAction:
        """
        ESTRATEGIA VORAZ MEJORADA: Con defensa táctica mediante muros.
        
        PSEUDOCÓDIGO:
        1. Si tengo muros Y oponente está amenazante:
           a. Calcular distancias (voraz)
           b. Si oponente más cerca que yo, colocar muro defensivo (voraz)
        2. Si no, mover usando Greedy hacia objetivo
        
        DECISIÓN VORAZ PARA MUROS:
        - Elegir muro que MAXIMIZA diferencia de distancias
        - No planificar múltiples turnos adelante
        - Decisión basada en estado actual (voraz)
        
        Complejidad: O(n × (V + E)) para muros, O(V + E) para movimiento
        """
        # ESTRATEGIA DEFENSIVA VORAZ: Si tengo muros y oponente está cerca
        if self.remainingFences() > 0 and len(board.storedValidFencePlacings) > 0:
            # Calcular mi distancia a objetivo
            my_path = Path.BreadthFirstSearch(
                board, self.pawn.coord, self.endPositions, ignorePawns=True
            )
            my_distance = len(my_path.moves) if my_path else float('inf')
            
            # Calcular distancia mínima de oponentes
            min_opponent_distance = float('inf')
            closest_opponent = None
            
            for player in board.game.players:
                if player.name != self.name:
                    opp_path = Path.BreadthFirstSearch(
                        board, player.pawn.coord, player.endPositions, ignorePawns=True
                    )
                    if opp_path:
                        opp_distance = len(opp_path.moves)
                        if opp_distance < min_opponent_distance:
                            min_opponent_distance = opp_distance
                            closest_opponent = player
            
            # DECISIÓN VORAZ: Si oponente está más cerca o muy cerca de mí, colocar muro
            threat_threshold = 3  # Oponente es amenaza si está ≤3 casillas más cerca
            if min_opponent_distance < my_distance or (my_distance - min_opponent_distance) <= threat_threshold:
                # Buscar muro que maximice ventaja (GREEDY)
                fence = self._greedy_defensive_fence(board, closest_opponent)
                if fence:
                    self.greedy_stats["moves_made"] += 1
                    return fence
        
        # ESTRATEGIA OFENSIVA VORAZ: Mover hacia objetivo
        move = GreedyStrategy.greedyMove(board, self)
        
        if move is not None:
            # Estadísticas
            self.move_count += 1
            self.greedy_stats["moves_made"] += 1
            
            # Calcular reducción de distancia (para análisis)
            try:
                path = Path.BreadthFirstSearch(
                    board, self.pawn.coord, self.endPositions, ignorePawns=True
                )
                if path:
                    before_distance = len(path.moves)
                    # Estadística guardada para análisis
                    self.greedy_stats["total_distance_reduced"] += 1
            except:
                pass
            
            return move
        
        # Fallback: si voraz falla, intentar cualquier movimiento válido
        self.greedy_stats["times_blocked"] += 1
        return self._fallback_move(board)
    
    def _greedy_defensive_fence(self, board, target_opponent):
        """
        ALGORITMO VORAZ para colocar muro defensivo.
        
        ESTRATEGIA:
        - Evaluar cada muro válido
        - Calcular impacto inmediato en distancias
        - ELEGIR muro con MAYOR diferencia positiva (decisión voraz)
        - NO considerar respuestas futuras
        
        Returns:
            FencePlacing si encuentra buen muro, None si no
        """
        from src.exception.PlayerPathObstructedException import PlayerPathObstructedException
        
        best_fence = None
        best_score = -float('inf')
        
        # Limitar búsqueda a 30 muros aleatorios para mantener velocidad
        import random
        fences_to_check = board.storedValidFencePlacings
        if len(fences_to_check) > 30:
            fences_to_check = random.sample(fences_to_check, 30)
        
        for fence in fences_to_check:
            try:
                impact = board.getFencePlacingImpactOnPaths(fence)
                
                # FUNCIÓN VORAZ: maximizar diferencia
                # Positivo si aumenta más distancia de oponente que mía
                score = 0
                for player_name, distance_increase in impact.items():
                    if player_name == self.name:
                        score -= distance_increase * 1.5  # Penalizar más auto-bloqueo
                    elif target_opponent and player_name == target_opponent.name:
                        score += distance_increase * 2.0  # Priorizar bloquear al más cercano
                    else:
                        score += distance_increase
                
                # DECISIÓN VORAZ: tomar mejor hasta ahora
                if score > best_score:
                    best_score = score
                    best_fence = fence
            
            except PlayerPathObstructedException:
                continue
        
        # Solo devolver muro si tiene impacto positivo significativo
        if best_score > 1.0:
            return best_fence
        
        return None
    
    def _fallback_move(self, board):
        """
        Movimiento de respaldo cuando estrategia voraz falla
        (atrapado sin camino directo).
        """
        valid_moves = board.storedValidPawnMoves[self.pawn.coord]
        if valid_moves:
            # Elegir aleatoriamente entre movimientos válidos
            import random
            return random.choice(valid_moves)
        return None
    
    def get_strategy_info(self):
        """
        Retorna información sobre la estrategia implementada.
        Útil para análisis académico.
        """
        return {
            "bot_class": "RunnerBotImproved",
            "strategy_type": "Greedy/Voraz (Ofensiva + Defensiva)",
            "algorithm": self.ALGORITHM,
            "algorithm_code": self.ALGORITHM_CODE,
            "decision_making": "Local optimum (shortest path + defensive fences)",
            "time_complexity": "O(n × (V + E)) with fences, O(V + E) movement only",
            "space_complexity": "O(V)",
            "optimality_guarantee": "None (greedy limitation)",
            "approximation_ratio": "Unbounded",
            "improvements": [
                "Now places defensive fences when threatened",
                "Evaluates opponent distances (greedy)",
                "Maximizes distance differential (greedy decision)",
                "Still maintains fast movement strategy"
            ],
            "best_case": "Open boards or passive opponents",
            "worst_case": "Intelligent blocking opponents with complex strategies",
            "stats": self.greedy_stats,
            "algorithm_fixed": True
        }
    
    def explain_last_move(self, board):
        """
        Explica por qué se tomó el último movimiento.
        Útil para debugging y enseñanza.
        """
        path = Path.BreadthFirstSearch(
            board, self.pawn.coord, self.endPositions, ignorePawns=False
        )
        
        if path:
            return {
                "decision": "Greedy - Take first step of shortest path",
                "algorithm": self.ALGORITHM,
                "path_length": len(path.moves),
                "path": str(path),
                "reasoning": "Minimizes immediate distance to goal",
                "alternatives_considered": 0,
                "lookahead_depth": 0
            }
        else:
            return {
                "decision": "Blocked - No direct path available",
                "algorithm": self.ALGORITHM,
                "reasoning": "Fallback to any valid move"
            }
    
    def __str__(self):
        return f"[GREEDY BOT] {self.name} ({self.color.name}) - Moves: {self.move_count}"


class RunnerBotWithAnalysis(RunnerBotImproved):
    """
    Variante que incluye análisis detallado de cada decisión.
    Útil para investigación y presentaciones académicas.
    """
    
    def __init__(self, name=None, color=None, verbose=True):
        super().__init__(name, color)
        self.verbose = verbose
        self.decision_log = []
    
    @Profiler.profile
    def play(self, board) -> IAction:
        """Versión con logging detallado de decisiones."""
        
        # Calcular todas las opciones
        path = Path.BreadthFirstSearch(
            board, self.pawn.coord, self.endPositions, ignorePawns=False
        )
        
        if path and self.verbose:
            decision = {
                "turn": self.move_count,
                "algorithm": self.ALGORITHM,
                "position": str(self.pawn.coord),
                "goal_distance": len(path.moves),
                "move_chosen": str(path.firstMove()),
                "strategy": "greedy_first_step",
                "alternatives_evaluated": "ninguna (greedy no mira adelante)"
            }
            self.decision_log.append(decision)

            print(f"\n[DECISIÓN VORAZ - Turno {self.move_count}]")
            print(f"  Algoritmo: {self.ALGORITHM}")
            print(f"  Posición: {self.pawn.coord}")
            print(f"  Distancia al objetivo: {len(path.moves)}")
            print(f"  Movimiento elegido: {path.firstMove()}")
            print(f"  Razonamiento: Primer paso del camino BFS más corto (DECISIÓN VORAZ)")
        
        return super().play(board)
    
    def export_decision_log(self, filename="greedy_decisions.json"):
        """Exporta log de decisiones para análisis."""
        import json
        with open(filename, 'w') as f:
            json.dump({
                "player": self.name,
                "bot_class": "RunnerBotImproved",
                "strategy": "Greedy/Voraz",
                "algorithm": self.ALGORITHM,
                "total_moves": self.move_count,
                "decisions": self.decision_log,
                "stats": self.greedy_stats
            }, f, indent=2)
        print(f"Registro de decisiones exportado a {filename}")