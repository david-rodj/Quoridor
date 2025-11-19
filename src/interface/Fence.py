from lib.graphics_pygame     import *

from src.interface.IDrawable import *
from src.interface.Color     import *
import pygame



class Fence(IDrawable):
    class DIRECTION(Enum):
        HORIZONTAL = 0
        VERTICAL   = 1

    def __init__(self, board, player):
        self.board  = board
        self.player = player

    def draw(self, color = None):
        if not INTERFACE:
            return 
        
        surface = self.board.window.surface
        square = self.getSquare()
        rectangleLength = 2*self.board.squareSize + self.board.innerSize
        rectangleWidth  = self.board.innerSize
        
        # Color del muro
        if color is None and self.player is not None:
            fence_color = self.player.color.value
        elif color is not None:
            fence_color = color
        else:
            fence_color = "#8B4513"  # Brown por defecto
        
        # Convertir color hex a RGB
        if isinstance(fence_color, str):
            fence_color = fence_color.lstrip('#')
            r, g, b = tuple(int(fence_color[i:i+2], 16) for i in (0, 2, 4))
            color_rgb = (r, g, b)
        else:
            color_rgb = fence_color
        
        # Calcular posición del muro
        if self.direction == Fence.DIRECTION.HORIZONTAL:
            x = square.left
            y = square.top - rectangleWidth
            width = rectangleLength
            height = rectangleWidth
        else:
            x = square.left - rectangleWidth
            y = square.top
            width = rectangleWidth
            height = rectangleLength
        
        # Sombra del muro (efecto 3D)
        shadow_offset = 2
        shadow_rect = pygame.Rect(
            x + shadow_offset, 
            y + shadow_offset, 
            width, 
            height
        )
        pygame.draw.rect(surface, (50, 50, 50), shadow_rect, border_radius=3)
        
        # Borde oscuro del muro
        dark_color = tuple(max(0, c - 50) for c in color_rgb)
        border_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, dark_color, border_rect, border_radius=3)
        
        # Muro principal
        main_rect = pygame.Rect(x + 1, y + 1, width - 2, height - 2)
        pygame.draw.rect(surface, color_rgb, main_rect, border_radius=2)
        
        # Brillo en el borde superior (efecto 3D)
        highlight_color = tuple(min(255, c + 40) for c in color_rgb)
        if self.direction == Fence.DIRECTION.HORIZONTAL:
            highlight_rect = pygame.Rect(x + 2, y + 1, width - 4, 2)
        else:
            highlight_rect = pygame.Rect(x + 1, y + 2, 2, height - 4)
        pygame.draw.rect(surface, highlight_color, highlight_rect)

    def place(self, coord, direction):
        self.coord = coord
        self.direction = direction
        self.board.fences.append(self)
        self.board.updateStoredValidActionsAfterFencePlacing(coord, direction)
        self.draw()

    def getSquare(self):
        return self.board.getSquareAt(self.coord)

    def __str__(self):
        vertical = (self.direction == Fence.DIRECTION.VERTICAL)
        return "%s-fence at %s" % ("V" if vertical else "H", self.coord)