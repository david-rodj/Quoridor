"""
graphics_pygame.py
Versión moderna de graphics.py usando Pygame

Proporciona una interfaz compatible con graphics.py pero usando Pygame
para mejor rendimiento y funcionalidades modernas.

USO:
    from lib.graphics_pygame import *
    
    win = GraphWin("Mi juego", 800, 600)
    # ... resto del código igual que con graphics.py
"""

import pygame
import sys
from typing import Tuple, Optional, Callable


# Colores predefinidos (RGB)
class Color:
    """Clase para almacenar colores en RGB."""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (192, 192, 192)
    DARK_GRAY = (64, 64, 64)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    
    @staticmethod
    def from_string(color_str: str) -> Tuple[int, int, int]:
        """Convierte string de color a RGB. Ej: '#FF0000' -> (255, 0, 0)"""
        color_str = color_str.strip('#')
        return tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))


class Point:
    """Representa un punto en el plano."""
    
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def clone(self):
        """Retorna una copia del punto."""
        return Point(self.x, self.y)
    
    def getX(self) -> float:
        return self.x
    
    def getY(self) -> float:
        return self.y


class GraphicsObject:
    """Clase base para todos los objetos gráficos."""
    
    def __init__(self):
        self.canvas = None
        self.fill_color = Color.WHITE
        self.outline_color = Color.BLACK
        self.width = 1
    
    def setFill(self, color):
        """Establece el color de relleno."""
        if isinstance(color, str):
            self.fill_color = Color.from_string(color)
        else:
            self.fill_color = color
    
    def setOutline(self, color):
        """Establece el color del contorno."""
        if isinstance(color, str):
            self.outline_color = Color.from_string(color)
        else:
            self.outline_color = color
    
    def setWidth(self, width: int):
        """Establece el ancho de línea."""
        self.width = int(width)
    
    def draw(self, canvas):
        """Dibuja el objeto en el canvas."""
        self.canvas = canvas
        canvas.addItem(self)
    
    def undraw(self):
        """Remueve el objeto del canvas."""
        if self.canvas:
            self.canvas.delItem(self)
            self.canvas = None
    
    def _draw_pygame(self, surface):
        """Método que deben implementar las subclases."""
        pass


class Circle(GraphicsObject):
    """Representa un círculo."""
    
    def __init__(self, center: Point, radius: float):
        super().__init__()
        self.center = center.clone()
        self.radius = float(radius)
    
    def __repr__(self):
        return f"Circle({self.center}, {self.radius})"
    
    def getCenter(self) -> Point:
        return self.center.clone()
    
    def getRadius(self) -> float:
        return self.radius
    
    def move(self, dx: float, dy: float):
        """Mueve el círculo."""
        self.center.x += dx
        self.center.y += dy
    
    def _draw_pygame(self, surface):
        """Dibuja el círculo en pygame."""
        x = int(self.center.x)
        y = int(self.center.y)
        r = int(self.radius)
        
        # Dibujar relleno si existe
        if self.fill_color != Color.WHITE or self.fill_color != (255, 255, 255):
            pygame.draw.circle(surface, self.fill_color, (x, y), r)
        
        # Dibujar contorno
        if self.width > 0:
            pygame.draw.circle(surface, self.outline_color, (x, y), r, self.width)


class Rectangle(GraphicsObject):
    """Representa un rectángulo."""
    
    def __init__(self, p1: Point, p2: Point):
        super().__init__()
        self.p1 = p1.clone()
        self.p2 = p2.clone()
    
    def __repr__(self):
        return f"Rectangle({self.p1}, {self.p2})"
    
    def getP1(self) -> Point:
        return self.p1.clone()
    
    def getP2(self) -> Point:
        return self.p2.clone()
    
    def move(self, dx: float, dy: float):
        """Mueve el rectángulo."""
        self.p1.x += dx
        self.p1.y += dy
        self.p2.x += dx
        self.p2.y += dy
    
    def _draw_pygame(self, surface):
        """Dibuja el rectángulo en pygame."""
        x1, y1 = int(self.p1.x), int(self.p1.y)
        x2, y2 = int(self.p2.x), int(self.p2.y)
        
        # Normalizar coordenadas
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)
        
        rect = pygame.Rect(x_min, y_min, x_max - x_min, y_max - y_min)
        
        # Dibujar relleno
        if self.fill_color != Color.WHITE or self.fill_color != (255, 255, 255):
            pygame.draw.rect(surface, self.fill_color, rect)
        
        # Dibujar contorno
        if self.width > 0:
            pygame.draw.rect(surface, self.outline_color, rect, self.width)


class Line(GraphicsObject):
    """Representa una línea."""
    
    def __init__(self, p1: Point, p2: Point):
        super().__init__()
        self.p1 = p1.clone()
        self.p2 = p2.clone()
        self.outline_color = Color.BLACK
    
    def __repr__(self):
        return f"Line({self.p1}, {self.p2})"
    
    def getP1(self) -> Point:
        return self.p1.clone()
    
    def getP2(self) -> Point:
        return self.p2.clone()
    
    def move(self, dx: float, dy: float):
        """Mueve la línea."""
        self.p1.x += dx
        self.p1.y += dy
        self.p2.x += dx
        self.p2.y += dy
    
    def _draw_pygame(self, surface):
        """Dibuja la línea en pygame."""
        x1, y1 = int(self.p1.x), int(self.p1.y)
        x2, y2 = int(self.p2.x), int(self.p2.y)
        pygame.draw.line(surface, self.outline_color, (x1, y1), (x2, y2), self.width)


