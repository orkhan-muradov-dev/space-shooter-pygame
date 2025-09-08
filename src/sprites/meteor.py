# ==============================================================================
# Meteor class representing asteroids falling from the top of the screen
# ==============================================================================

import pygame
from random import randint, uniform
from ..settings import WINDOW_WIDTH, WINDOW_HEIGHT

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.original_image = surf # Save the original image for rotation
        self.image = surf

        self.rect = self.image.get_rect(midbottom=(randint(0, WINDOW_WIDTH), 0)) # Random spawn on top
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1) # Meteor's initial movement direction
        self.rotation = 0 # Rotation angle of the meteor

        # Determine the size and properties of the meteor based on random chance
        chance = randint(1, 100)
        if chance <= 25:
            self.size_category = "small"
            self.scale_factor = 0.5
            self.speed = randint(500, 600)
            self.rotation_speed = randint(70, 100)
        elif chance <= 50:  # Ensures a distinct second 25% range
            self.size_category = "large"
            self.scale_factor = 1.5
            self.speed = randint(300, 400)
            self.rotation_speed = randint(10, 40)
        else:
            self.size_category = "medium"
            self.scale_factor = 1
            self.speed = randint(400, 500)
            self.rotation_speed = randint(40, 70)

    def update(self, dt):
        """Moves the meteor down the screen and removes it when it goes off-screen."""

        # Move meteor and rotate it
        self.rect.center += self.direction * self.speed * dt
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, self.scale_factor)
        self.rect = self.image.get_frect(center=self.rect.center)

        # Kill meteor if it goes off-screen
        if self.rect.top >= WINDOW_HEIGHT or self.rect.right <= 0 or self.rect.left >= WINDOW_WIDTH:
            self.kill()