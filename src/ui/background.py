# ==============================================================================
# Class to handle the star background.
# ==============================================================================

import pygame
from random import randint
from ..settings import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, STAR_COUNT, STAR_MIN_DISTANCE
from ..assets import assets

class Background:
    def __init__(self):
        self.star_positions = self._generate_stars()

    def _generate_stars(self):
        """Generates random star positions, ensuring a minimum distance between them."""
        star_positions = []
        while len(star_positions) < STAR_COUNT:
            x = randint(0, WINDOW_WIDTH)
            y = randint(0, WINDOW_HEIGHT)

            # Check for minimum distance from other stars
            is_valid_position = True
            for sx, sy in star_positions:
                if pygame.math.Vector2(x, y).distance_to((sx, sy)) < STAR_MIN_DISTANCE:
                    is_valid_position = False
                    break
            if is_valid_position:
                star_positions.append((x, y))
        return star_positions

    def draw(self, surface):
        """Fills the background color and draws the stars."""
        surface.fill(BG_COLOR)
        for x, y in self.star_positions:
            surface.blit(assets.star_surf, (x, y))