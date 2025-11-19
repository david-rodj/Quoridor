#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_fence_blocking.py

Script para probar y verificar que los muros bloqueantes 
NO se puedan colocar según las reglas de Quoridor.

Reproduce el escenario del log donde se colocó incorrectamente
un muro que bloqueó completamente al jugador O.
"""

import sys
sys.path.append('.')

from src.Game import Game
from src.player.Human import Human
from src.player.RandomBot import RandomBot
from src.GridCoordinates import GridCoordinates
from src.interface.Fence import Fence
from src.Path import Path
from src.Settings import *

def print_board_state(board, highlight_coords=None):
    """Imprime el estado del tablero en consola de forma visual."""
    print("\n" + "="*60)
    print("ESTADO DEL TABLERO")
    print("="*60)
    board.drawOnConsole()
    
    if highlight_coords:
        print(f"\n⚠️  Intentando colocar muro en: {highlight_coords}")
    print()


def test_log_scenario():
    """
    Reproduce el escenario exacto del log donde se colocó
    incorrectamente H-fence at 7,3 que bloqueó al jugador O.
    """
    print("\n" + "🔴"*30)
    print("PRUEBA: Escenario del Log - Muro Bloqueante")
    print("🔴"*30 + "\n")
    
    # Crear juego
    players = [Human("Me"), Human("O")]
    game = Game(players, cols=9, rows=9, totalFenceCount=20, squareSize=32)
    board = game.board
    board.initStoredValidActions()
    
    # Configurar posiciones según el log (convertir de 1-based a 0-based)
    # Me en 4,3 -> (col=3, row=2)
    game.players[0].pawn.coord = GridCoordinates(3, 2)
    board.pawns = [game.players[0].pawn]
    
    # O en 4,5 -> (col=3, row=4)
    game.players[1].pawn.coord = GridCoordinates(3, 4)
    board.pawns.append(game.players[1].pawn)
    
    print("Posiciones iniciales:")
    print(f"  Me (rojo): {game.players[0].pawn.coord}")
    print(f"  O (azul):  {game.players[1].pawn.coord}")
    
    # Colocar muros del log (convertir notación del log a 0-based)
    # Formato log: "H-fence at 5,3" significa col=5, row=3 (1-based)
    walls_from_log = [
        ("H", 4, 2, "Me"),  # H5,3
        ("H", 3, 5, "O"),   # H4,6
        ("H", 2, 2, "Me"),  # H3,3
        ("V", 2, 2, "Me"),  # V3,3
        ("V", 2, 4, "Me"),  # V3,5
        ("V", 2, 6, "O"),   # V3,7
    ]
    
    print("\nMuros ya colocados:")
    for direction_str, col, row, owner in walls_from_log:
        direction = Fence.DIRECTION.HORIZONTAL if direction_str == "H" else Fence.DIRECTION.VERTICAL
        coord = GridCoordinates(col, row)
        
        # Encontrar jugador
        player = game.players[0] if owner == "Me" else game.players[1]
        
        fence = Fence(board, player)
        fence.coord = coord
        fence.direction = direction
        board.fences.append(fence)
        
        print(f"  {direction_str}-fence at {col+1},{row+1} (jugador {owner})")
    
    # Actualizar estado del tablero
    board.updateStoredValidActionsAfterPawnMove(None, game.players[0].pawn.coord)
    board.updateStoredValidActionsAfterPawnMove(None, game.players[1].pawn.coord)
    
    # Mostrar tablero
    print_board_state(board)
    
    # Verificar caminos ANTES del muro problemático
    print("\n" + "-"*60)
    print("VERIFICACIÓN ANTES DEL MURO PROBLEMÁTICO")
    print("-"*60)
    
    for player in game.players:
        path = Path.BreadthFirstSearch(
            board,
            player.pawn.coord,
            player.endPositions,
            ignorePawns=True
        )
        if path:
            print(f"✓ {player.name}: Tiene camino (longitud {len(path.moves)})")
        else:
            print(f"✗ {player.name}: SIN CAMINO")
    
    # PRUEBA CRÍTICA: Intentar colocar H-fence at 7,3
    # En notación 1-based del log: 7,3 -> 0-based: (6, 2)
    problem_coord = GridCoordinates(6, 2)
    problem_direction = Fence.DIRECTION.HORIZONTAL
    
    print("\n" + "!"*60)
    print(f"INTENTANDO COLOCAR: H-fence at 7,3 (coord {problem_coord})")
    print("!"*60)
    
    # Verificar si el sistema lo permite
    is_valid = board.isValidFencePlacing(problem_coord, problem_direction)
    
    print(f"\n¿Sistema dice que es válido? {is_valid}")
    
    if is_valid:
        print("\n❌ ERROR DETECTADO:")
        print("   El sistema permite un muro que bloquea completamente.")
        print("   Esto VIOLA las reglas de Quoridor.")
        
        # Mostrar qué pasaría
        temp_fence = Fence(board, game.players[0])
        temp_fence.coord = problem_coord
        temp_fence.direction = problem_direction
        board.fences.append(temp_fence)
        board.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(
            problem_coord, problem_direction
        )
        
        print("\n   Si se colocara, resultado:")
        for player in game.players:
            path = Path.BreadthFirstSearch(
                board,
                player.pawn.coord,
                player.endPositions,
                ignorePawns=True
            )
            if path:
                print(f"     {player.name}: Camino de {len(path.moves)} movimientos")
            else:
                print(f"     {player.name}: ❌ BLOQUEADO COMPLETAMENTE")
        
        board.fences.pop()
        board.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(
            problem_coord, problem_direction
        )
        
        return False
    else:
        print("\n✅ CORRECTO:")
        print("   El sistema correctamente rechaza este muro bloqueante.")
        print("   Las reglas de Quoridor se están cumpliendo.")
        return True


def test_various_blocking_scenarios():
    """Prueba varios escenarios de muros potencialmente bloqueantes."""
    print("\n" + "🟢"*30)
    print("PRUEBAS ADICIONALES: Varios Escenarios")
    print("🟢"*30 + "\n")
    
    scenarios_passed = 0
    scenarios_total = 0
    
    # Escenario 1: Tablero vacío - ningún muro debería bloquear
    print("Escenario 1: Tablero vacío")
    game = Game([Human("P1"), Human("P2")])
    board = game.board
    board.initStoredValidActions()
    
    # Colocar jugadores en posiciones iniciales
    game.players[0].pawn.coord = GridCoordinates(4, 0)  # Top
    game.players[1].pawn.coord = GridCoordinates(4, 8)  # Bottom
    
    # Intentar muro en medio
    test_coord = GridCoordinates(4, 4)
    is_valid = board.isValidFencePlacing(test_coord, Fence.DIRECTION.HORIZONTAL)
    
    if is_valid:
        print("  ✓ Muro en tablero vacío: permitido (correcto)")
        scenarios_passed += 1
    else:
        print("  ✗ Muro en tablero vacío: rechazado (incorrecto)")
    scenarios_total += 1
    
    # Escenario 2: Intentar bloquear completamente con múltiples muros
    print("\nEscenario 2: Intentar bloqueo completo con múltiples muros")
    game = Game([Human("P1"), Human("P2")])
    board = game.board
    board.initStoredValidActions()
    
    game.players[0].pawn.coord = GridCoordinates(4, 0)
    game.players[1].pawn.coord = GridCoordinates(4, 8)
    
    # Crear "corredor" de muros dejando solo una salida
    walls = [
        (GridCoordinates(3, 4), Fence.DIRECTION.VERTICAL),
        (GridCoordinates(5, 4), Fence.DIRECTION.VERTICAL),
        (GridCoordinates(3, 3), Fence.DIRECTION.HORIZONTAL),
        # Falta el muro que cerraría completamente
    ]
    
    for coord, direction in walls:
        fence = Fence(board, game.players[0])
        fence.coord = coord
        fence.direction = direction
        board.fences.append(fence)
    
    # Intentar cerrar el corredor (debería fallar)
    closing_wall = GridCoordinates(3, 5)
    is_valid = board.isValidFencePlacing(closing_wall, Fence.DIRECTION.HORIZONTAL)
    
    if not is_valid:
        print("  ✓ Muro que cierra corredor: rechazado (correcto)")
        scenarios_passed += 1
    else:
        print("  ✗ Muro que cierra corredor: permitido (incorrecto)")
    scenarios_total += 1
    
    print(f"\nResultados: {scenarios_passed}/{scenarios_total} pruebas pasadas")
    return scenarios_passed == scenarios_total


def main():
    """Ejecuta todas las pruebas."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  PRUEBAS DE VALIDACIÓN: Muros Bloqueantes".center(68) + "║")
    print("║" + "  Verificación de Reglas de Quoridor".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Deshabilitar interfaz gráfica para pruebas
    global INTERFACE
    INTERFACE = False
    
    # Ejecutar pruebas
    test1_passed = test_log_scenario()
    test2_passed = test_various_blocking_scenarios()
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE PRUEBAS")
    print("="*70)
    
    if test1_passed:
        print("✅ Escenario del log: CORREGIDO")
    else:
        print("❌ Escenario del log: AÚN TIENE PROBLEMA")
    
    if test2_passed:
        print("✅ Escenarios adicionales: TODOS PASARON")
    else:
        print("⚠️  Escenarios adicionales: ALGUNOS FALLARON")
    
    if test1_passed and test2_passed:
        print("\n🎉 TODAS LAS PRUEBAS PASARON")
        print("   El sistema ahora respeta correctamente las reglas de Quoridor")
    else:
        print("\n⚠️  ALGUNAS PRUEBAS FALLARON")
        print("   Revisar la implementación de isValidFencePlacing()")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()