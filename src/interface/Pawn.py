from lib.graphics_pygame     import *

from src.interface.IDrawable import *
from src.interface.Color     import *
import pygame



class Pawn(IDrawable):
    def __init__(self, board, player):
        self.board  = board
        self.player = player
        self.coord  = None

    def draw(self, fillColor = None, textColor = Color.WHITE.value):
        if not INTERFACE:
            return 
        
        surface = self.board.window.surface
        square = self.getSquare()
        center = square.middle
        radius = int(self.board.squareSize*0.4)
        
        color = self.player.color.value if fillColor is None else fillColor
        
        # Convertir color hex a RGB
        if isinstance(color, str):
            color = color.lstrip('#')
            r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            color_rgb = (r, g, b)
        else:
            color_rgb = color
        
        # Sombra del peón (efecto 3D)
        shadow_offset = 3
        shadow_color = (50, 50, 50, 100)  # Gris semi-transparente
        pygame.draw.circle(
            surface, 
            (50, 50, 50), 
            (int(center.x) + shadow_offset, int(center.y) + shadow_offset), 
            radius
        )
        
        # Círculo principal del peón con gradiente simulado
        # Círculo oscuro (borde)
        dark_color = tuple(max(0, c - 40) for c in color_rgb)
        pygame.draw.circle(surface, dark_color, (int(center.x), int(center.y)), radius + 2)
        
        # Círculo principal
        pygame.draw.circle(surface, color_rgb, (int(center.x), int(center.y)), radius)
        
        # Brillo en la parte superior (efecto 3D)
        highlight_radius = int(radius * 0.4)
        highlight_offset_x = -int(radius * 0.2)
        highlight_offset_y = -int(radius * 0.2)
        highlight_color = tuple(min(255, c + 60) for c in color_rgb)
        pygame.draw.circle(
            surface, 
            highlight_color, 
            (int(center.x) + highlight_offset_x, int(center.y) + highlight_offset_y), 
            highlight_radius
        )
        
        # Borde brillante
        pygame.draw.circle(surface, (255, 255, 255), (int(center.x), int(center.y)), radius, 2)
        
        # Letra del jugador
        font_size = min(max(5, int(self.board.squareSize/2)), 36)
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        
        # Convertir textColor si es necesario
        if isinstance(textColor, str):
            textColor = textColor.lstrip('#')
            text_r, text_g, text_b = tuple(int(textColor[i:i+2], 16) for i in (0, 2, 4))
            text_color_rgb = (text_r, text_g, text_b)
        else:
            text_color_rgb = textColor
        
        text_surface = font.render(self.player.name[:1], True, text_color_rgb)
        text_rect = text_surface.get_rect(center=(int(center.x), int(center.y)))
        
        # Sombra del texto
        shadow_text = font.render(self.player.name[:1], True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(int(center.x) + 1, int(center.y) + 1))
        surface.blit(shadow_text, shadow_rect)
        
        # Texto principal
        surface.blit(text_surface, text_rect)

    def place(self, coord):
        fromCoord, toCoord = None if self.coord is None else self.coord.clone(), coord
        self.coord = coord
        self.board.pawns.append(self)
        self.board.updateStoredValidActionsAfterPawnMove(fromCoord, toCoord)
        self.draw()

    def move(self, coord):
        self.getSquare().draw()
        self.place(coord)

    def getSquare(self):
        return self.board.getSquareAt(self.coord)