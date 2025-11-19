from src.player.IPlayer      import *
from src.action.FencePlacing import *



class PlayerPathObstructedException(Exception):
        def __init__(self, player: IPlayer, fencePlacing: FencePlacing = None):
            self.message = "El camino del jugador %s está obstruido" % (player)
            if fencePlacing is not None:
                self.message += " por %s" % (fencePlacing)
