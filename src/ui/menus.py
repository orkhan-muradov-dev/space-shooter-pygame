# ==============================================================================
# Menus for the game, including main menu, settings, pause and game over screens.
# ==============================================================================

import pygame
from .frame import Frame
from ..settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, HORIZONTAL_MARGIN, VERTICAL_MARGIN, BG_COLOR,
    TEXT_COLOR, TITLE_COLOR, MUTE_COLOR, PAUSE_COLOR, BACK_BUTTON_COLOR,
    GAME_OVER_COLOR, HIGH_SCORE_COLOR, LEADING, BUTTON_SPACE, DEFAULT_MENU_VOLUME
)
from ..assets import assets
from ..game import Game
from .button import Button
from .background import Background

def _display_text(display_surface, text, font, pos, color=TEXT_COLOR):
    """A helper function to render and display text."""
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=pos)
    display_surface.blit(text_surf, text_rect)

def main_menu(display_surface, sounds, high_score_manager):
    background = Background()

    try:
        sounds.set_display_volume(sounds.set_volume(DEFAULT_MENU_VOLUME))
    except Exception:
        sounds.set_volume(1.0)
    sounds.play_menu_music()

    def start_game():
        game_instance = Game(display_surface, sounds, high_score_manager)
        game_instance.run(sounds.get_game_volume() / 3)
        return True

    def open_settings():
        settings_menu(display_surface, sounds)

    def open_how_to_play():
        how_to_play_menu(display_surface)

    def exit_game():
        pygame.quit()
        exit()

    # Create the menu buttons, dynamically spaced
    button_x_start = WINDOW_WIDTH // 2
    button_y_start = WINDOW_HEIGHT // 3
    buttons = [
        Button("Play", assets.font_large, (button_x_start, button_y_start), start_game),
        Button("Settings", assets.font_large, (button_x_start, button_y_start + BUTTON_SPACE), open_settings),
        Button("How to Play", assets.font_large, (button_x_start, button_y_start + 2 * BUTTON_SPACE),
               open_how_to_play),
        Button("Exit", assets.font_large, (button_x_start, button_y_start + 3 * BUTTON_SPACE), exit_game),
    ]

    # Draw the player image at the center of the screen
    player_rect = assets.player_surf.get_rect(center=(button_x_start, button_y_start - BUTTON_SPACE))

    while True:
        in_game = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.check_click(mouse_pos):
                        background = Background()
                        in_game = True

        if in_game:
            if not sounds.is_mute():
                sounds.set_display_volume(sounds.set_volume(sounds.get_menu_volume()))
            sounds.play_menu_music()

        # Draw the background and buttons
        background.draw(display_surface)
        display_surface.blit(assets.player_surf, player_rect)
        for button in buttons:
            button.draw(display_surface)

        # Update the screen display
        pygame.display.update()

