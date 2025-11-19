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

        # Márgenes para estadísticas y coordenadas
        self.margin_top = 80  # Para estadísticas de jugadores
        self.margin_left = 50  # Para coordenadas verticales
        self.margin_right = 50  # Para balance
        self.margin_bottom = 50  # Para coordenadas horizontales

        # Tamaño del tablero
        board_width = squareSize*cols + innerSize*(cols - 1)
        board_height = squareSize*rows + innerSize*(rows - 1)

        # Tamaño total de la ventana
        self.width = board_width + self.margin_left + self.margin_right
        self.height = board_height + self.margin_top + self.margin_bottom

        # Offset para el tablero
        self.board_offset_x = self.margin_left
        self.board_offset_y = self.margin_top

        self.grid = [[Square(self, GridCoordinates(col, row)) for row in range(rows)] for col in range(cols)]
        
        if INTERFACE:
            self.window = GraphWin("Quoridor - Tablero de Madera", self.width, self.height)
        self.pawns  = []
        self.fences = []
        self.firstCol  = 0
        self.middleCol = int((self.cols - 1)/2)
        self.lastCol   = self.cols - 1
        self.firstRow  = 0
        self.middleRow = int((self.rows - 1)/2)
        self.lastRow   = self.rows - 1
        
        # Colores estilo madera
        self.wood_dark = "#654321"
        self.wood_light = "#8B6914"
        self.wood_border = "#4A3319"
        self.square_light = "#F5DEB3"
        self.square_dark = "#DEB887"
        self.text_color = "#2F1B0E"
        
        # Fuente para números
        if INTERFACE:
            import pygame
            pygame.font.init()
            self.coord_font = pygame.font.SysFont('Arial', 16, bold=True)
            self.stat_font = pygame.font.SysFont('Arial', 14, bold=True)
            self.stat_font_small = pygame.font.SysFont('Arial', 12)

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
                    if col == self.firstCol + 1 and row == self.middleRow:
                        coordValidPawnMoves.append(PawnMove(coord, coord.left().top(),    coord.left()))
                        coordValidPawnMoves.append(PawnMove(coord, coord.left().bottom(), coord.left()))
                    elif col == self.middleCol + 1 and (row == self.firstRow or row == self.lastRow):
                        coordValidPawnMoves.append(PawnMove(coord, coord.left().left(), coord.left()))
                    else:
                        coordValidPawnMoves.append(PawnMove(coord, coord.left()))
                if col != self.lastCol:
                    coordValidPawnMovesIgnoringPawns.append(PawnMove(coord, coord.right()))
                    if col == self.lastCol - 1 and row == self.middleRow:
                        coordValidPawnMoves.append(PawnMove(coord, coord.right().top(),    coord.right()))
                        coordValidPawnMoves.append(PawnMove(coord, coord.right().bottom(), coord.right()))
                    elif col == self.middleCol - 1 and (row == self.firstRow or row == self.lastRow):
                        coordValidPawnMoves.append(PawnMove(coord, coord.right().right(), coord.right()))
                    else:
                        coordValidPawnMoves.append(PawnMove(coord, coord.right()))
                if row != self.firstRow:
                    coordValidPawnMovesIgnoringPawns.append(PawnMove(coord, coord.top()))
                    if col == self.middleCol and row == self.firstRow + 1:
                        coordValidPawnMoves.append(PawnMove(coord, coord.top().left(),  coord.top()))
                        coordValidPawnMoves.append(PawnMove(coord, coord.top().right(), coord.top()))
                    elif (col == self.firstCol or col == self.lastCol) and row == self.middleRow + 1:
                        coordValidPawnMoves.append(PawnMove(coord, coord.top().top(), coord.top()))
                    else:
                        coordValidPawnMoves.append(PawnMove(coord, coord.top()))
                if row != self.lastRow:
                    coordValidPawnMovesIgnoringPawns.append(PawnMove(coord, coord.bottom()))
                    if col == self.middleCol and row == self.lastRow - 1:
                        coordValidPawnMoves.append(PawnMove(coord, coord.bottom().left(),  coord.bottom()))
                        coordValidPawnMoves.append(PawnMove(coord, coord.bottom().right(), coord.bottom()))
                    elif (col == self.firstCol or col == self.lastCol) and row == self.middleRow - 1:
                        coordValidPawnMoves.append(PawnMove(coord, coord.bottom().bottom(), coord.bottom()))
                    else:
                        coordValidPawnMoves.append(PawnMove(coord, coord.bottom()))
                self.storedValidPawnMoves[coord], self.storedValidPawnMovesIgnoringPawns[coord] = coordValidPawnMoves, coordValidPawnMovesIgnoringPawns

    def draw(self):
        if not INTERFACE:
            return
        
        import pygame
        surface = self.window.surface
        
        # Fondo estilo madera oscura
        surface.fill(pygame.Color(self.wood_dark))
        
        # Borde decorativo del tablero
        border_rect = pygame.Rect(
            self.board_offset_x - 10,
            self.board_offset_y - 10,
            self.squareSize*self.cols + self.innerSize*(self.cols - 1) + 20,
            self.squareSize*self.rows + self.innerSize*(self.rows - 1) + 20
        )
        pygame.draw.rect(surface, pygame.Color(self.wood_border), border_rect, 5)
        
        # Fondo del tablero (madera clara)
        board_rect = pygame.Rect(
            self.board_offset_x,
            self.board_offset_y,
            self.squareSize*self.cols + self.innerSize*(self.cols - 1),
            self.squareSize*self.rows + self.innerSize*(self.rows - 1)
        )
        pygame.draw.rect(surface, pygame.Color(self.wood_light), board_rect)
        
        # Dibujar casillas
        for col in range(self.cols):
            for row in range(self.rows):
                self.grid[col][row].draw()
        
        # Dibujar coordenadas estilo ajedrez
        self._draw_coordinates()
        
        # Dibujar estadísticas de jugadores
        self._draw_player_stats()
        
        pygame.display.flip()

    def _draw_coordinates(self):
        """Dibuja las coordenadas estilo ajedrez (A-I, 1-9)"""
        if not INTERFACE:
            return
        
        import pygame
        surface = self.window.surface
        
        # Letras horizontales (A, B, C, ...)
        for col in range(self.cols):
            letter = chr(65 + col)  # A=65 en ASCII
            x = self.board_offset_x + col * (self.squareSize + self.innerSize) + self.squareSize // 2
            
            # Arriba del tablero
            y_top = self.board_offset_y - 25
            text_surface = self.coord_font.render(letter, True, pygame.Color(self.square_light))
            text_rect = text_surface.get_rect(center=(x, y_top))
            surface.blit(text_surface, text_rect)
            
            # Abajo del tablero
            y_bottom = self.board_offset_y + self.squareSize*self.rows + self.innerSize*(self.rows - 1) + 25
            text_surface = self.coord_font.render(letter, True, pygame.Color(self.square_light))
            text_rect = text_surface.get_rect(center=(x, y_bottom))
            surface.blit(text_surface, text_rect)
        
        # Números verticales (1, 2, 3, ...)
        for row in range(self.rows):
            number = str(row + 1)
            y = self.board_offset_y + row * (self.squareSize + self.innerSize) + self.squareSize // 2
            
            # Izquierda del tablero
            x_left = self.board_offset_x - 25
            text_surface = self.coord_font.render(number, True, pygame.Color(self.square_light))
            text_rect = text_surface.get_rect(center=(x_left, y))
            surface.blit(text_surface, text_rect)
            
            # Derecha del tablero
            x_right = self.board_offset_x + self.squareSize*self.cols + self.innerSize*(self.cols - 1) + 25
            text_surface = self.coord_font.render(number, True, pygame.Color(self.square_light))
            text_rect = text_surface.get_rect(center=(x_right, y))
            surface.blit(text_surface, text_rect)

    def _draw_player_stats(self):
        """Dibuja las estadísticas de cada jugador (turno y muros restantes)"""
        if not INTERFACE:
            return
        
        import pygame
        surface = self.window.surface
        
        num_players = len(self.game.players)
        section_width = self.width // num_players
        
        for i, player in enumerate(self.game.players):
            x_center = section_width * i + section_width // 2
            y_base = 30
            
            # Cuadro de fondo para cada jugador
            box_rect = pygame.Rect(
                section_width * i + 10,
                10,
                section_width - 20,
                60
            )
            # Color de fondo según el jugador
            bg_color = self._hex_to_rgb(player.color.value)
            bg_color_light = tuple(min(255, c + 80) for c in bg_color)
            pygame.draw.rect(surface, bg_color_light, box_rect, border_radius=8)
            pygame.draw.rect(surface, bg_color, box_rect, 3, border_radius=8)
            
            # Nombre del jugador
            name_text = self.stat_font.render(player.name, True, pygame.Color(self.text_color))
            name_rect = name_text.get_rect(center=(x_center, y_base - 5))
            surface.blit(name_text, name_rect)
            
            # Icono y cantidad de muros
            fences_remaining = player.remainingFences()
            fences_text = f"🧱 {fences_remaining}"
            fences_surface = self.stat_font_small.render(fences_text, True, pygame.Color(self.text_color))
            fences_rect = fences_surface.get_rect(center=(x_center, y_base + 15))
            surface.blit(fences_surface, fences_rect)
            
            # Indicador del jugador actual
            if hasattr(self.game, 'current_player_index'):
                if self.game.players[self.game.current_player_index] == player:
                    # Dibujar flecha o indicador
                    indicator_text = "◀▶"
                    indicator_surface = self.stat_font.render(indicator_text, True, pygame.Color("#FFD700"))
                    indicator_rect = indicator_surface.get_rect(center=(x_center, y_base + 35))
                    surface.blit(indicator_surface, indicator_rect)

    def _hex_to_rgb(self, hex_color):
        """Convierte color hex a tupla RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

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
            validMoves = self.storedValidPawnMovesIgnoringPawns[fromCoord] if ignorePawns else self.storedValidPawnMoves[fromCoord]
        for validMove in validMoves:
            if validMove.toCoord == toCoord:
                return True
        return False

    def displayValidPawnMoves(self, player, validMoves = None):
        if not INTERFACE:
            return
        if validMoves is None:
            validMoves = self.storedValidPawnMoves[player.pawn.coord]
        for validMove in validMoves:
            possiblePawn = Pawn(self, player)
            possiblePawn.coord = validMove.toCoord.clone()
            possiblePawn.draw(Color.Mix(player.color.value, Color.SQUARE.value))
            del possiblePawn

    def hideValidPawnMoves(self, player, validMoves = None):
        if not INTERFACE:
            return
        if validMoves is None:
            validMoves = self.storedValidPawnMoves[player.pawn.coord]
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
        global TRACE
        TRACE["Board.isValidFencePlacing"] += 1
        
        if direction == Fence.DIRECTION.HORIZONTAL:
            if self.isAtTopEdge(coord) or self.isAtRightEdge(coord):
                return False
            if self.hasFenceAtTop(coord) or self.hasFenceAtTop(coord.right()):
                return False
        elif direction == Fence.DIRECTION.VERTICAL:
            if self.isAtLeftEdge(coord) or self.isAtBottomEdge(coord):
                return False
            if self.hasFenceAtLeft(coord) or self.hasFenceAtLeft(coord.bottom()):
                return False
        else:
            return False
        
        if direction == Fence.DIRECTION.HORIZONTAL:
            crossingFenceCoord = coord.top().right()
            for fence in self.fences:
                if fence.coord == crossingFenceCoord and fence.direction == Fence.DIRECTION.VERTICAL:
                    return False
        else:
            crossingFenceCoord = coord.bottom().left()
            for fence in self.fences:
                if fence.coord == crossingFenceCoord and fence.direction == Fence.DIRECTION.HORIZONTAL:
                    return False
        
        checkedFence = Fence(self, None)
        checkedFence.coord = coord
        checkedFence.direction = direction
        self.fences.append(checkedFence)
        
        self.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(coord, direction)
        
        all_players_have_path = True
        for player in self.game.players:
            path = Path.BreadthFirstSearch(
                self, 
                player.pawn.coord, 
                player.endPositions, 
                ignorePawns=True
            )
            
            if path is None:
                all_players_have_path = False
                if DEBUG:
                    print(f"⚠️  Muro {direction.name} en {coord} bloquearía completamente a {player.name}")
                break
        
        self.fences.pop()
        self.updateStoredValidPawnMovesIgnoringPawnsAfterFencePlacing(coord, direction)
        
        return all_players_have_path

    def displayValidFencePlacings(self, player, validPlacings = None):
        if not INTERFACE:
            return
        if validPlacings is None:
            validPlacings = self.storedValidFencePlacings
        for validPlacing in validPlacings:
            possibleFence = Fence(self, player)
            possibleFence.coord, possibleFence.direction = validPlacing.coord, validPlacing.direction
            possibleFence.draw(Color.Lighter(player.color.value))
            del possibleFence

    def hideValidFencePlacings(self, player, validPlacings = None):
        if not INTERFACE:
            return
        if validPlacings is None:
            validPlacings = self.storedValidFencePlacings
        for validPlacing in validPlacings:
            possibleFence = Fence(self, player)
            possibleFence.coord, possibleFence.direction = validPlacing.coord, validPlacing.direction
            possibleFence.draw(Color.WHITE.value)
            del possibleFence

    def getSquareFromMousePosition(self, x, y):
        # Ajustar por el offset del tablero
        x -= self.board_offset_x
        y -= self.board_offset_y
        
        if x < 0 or y < 0:
            return None
        
        fullSize = self.squareSize + self.innerSize
        if x % fullSize > self.squareSize or y % fullSize > self.squareSize:
            return None
        
        col = int(x / fullSize)
        row = int(y / fullSize)
        
        if col >= self.cols or row >= self.rows:
            return None
            
        return self.grid[col][row]

    def getPawnMoveFromMousePosition(self, pawn, x, y) -> PawnMove:
        square = self.getSquareFromMousePosition(x, y)
        if square is None or not self.isValidPawnMove(pawn.coord, square.coord):
            return None
        return PawnMove(pawn, square.coord)

    def getFencePlacingFromMousePosition(self, x, y) -> FencePlacing:
        # Ajustar por el offset del tablero
        x -= self.board_offset_x
        y -= self.board_offset_y
        
        if x < 0 or y < 0:
            return None
        
        fullSize = self.squareSize + self.innerSize
        if self.getSquareFromMousePosition(x + self.board_offset_x, y + self.board_offset_y) is not None:
            return None
        
        if x % fullSize > self.squareSize and y % fullSize < self.squareSize:
            square = self.getSquareFromMousePosition(x + self.squareSize + self.board_offset_x, y + self.board_offset_y)
            if square:
                return FencePlacing(square.coord, Fence.DIRECTION.VERTICAL) if self.isValidFencePlacing(square.coord, Fence.DIRECTION.VERTICAL) else None
        
        if x % fullSize < self.squareSize and y % fullSize > self.squareSize:
            square = self.getSquareFromMousePosition(x + self.board_offset_x, y + self.squareSize + self.board_offset_y)
            if square:
                return FencePlacing(square.coord, Fence.DIRECTION.HORIZONTAL) if self.isValidFencePlacing(square.coord, Fence.DIRECTION.HORIZONTAL) else None
        
        if x % fullSize > self.squareSize and y % fullSize > self.squareSize:
            square = self.getSquareFromMousePosition(x + self.squareSize + self.board_offset_x, y + self.squareSize + self.board_offset_y)
            if square:
                direction = Fence.DIRECTION.HORIZONTAL if (square.left + self.board_offset_x) - (x + self.board_offset_x) < (square.top + self.board_offset_y) - (y + self.board_offset_y) else Fence.DIRECTION.VERTICAL
                return FencePlacing(square.coord, direction) if self.isValidFencePlacing(square.coord, direction) else None
        return None

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
            path = Path.BreadthFirstSearch(self, player.pawn.coord, player.endPositions, ignorePawns = True)
            if path is None:
                isBlocking = True
                break
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
        coords = [fromCoord] if fromCoord is not None else []
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
        print("." + "-+"*(self.cols - 1) + "-.")
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