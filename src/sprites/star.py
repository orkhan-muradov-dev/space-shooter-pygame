# ==============================================================================
# Star class to display stars in the background
# ==============================================================================

import pygame

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos) # Position stars at predefined locations