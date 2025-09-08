# ==============================================================================
# The core game logic and main game loop.
# ==============================================================================

import pygame
import math
from .settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, METEOR_BASE_SPAWN, BG_COLOR, ACCENT_COLOR, TEXT_COLOR, VERTICAL_MARGIN
from .events import METEOR_SPAWN_EVENT
from .assets import assets
from .ui.background import Background
from .sprites.player import Player
from .sprites.meteor import Meteor
from .sprites.explosion import AnimatedExplosion
from .sprites.confetti import AnimatedConfetti

class Game:
    def __init__(self, display_surface, sounds, high_score_manager):
        self.display_surface = display_surface
        self.clock = pygame.time.Clock()
        self.sounds = sounds
        self.high_score_manager = high_score_manager

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.meteor_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.explosion_sprites = pygame.sprite.Group()
        self.confetti_sprites = pygame.sprite.Group()

        # Game state
        self.score = 0
        self.elapsed_time = 0
        self.music_elapsed_time = 0.0
        self.running = True
        self.paused = False
        self.frozen_screen = None

        # Objects
        self.player = None
        self.background = Background()

    # Function to calculate spawn rate based on score
    # The spawn rate decreases (meteors spawn faster) as the player's score increases
    def _calculate_spawn_rate(self) -> int:
        """Return spawn interval in ms. Fewer ms = more meteors.
        Uses a gentle logarithmic curve so difficulty ramps smoothly."""
        # Use a diminishing returns curve
        interval = METEOR_BASE_SPAWN - int(200 * (math.log1p(self.score) / math.log1p(100)))
        return max(100, interval)

    def reset(self, volume):
        """Resets the game state for a new round."""
        self.all_sprites.empty()
        self.meteor_sprites.empty()
        self.laser_sprites.empty()
        self.explosion_sprites.empty()
        self.confetti_sprites.empty()

        # Recreate the player
        self.player = Player(self.all_sprites, assets.player_surf, assets.laser_surf, self.laser_sprites, self.sounds)

        # Reset the survival time
        self.score = 0
        self.elapsed_time = 0
        self.music_elapsed_time = 0.0

        # Reset the game state
        self.running = True

        # Create a custom event for meteor spawning based on the updated spawn rate
        pygame.time.set_timer(METEOR_SPAWN_EVENT, self._calculate_spawn_rate())

        # Reset volume
        self.sounds.set_volume(0.0 if self.sounds.is_mute() else volume)
        self.sounds.play_game_music()

    def _display_score(self):
        """Renders and displays the score on the screen."""

        # Display the score in the bottom-center of the screen
        text_surf = assets.font_small.render(str(self.score), True, TEXT_COLOR)
        text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - VERTICAL_MARGIN / 2))

        # Draw background and score text
        pygame.draw.rect(self.display_surface, BG_COLOR, text_rect.inflate(20, 10).move(0, -5), 0, 10)
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, ACCENT_COLOR, text_rect.inflate(20,10).move(0,-5), 5, 10)

    def _display_mute(self):
        # Display the mute sign in the top-center of the screen
        mute_rect = assets.mute_surf.get_rect(midtop=(WINDOW_WIDTH / 2, VERTICAL_MARGIN / 4))
        self.display_surface.blit(assets.mute_surf, mute_rect)

    def _collisions(self):
        """Return True if the player died this frame."""

        # Player-Meteor collisions
        if self.player and self.player.alive():
            collided = pygame.sprite.spritecollide(
                self.player, self.meteor_sprites, dokill=True, collided=pygame.sprite.collide_mask
            )
            if collided:
                try:
                    self.sounds.death.play()
                except Exception:
                    pass

                # Trigger explosion animation at player position
                AnimatedExplosion(assets.explosion_frames, self.player.rect.center,
                                  (self.all_sprites, self.explosion_sprites), size='large')
                self.player.kill()
                return True

        # Laser-Meteor collisions
        for laser in list(self.laser_sprites):
            # Use rect collision then mask for confirm
            possible = pygame.sprite.spritecollide(laser, self.meteor_sprites, dokill=True, collided= pygame.sprite.collide_mask)
            if possible:
                laser.kill()
                meteor = possible[0]
                AnimatedExplosion(assets.explosion_frames, meteor.rect.center,
                                  (self.all_sprites, self.explosion_sprites), size=meteor.size_category)
                try:
                    self.sounds.explosion.play()
                except Exception:
                    pass
        return False

    def run(self, volume):
        """The main game loop."""
        while True:
            self.reset(volume)

            while self.running:
                dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds (for frame rate independent movement)

                # Event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == METEOR_SPAWN_EVENT: # Spawn a new meteor when the timer expires
                        if not self.paused:
                            Meteor(assets.meteor_surf, (self.all_sprites, self.meteor_sprites))
                            pygame.time.set_timer(METEOR_SPAWN_EVENT, self._calculate_spawn_rate()) # Reset timer
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            if not self.paused:
                                self.paused = True
                                self.frozen_screen = self.display_surface.copy()
                        if event.key == pygame.K_m:
                            self.sounds.toggle_mute(volume)

                if not self.paused:
                    self.elapsed_time += dt
                    self.score = int(self.elapsed_time)
                    self.music_elapsed_time += dt

                    self.all_sprites.update(dt)

                    # Check for collisions and see if the player has died
                    if self._collisions() or not self.player.alive():
                        self.running = False  # End the main game loop

                    self.background.draw(self.display_surface)
                    self.all_sprites.draw(self.display_surface)
                    self._display_score()
                    if self.sounds.is_mute():
                        self._display_mute()
                else:
                    game_volume = self.sounds.get_game_volume()

                    # Accounting for playback delay
                    self.music_elapsed_time += self.clock.get_time() / 1000.0

                    from .ui.menus import pause_menu
                    result = pause_menu(self.display_surface, self.sounds, self.frozen_screen, self.music_elapsed_time)

                    self.paused = False
                    self.clock.tick()
                    self.sounds.set_volume(game_volume)

                    if result == "restart":
                        break
                    elif result == 'main_menu':
                        return

                # Update the screen display
                pygame.display.update()

            if self._collisions() or not self.player.alive():
                # Stop the meteor spawn timer to prevent any new meteors after the game ends.
                pygame.time.set_timer(METEOR_SPAWN_EVENT, 0)

                # This loop runs after the player has died to show the explosion animation.
                while self.explosion_sprites:
                    dt = self.clock.tick(FPS) / 1000.0

                    # Event loop to allow quitting during the animation
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()

                    # Update all sprites to keep the game world moving, but stop player input
                    self.all_sprites.update(dt)
                    self.explosion_sprites.update(dt)

                    # Redraw the screen to show the animation
                    self.background.draw(self.display_surface)
                    self.all_sprites.draw(self.display_surface)
                    self.explosion_sprites.draw(self.display_surface)

                    # Update the screen
                    pygame.display.update()

                # Creating confetti animation
                if self.score > self.high_score_manager.get_high_score():
                    AnimatedConfetti(assets.confetti_frames, (self.all_sprites, self.confetti_sprites))

                # Once the explosion animation is complete, transition to the game over menu.
                from .ui.menus import game_over_menu

                # The game over menu now returns a boolean to control the outer loop.
                should_play_again = game_over_menu(self.display_surface, self.sounds, self.score, self.high_score_manager, self.confetti_sprites)

                self.clock.tick()

                # If the user chooses "Main Menu" (False), break the outer loop and exit.
                if not should_play_again:
                    break