class Text(GraphicsObject):
    """Representa texto."""
    
    def __init__(self, anchor: Point, text: str):
        super().__init__()
        self.anchor = anchor.clone()
        self.text = str(text)
        self.font_name = "arial"
        self.font_size = 12
        self.font = None
        self._update_font()
        self.fill_color = Color.BLACK
    
    def __repr__(self):
        return f"Text({self.anchor}, '{self.text}')"
    
    def getText(self) -> str:
        return self.text
    
    def setText(self, text: str):
        """Establece el texto."""
        self.text = str(text)
    
    def getAnchor(self) -> Point:
        return self.anchor.clone()
    
    def move(self, dx: float, dy: float):
        """Mueve el texto."""
        self.anchor.x += dx
        self.anchor.y += dy
    
    def setFace(self, face: str):
        """Establece la fuente."""
        self.font_name = face
        self._update_font()
    
    def setSize(self, size: int):
        """Establece el tamaño de fuente."""
        self.font_size = int(size)
        self._update_font()
    
    def _update_font(self):
        """Actualiza el objeto fuente de pygame."""
        if pygame.font.match_font(self.font_name):
            self.font = pygame.font.SysFont(self.font_name, self.font_size)
        else:
            self.font = pygame.font.Font(None, self.font_size)
    
    def setTextColor(self, color):
        """Alias para setFill (compatibilidad con graphics.py)."""
        self.setFill(color)

    def _draw_pygame(self, surface):
        """Dibuja el texto en pygame."""
        text_surface = self.font.render(self.text, True, self.fill_color)
        x = int(self.anchor.x)
        y = int(self.anchor.y)
        # Centrar el texto en el punto ancla (comportamiento compatible con graphics.py)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect.topleft)


class GraphWin:
    """Ventana principal para dibujar (usando Pygame)."""
    
    def __init__(self, title: str = "Pygame Graphics", width: int = 800, height: int = 600, autoflush: bool = True):
        """
        Inicializa la ventana gráfica.
        
        Args:
            title: Título de la ventana
            width: Ancho en píxeles
            height: Alto en píxeles
            autoflush: Si True, actualiza automáticamente
        """
        pygame.init()
        
        self.width = int(width)
        self.height = int(height)
        self.title = str(title)
        self.autoflush = autoflush
        
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        
        self.background_color = Color.WHITE
        self.items = []
        self.closed = False
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        self.mouseX = None
        self.mouseY = None
        self.lastKey = ""
    
    def __repr__(self):
        if self.closed:
            return "<Closed GraphWin>"
        else:
            return f"GraphWin('{self.title}', {self.width}, {self.height})"
    
    def setBackground(self, color):
        """Establece el color de fondo."""
        if isinstance(color, str):
            self.background_color = Color.from_string(color)
        else:
            self.background_color = color
    
    def getWidth(self) -> int:
        return self.width
    
    def getHeight(self) -> int:
        return self.height
    
    def isClosed(self) -> bool:
        return self.closed
    
    def isOpen(self) -> bool:
        return not self.closed
    
    def addItem(self, item):
        """Añade un item para ser dibujado."""
        self.items.append(item)
        if self.autoflush:
            self.update()
    
    def delItem(self, item):
        """Remueve un item."""
        if item in self.items:
            self.items.remove(item)
            if self.autoflush:
                self.update()
    
    def plot(self, x: float, y: float, color="black"):
        """Dibuja un pixel."""
        if isinstance(color, str):
            color = Color.from_string(color)
        pygame.draw.circle(self.surface, color, (int(x), int(y)), 1)
        if self.autoflush:
            self.update()
    
    def update(self):
        """Actualiza la pantalla dibujando todos los items."""
        self.surface.fill(self.background_color)
        
        # Dibujar todos los items
        for item in self.items:
            item._draw_pygame(self.surface)
        
        pygame.display.flip()
    
    def flush(self):
        """Equivalente a update()."""
        self.update()
    
    def getMouse(self) -> Point:
        """Espera a que el usuario haga clic y retorna el punto."""
        self.mouseX = None
        self.mouseY = None
        
        waiting = True
        while waiting and not self.closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseX, self.mouseY = event.pos
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    self.lastKey = pygame.key.name(event.key)
            
            self.clock.tick(30)
        
        if self.mouseX is not None and self.mouseY is not None:
            return Point(self.mouseX, self.mouseY)
        return None
    
    def checkMouse(self) -> Optional[Point]:
        """Retorna el último clic del ratón o None."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseX, self.mouseY = event.pos
        
        if self.mouseX is not None and self.mouseY is not None:
            x, y = self.mouseX, self.mouseY
            self.mouseX = None
            self.mouseY = None
            return Point(x, y)
        return None
    
    def getKey(self) -> str:
        """Espera a que el usuario presione una tecla."""
        self.lastKey = ""
        
        waiting = True
        while waiting and not self.closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    return None
                elif event.type == pygame.KEYDOWN:
                    self.lastKey = pygame.key.name(event.key)
                    waiting = False
            
            self.clock.tick(30)
        
        return self.lastKey
    
    def checkKey(self) -> str:
        """Retorna la última tecla presionada o string vacío."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.KEYDOWN:
                self.lastKey = pygame.key.name(event.key)
        
        key = self.lastKey
        self.lastKey = ""
        return key
    
    def close(self):
        """Cierra la ventana."""
        if not self.closed:
            self.closed = True
            pygame.quit()


def update(rate: Optional[int] = None):
    """Actualiza la pantalla (compatible con graphics.py)."""
    pygame.display.flip()
    if rate:
        pygame.time.Clock().tick(rate)


# Exportar funciones y clases para 'from graphics_pygame import *'
__all__ = [
    'Point', 'Circle', 'Rectangle', 'Line', 'Text', 
    'GraphicsObject', 'GraphWin', 'Color',
    'update'
]
