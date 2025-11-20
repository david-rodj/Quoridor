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
          "      \t\t\t  RandomBot: Movimientos aleatorios, sin estrategia ni algoritmo\n"+
          "      \t\t\t  RunnerBotImproved: Usa algoritmo Greedy (voraz) - siempre busca camino más corto\n"+
          "      \t\t\t  BuilderBot: Usa algoritmo DynamicProgramming - estrategia defensiva avanzada\n"+
          "      \t\t\t  BuildAndRunBot: Usa algoritmo DivideAndConquer - estrategia balanceada óptima\n"+
          "  -r, --rounds=\t\tNúmero de rondas a jugar (por defecto 1)\n"+
          "  -x, --cols=\t\tNúmero de columnas del tablero (por defecto 9)\n"+
          "  -y, --rows=\t\tNúmero de filas del tablero (por defecto 9)\n"+
          "  -f, --fences=\t\tNúmero de muros por jugador (por defecto 5)\n"+
          "  -s, --square_size=\tTamaño de cada casilla en píxeles (por defecto 32)\n\n"+
          "NOTA: Cada bot tiene su algoritmo fijo asignado:\n"+
          "  - RunnerBotImproved → Greedy Strategy (Estrategia Voraz)\n"+
          "  - BuilderBot → Dynamic Programming (Programación Dinámica)\n"+
          "  - BuildAndRunBot → Divide and Conquer (Divide y Vencerás)\n\n"+
          "Ejemplo:\n  python main.py --players=Me:Human,IA:BuildAndRunBot --fences=5 --square_size=32")

def readArguments():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:r:w:x:y:s:fh", ["players=", "rounds=", "cols=", "rows=", "fences=", "square_size=", "help"])
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
        else:
            print("Opción no manejada. Abortando.")
            sys.exit(PARAMETERS_ERROR_RETURN_CODE)
    
    return players, rounds, cols, rows, fencesPerPlayer, squareSize

def main():
    players, rounds, cols, rows, fencesPerPlayer, squareSize = readArguments()

    # Mostrar información de algoritmos asignados
    print("\n" + "="*60)
    print("CONFIGURACIÓN DE JUGADORES Y ALGORITMOS")
    print("="*60)
    for p in players:
        algo_info = getattr(p, 'ALGORITHM', 'N/A')
        bot_type = type(p).__name__
        print(f"  {p.name} ({bot_type}) → Algoritmo: {algo_info}")
    print("="*60 + "\n")

    game = Game(players, cols, rows, fencesPerPlayer, squareSize)
    game.start(rounds)
    game.end()

    global TRACE
    print("\nTrazas (TRACE):")
    for i in TRACE:
        print("%s: %s" % (i, TRACE[i]))

main()