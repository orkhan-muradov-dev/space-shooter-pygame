# ==============================================================================
# Player class for the spaceship, which can move and shoot lasers.
# ==============================================================================

import pygame
from ..settings import PLAYER_SPEED, SHOOT_COOLDOWN, WINDOW_WIDTH, WINDOW_HEIGHT
from .laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, surf, laser_surf, laser_group, sounds):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + WINDOW_HEIGHT/4))
        self.direction = pygame.math.Vector2() # Vector to store movement direction
        self.speed = PLAYER_SPEED

        # Cooldown variables for shooting lasers
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.shoot_cooldown = SHOOT_COOLDOWN

        self._laser_surf = laser_surf
        self._laser_group = laser_group
        self._all_group = groups[0] if isinstance(groups, tuple) and groups else groups
        self._sounds = sounds

    def _laser_cooldown(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.shoot_cooldown:
                self.can_shoot = True # Allow shooting again after cooldown

    def update(self, dt):
        """Updates the player's state each frame."""

        # Movement
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * self.speed * dt

        # Keeps the player within the screen boundaries
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

        # Shooting
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(self._laser_surf, self.rect.midtop, (self._all_group, self._laser_group))
            self.can_shoot = False # Prevent shooting until cooldown ends
            self.laser_shoot_time = pygame.time.get_ticks() # Record time of shooting
            self._sounds.laser.play()
        self._laser_cooldown()