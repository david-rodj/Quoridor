from lib.graphics_pygame     import *

from src.interface.IDrawable import *
from src.interface.Color     import *



class Square(IDrawable):
    def __init__(self, board, coord):
        self.board = board
        self.coord = coord
        
        # Calcular posiciones con offset del tablero
        self.left    = board.board_offset_x + (board.squareSize + board.innerSize)*coord.col
        self.xMiddle = self.left + int(board.squareSize/2)
        self.right   = self.left + board.squareSize
        self.top     = board.board_offset_y + (board.squareSize + board.innerSize)*coord.row
        self.yMiddle = self.top + int(board.squareSize/2)
        self.bottom  = self.top + board.squareSize
        self.topLeft     = Point(self.left,    self.top)
        self.topRight    = Point(self.right,   self.top)
        self.bottomLeft  = Point(self.left,    self.bottom)
        self.bottomRight = Point(self.right,   self.bottom)
        self.middle      = Point(self.xMiddle, self.yMiddle)
        
        # Colores estilo madera (patrón de ajedrez)
        if (coord.col + coord.row) % 2 == 0:
            self.default_color = "#F5DEB3"  # Wheat (claro)
        else:
            self.default_color = "#DEB887"  # BurlyWood (oscuro)

    def draw(self, color = None):
        if not INTERFACE:
            return
        
        if color is None:
            color = self.default_color
        
        import pygame
        surface = self.board.window.surface
        
        # Dibujar rectángulo de la casilla
        rect = pygame.Rect(self.left, self.top, self.board.squareSize, self.board.squareSize)
        pygame.draw.rect(surface, pygame.Color(color), rect)
        
        # Borde sutil para dar efecto 3D
        border_color = "#C4A367" if (self.coord.col + self.coord.row) % 2 == 0 else "#BCA176"
        pygame.draw.rect(surface, pygame.Color(border_color), rect, 1)