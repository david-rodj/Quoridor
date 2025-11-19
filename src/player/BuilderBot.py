import random
import time

from src.player.RandomBot import *
from src.action.IAction   import *
from src.exception.PlayerPathObstructedException import *
from src.algorithm.DivideAndConquer import DivideAndConquer
from src.algorithm.DynamicProgramming import DynamicProgramming
from src.algorithm.GreedyStrategy import GreedyStrategy



class BuilderBot(RandomBot):
    def computeFencePlacingImpacts(self, board):
        fencePlacingImpacts = {}
        # Compute impact of every valid fence placing
        for fencePlacing in board.storedValidFencePlacings:
            try:
                impact = board.getFencePlacingImpactOnPaths(fencePlacing)
            # Ignore path if it is blocking a player
            except PlayerPathObstructedException as e:
                continue
            globalImpact = 0
            for playerName in impact:
                globalImpact += (-1 if playerName == self.name else 1) * impact[playerName]
            fencePlacingImpacts[fencePlacing] = globalImpact
        return fencePlacingImpacts

    def getFencePlacingWithTheHighestImpact(self, fencePlacingImpacts):
        return max(fencePlacingImpacts, key = fencePlacingImpacts.get)

    def play(self, board) -> IAction:
        # If no fence left, move pawn (respect algorithm preference)
        if self.remainingFences() < 1 or len(board.storedValidFencePlacings) < 1:
            if getattr(self, 'algorithm', None) == 'Greedy':
                return GreedyStrategy.greedyMove(board, self)
            return self.moveRandomly(board)

        # If an algorithm preference exists, try to use it for fence placement
        if getattr(self, 'algorithm', None) == 'DivideAndConquer':
            bestFence, score = DivideAndConquer.findOptimalFenceWithPruning(board, self)
            if bestFence is not None and score > 0:
                return bestFence

        # DynamicProgramming could be used to precompute distances and then score fences
        if getattr(self, 'algorithm', None) == 'DynamicProgramming':
            # Use a DP precomputation (heavy but illustrative)
            try:
                _ = DynamicProgramming.floydWarshall(board)
            except Exception:
                pass

        # Default behavior: evaluate impacts and choose best
        fencePlacingImpacts = self.computeFencePlacingImpacts(board)
        # If no valid fence placing, move pawn
        if len(fencePlacingImpacts) < 1:
            if getattr(self, 'algorithm', None) == 'Greedy':
                return GreedyStrategy.greedyMove(board, self)
            return self.moveRandomly(board)
        # Choose fence placing with the greatest impact
        bestFencePlacing = self.getFencePlacingWithTheHighestImpact(fencePlacingImpacts)
        # If impact is not positive, move pawn
        if fencePlacingImpacts[bestFencePlacing] < 1:
            if getattr(self, 'algorithm', None) == 'Greedy':
                return GreedyStrategy.greedyMove(board, self)
            return self.moveRandomly(board)
        return bestFencePlacing
