# ==============================================================================
# The main entry point for the Space Shooter game.
# ==============================================================================

import pygame
from .settings import WINDOW_WIDTH, WINDOW_HEIGHT, CAPTION
from .assets import assets
from .sounds import Sounds
from .ui.menus import main_menu
from .high_score import HighScoreManager

def run():
    """Initializes pygame, loads assets, and starts the main menu loop."""

    # General setup
    pygame.init()
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(CAPTION)

    # Load all game assets once
    assets.init()

    # Set window icon if available
    try:
        pygame.display.set_icon(assets.player_surf)
    except Exception:
        pass

    # Initialize game sounds and high score manager
    sounds = Sounds()
    high_score_manager = HighScoreManager()

    # Start the main menu loop, which will handle all sub-menus and the game itself.
    main_menu(display_surface, sounds, high_score_manager)

if __name__ == "__main__":
    run()