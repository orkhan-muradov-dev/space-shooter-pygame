# ==============================================================================
# Frame class for creating a visual frame for text.
# ==============================================================================

import pygame
from ..settings import BORDER_RADIUS, BG_COLOR, ACCENT_COLOR

class Frame:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, border_radius = BORDER_RADIUS, bg=BG_COLOR, border=ACCENT_COLOR):
        """Draws the frame on the given surface."""
        pygame.draw.rect(surface, bg, self.rect, border_radius=border_radius)
        pygame.draw.rect(surface, border, self.rect, 5, border_radius=border_radius)