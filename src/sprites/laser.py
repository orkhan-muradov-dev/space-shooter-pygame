# ==============================================================================
# Laser class that represents the laser shot by the player
# ==============================================================================

import pygame
from ..settings import LASER_SPEED

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom=pos) # Position laser at player's top
        self.speed = LASER_SPEED

    def update(self, dt):
        """Moves the laser up the screen and removes it when it goes off-screen."""
        self.rect.y -= int(self.speed * dt)
        if self.rect.bottom < 0:
            self.kill()