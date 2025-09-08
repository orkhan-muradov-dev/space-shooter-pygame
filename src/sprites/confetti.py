# ==============================================================================
# AnimatedConfetti class for confetti animations when new high score is set.
# ==============================================================================

import pygame
from ..settings import WINDOW_WIDTH, WINDOW_HEIGHT, CONFETTI_ANIMATION_SPEED

class AnimatedConfetti(pygame.sprite.Sprite):
    def __init__(self, frames, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    def update(self, dt):
        """Updates the animation frame based on time."""
        self.frame_index += CONFETTI_ANIMATION_SPEED * dt

        # Check if the animation is still running
        if int(self.frame_index) < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill() # Remove explosion after it finishes