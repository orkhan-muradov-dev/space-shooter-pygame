# ==============================================================================
# Pygame Game Constants and Configuration
# ==============================================================================

from os.path import join
from pathlib import Path

# Screen dimensions
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720

# UI
CAPTION = "Space Shooter"
STAR_COUNT = 25
STAR_MIN_DISTANCE = 150

# Gameplay tuning
FPS = 120
PLAYER_SPEED = 300 # px / sec
LASER_SPEED = 400 # ms
SHOOT_COOLDOWN = 400 # ms
METEOR_BASE_SPAWN = 500 # ms
EXPLOSION_ANIMATION_SPEED = 25 # ms
CONFETTI_ANIMATION_SPEED = 25 # ms

# Colors
BG_COLOR = "#503b5c"
ACCENT_COLOR = "#b297cc"
TEXT_COLOR = "#f8e2f1"
TITLE_COLOR = "#e0c8e4"
MUTE_COLOR = "#808080"
GAME_OVER_COLOR = "#FBAEBD"
PAUSE_COLOR = GAME_OVER_COLOR
BACK_BUTTON_COLOR = GAME_OVER_COLOR
HIGH_SCORE_COLOR = "#FFE27A"

# Layout
HORIZONTAL_MARGIN = int(WINDOW_WIDTH * 0.1)
VERTICAL_MARGIN = int(WINDOW_HEIGHT * 0.1)
LEADING = 10
BUTTON_SPACE = 115
BORDER_RADIUS = 25

# Files
HIGH_SCORE_FILE = Path(__file__).resolve().parent / "high_score.txt"

# Images
STAR_IMAGE_PATH = join("images", "star.png")
METEOR_IMAGE_PATH = join("images", "meteor.png")
LASER_IMAGE_PATH = join("images", "laser.png")
PLAYER_IMAGE_PATH = join("images", "player.png")
MUTE_IMAGE_PATH = join("images", "mute.png")
EXPLOSION_FRAMES_PATH = join("images", "explosion")
CONFETTI_FRAMES_PATH = join("images", "confetti")

# Fonts
FONT_LARGE_PATH = join("images", "Oxanium-Bold.ttf")
FONT_LARGE_SIZE = 70
FONT_SMALL_PATH = join("images", "Oxanium-Bold.ttf")
FONT_SMALL_SIZE = 35

# Sounds
DEFAULT_GAME_VOLUME = 0.1
DEFAULT_MENU_VOLUME = 0.3
LASER_SOUND_PATH = "audio/laser.wav"
EXPLOSION_SOUND_PATH = "audio/explosion.wav"
DEATH_SOUND_PATH = "audio/death.mp3"
MENU_MUSIC_PATH = "audio/menu_music.wav"
GAME_MUSIC_PATH = "audio/game_music.wav"
PAUSE_MUSIC_PATH = "audio/pause_music.wav"
GAME_OVER_MUSIC = "audio/game_over_music.wav"