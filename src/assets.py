# ==============================================================================
# A singleton class to manage and load all game assets.
# ==============================================================================

import pygame
from os.path import join
from .settings import (
    STAR_IMAGE_PATH, METEOR_IMAGE_PATH, LASER_IMAGE_PATH, PLAYER_IMAGE_PATH,
    MUTE_IMAGE_PATH, EXPLOSION_FRAMES_PATH, CONFETTI_FRAMES_PATH,
    FONT_LARGE_PATH, FONT_LARGE_SIZE, FONT_SMALL_PATH, FONT_SMALL_SIZE
)

class Assets:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Assets, cls).__new__(cls)
            cls._instance.initialized = False

            # Placeholders
            cls._instance.star_surf = None
            cls._instance.meteor_surf = None
            cls._instance.laser_surf = None
            cls._instance.player_surf = None
            cls._instance.mute_surf = None

            cls._instance.explosion_frames = []
            cls._instance.confetti_frames = []

            cls._instance.font_large = None
            cls._instance.font_small = None
        return cls._instance

    def init(self):
        """Loads all assets into memory. This method should only be called once."""
        if self.initialized:
            return

        print("Loading assets...")
        try:
            # Load images
            self.star_surf = pygame.image.load(STAR_IMAGE_PATH).convert_alpha()
            self.meteor_surf = pygame.image.load(METEOR_IMAGE_PATH).convert_alpha()
            self.laser_surf = pygame.image.load(LASER_IMAGE_PATH).convert_alpha()
            self.player_surf = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
            self.mute_surf = pygame.image.load(MUTE_IMAGE_PATH).convert_alpha()

            # Load animation frames
            self.explosion_frames = [
                pygame.image.load(join(EXPLOSION_FRAMES_PATH, f"{i}.png")).convert_alpha()
                for i in range(21)
            ]
            self.confetti_frames = [
                pygame.image.load(join(CONFETTI_FRAMES_PATH, f"{i}.png")).convert_alpha()
                for i in range(59)
            ]

            # Load fonts
            self.font_large = pygame.font.Font(FONT_LARGE_PATH, FONT_LARGE_SIZE)
            self.font_small = pygame.font.Font(FONT_SMALL_PATH, FONT_SMALL_SIZE)

            self.initialized = True
            print("Assets loaded successfully.")
        except pygame.error as e:
            print(f"Error loading assets: {e}")
            self.initialized = False

# Create a global instance of Assets
assets = Assets()