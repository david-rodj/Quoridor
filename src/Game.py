import random
import time

from src.Settings            import *
from src.interface.Color     import *
from src.interface.Board     import *
from src.interface.Pawn      import *
from src.player.Human        import *
from src.action.PawnMove     import *
from src.action.FencePlacing import *
from src.Path                import *



class Game:
    """
    Define jugadores y parámetros del juego, y gestiona las rondas.
    """

    DefaultColorForPlayer = [
        Color.RED,
        Color.BLUE,
        Color.GREEN,
        Color.ORANGE
    ]

    DefaultNameForPlayer = [
        "1",
        "2",
        "3",
        "4"
    ]

    def __init__(self, players, cols = 9, rows = 9, totalFenceCount = 20, squareSize = 32, innerSize = None):
        if innerSize is None:
            innerSize = int(squareSize/8)
        self.totalFenceCount = totalFenceCount
        self.current_player_index = 0  # Para tracking del jugador actual
        board = Board(self, cols, rows, squareSize, innerSize)
        playerCount = min(int(len(players)/2)*2, 4)
        self.players = []
        for i in range(playerCount):
            if not INTERFACE and isinstance(players[i], Human):
                raise Exception("No es posible iniciar una partida sin interfaz con jugadores humanos")
            if players[i].name is None:
                players[i].name = Game.DefaultNameForPlayer[i]
            if players[i].color is None:
                players[i].color = Game.DefaultColorForPlayer[i]
            players[i].pawn = Pawn(board, players[i])
            players[i].startPosition = board.startPosition(i)
            players[i].endPositions = board.endPositions(i)
            self.players.append(players[i])
        self.board = board

    def start(self, roundCount = 1):
        """
        Inicia una serie de rondas; para cada ronda, solicita sucesivamente a cada jugador que juegue.
        """
        roundNumberZeroFill = len(str(roundCount))
        for roundNumber in range(1, roundCount + 1):
            self.board.current_round = roundNumber
            self.board.initStoredValidActions()
            print("Ronda #%s: " % str(roundNumber).zfill(roundNumberZeroFill), end="")
            playerCount = len(self.players)
            playerFenceCount = self.totalFenceCount
            self.board.fences, self.board.pawns = [], []
            for i in range(playerCount):
                player = self.players[i]
                player.pawn.place(player.startPosition)
                for j in range(playerFenceCount):
                    player.fences.append(Fence(self.board, player))
            self.board.draw()
            
            self.current_player_index = random.randrange(playerCount)
            finished = False
            turn_number = 0

            while not finished:
                turn_number += 1
                self.board.current_turn = turn_number
                player = self.players[self.current_player_index]

                # Redibujar el tablero para actualizar el indicador de turno
                if INTERFACE:
                    self.board.draw()
                
                action = player.play(self.board)
                
                if isinstance(action, PawnMove):
                    player.movePawn(action.toCoord)
                    if player.hasWon():
                        finished = True
                        print("El jugador %s ganó" % player.name)
                        player.score += 1
                elif isinstance(action, FencePlacing):
                    player.placeFence(action.coord, action.direction)
                elif isinstance(action, Quit):
                    finished = True
                    print("El jugador %s se rindió" % player.name)
                
                self.current_player_index = (self.current_player_index + 1) % playerCount
                
                if INTERFACE:
                    time.sleep(TEMPO_SEC)
        
        print()
        print("PUNTUACIONES FINALES:")
        bestPlayer = self.players[0]
        for player in self.players:
            print("- %s: %d" % (str(player), player.score))
            if player.score > bestPlayer.score:
                bestPlayer = player
        print("¡El jugador %s ganó con %d victorias!" % (bestPlayer.name, bestPlayer.score))

    def end(self):
        """
        Llamado al final para cerrar la ventana de la interfaz.
        """
        if INTERFACE:
            self.board.window.close()