import pygame
from os.path import join
from random import randint, uniform
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("../images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + WINDOW_HEIGHT/4))
        self.direction = pygame.Vector2() # Vector to store movement direction
        self.speed = 300

        # Cooldown variables for shooting lasers
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400 # Cooldown time in milliseconds

    # Function to manage shooting cooldown
    def laser_time(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True # Allow shooting again after cooldown

    def update(self, dt):
        # Handle player movement based on keys pressed
        keys = pygame.key.get_pressed()

        # Prevent player from moving off-screen
        if self.rect.centerx >= WINDOW_WIDTH and (keys[pygame.K_d] == True or keys[pygame.K_RIGHT] == True):
            self.direction.x = 0 - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        elif self.rect.centerx <= 0 and (keys[pygame.K_a] == True or keys[pygame.K_LEFT]):
            self.direction.x = 1 - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        elif self.rect.centery >= WINDOW_HEIGHT and (keys[pygame.K_s] == True or keys[pygame.K_DOWN] == True):
            self.direction.y = 0 - int(keys[pygame.K_w] or keys[pygame.K_UP])
        elif self.rect.centery <= 0 and (keys[pygame.K_w] == True or keys[pygame.K_UP] == True):
            self.direction.y = 1 - int(keys[pygame.K_w] or keys[pygame.K_UP])
        else:
            self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
            self.direction.y = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt # Update position based on direction and speed
        self.direction.x = 0 # Reset x direction after movement
        self.direction.y = 0 # Reset y direction after movement

        # Check if space bar is pressed to shoot a laser
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites)) # Create laser
            self.can_shoot = False # Prevent shooting until cooldown ends
            self.laser_shoot_time = pygame.time.get_ticks() # Record time of shooting
            sounds.laser.play() # Play laser sound
        self.laser_time() # Handle cooldown

# Laser class that represents the laser shot by the player
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos) # Position laser at player's top

    def update(self, dt):
        self.rect.centery -= 400 * dt # Move the laser upwards
        if self.rect.bottom < 0: # If the laser goes off-screen, remove it
            self.kill()

# Meteor class representing asteroids falling from the top of the screen
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.original_image = surf # Save the original image for rotation
        self.image = surf
        self.rect = self.image.get_frect(midbottom = (randint(0, WINDOW_WIDTH), 0)) # Random starting position
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1) # Meteor's initial movement direction
        self.rotation = 0 # Rotation angle of the meteor
        self.size_category = "medium"  # Default size category
        self.speed = randint(400, 500)
        self.rotation_speed = randint(40,70)
        self.scale_factor = 1  # Default scale factor

        # Determine the size and properties of the meteor based on random chance
        chance = randint(1,101)
        if chance < 25:
            self.size_category = "small"
            self.scale_factor = 0.5
            self.speed = randint(500, 600)
            self.rotation_speed = randint(70, 100)
        elif chance < 50:  # Ensures a distinct second 25% range
            self.size_category = "large"
            self.scale_factor = 1.5
            self.speed = randint(300, 400)
            self.rotation_speed = randint(10, 40)

    def update(self, dt):
        # Move meteor and rotate it
        self.rect.center += self.direction * self.speed * dt
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, self.scale_factor)
        self.rect = self.image.get_frect(center = self.rect.center)

        # Kill meteor if it goes off-screen
        if self.rect.top >= WINDOW_HEIGHT or self.rect.right <= 0 or self.rect.left >= WINDOW_WIDTH:
            self.kill()

# Star class to display stars in the background
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf, i):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (star_positions[i])) # Position stars at predefined locations

# AnimatedExplosion class for explosion animations when objects are destroyed
class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups, size):
        super().__init__(groups)
        self.frames = [self.scale_frame(frame, size) for frame in frames] # Scale frames based on size
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    # Scale explosion frames based on the size of the explosion
    def scale_frame(self, frame, size):
        original_size = frame.get_size()
        if size == 'small':
            scale_factor = 0.5
        elif size == 'large':
            scale_factor = 1.5
        else:  # Medium size
            scale_factor = 1
        return pygame.transform.scale(frame, (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor)))

    def update(self, dt):
        self.frame_index += 25 * dt # Move through frames based on time
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill() # Remove explosion after it finishes

