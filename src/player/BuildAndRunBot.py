import random
import time

from src.player.BuilderBot import *
from src.player.RunnerBotImproved import *
from src.action.IAction    import *
from src.algorithm.GreedyStrategy import GreedyStrategy
from src.algorithm.DivideAndConquer import DivideAndConquer



class BuildAndRunBot(BuilderBot, RunnerBotImproved):
    def __init__(self, name=None, color=None):
        super().__init__(name, color)
        self.algorithm = 'DivideAndConquer'  # Default algorithm for balanced strategy
    def play(self, board) -> IAction:
        # If no fence left, fallback to move strategy
        if self.remainingFences() < 1 or len(board.storedValidFencePlacings) < 1:
            return GreedyStrategy.greedyMove(board, self)

        # If algorithm requested for fence placement, use it
        if getattr(self, 'algorithm', None) == 'DivideAndConquer':
            bestFence, score = DivideAndConquer.findOptimalFenceWithPruning(board, self)
            if bestFence is not None and score > 0:
                return bestFence

        # Otherwise use BuilderBot heuristic then Greedy for movement
        fencePlacingImpacts = self.computeFencePlacingImpacts(board)
        # If no valid fence placing, move pawn
        if len(fencePlacingImpacts) < 1:
            return GreedyStrategy.greedyMove(board, self)
        # Choose fence placing with the greatest impact
        bestFencePlacing = self.getFencePlacingWithTheHighestImpact(fencePlacingImpacts)
        # If impact is not positive, move pawn
        if fencePlacingImpacts[bestFencePlacing] < 1:
            return GreedyStrategy.greedyMove(board, self)
        return bestFencePlacing
