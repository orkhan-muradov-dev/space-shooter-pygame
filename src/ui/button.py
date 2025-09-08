# ==============================================================================
# Button class for creating interactive buttons in the game menus.
# ==============================================================================

import pygame
from ..settings import TEXT_COLOR, BORDER_RADIUS, BG_COLOR, ACCENT_COLOR

class Button:
    def __init__(self, text, font, center, callback, color = TEXT_COLOR):
        self.surface = font.render(text, True, color = color)
        self.rect = self.surface.get_rect(center=center)
        self.padding = 12
        self.frame = self.rect.inflate(self.padding * 2, self.padding).move(0, -5)
        self.callback = callback

    def draw(self, surface, border_radius = BORDER_RADIUS, bg=BG_COLOR, border=ACCENT_COLOR):
        """Draws the button frame, border, and text on the given surface."""
        pygame.draw.rect(surface, bg, self.frame, border_radius=border_radius)
        pygame.draw.rect(surface, border, self.frame, 5, border_radius=border_radius)
        surface.blit(self.surface, self.rect)

    def check_click(self, mouse_pos):
        """
        Checks if the mouse click position is within the button's rectangle and
        calls the callback function if it is.
        """
        if self.rect.collidepoint(mouse_pos):
            return self.callback()
        return None