# Sounds class for handling all audio in the game
class Sounds:
    def __init__(self):
        self.laser = pygame.mixer.Sound(join("../audio", "laser.wav"))
        self.explosion = pygame.mixer.Sound(join("../audio", "explosion.wav"))
        self.damage = pygame.mixer.Sound(join("../audio", "damage.mp3"))
        self.game_music = pygame.mixer.Sound(join("../audio", "game_music.wav"))

    def set_volume(self, volume):
        # Set volume for all sounds
        self.laser.set_volume(volume)
        self.explosion.set_volume(volume)
        self.damage.set_volume(2*volume)
        self.game_music.set_volume(volume)

# Button class for creating interactive buttons in the game menus
class Button:
    def __init__(self, text, font, center, action):
        self.text = text
        self.font = font
        self.surface = font.render(text, True, "#ffffff")
        self.rect = self.surface.get_rect(center=center)
        self.action = action  # A method to call when the button is clicked

    def draw(self, display_surface, margin):
        # Draw the button's background and text
        background_rect = self.rect.inflate(margin // 4, margin // 6).move(0, -5)
        pygame.draw.rect(display_surface, "#503b5c", background_rect, border_radius=margin // 4)
        pygame.draw.rect(display_surface, "#b297cc", background_rect, 5, border_radius=margin // 4)
        display_surface.blit(self.surface, self.rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos): # Check if the button was clicked
            self.action()  # Call the assigned action

# Function to check distance between stars to avoid overlap during star placement
def check_distance(x, y, star_positions, min_distance):
    for (sx, sy) in star_positions:
        distance = math.sqrt((x - sx) ** 2 + (y - sy) ** 2)
        if distance < min_distance:
            return False
    return True

def collisions():
    # Check for collision between the player and meteors. If a collision occurs, meteor sprites are removed.
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        sounds.game_music.set_volume((volume/2)) # Lower the background music volume
        sounds.damage.play() # Play damage sound when player collides with meteor

        # Trigger explosion animation at player position
        AnimatedExplosion(explosion_frames, player.rect.center, explosion_sprites, 'large')
        player.kill()  # Remove the player from the game after collision
        game_over() # End the game

    # Check for collisions between lasers and meteors
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask)
        for meteor in collided_sprites:
            laser.kill() # Remove the laser when it collides with a meteor
            # Trigger explosion animation at the laser's position and meteor's size category
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites, meteor.size_category)
            sounds.explosion.play() # Play explosion sound upon meteor destruction

# Function to calculate spawn rate based on score
# The spawn rate decreases (meteors spawn faster) as the player's score increases.
def calculate_spawn_rate(score):
    initial_spawn_rate = 500 # Start with a 500ms spawn rate
    return max(100, initial_spawn_rate - (score // 10) * 50)  # Decrease by 50ms every 10 points, minimum 100ms

def reset_game():
    global all_sprites, meteor_sprites, laser_sprites, player, star_positions, start_time, score, meteor_event

    # Clear all sprite groups to reset the game
    all_sprites = pygame.sprite.Group()
    meteor_sprites = pygame.sprite.Group()
    laser_sprites = pygame.sprite.Group()
    star_positions = []

    # Generate random positions for the stars in the background
    for i in range(25):
        while True:
            x = randint(0, WINDOW_WIDTH)
            y = randint(0, WINDOW_HEIGHT)
            if check_distance(x, y, star_positions, min_distance):
                star_positions.append((x, y))
                break
        Star(all_sprites, star_surf, i) # Create stars at the given position

    # Recreate the player
    player = Player(all_sprites)

    # Reset the survival time
    start_time = pygame.time.get_ticks()

    # Update spawn rate based on score
    spawn_rate = calculate_spawn_rate(score)

    # Create a custom event for meteor spawning based on the updated spawn rate
    meteor_event = pygame.event.custom_type()
    pygame.time.set_timer(meteor_event, spawn_rate) # Set a timer for meteor event with the spawn rate

def game():
    global running

    reset_game() # Initialize the game state and reset variables

    # Main game loop
    while running:
        dt = clock.tick(120) / 1000  # Delta time in seconds (for frame rate independent movement)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Exit the game
                pygame.quit()
                exit()
            elif event.type == meteor_event: # Spawn a new meteor when the timer expires
                Meteor(meteor_surf, (all_sprites, meteor_sprites))

        # Update all sprites (player, meteors, lasers, etc.)
        all_sprites.update(dt)

        # Check for collisions (player with meteors and lasers with meteors)
        collisions()

        # Draw the updated game state
        display_surface.fill("#503b5c")  # Fill the background with a color
        all_sprites.draw(display_surface)  # Draw all sprites on the screen
        display_score()  # Display the current score

        pygame.display.update()  # Update the screen

def game_over():
    # Wait for user input to restart the game or quit after the player dies
    while True:
        dt = clock.tick(120) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Press 'R' to restart the game
                    game()
                    return
                elif event.key == pygame.K_ESCAPE: # Press 'Esc' to go back to the main menu
                    reset_game()
                    main_menu()
                    return

        # Update explosion animations for visual effects after player death
        explosion_sprites.update(dt)

        # Draw game over screen with animations and text
        display_surface.fill("#503b5c")  # Background color
        all_sprites.draw(display_surface)  # Draw game objects
        explosion_sprites.draw(display_surface)  # Draw explosions

        # Create a semi-transparent overlay surface for better readability
        overlay_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 1.25 * margin))  # Blacking for semi-transparency
        display_surface.blit(overlay_surface, (0, 0))

        # Create the text for the Game Over screen
        game_over_text = font_large.render("GAME OVER", True, "#ffffff")
        restart_text = font_small.render("Press 'R' to Restart or 'Esc' to quit", True, "#ffffff")

        # Calculate positions for the text
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - margin//2))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + margin//4))

        # Draw a rectangle behind the text for better readability
        background_rect = game_over_rect.union(restart_rect).inflate(margin//2, margin//4)  # Create a background encompassing both texts
        pygame.draw.rect(display_surface, "#503b5c", background_rect, border_radius=margin//3)
        pygame.draw.rect(display_surface, "#b297cc", background_rect, 5, border_radius=margin//3)  # Border for better design

        # Draw the actual text
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(restart_text, restart_rect)

        pygame.display.update()

def display_score():
    global start_time, score

    # Calculate elapsed time in seconds
    score = (pygame.time.get_ticks() - start_time) // 1000

    # Display the score in the bottom-center of the screen
    text_surf = font_small.render(str(score), True, "#ffffff")
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT-30))

    # Draw background and score text
    pygame.draw.rect(display_surface, "#503b5c", text_rect.inflate(20, 10).move(0, -5), 0, 10)
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, "#b297cc", text_rect.inflate(20,10).move(0,-5), 5, 10)

def draw_background():
    display_surface.fill("#503b5c") # Background color
    for x, y in star_positions: # Draw stars in the background
        display_surface.blit(star_surf, (x, y))

def main_menu():
    # Menu buttons actions
    def start_game():
        game()

    def open_settings():
        settings_menu()

    def open_how_to_play():
        how_to_play_menu()

    def exit_game():
        pygame.quit()
        exit()

    # Create the menu buttons
    buttons = [
        Button("Play", font_large, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + margin // 5), start_game),
        Button("Settings", font_large, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + margin // 5), open_settings),
        Button("How to Play", font_large, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.5 + margin // 5), open_how_to_play),
        Button("Exit", font_large, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - margin), exit_game)
    ]

    # Draw the player image at the center of the screen
    player_rect = player.image.get_rect(center=(WINDOW_WIDTH // 2, margin * 1.30))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.check_click(mouse_pos)

        # Draw the background and buttons
        draw_background()
        display_surface.blit(player.image, player_rect)
        for button in buttons:
            button.draw(display_surface, margin)

        pygame.display.update()

def settings_menu():
    global volume

    settings_running = True
    muted = False

    def return_to_menu():
        nonlocal settings_running
        settings_running = False  # Exit settings menu

    # Create a button for going back to the main menu
    back_button = Button("Back", font_small, (margin//1.5, margin//1.5), return_to_menu)

    # Render the title text of the Settings menu
    title_surface = font_large.render("Settings", True, "#ffffff")

    # Create a list of 10 segments to represent the volume
    volume_segments = []
    segment_width = 60  # Width of each segment
    segment_height = 20  # Height of the segment
    margin_segments = 10  # Space between segments
    for i in range(10):
        # Calculate the x and y position for each volume segment
        x_pos = (WINDOW_WIDTH // 2 - (5.5 * segment_width)) + i * (segment_width + margin_segments)
        y_pos = WINDOW_HEIGHT // 2
        volume_segments.append(pygame.Rect(x_pos, y_pos, segment_width, segment_height))

    # Define the border for the volume control
    volume_border = pygame.Rect(
        volume_segments[0].x - 5,
        volume_segments[0].y - 5,
        (segment_width + margin_segments) * 10 - margin_segments + 10,
        segment_height + 10
    )

    # Define the mute checkbox
    mute_checkbox_rect = pygame.Rect(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 75, font_small_size, font_small_size)
    mute_text = font_small.render("Mute", True, "#ffffff")

    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                back_button.check_click(mouse_pos) # Check if the back button is clicked

                # Check if any of the volume segments are clicked and adjust the volume
                for i, rect in enumerate(volume_segments):
                    if rect.collidepoint(mouse_pos):
                        volume = (i+1) / 10  # Maps clicks to 0.1 - 1.0 volume range (10 segments, 0 to 1)
                        muted = False  # Unmute when volume changes

                # Check for clicks on the mute checkbox
                if mute_checkbox_rect.collidepoint(mouse_pos):
                    if not muted:
                        muted = True  # Toggle muted state
                    else:
                        muted = False

        # Update the sound volume based on mute state and the current volume
        if muted:
            sounds.set_volume(0)  # Mute the sound
            color = "#808080"  # Change the segment color to gray when muted
        else:
            sounds.set_volume(volume)  # Set volume to current level
            color = "#ffffff"  # Set the segment color to white when unmuted

        draw_background()  # Redraw the background for the settings menu

        # Draw return button
        back_button.draw(display_surface, margin)

        # Draw the title at the top of the screen
        display_surface.blit(title_surface, title_surface.get_rect(center=(WINDOW_WIDTH//2, margin * 1.5)))

        # Display the current volume level as a percentage
        volume_text = font_small.render(f"Volume: {int(volume * 100)}%", True, "#ffffff")
        display_surface.blit(volume_text, volume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 3 * segment_height)))

        # Draw the border around the volume control
        pygame.draw.rect(display_surface, "#ffffff", volume_border, 3)  # White border around volume control

        # Draw the volume segments and fill them according to the current volume
        for i, rect in enumerate(volume_segments):
            if i / 10 < volume:  # If the segment is part of the current volume level, fill it with white
                pygame.draw.rect(display_surface, color, rect)
            else:
                pygame.draw.rect(display_surface, "#503b5c", rect)  # Empty segment (background color)

        # Draw the mute checkbox
        pygame.draw.rect(display_surface, "#ffffff" if muted else "#503b5c", mute_checkbox_rect)  # Fill if muted
        pygame.draw.rect(display_surface, "#ffffff", mute_checkbox_rect, 3)  # Border
        display_surface.blit(mute_text, mute_text.get_rect(topleft=(mute_checkbox_rect.left + 45, mute_checkbox_rect.y)))

        pygame.display.update()  # Update the screen display

def how_to_play_menu():
    how_to_play_running = True

    def return_to_menu():
        nonlocal how_to_play_running
        how_to_play_running = False  # Exit settings menu

    # Create the Back button
    back_button = Button("Back", font_small, (margin//1.5, margin//1.5), return_to_menu)

    # Instructions for the game and meteor types
    title_text = "How to Play"
    instructions = [
        "W/A/S/D or Arrow Keys to move.",
        "Press SPACE to shoot lasers.",
        "Avoid meteors - getting hit will destroy your ship.",
        "Live longer to earn points."
    ]
    subtitle_text = "Meteor types"
    meteor_details = [
        "- Small Meteors: Small, fast, and tricky to hit.",
        "- Medium Meteors: Medium size with normal speed.",
        "- Big Meteors: Large, slow, but hard to avoid."
    ]

    # Render the text surfaces for title, instructions, and meteor details
    title_surface = font_large.render(title_text, True, "#ffffff")
    subtitle_surface = font_small.render(subtitle_text, True, "#ffffff")
    instruction_texts = [font_small.render(text, True, "#ffffff") for text in instructions]
    meteor_texts = [font_small.render(text, True, "#ffffff") for text in meteor_details]

    while how_to_play_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                back_button.check_click(mouse_pos) # Check if the back button is clicked

        draw_background() # Redraw the background for the How To Play menu

        # Draw the return button
        back_button.draw(display_surface, margin)

        # Draw the title
        display_surface.blit(title_surface, title_surface.get_rect(center=(WINDOW_WIDTH//2, margin * 1.25)))

        # Draw the game instructions
        for i, text_surf in enumerate(instruction_texts):
            display_surface.blit(text_surf, (margin, 1.5 * margin + font_large_size + i * 50))

        # Draw the subtitle for meteor types
        display_surface.blit(subtitle_surface, (margin, 1.75 * margin + font_large_size + len(instruction_texts) * 50))

        # Draw meteor details
        for i, text_surf in enumerate(meteor_texts):
            display_surface.blit(text_surf, (margin, 2.5 * margin + font_large_size + len(instruction_texts) * 50 + i * 50))

        pygame.display.update()  # Update the screen display

# General setup for Pygame
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1080, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space shooter")
clock = pygame.time.Clock()

# Game Variables
running = True
score = 0
volume = 0.1  # Default volume level
margin = 100  # Margin for positioning UI elements

# Load Assets (images, fonts, sounds)
star_surf = pygame.image.load(join("../images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(join("../images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(join("../images", "laser.png")).convert_alpha()
font_large_size = 70
font_large = pygame.font.Font(join("../images", "Oxanium-Bold.ttf"), font_large_size)
font_small_size = 35
font_small = pygame.font.Font(join("../images", "Oxanium-Bold.ttf"), font_small_size)
back_button = font_small.render("Back", True, "#ffffff")
explosion_frames = [pygame.image.load(join("../images", "explosion", f"{i}.png")).convert_alpha() for i in range (21)]

# Initialize Sounds
sounds = Sounds()
sounds.set_volume(volume) # Set all volume to 10%
sounds.game_music.play(loops=-1)  # Play background music indefinitely

# Initialize Sprite Groups
all_sprites = pygame.sprite.Group()
star_positions = []
min_distance = 150 # Minimum distance between stars
for i in range(25):
    while True:
        x = randint(0, WINDOW_WIDTH)
        y = randint(0, WINDOW_HEIGHT)
        if check_distance(x, y, star_positions, min_distance): # Check if the position is far enough from existing stars
            star_positions.append((x, y))
            break
    Star(all_sprites, star_surf, i)
player = Player(all_sprites)
explosion_sprites = pygame.sprite.Group()

# Run the main menu
main_menu()