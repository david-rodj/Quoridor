import random

from src.player.IBot    import *
from src.action.IAction import *


class RandomBot(IBot):
    """
    Bot que toma decisiones completamente aleatorias.
    
    ALGORITMO: NINGUNO (Aleatorio)
    ===============================
    Este bot NO usa ningún algoritmo específico, solo genera
    acciones aleatorias válidas.
    
    ESTRATEGIA:
    - 33% probabilidad de intentar colocar muro aleatorio
    - 67% probabilidad de mover peón aleatoriamente
    - Evita muros que bloquean completamente caminos
    - Sin planificación ni análisis
    
    CARACTERÍSTICAS:
    ✓ Muy rápido (~0.1ms/decisión)
    ✓ Impredecible
    ✓ Útil como baseline para comparaciones
    ✗ Sin estrategia
    ✗ Fácil de vencer
    ✗ No aprende ni mejora
    
    COMPLEJIDAD:
    - Temporal: O(1) por decisión
    - Espacial: O(1)
    
    USO:
    - Baseline para pruebas de otros bots
    - Aprendizaje de reglas del juego
    - Partidas casuales rápidas
    """
    
    # No usa algoritmo específico
    ALGORITHM = "None (Random)"
    ALGORITHM_CODE = "RANDOM"
    
    def moveRandomly(self, board) -> IAction:
        """Selecciona un movimiento de peón aleatorio entre los válidos."""
        validPawnMoves = board.storedValidPawnMoves[self.pawn.coord]
        return random.choice(validPawnMoves)

    def placeFenceRandomly(self, board) -> IAction:
        """
        Intenta colocar un muro aleatorio.
        
        Si el muro bloquea completamente a algún jugador,
        intenta hasta 5 veces encontrar uno válido.
        Si falla, mueve el peón.
        """
        randomFencePlacing = random.choice(board.storedValidFencePlacings)
        attempts = 5
        while board.isFencePlacingBlocking(randomFencePlacing) and attempts > 0:
            randomFencePlacing = random.choice(board.storedValidFencePlacings)
            attempts -= 1
        
        if attempts == 0:
            return self.moveRandomly(board)
        
        return randomFencePlacing

    def play(self, board) -> IAction:
        """
        Estrategia completamente aleatoria:
        - 1 de cada 3 veces: intenta colocar muro
        - Resto del tiempo: mueve peón
        """
        # 1 chance over 3 to place a fence
        if random.randint(0, 2) == 0 and self.remainingFences() > 0 and len(board.storedValidFencePlacings) > 0:
            return self.placeFenceRandomly(board)
        else:
            return self.moveRandomly(board)
    
    def get_strategy_info(self):
        """Información sobre la (falta de) estrategia."""
        return {
            "bot_class": "RandomBot",
            "strategy_type": "Random",
            "algorithm": self.ALGORITHM,
            "algorithm_code": self.ALGORITHM_CODE,
            "decision_making": "Uniform random selection",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "optimality_guarantee": "None",
            "best_case": "Never (pure luck)",
            "worst_case": "Always (no strategy)",
            "use_cases": [
                "Baseline for bot comparisons",
                "Learning game rules",
                "Quick casual games",
                "Random testing"
            ],
            "algorithm_fixed": True
        }
    
    def __str__(self):
        return f"[RANDOM BOT] {self.name} ({self.color.name})"