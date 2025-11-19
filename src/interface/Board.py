from lib.graphics_pygame     import *

from src.Settings            import *
from src.interface.IDrawable import *
from src.interface.Color     import *
from src.GridCoordinates     import *
from src.interface.Square    import *
from src.interface.Pawn      import *
from src.interface.Fence     import *
from src.action.PawnMove     import *
from src.action.FencePlacing import *
from src.Path                import *
from src.exception.PlayerPathObstructedException import *



class Board(IDrawable):
    def __init__(self, game, cols, rows, squareSize, innerSize):
        self.game = game
        self.cols,       self.rows      = cols,       rows
        self.squareSize, self.innerSize = squareSize, innerSize
        self.grid = [[Square(self, GridCoordinates(col, row)) for row in range(rows)] for col in range(cols)]
        self.width, self.height = squareSize*cols + innerSize*(cols - 1), squareSize*rows + innerSize*(rows - 1)
        if INTERFACE:
            self.window = GraphWin("Quoridor", self.width, self.height)
        self.pawns  = []
        self.fences = []
        self.firstCol  = 0
        self.middleCol = int((self.cols - 1)/2)
        self.lastCol   = self.cols - 1
        self.firstRow  = 0
        self.middleRow = int((self.rows - 1)/2)
        self.lastRow   = self.rows - 1

    def initStoredValidActions(self):
        self.storedValidFencePlacings, self.storedValidPawnMoves, self.storedValidPawnMovesIgnoringPawns = [], {}, {}
        for col in range(self.cols):
            for row in range(self.rows):
                coord = GridCoordinates(col, row)
                if col != self.lastCol and row != self.firstRow:
                    self.storedValidFencePlacings.append(FencePlacing(coord, Fence.DIRECTION.HORIZONTAL))
                if col != self.firstCol and row != self.lastRow:
                    self.storedValidFencePlacings.append(FencePlacing(coord, Fence.DIRECTION.VERTICAL))
                coordValidPawnMoves, coordValidPawnMovesIgnoringPawns = [], []
                if col != self.firstCol:
                    coordValidPawnMovesIgnoringPawns.append(PawnMove(coord, coord.left()))
                    if col == self.firstCol + 1 and row == self.middleRow: # left pawn
                        coordValidPawnMoves.append(PawnMove(coord, coord.left().top(),    coord.left()))
                        coordValidPawnMoves.append(PawnMove(coord, coord.left().bottom(), coord.left()))
                    elif col == self.middleCol + 1 and (row == self.firstRow or row == self.lastRow): # top and bottom pawns
                        coordValidPawnMoves.append(PawnMove(coord, coord.left().left(), coord.left()))
                    else:
                        coordValidPawnMoves.append(PawnMove(coord, coord.left()))
                if col != self.lastCol:
                    coordValidPawnMovesIgnoringPawns.append(PawnMove(coord, coord.right()))
                    if col == self.lastCol - 1 and row == self.middleRow: # right pawn
                        coordValidPawnMoves.append(PawnMove(coord, coord.right().top(),    coord.right()))
                        coordValidPawnMoves.append(PawnMove(coord, coord.right().bottom(), coord.right()))
                    elif col == self.middleCol - 1 and (row == self.firstRow or row == self.lastRow): # top and bottom pawns
                        coordValidPawnMoves.append(PawnMove(coord, coord.right().right(), coord.right()))
                    else:
                        coordValidPawnMoves.append(PawnMove(coord, coord.right()))
                if row != self.firstRow:
                    coordValidPawnMovesIgnoringPawns.append(PawnMove(coord, coord.top()))
                    if col == self.middleCol and row == self.firstRow + 1: # top pawn
                        coordValidPawnMoves.append(PawnMove(coord, coord.top().left(),  coord.top()))
                        coordValidPawnMoves.append(PawnMove(coord, coord.top().right(), coord.top()))
                    elif (col == self.firstCol or col == self.lastCol) and row == self.middleRow + 1: # left and right pawns
                        coordValidPawnMoves.append(PawnMove(coord, coord.top().top(), coord.top()))
                    else:
                        coordValidPawnMoves.append(PawnMove(coord, coord.top()))
                if row != self.lastRow:
                    coordValidPawnMovesIgnoringPawns.append(PawnMove(coord, coord.bottom()))
                    if col == self.middleCol and row == self.lastRow - 1: # bottom pawn
                        coordValidPawnMoves.append(PawnMove(coord, coord.bottom().left(),  coord.bottom()))
                        coordValidPawnMoves.append(PawnMove(coord, coord.bottom().right(), coord.bottom()))
                    elif (col == self.firstCol or col == self.lastCol) and row == self.middleRow - 1: # left and right pawns
                        coordValidPawnMoves.append(PawnMove(coord, coord.bottom().bottom(), coord.bottom()))
                    else:
                        coordValidPawnMoves.append(PawnMove(coord, coord.bottom()))
                self.storedValidPawnMoves[coord], self.storedValidPawnMovesIgnoringPawns[coord] = coordValidPawnMoves, coordValidPawnMovesIgnoringPawns

    def draw(self):
        if not INTERFACE:
            return
        background = Rectangle(Point(0, 0), Point(self.width, self.height))
        background.setFill(Color.WHITE.value)
        background.setWidth(0)
        background.draw(self.window)
        for col in range(self.cols):
            for row in range(self.rows):
                self.grid[col][row].draw()

    def startPosition(self, playerIndex) -> GridCoordinates:
        switcher = {
            0: GridCoordinates(self.middleCol, self.firstRow ),
            1: GridCoordinates(self.middleCol, self.lastRow  ),
            2: GridCoordinates(self.firstCol , self.middleRow),
            3: GridCoordinates(self.lastCol  , self.middleRow)
        }
        return switcher[playerIndex]

    def endPositions(self, playerIndex):
        colSwitcher = {
            0: None,
            1: None,
            2: self.lastCol,
            3: self.firstCol
        }
        rowSwitcher = {
            0: self.lastRow,
            1: self.firstRow,
            2: None,
            3: None
        }
        endCol, endRow = colSwitcher[playerIndex], rowSwitcher[playerIndex]
        endPositions = []
        if endCol is None and endRow is not None:
            for col in range(self.cols):
                endPositions.append(GridCoordinates(col, endRow))
        if endRow is None and endCol is not None:
            for row in range(self.rows):
                endPositions.append(GridCoordinates(endCol, row))
        return endPositions

    def getSquareAt(self, coord):
        return self.grid[coord.col][coord.row]

    def hasPawn(self, coord):
        for pawn in self.pawns:
            if pawn.coord == coord:
                return True
        return False

    def getPawnAt(self, coord):
        for pawn in self.pawns:
            if pawn.coord == coord:
                return pawn
        return None

    def hasFenceAtLeft(self, coord):
        for fence in self.fences:
            if fence.direction == Fence.DIRECTION.VERTICAL and (fence.coord == coord or fence.coord == coord.top()):
                return True
        return False

    def hasFenceAtRight(self, coord):
        return self.hasFenceAtLeft(coord.right())

    def hasFenceAtTop(self, coord):
        for fence in self.fences:
            if fence.direction == Fence.DIRECTION.HORIZONTAL and (fence.coord == coord or fence.coord == coord.left()):
                return True
        return False

    def hasFenceAtBottom(self, coord):
        return self.hasFenceAtTop(coord.bottom())

    def isAtLeftEdge(self, coord):
        return (coord.col == self.firstCol)

    def isAtRightEdge(self, coord):
        return (coord.col == self.lastCol)

    def isAtTopEdge(self, coord):
        return (coord.row == self.firstRow)

    def isAtBottomEdge(self, coord):
        return (coord.row == self.lastRow)

    def validPawnMoves(self, coord, ignorePawns = False):
        global TRACE
        TRACE["Board.validPawnMoves"] += 1
        validMoves = []
        if not self.isAtLeftEdge(coord) and not self.hasFenceAtLeft(coord):
            leftCoord = coord.left()
            if ignorePawns or not self.hasPawn(leftCoord):
                validMoves.append(PawnMove(coord, leftCoord))
            else:
                if not self.isAtLeftEdge(leftCoord) and not self.hasFenceAtLeft(leftCoord) and not self.hasPawn(leftCoord.left()):
                    validMoves.append(PawnMove(coord, leftCoord.left(), leftCoord))
                else:
                    if not self.isAtTopEdge(leftCoord) and not self.hasFenceAtTop(leftCoord) and not self.hasPawn(leftCoord.top()):
                        validMoves.append(PawnMove(coord, leftCoord.top(), leftCoord))
                    if not self.isAtBottomEdge(leftCoord) and not self.hasFenceAtBottom(leftCoord) and not self.hasPawn(leftCoord.bottom()):
                        validMoves.append(PawnMove(coord, leftCoord.bottom(), leftCoord))
        if not self.isAtRightEdge(coord) and not self.hasFenceAtRight(coord):
            rightCoord = coord.right()
            if ignorePawns or not self.hasPawn(rightCoord):
                validMoves.append(PawnMove(coord, rightCoord))
            else:
                if not self.isAtRightEdge(rightCoord) and not self.hasFenceAtRight(rightCoord) and not self.hasPawn(rightCoord.right()):
                    validMoves.append(PawnMove(coord, rightCoord.right(), rightCoord))
                else:
                    if not self.isAtTopEdge(rightCoord) and not self.hasFenceAtTop(rightCoord) and not self.hasPawn(rightCoord.top()):
                        validMoves.append(PawnMove(coord, rightCoord.top(), rightCoord))
                    if not self.isAtBottomEdge(rightCoord) and not self.hasFenceAtBottom(rightCoord) and not self.hasPawn(rightCoord.bottom()):
                        validMoves.append(PawnMove(coord, rightCoord.bottom(), rightCoord))
        if not self.isAtTopEdge(coord) and not self.hasFenceAtTop(coord):
            topCoord = coord.top()
            if ignorePawns or not self.hasPawn(topCoord):
                validMoves.append(PawnMove(coord, topCoord))
            else:
                if not self.isAtTopEdge(topCoord) and not self.hasFenceAtTop(topCoord) and not self.hasPawn(topCoord.top()):
                    validMoves.append(PawnMove(coord, topCoord.top(), topCoord))
                else:
                    if not self.isAtLeftEdge(topCoord) and not self.hasFenceAtLeft(topCoord) and not self.hasPawn(topCoord.left()):
                        validMoves.append(PawnMove(coord, topCoord.left(), topCoord))
                    if not self.isAtRightEdge(topCoord) and not self.hasFenceAtRight(topCoord) and not self.hasPawn(topCoord.right()):
                        validMoves.append(PawnMove(coord, topCoord.right(), topCoord))
        if not self.isAtBottomEdge(coord) and not self.hasFenceAtBottom(coord):
            bottomCoord = coord.bottom()
            if ignorePawns or not self.hasPawn(bottomCoord):
                validMoves.append(PawnMove(coord, bottomCoord))
            else:
                if not self.isAtBottomEdge(bottomCoord) and not self.hasFenceAtBottom(bottomCoord) and not self.hasPawn(bottomCoord.bottom()):
                    validMoves.append(PawnMove(coord, bottomCoord.bottom(), bottomCoord))
                else:
                    if not self.isAtLeftEdge(bottomCoord) and not self.hasFenceAtLeft(bottomCoord) and not self.hasPawn(bottomCoord.left()):
                        validMoves.append(PawnMove(coord, bottomCoord.left(), bottomCoord))
                    if not self.isAtRightEdge(bottomCoord) and not self.hasFenceAtRight(bottomCoord) and not self.hasPawn(bottomCoord.right()):
                        validMoves.append(PawnMove(coord, bottomCoord.right(), bottomCoord))
        return validMoves

    def isValidPawnMove(self, fromCoord, toCoord, validMoves = None, ignorePawns = False):
        global TRACE
        TRACE["Board.isValidPawnMove"] += 1
        if validMoves is None:
            validMoves = self.storedValidPawnMovesIgnoringPawns[fromCoord] if ignorePawns else self.storedValidPawnMoves[fromCoord] #self.validPawnMoves(fromCoord)
        for validMove in validMoves:
            if validMove.toCoord == toCoord:
                return True
        return False

    def displayValidPawnMoves(self, player, validMoves = None):
        if not INTERFACE:
            return
        if validMoves is None:
            validMoves = self.storedValidPawnMoves[player.pawn.coord] #self.validPawnMoves(player.pawn.coord)
        for validMove in validMoves:
            possiblePawn = Pawn(self, player)
            possiblePawn.coord = validMove.toCoord.clone()
            possiblePawn.draw(Color.Mix(player.color.value, Color.SQUARE.value))
            del possiblePawn

    def hideValidPawnMoves(self, player, validMoves = None):
        if not INTERFACE:
            return
        if validMoves is None:
            validMoves = self.storedValidPawnMoves[player.pawn.coord] #self.validPawnMoves(player.pawn.coord)
        for validMove in validMoves:
            possiblePawn = Pawn(self, player)
            possiblePawn.coord = validMove.toCoord.clone()
            possiblePawn.draw(Color.SQUARE.value, Color.SQUARE.value)
            del possiblePawn

    def validFencePlacings(self):
        global TRACE
        TRACE["Board.validFencePlacings"] += 1
        validPlacings = []
        for col in range(self.cols):
            for row in range(self.rows):
                if (self.isValidFencePlacing(GridCoordinates(col, row), Fence.DIRECTION.HORIZONTAL)):
                    validPlacings.append(FencePlacing(GridCoordinates(col, row), Fence.DIRECTION.HORIZONTAL))
                if (self.isValidFencePlacing(GridCoordinates(col, row), Fence.DIRECTION.VERTICAL)):
                    validPlacings.append(FencePlacing(GridCoordinates(col, row), Fence.DIRECTION.VERTICAL))
        return validPlacings

    def isValidFencePlacing(self, coord, direction):
        """
        Verifica si un muro puede colocarse en la posición dada.
        
        REGLA CRÍTICA DE QUORIDOR:
        Nunca se puede colocar un muro que bloquee COMPLETAMENTE 
        el camino de cualquier jugador hacia su meta.
        
        Verificaciones:
        1. El muro no está fuera de límites
        2. El muro no se cruza con otro muro
        3. El muro no sobrepone otro muro existente
        4. CRÍTICO: Después de colocar el muro, TODOS los jugadores
        aún tienen al menos un camino válido hacia su meta
        """
        global TRACE
        TRACE["Board.isValidFencePlacing"] += 1
        
        # Validación 1: Límites del tablero
        if direction == Fence.DIRECTION.HORIZONTAL:
            # Muro horizontal necesita espacio en top y right
            if self.isAtTopEdge(coord) or self.isAtRightEdge(coord):
                return False
            # Verificar que no haya muros en las dos posiciones que ocuparía
            if self.hasFenceAtTop(coord) or self.hasFenceAtTop(coord.right()):
                return False
        elif direction == Fence.DIRECTION.VERTICAL:
            # Muro vertical necesita espacio en left y bottom
            if self.isAtLeftEdge(coord) or self.isAtBottomEdge(coord):
                return False
            # Verificar que no haya muros en las dos posiciones que ocuparía
            if self.hasFenceAtLeft(coord) or self.hasFenceAtLeft(coord.bottom()):
                return False
        else:
            return False
        
        # Validación 2: No cruzarse con muro perpendicular
        if direction == Fence.DIRECTION.HORIZONTAL:
            # Un muro horizontal en coord bloquea entre coord y coord.top()
            # Se cruza con un muro vertical en coord.top().right()
            crossingFenceCoord = coord.top().right()
            for fence in self.fences:
                if fence.coord == crossingFenceCoord and fence.direction == Fence.DIRECTION.VERTICAL:
                    return False
        else:  # VERTICAL
            # Un muro vertical en coord bloquea entre coord y coord.left()
            # Se cruza con un muro horizontal en coord.bottom().left()
            crossingFenceCoord = coord.bottom().left()
            for fence in self.fences:
                if fence.coord == crossingFenceCoord and fence.direction == Fence.DIRECTION.HORIZONTAL:
                    return False
        
        # Validación 3: CRÍTICA - Verificar que no bloquee completamente a ningún jugador
        # Simular colocación del muro temporalmente
        checkedFence = Fence(self, None)
        checkedFence.coord = coord
        checkedFence.direction = direction
        self.fences.append(checkedFence)
        
        # IMPORTANTE: Actualizar movimientos válidos para reflejar el nuevo muro
        # (esto es crítico para que BFS encuentre caminos correctamente)
        self.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(coord, direction)
        
        # Verificar que CADA jugador aún tenga al menos un camino válido
        all_players_have_path = True
        for player in self.game.players:
            # Buscar camino ignorando otros peones (solo considerando muros)
            path = Path.BreadthFirstSearch(
                self, 
                player.pawn.coord, 
                player.endPositions, 
                ignorePawns=True
            )
            
            if path is None:
                # Este jugador quedaría bloqueado - muro NO válido
                all_players_have_path = False
                if DEBUG:
                    print(f"⚠️  Muro {direction.name} en {coord} bloquearía completamente a {player.name}")
                break
        
        # Remover muro temporal y restaurar estado
        self.fences.pop()
        self.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(coord, direction)
        
        return all_players_have_path

    def displayValidFencePlacings(self, player, validPlacings = None):
        if not INTERFACE:
            return
        if validPlacings is None:
            validPlacings = self.storedValidFencePlacings#self.validFencePlacings()
        for validPlacing in validPlacings:
            possibleFence = Fence(self, player)
            possibleFence.coord, possibleFence.direction = validPlacing.coord, validPlacing.direction
            possibleFence.draw(Color.Lighter(player.color.value))
            del possibleFence

    def hideValidFencePlacings(self, player, validPlacings = None):
        if not INTERFACE:
            return
        if validPlacings is None:
            validPlacings = self.storedValidFencePlacings#self.validFencePlacings()
        for validPlacing in validPlacings:
            possibleFence = Fence(self, player)
            possibleFence.coord, possibleFence.direction = validPlacing.coord, validPlacing.direction
            possibleFence.draw(Color.WHITE.value)
            del possibleFence

    def getSquareFromMousePosition(self, x, y):
        fullSize = self.squareSize + self.innerSize
        # on inner space
        if x % fullSize > self.squareSize or y % fullSize > self.squareSize:
            return None
        return self.grid[int(x/fullSize)][int(y/fullSize)]

    def getPawnMoveFromMousePosition(self, pawn, x, y) -> PawnMove:
        square = self.getSquareFromMousePosition(x, y)
        if square is None or not self.isValidPawnMove(pawn.coord, square.coord):
            return None
        return PawnMove(pawn, square.coord)

    def getFencePlacingFromMousePosition(self, x, y) -> FencePlacing:
        fullSize = self.squareSize + self.innerSize
        # on square space
        if self.getSquareFromMousePosition(x, y) is not None:
            return None
        # vertical fence
        if x % fullSize > self.squareSize and y % fullSize < self.squareSize:
            square = self.getSquareFromMousePosition(x + self.squareSize, y)
            return FencePlacing(square.coord, Fence.DIRECTION.VERTICAL) if self.isValidFencePlacing(square.coord, Fence.DIRECTION.VERTICAL) else None
        # horizontal fence
        if x % fullSize < self.squareSize and y % fullSize > self.squareSize:
            square = self.getSquareFromMousePosition(x, y + self.squareSize)
            return FencePlacing(square.coord, Fence.DIRECTION.HORIZONTAL) if self.isValidFencePlacing(square.coord, Fence.DIRECTION.HORIZONTAL) else None
        # on inner crossing space
        if x % fullSize > self.squareSize and y % fullSize > self.squareSize:
            square = self.getSquareFromMousePosition(x + self.squareSize, y + self.squareSize)
            direction = Fence.DIRECTION.HORIZONTAL if square.left - x < square.top - y else Fence.DIRECTION.VERTICAL
            return FencePlacing(square.coord, direction) if self.isValidFencePlacing(square.coord, direction) else None
        return None

    # Move to Path.draw (idem for displayPawnMove and displayFencePlacing)
    def displayPath(self, path, color = None):
        if not INTERFACE:
            return
        if not path.moves:
            return
        for move in path.moves:
            center = self.getSquareAt(move.toCoord).middle
            radius = int(self.squareSize*0.2)
            circle = Circle(center, radius)
            circle.setFill(Color.PURPLE.value if color is None else color)
            circle.setWidth(0)
            circle.draw(self.window)

    def hidePath(self, path):
        if not INTERFACE:
            return
        if not path.moves:
            return
        for move in path.moves[1:]:
            self.getSquareAt(move.toCoord).draw()

    def isFencePlacingBlocking(self, fencePlacing):
        global TRACE
        TRACE["Board.isFencePlacingBlocking"] += 1
        fence = Fence(self, None)
        fence.coord, fence.direction = fencePlacing.coord, fencePlacing.direction
        self.fences.append(fence)
        self.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(fencePlacing.coord, fencePlacing.direction)
        isBlocking = False
        for player in self.game.players:
            #print("¿Puede el jugador %s alcanzar uno de sus objetivos con %s? " % (player.name, fencePlacing), end="")
            path = Path.BreadthFirstSearch(self, player.pawn.coord, player.endPositions, ignorePawns = True)
            if path is None:
                #print("NO")
                isBlocking = True
                break
            #print("SÍ, a través de %s" % path)
        self.fences.pop()
        self.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(fencePlacing.coord, fencePlacing.direction)
        return isBlocking

    def updateStoredValidPawnMovesAt(self, coord):
        self.storedValidPawnMoves[coord] = self.validPawnMoves(coord, False)

    def updateStoredValidPawnMovesIgnoringPawnsAt(self, coord):
        self.storedValidPawnMovesIgnoringPawns[coord] = self.validPawnMoves(coord, True)

    def removeIfExistStoredValidFencePlacing(self, fencePlacing):
        if fencePlacing in self.storedValidFencePlacings: self.storedValidFencePlacings.remove(fencePlacing)

    def updateStoredValidPawnMovesAfterPawnMove(self, fromCoord, toCoord):
        coords = [fromCoord] if fromCoord is not None else [] # fromCoord is None at start
        coords.append(toCoord)
        for col in range(self.cols):
            for row in range(self.rows):
                coord = GridCoordinates(col, row)
                if Path.ManhattanDistanceMulti(coord, coords) <= 2:
                    self.updateStoredValidPawnMovesAt(coord)

    def updateStoredValidActionsAfterPawnMove(self, fromCoord, toCoord):
        global TRACE
        TRACE["Board.updateStoredValidActionsAfterPawnMove"] += 1
        self.updateStoredValidPawnMovesAfterPawnMove(fromCoord, toCoord)

    def updateStoredValidFencePlacingsAfterFencePlacing(self, coord, direction):
        v, h = Fence.DIRECTION.VERTICAL, Fence.DIRECTION.HORIZONTAL
        self.removeIfExistStoredValidFencePlacing(FencePlacing(coord, direction))
        self.removeIfExistStoredValidFencePlacing(FencePlacing(coord.top()    if direction == v else coord.left() , direction))
        self.removeIfExistStoredValidFencePlacing(FencePlacing(coord.bottom() if direction == v else coord.right(), direction))
        self.removeIfExistStoredValidFencePlacing(FencePlacing(coord.bottom().left() if direction == v else coord.top().right(), h if direction == v else v))

    def updateStoredValidPawnMovesAfterFencePlacing(self, coord, direction):
        v, h = Fence.DIRECTION.VERTICAL, Fence.DIRECTION.HORIZONTAL
        minCol, minRow = coord.col - 2 if direction == v else coord.col - 1, coord.row - 1 if direction == v else coord.row - 2
        maxCol, maxRow = minCol + 3, minRow + 3
        for col in range(minCol, maxCol + 1):
            for row in range(minRow, maxRow + 1):
                if minCol < col < maxCol or minRow < row < maxRow:
                    self.updateStoredValidPawnMovesAt(GridCoordinates(col, row))

    def updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(self, coord, direction):
        v, h = Fence.DIRECTION.VERTICAL, Fence.DIRECTION.HORIZONTAL
        minCol, minRow = coord.col - 1 if direction == v else coord.col, coord.row if direction == v else coord.row - 1
        maxCol, maxRow = minCol + 1, minRow + 1
        for col in range(minCol, maxCol + 1):
            for row in range(minRow, maxRow + 1):
                self.updateStoredValidPawnMovesIgnoringPawnsAt(GridCoordinates(col, row))

    def updateStoredValidActionsAfterFencePlacing(self, coord, direction):
        global TRACE
        TRACE["Board.updateStoredValidActionsAfterFencePlacing"] += 1
        self.updateStoredValidFencePlacingsAfterFencePlacing(coord, direction)
        self.updateStoredValidPawnMovesAfterFencePlacing(coord, direction)
        self.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(coord, direction)

    def drawOnConsole(self):
        # top edge
        print("." + "-+"*(self.cols - 1) + "-.")
        # first row
        coord = GridCoordinates(0, 0)
        pawn = self.getPawnAt(coord)
        print("|%s" % (" " if pawn is None else pawn.player.name[:1]), end="")
        for col in range(1, self.cols):
            coord = GridCoordinates(col, 0)
            pawn = self.getPawnAt(coord)
            print("%s%s" % (" " if not self.hasFenceAtLeft(coord) else "|", " " if pawn is None else pawn.player.name[:1]), end="")
        print("|")
        for row in range(1, self.rows):
            print("+", end="")
            for col in range(self.cols):
                coord = GridCoordinates(col, row)
                print("%s+" % (" " if not self.hasFenceAtTop(coord) else "-"), end="")
            print("")
            coord = GridCoordinates(0, row)
            pawn = self.getPawnAt(coord)
            print("|%s" % (" " if pawn is None else pawn.player.name[:1]), end="")
            for col in range(1, self.cols):
                coord = GridCoordinates(col, row)
                pawn = self.getPawnAt(coord)
                print("%s%s" % (" " if not self.hasFenceAtLeft(coord) else "|", " " if pawn is None else pawn.player.name[:1]), end="")
            print("|")
        print("'" + "-+"*(self.cols - 1) + "-'")

    def getFencePlacingImpactOnPaths(self, fencePlacing: FencePlacing):
        global TRACE
        TRACE["Board.getFencePlacingImpactOnPaths"] += 1
        stateBefore = {}
        for player in self.game.players:
            path = Path.BreadthFirstSearch(self, player.pawn.coord, player.endPositions, ignorePawns = True)
            if path is None:
                print("¡El jugador %s ya está bloqueado!" % (player.name))
                return None
            stateBefore[player.name] = len(path.moves)
        fence = Fence(self, None)
        fence.coord, fence.direction = fencePlacing.coord, fencePlacing.direction
        self.fences.append(fence)
        self.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(fencePlacing.coord, fencePlacing.direction)
        impact = {}
        for player in self.game.players:
            path = Path.BreadthFirstSearch(self, player.pawn.coord, player.endPositions, ignorePawns = True)
            if path is None:
                self.fences.pop()
                self.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(fencePlacing.coord, fencePlacing.direction)
                raise PlayerPathObstructedException(player, fencePlacing)
            impact[player.name] = len(path.moves) - stateBefore[player.name]
        self.fences.pop()
        self.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(fencePlacing.coord, fencePlacing.direction)
        return impact
    
    def test_blocking_scenario():
        """
        Prueba el escenario del log donde M (rojo) en 4,3 y O (azul) en 4,5
        con muros ya colocados, e intenta colocar H-fence at 7,3
        """
        from src.Game import Game
        from src.player.Human import Human
        from src.GridCoordinates import GridCoordinates
        from src.interface.Fence import Fence
        
        # Crear juego de prueba
        game = Game([Human("M"), Human("O")], cols=9, rows=9)
        board = game.board
        
        # Simular estado del log
        # M en 4,3 (fila 3, columna 4 en índices 0-based)
        game.players[0].pawn.coord = GridCoordinates(3, 2)  # col, row (0-based)
        
        # O en 4,5 (fila 5, columna 4)
        game.players[1].pawn.coord = GridCoordinates(3, 4)
        
        # Colocar muros del log (convertir a 0-based)
        existing_walls = [
            ("H", GridCoordinates(4, 2)),  # H-fence at 5,3
            ("H", GridCoordinates(3, 5)),  # H-fence at 4,6
            ("H", GridCoordinates(2, 2)),  # H-fence at 3,3
            ("V", GridCoordinates(2, 2)),  # V-fence at 3,3
            ("V", GridCoordinates(2, 4)),  # V-fence at 3,5
            ("V", GridCoordinates(2, 6)),  # V-fence at 3,7
        ]
        
        for direction_str, coord in existing_walls:
            direction = Fence.DIRECTION.HORIZONTAL if direction_str == "H" else Fence.DIRECTION.VERTICAL
            fence = Fence(board, game.players[0])
            fence.coord = coord
            fence.direction = direction
            board.fences.append(fence)
        
        # Actualizar movimientos válidos
        board.initStoredValidActions()
        
        # PRUEBA: Intentar colocar H-fence at 7,3 (coord 6,2 en 0-based)
        test_coord = GridCoordinates(6, 2)
        test_direction = Fence.DIRECTION.HORIZONTAL
        
        is_valid = board.isValidFencePlacing(test_coord, test_direction)
        
        print(f"\n{'='*60}")
        print(f"PRUEBA: H-fence at 7,3 (coord {test_coord})")
        print(f"¿Es válido? {is_valid}")
        print(f"{'='*60}\n")
        
        if is_valid:
            print("❌ ERROR: El muro debería ser INVÁLIDO (bloquea al jugador O)")
        else:
            print("CORRECTO: El muro es inválido como debería ser")
        
        # Verificar caminos de ambos jugadores
        for i, player in enumerate(game.players):
            path = Path.BreadthFirstSearch(
                board,
                player.pawn.coord,
                player.endPositions,
                ignorePawns=True
            )
            if path:
                print(f"Jugador {player.name}: Tiene camino (longitud {len(path.moves)})")
            else:
                print(f"Jugador {player.name}: SIN CAMINO")
        
        return is_valid


    # Función de debugging adicional
    def visualize_blocking_check(board, coord, direction, player):
        """
        Visualiza por qué un muro bloquea o no a un jugador.
        Útil para debugging.
        """
        print(f"\n{'='*70}")
        print(f"ANÁLISIS DE BLOQUEO: {direction.name} fence at {coord}")
        print(f"Jugador: {player.name} en {player.pawn.coord}")
        print(f"Objetivos: {[str(g) for g in player.endPositions]}")
        print(f"{'='*70}")
        
        # Estado ANTES del muro
        path_before = Path.BreadthFirstSearch(
            board,
            player.pawn.coord,
            player.endPositions,
            ignorePawns=True
        )
        
        if path_before:
            print(f"ANTES del muro: Camino de longitud {len(path_before.moves)}")
            print(f"  Ruta: {path_before}")
        else:
            print(f"ANTES del muro: Ya está bloqueado")
        
        # Simular muro
        temp_fence = Fence(board, None)
        temp_fence.coord = coord
        temp_fence.direction = direction
        board.fences.append(temp_fence)
        board.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(coord, direction)
        
        # Estado DESPUÉS del muro
        path_after = Path.BreadthFirstSearch(
            board,
            player.pawn.coord,
            player.endPositions,
            ignorePawns=True
        )
        
        if path_after:
            print(f"DESPUÉS del muro: Camino de longitud {len(path_after.moves)}")
            print(f"  Ruta: {path_after}")
            print(f"  Impacto: +{len(path_after.moves) - len(path_before.moves)} movimientos")
        else:
            print(f"DESPUÉS del muro: BLOQUEADO COMPLETAMENTE")
            print(f"  Este muro NO es válido según las reglas de Quoridor")
        
        # Limpiar
        board.fences.pop()
        board.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(coord, direction)
        
        print(f"{'='*70}\n")
        
        return path_after is not None
