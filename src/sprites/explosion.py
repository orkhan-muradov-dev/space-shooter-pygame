# ==============================================================================
# AnimatedExplosion class for explosion animations when objects are destroyed.
# ==============================================================================

import pygame
from ..settings import EXPLOSION_ANIMATION_SPEED

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups, size):
        super().__init__(groups)
        self.frames = [self._scale_frame(f, size) for f in frames] # Scale frames based on size
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def _scale_frame(self, frame, size):
        """Scales explosion frames based on the size of the explosion."""
        scale_map = {'small': 0.5, 'large': 1.5, 'normal': 1.0}
        scale_factor = scale_map.get(size, 1.0)

        w, h = frame.get_size()
        new_size = (int(w * scale_factor), int(h * scale_factor))
        return pygame.transform.scale(frame, new_size)

    def update(self, dt):
        """Updates the animation frame based on time."""
        self.frame_index += EXPLOSION_ANIMATION_SPEED * dt
        if int(self.frame_index) < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill() # Remove explosion after it finishes