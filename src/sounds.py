# ==============================================================================
# Sounds class for handling all audio in the game.
# ==============================================================================

import pygame
from .settings import (
    DEFAULT_GAME_VOLUME, DEFAULT_MENU_VOLUME, LASER_SOUND_PATH, EXPLOSION_SOUND_PATH,
    DEATH_SOUND_PATH, MENU_MUSIC_PATH, GAME_MUSIC_PATH, PAUSE_MUSIC_PATH, GAME_OVER_MUSIC
)

class Sounds:
    def __init__(self):
        # Short sounds
        self.laser = pygame.mixer.Sound(LASER_SOUND_PATH)
        self.explosion = pygame.mixer.Sound(EXPLOSION_SOUND_PATH)
        self.death = pygame.mixer.Sound(DEATH_SOUND_PATH)

        # Sounds stats
        self._muted = False
        self._game_volume = DEFAULT_GAME_VOLUME
        self._menu_volume = DEFAULT_MENU_VOLUME
        self._display_volume = self._game_volume

    def set_volume(self, volume):
        """Sets the volume for all sound effects and music."""
        self._game_volume = volume
        self._menu_volume = self._game_volume * 3
        self.laser.set_volume(self._game_volume)
        self.explosion.set_volume(self._game_volume)
        self.death.set_volume(self._game_volume)
        pygame.mixer.music.set_volume(self._game_volume)
        return volume

    def get_game_volume(self):
        """Returns the current game volume."""
        return self._game_volume

    def set_menu_volume(self, volume):
        """Sets the menu volume."""
        self._menu_volume = volume
        pygame.mixer.music.set_volume(self._menu_volume)

    def get_menu_volume(self):
        """Returns the current menu volume."""
        return self._menu_volume

    def set_display_volume(self, volume):
        """Sets the display volume."""
        self._display_volume = volume

    def get_display_volume(self):
        """Returns the current display volume."""
        return self._display_volume

    def set_mute(self, state):
        """Sets the mute state."""
        self._muted = state

    def is_mute(self):
        """Returns True if the sounds are muted, False otherwise."""
        return self._muted

    def toggle_mute(self, volume):
        """Toggles the mute state and adjusts volume accordingly."""
        self._muted = not self._muted
        if self._muted:
            self.set_volume(0.0)
        else:
            self.set_volume(volume)

    def play_music(self, music_path, loop=-1, start=0.0):
        """Loads and plays music from a given path."""
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loops=loop, start=start)
        except pygame.error as e:
            print(f"Error playing music: {e}")

    def play_menu_music(self, loop=-1):
        self.play_music(MENU_MUSIC_PATH, loop)

    def play_game_music(self, start=0.0, loop=-1):
        self.play_music(GAME_MUSIC_PATH, loop, start)

    def play_pause_music(self, loop=-1):
        self.play_music(PAUSE_MUSIC_PATH, loop)

    def play_game_over_music(self, loop=-1):
        self.play_music(GAME_OVER_MUSIC, loop)