def settings_menu(display_surface, sounds):
    running = True
    background = Background()

    try:
        volume = sounds.get_display_volume()
    except Exception:
        volume = 0.0

    def back():
        nonlocal running
        running = False

    # Create a button for going back to the main menu
    back_button = Button("Back", assets.font_small, (HORIZONTAL_MARGIN, VERTICAL_MARGIN), back, BACK_BUTTON_COLOR)

    # Render the title text of the Settings menu
    title_surface = assets.font_large.render("Settings", True, TITLE_COLOR)

    # Segments volume UI
    volume_segments = []
    segment_width = 60
    segment_height = 20
    margin_segments = 10 # Space between segments
    for i in range(10):
        # Calculate the x and y position for each volume segment
        x_pos = (WINDOW_WIDTH // 2 - int(5.5 * segment_width)) + i * (segment_width + margin_segments)
        y_pos = WINDOW_HEIGHT // 2 - VERTICAL_MARGIN // 2.5
        volume_segments.append(pygame.Rect(x_pos, y_pos, segment_width, segment_height))

    # Define the border for the volume control
    volume_border = pygame.Rect(
        volume_segments[0].x - 5,
        volume_segments[0].y - 5,
        (segment_width + margin_segments) * 10 - margin_segments + 10,
        segment_height + 10
    )

    # Define the mute checkbox
    mute_checkbox_rect = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + VERTICAL_MARGIN // 2, assets.font_small.get_height(), assets.font_small.get_height())
    mute_text = assets.font_small.render("Mute", True, TEXT_COLOR)

    # Create a frame for settings menu
    frame_x_start = HORIZONTAL_MARGIN
    frame_y_strat = VERTICAL_MARGIN * 1.75
    frame_width = WINDOW_WIDTH - HORIZONTAL_MARGIN * 2
    frame = Frame(frame_x_start, frame_y_strat, frame_width, mute_checkbox_rect.y - VERTICAL_MARGIN + LEADING * 2)
    title_frame = Frame(frame_x_start, frame_y_strat, frame_width , VERTICAL_MARGIN * 1.5)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                back_button.check_click(mouse_pos)

                # Check if any of the volume segments are clicked and adjust the volume
                for i, rect in enumerate(volume_segments):
                    if rect.collidepoint(mouse_pos):
                        volume = (i + 1) / 10 # Maps clicks to 0.1 - 1.0 volume range (10 segments, 0 to 1)
                        sounds.set_display_volume(sounds.set_volume(volume))
                        sounds.set_mute(False) # Unmute when volume changes

                # Check for clicks on the mute checkbox
                if mute_checkbox_rect.collidepoint(mouse_pos):
                    sounds.toggle_mute(volume)

        # Update the sound volume based on mute state and the current volume
        color = MUTE_COLOR if sounds.is_mute() else TEXT_COLOR

        # Draw the background and buttons
        background.draw(display_surface)
        back_button.draw(display_surface)

        # Draw the frame for menu and title
        frame.draw(display_surface)
        title_frame.draw(display_surface)

        # Draw the title at the top of the screen
        display_surface.blit(title_surface, title_surface.get_rect(center=(WINDOW_WIDTH // 2, VERTICAL_MARGIN * 1.5 + assets.font_large.get_height() + 10)))

        # Display the current volume level as a percentage
        display_volume = round(volume * 10) / 10
        volume_text = assets.font_small.render(f"Volume: {int(display_volume * 100)}%", True, TEXT_COLOR)
        display_surface.blit(volume_text, volume_text.get_rect(center=(WINDOW_WIDTH // 2, VERTICAL_MARGIN * 4)))

        # Draw the border around the volume control
        pygame.draw.rect(display_surface, TEXT_COLOR, volume_border, 3)

        # Draw the volume segments and fill them according to the current volume
        filled_segments = int(display_volume * 10)
        for i, rect in enumerate(volume_segments):
            pygame.draw.rect(display_surface, color if i < filled_segments else BG_COLOR, rect)

        # Draw the mute checkbox
        pygame.draw.rect(display_surface, TEXT_COLOR if sounds.is_mute() else BG_COLOR, mute_checkbox_rect)
        pygame.draw.rect(display_surface, TEXT_COLOR, mute_checkbox_rect, 3)
        display_surface.blit(mute_text, mute_text.get_rect(topleft=(mute_checkbox_rect.left + 45, mute_checkbox_rect.y)))

        # Update the screen display
        pygame.display.update()

def how_to_play_menu(display_surface):
    running = True
    background = Background()

    def back():
        nonlocal running
        running = False

    # Create the Back button
    back_button = Button("Back", assets.font_small, (HORIZONTAL_MARGIN, VERTICAL_MARGIN), back, BACK_BUTTON_COLOR)

    # Create a frame for how_to_play_menu
    frame_x_start = HORIZONTAL_MARGIN // 2
    frame_y_strat = VERTICAL_MARGIN * 1.5
    frame_width = WINDOW_WIDTH - HORIZONTAL_MARGIN
    frame = Frame(frame_x_start, frame_y_strat, frame_width, WINDOW_HEIGHT - VERTICAL_MARGIN * 2 - LEADING * 2)
    title_frame = Frame(frame_x_start, frame_y_strat, frame_width, VERTICAL_MARGIN * 1.5 - LEADING)

    # Render the text surfaces for title and instructions
    title_surface = assets.font_large.render("How to Play", True, TITLE_COLOR)
    instructions = [
        "- W/A/S/D or Arrow Keys to move.",
        "- Press SPACE to shoot lasers.",
        "- Avoid meteors - getting hit will destroy your ship.",
        "- Live longer to earn points."
    ]
    instruction_texts = [assets.font_small.render(t, True, TEXT_COLOR) for t in instructions]

    # Render the text surfaces for subtitle and meteor details
    subtitle_surface = assets.font_small.render("Meteor types:", True, TEXT_COLOR)
    meteor_details = [
        "- Small Meteors: Small, fast, and tricky to hit.",
        "- Medium Meteors: Medium size with normal speed.",
        "- Big Meteors: Large, slow, but hard to avoid."
    ]
    meteor_texts = [assets.font_small.render(t, True, TEXT_COLOR) for t in meteor_details]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                back_button.check_click(pygame.mouse.get_pos())

        # Draw the background and buttons
        background.draw(display_surface)
        back_button.draw(display_surface)

        # Draw the frame for menu and title
        frame.draw(display_surface)
        title_frame.draw(display_surface)

        # Draw the title
        display_surface.blit(title_surface, title_surface.get_rect(center=(WINDOW_WIDTH // 2, VERTICAL_MARGIN * 2 + LEADING * 2)))

        # Draw the game instructions
        for i, surf in enumerate(instruction_texts):
            display_surface.blit(surf, (HORIZONTAL_MARGIN, VERTICAL_MARGIN * 2 + LEADING * 2 + assets.font_large.get_height() + i * 50))

        # Draw the subtitle for meteor types
        display_surface.blit(subtitle_surface, (HORIZONTAL_MARGIN, VERTICAL_MARGIN * 2 + LEADING * 3 + assets.font_large.get_height() + len(instruction_texts) * 50))

        # Draw meteor details
        for i, surf in enumerate(meteor_texts):
            display_surface.blit(surf, (HORIZONTAL_MARGIN, VERTICAL_MARGIN * 3 + LEADING / 2 + assets.font_large.get_height() + len(instruction_texts) * 50 + i * 50))

        # Update the screen display
        pygame.display.update()

def pause_menu(display_surface, sounds, frozen_screen, music_elapsed_time):
    sounds.set_volume(sounds.get_menu_volume())
    sounds.play_pause_music()

    def resume_game():
        sounds.play_game_music(start=music_elapsed_time)
        return 'resume'

    def return_to_main_menu():
        sounds.play_menu_music()
        return 'main_menu'

    # Create a frame for game_over_menu
    frame_x_start = HORIZONTAL_MARGIN * 4 - LEADING * 2
    frame_y_strat = VERTICAL_MARGIN * 2.5 - LEADING / 2
    frame_width = HORIZONTAL_MARGIN * 2.5 - LEADING * 1.5
    frame = Frame(frame_x_start, frame_y_strat, frame_width, WINDOW_HEIGHT // 2 - VERTICAL_MARGIN // 4 + LEADING * 1.2)
    title_frame = Frame(frame_x_start, frame_y_strat, frame_width, VERTICAL_MARGIN * 1.5)

    # Create the menu buttons, dynamically spaced
    button_x_start = WINDOW_WIDTH // 2
    button_y_start = WINDOW_HEIGHT // 2 - VERTICAL_MARGIN // 3 - LEADING / 5
    buttons = [
        Button("   Resume   ", assets.font_small, (button_x_start, button_y_start), resume_game),
        Button("   Restart   ", assets.font_small, (button_x_start, button_y_start + BUTTON_SPACE * 0.65), lambda: 'restart'),
        Button("Main Menu", assets.font_small, (button_x_start, button_y_start + BUTTON_SPACE * 0.65 * 2), return_to_main_menu),
    ]

    # Wait for the user input to restart the game or quit after the player dies
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    result = button.check_click(mouse_pos)
                    if result:
                        return result
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return resume_game()
                elif event.key == pygame.K_r:
                    return 'restart'
                elif event.key == pygame.K_ESCAPE:
                    return return_to_main_menu()

        # Draw the frozen screen
        display_surface.blit(frozen_screen, (0, 0))

        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 125))
        display_surface.blit(overlay, (0, 0))

        # Draw the frame for menu and title
        frame.draw(display_surface)
        title_frame.draw(display_surface)

        # Draw Pause text
        _display_text(display_surface, "Pause", assets.font_large, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3), PAUSE_COLOR)

        # Draw the buttons
        for button in buttons:
            button.draw(display_surface)

        # Update the screen display
        pygame.display.update()

def game_over_menu(display_surface, sounds, score, high_score_manager, confetti_sprites):
    running = True
    result = False
    background = Background()
    is_new_high_score = score > high_score_manager.get_high_score()
    high_score_manager.save_high_score(score)

    sounds.set_menu_volume(sounds.get_menu_volume())
    sounds.play_game_over_music()

    def play_again():
        nonlocal running, result
        running = False
        result = True

    def return_to_main_menu():
        nonlocal running, result
        running = False
        result = False
        sounds.play_menu_music()

    # Create a frame for game_over_menu
    frame_x_start = HORIZONTAL_MARGIN * 3 - LEADING
    frame_y_strat = VERTICAL_MARGIN * 2.5 - LEADING / 2
    frame_width = HORIZONTAL_MARGIN * 4 + LEADING * 2
    frame = Frame(frame_x_start, frame_y_strat, frame_width, WINDOW_HEIGHT // 2 + VERTICAL_MARGIN // 2 - LEADING // 2)
    title_frame = Frame(frame_x_start, frame_y_strat, frame_width, VERTICAL_MARGIN * 1.5)

    # Create the menu buttons, dynamically spaced
    button_x_start = WINDOW_WIDTH // 2
    button_y_start = WINDOW_HEIGHT // 2 + VERTICAL_MARGIN + LEADING
    buttons = [
        Button("Play Again", assets.font_small, (button_x_start, button_y_start), play_again),
        Button("Main Menu", assets.font_small, (button_x_start, button_y_start + BUTTON_SPACE * 0.65), return_to_main_menu),
    ]

    # Wait for the user input to restart the game or quit after the player dies
    while running:
        dt = pygame.time.Clock().tick(FPS) / 1000.0  # Delta time in seconds (for frame rate independent movement)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.check_click(mouse_pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    play_again()
                if event.key == pygame.K_ESCAPE:
                    return_to_main_menu()

        # Draw the background
        background.draw(display_surface)

        # Draw the confetti effect
        confetti_sprites.update(dt)
        confetti_sprites.draw(display_surface)

        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 125))
        display_surface.blit(overlay, (0, 0))

        # Draw the frame for menu and title
        frame.draw(display_surface)
        title_frame.draw(display_surface)

        if is_new_high_score:
            # Draw the frame for the new high score
            new_high_score_frame = Frame(HORIZONTAL_MARGIN * 2 + LEADING * 2, VERTICAL_MARGIN // 2 + LEADING, HORIZONTAL_MARGIN * 5.5 + LEADING * 1.5, VERTICAL_MARGIN * 1.5)
            new_high_score_frame.draw(display_surface)

            # New High Score text
            _display_text(display_surface, "New High Score!", assets.font_large, (WINDOW_WIDTH // 2, VERTICAL_MARGIN * 1.5), HIGH_SCORE_COLOR)

        # Game Over text
        _display_text(display_surface, "GAME OVER", assets.font_large, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3), GAME_OVER_COLOR)

        # Score and High Score
        _display_text(display_surface, f"Score: {score}", assets.font_small, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - VERTICAL_MARGIN // 2))
        _display_text(display_surface, f"High Score: {high_score_manager.get_high_score()}", assets.font_small, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - VERTICAL_MARGIN // 3 + LEADING * 4), HIGH_SCORE_COLOR)

        # Draw the buttons
        for button in buttons:
            button.draw(display_surface)

        # Update the screen display
        pygame.display.update()

    return result