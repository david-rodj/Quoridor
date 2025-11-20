import getopt

from src.Settings              import *
from src.Game                  import *
from src.player.Human          import *
from src.player.RandomBot      import *
from src.player.RunnerBotImproved import *
from src.player.BuilderBot     import *
from src.player.BuildAndRunBot import *
import sys


PARAMETERS_ERROR_RETURN_CODE = 1

def printUsage():
    print("Uso: python main.py [opciones]\n\n"+
          "Opciones:\n"+
          "  -h, --help\t\t\tMostrar esta ayuda\n"+
          "  -p, --players=\t\tLista de jugadores en formato Nombre:TipoJugador,ej: Me:Human,Benoit:BuilderBot\n"+
          "      \t\t\tTipos disponibles:\n"+
          "      \t\t\t  Human: Jugador humano con control por mouse/teclado\n"+
          "      \t\t\t  RandomBot: Movimientos aleatorios, sin estrategia\n"+
          "      \t\t\t  RunnerBotImproved: Estrategia voraz, siempre busca el camino más corto a la meta\n"+
          "      \t\t\t  BuilderBot: Enfocado en colocar muros para bloquear oponentes\n"+
          "      \t\t\t  BuildAndRunBot: Combina colocación de muros y movimiento estratégico\n"+
          "  -r, --rounds=\t\tNúmero de rondas a jugar (por defecto 1)\n"+
          "  -x, --cols=\t\tNúmero de columnas del tablero (por defecto 9)\n"+
          "  -y, --rows=\t\tNúmero de filas del tablero (por defecto 9)\n"+
          "  -f, --fences=\t\tNúmero de muros por jugador (por defecto 5)\n"+
          "  -s, --square_size=\tTamaño de cada casilla en píxeles (por defecto 32)\n"+
          "  -a, --algorithm=\tAlgoritmo global para bots. Opciones: Greedy | DivideAndConquer | DynamicProgramming\n\n"+
          "Ejemplo:\n  python main.py --players=Me:Human,Benoit:BuilderBot --algorithm=DivideAndConquer --fences=5 --square_size=32")

def readArguments():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:r:w:x:y:s:fha:", ["players=", "rounds=", "cols=", "rows=", "fences=", "square_size=", "help", "algorithm="])
    except getopt.GetoptError as err:
        print(err)
        printUsage()
        sys.exit(PARAMETERS_ERROR_RETURN_CODE)
    players = []
    rounds = 1
    cols = 9
    rows = 9
    fencesPerPlayer = 5
    squareSize = 32
    selected_algorithm = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printUsage()
            sys.exit(0)
        elif opt in ("-p", "--players"):
            for playerData in arg.split(","):
                playerName, playerType = playerData.split(":")
                if playerType not in globals():
                    print("Tipo de jugador desconocido: %s. Abortando." % (playerType))
                    sys.exit(PARAMETERS_ERROR_RETURN_CODE)
                players.append(globals()[playerType](playerName))
            # If a global algorithm was specified, propagate to created players later
            if len(players) not in (2, 4):
                print("Se esperan 2 o 4 jugadores. Abortando.")
                sys.exit(PARAMETERS_ERROR_RETURN_CODE)
        elif opt in ("-r", "--rounds"):
            rounds = int(arg)
        elif opt in ("-x", "--cols"):
            cols = int(arg)
        elif opt in ("-y", "--rows"):
            rows = int(arg)
        elif opt in ("-f", "--fences"):
            fencesPerPlayer = int(arg)
        elif opt in ("-s", "--square_size"):
            squareSize = int(arg)
        elif opt in ("-a", "--algorithm"):
            selected_algorithm = arg
        else:
            print("Opción no manejada. Abortando.")
            sys.exit(PARAMETERS_ERROR_RETURN_CODE)
    return players, rounds, cols, rows, fencesPerPlayer, squareSize, selected_algorithm

def main():
    players, rounds, cols, rows, fencesPerPlayer, squareSize, selected_algorithm = readArguments()

    game = Game(players, cols, rows, fencesPerPlayer, squareSize)
    # If the user specified a global algorithm, set it on all players that support it
    if selected_algorithm is not None:
        for p in players:
            try:
                p.set_algorithm(selected_algorithm)
            except Exception:
                # player may not implement set_algorithm; ignore
                pass
    game.start(rounds)
    game.end()

    global TRACE
    print("Trazas (TRACE):")
    for i in TRACE:
        print("%s: %s" % (i, TRACE[i]))

main()
