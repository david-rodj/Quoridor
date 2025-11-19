from src.player.IBot import *
from src.action.IAction import *
from src.Path import *
from src.algorithm.GreedyStrategy import GreedyStrategy
from src.benchmark.Profiler import Profiler
from src.algorithm.DynamicProgramming import DynamicProgramming


class RunnerBotImproved(IBot):
    """
    Bot que implementa ESTRATEGIA VORAZ (Greedy) para Quoridor.
    
    ALGORITMO VORAZ:
    En cada turno, seleccionar el movimiento que MÁS REDUCE
    la distancia al objetivo, sin considerar consecuencias futuras.
    
    CARACTERÍSTICAS:
    ✓ Decisiones rápidas: O(V + E) por turno
    ✓ Simple de implementar
    ✓ Bueno contra oponentes pasivos
    ✗ NO garantiza solución óptima
    ✗ Vulnerable a trampas del oponente
    ✗ Puede quedar atrapado en mínimos locales
    
    COMPLEJIDAD POR PARTIDA:
    - Tiempo: O(T × (V + E)) donde T = turnos
    - Para T=30, V=81, E=324: O(12,150) operaciones
    
    OPTIMALIDAD:
    - NO garantizada (ver docs/optimality_analysis.md)
    - Ratio de aproximación: Ilimitado
    - Funciona bien en tableros simples
    """
    
    def __init__(self, name=None, color=None):
        super().__init__(name, color)
        self.move_count = 0
        self.greedy_stats = {
            "total_distance_reduced": 0,
            "moves_made": 0,
            "times_blocked": 0
        }
    
    @Profiler.profile
    def play(self, board) -> IAction:
        """
        ESTRATEGIA VORAZ: Elegir movimiento que minimiza distancia a objetivo.
        
        PSEUDOCÓDIGO:
        1. Calcular camino más corto actual (BFS)
        2. Tomar PRIMER PASO de ese camino (decisión voraz)
        3. NO evaluar alternativas
        4. NO anticipar respuestas del oponente
        
        Complejidad: O(V + E) = O(405)
        """
        # If a preferred algorithm is selected, try to use it
        algo = getattr(self, 'algorithm', None)
        if algo == 'DynamicProgramming':
            # Use DP bellman-ford distances to choose neighbour that reduces distance
            try:
                dist = DynamicProgramming.bellmanFord(board, self.pawn.coord, self.endPositions)
                # choose a valid move that reduces distance
                candidates = board.storedValidPawnMoves[self.pawn.coord]
                best = None
                best_d = float('inf')
                for mv in candidates:
                    d = dist.get(mv.toCoord, float('inf'))
                    if d < best_d:
                        best_d = d
                        best = mv
                if best is not None:
                    move = best
                else:
                    move = GreedyStrategy.greedyMove(board, self)
            except Exception:
                move = GreedyStrategy.greedyMove(board, self)
        else:
            # Usar estrategia voraz explícitamente
            move = GreedyStrategy.greedyMove(board, self)
        
        if move is not None:
            # Estadísticas
            self.move_count += 1
            self.greedy_stats["moves_made"] += 1
            
            # Calcular reducción de distancia (para análisis)
            before = len(Path.BreadthFirstSearch(
                board, self.pawn.coord, self.endPositions, ignorePawns=True
            ).moves)
            
            return move
        
        # Fallback: si voraz falla, intentar cualquier movimiento válido
        self.greedy_stats["times_blocked"] += 1
        return self._fallback_move(board)
    
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
            "strategy_type": "Greedy/Voraz",
            "decision_making": "Local optimum (shortest path first step)",
            "time_complexity": "O(V + E) per turn",
            "space_complexity": "O(V)",
            "optimality_guarantee": "None",
            "approximation_ratio": "Unbounded",
            "best_case": "No opponents or simple board",
            "worst_case": "Intelligent blocking opponent",
            "stats": self.greedy_stats
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
                "path_length": len(path.moves),
                "path": str(path),
                "reasoning": "Minimizes immediate distance to goal",
                "alternatives_considered": 0,
                "lookahead_depth": 0
            }
        else:
            return {
                "decision": "Blocked - No direct path available",
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
                "position": str(self.pawn.coord),
                "goal_distance": len(path.moves),
                "move_chosen": str(path.firstMove()),
                "strategy": "greedy_first_step",
                "alternatives_evaluated": "ninguna (greedy no mira adelante)"
            }
            self.decision_log.append(decision)

            print(f"\n[DECISIÓN VORAZ - Turno {self.move_count}]")
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
                "strategy": "Greedy/Voraz",
                "total_moves": self.move_count,
                "decisions": self.decision_log,
                "stats": self.greedy_stats
            }, f, indent=2)
        print(f"Registro de decisiones exportado a {filename}")