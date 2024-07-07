import pygame
import random
import math
import time
import os
import sys
from colorama import init, Fore, Style

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Suppress Pygame welcome message and MESA errors
class NullWriter:
    def write(self, s):
        pass

null_writer = NullWriter()
sys.stdout = null_writer
sys.stderr = null_writer

# Initialize pygame
pygame.init()

# Restore stdout and stderr
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

# Suppress MESA error messages
with open(os.devnull, 'w') as fnull:
    sys.stderr = fnull
    sys.stdout = fnull

    # Initialize mixer
    pygame.mixer.init()

    # Screen dimensions
    splash_screen_path = os.path.join('img', 'splash_screen.png')
    splash_screen_img = pygame.image.load(splash_screen_path)
    splash_screen_width, splash_screen_height = splash_screen_img.get_size()
    screen_width = 1920
    screen_height = 1080
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the window
    screen = pygame.display.set_mode((splash_screen_width, splash_screen_height))

    # Title and Icon
    pygame.display.set_caption("Space Invaders")
    icon_path = os.path.join('img', 'ufo.png')
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    # Load sounds
    shoot_sound = pygame.mixer.Sound(os.path.join('music', 'guns.wav'))
    pygame.mixer.music.load(os.path.join('music', 'music.mp3'))

    # Restore stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

# Clear console and output credits and controls
clear_console()
# Initialize colorama
init()

# Print credits to console
print(Fore.GREEN + "Credits" + Style.RESET_ALL)
print(Fore.YELLOW + "Developed by: CBKB - DeadlyData" + Style.RESET_ALL)
print(Fore.CYAN + "\nControls:" + Style.RESET_ALL)
print(Fore.CYAN + "M - Mute/Unmute music and sound" + Style.RESET_ALL)
print(Fore.CYAN + "P - Pause/Unpause game" + Style.RESET_ALL)
print(Fore.CYAN + "Arrow keys - Move player" + Style.RESET_ALL)
print(Fore.CYAN + "Space - Shoot" + Style.RESET_ALL)
print(Fore.CYAN + "Enter - Start/Restart game" + Style.RESET_ALL)

# Player
player_img_path = os.path.join('img', 'player.png')
player_img = pygame.image.load(player_img_path)
player_x_start = screen_width // 2 - 32
player_y_start = screen_height - 100
player_x = player_x_start
player_y = player_y_start
player_x_change = 0
player_y_change = 0
player_speed = 8
is_powered_up = False

# Invincibility
invincible = False
invincible_start_time = 0
invincible_duration = 5  # seconds

# Enemy
enemy_imgs = [os.path.join('img', 'enemy1.png'), os.path.join('img', 'enemy2.png')]
enemies = []
base_enemy_speed = 2  # Initial speed of enemies
enemy_spawn_rate = 0.3  # Time in seconds between enemy spawns
last_enemy_spawn_time = 0
max_enemies_on_screen = 18  # Maximum number of enemies allowed on screen at any time

# Bullet
bullet_img_path = os.path.join('img', 'bullet.png')
bullet_img = pygame.image.load(bullet_img_path)
bullets = []
bullet_y_change = 10
bullet_cooldown = 0.2  # seconds between shots
last_shot = time.time()

# Power-Up
power_up_img_path = os.path.join('img', 'powerup.png')
power_up_img = pygame.image.load(power_up_img_path).convert_alpha()
power_up = {"x": random.randint(0, screen_width - 64), "y": -100, "y_change": 3, "alive": False}
power_up_spawn_rate = 20  # seconds between power-up spawns
last_power_up_spawn_time = time.time()
power_up_pulse_direction = 1
power_up_alpha = 255  # Start with fully opaque

# Coin
coin_img_path = os.path.join('img', 'coin.png')
coin_img = pygame.image.load(coin_img_path).convert_alpha()
coins = []
coin_spawn_rate = 12  # seconds between coin spawns
last_coin_spawn_time = time.time()
coin_pulse_direction = 1
coin_alpha = 255  # Start with fully opaque

# Score
score_value = 0
high_score = 0
level = 1
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Player Lives
lives = 5
lives_x = screen_width - 150
lives_y = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Game States
state_start = 'start'
state_playing = 'playing'
state_game_over = 'game_over'
state_paused = 'paused'
game_state = state_start

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Background music and sound control
music_playing = True
sounds_muted = False
mute_state = 0  # 0: All sounds on, 1: Only music off, 2: All sounds off

# Trail effect
trail_particles = []

def create_space_background(screen_width, screen_height, star_count=100):
    background = pygame.Surface((screen_width, screen_height))
    background.fill((0, 0, 0))
    for _ in range(star_count):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        pygame.draw.circle(background, (255, 255, 255), (x, y), 1)
    return background

background = create_space_background(screen_width, screen_height)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_high_score(x, y):
    high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
    screen.blit(high_score_text, (x, y))

def show_lives(x, y):
    lives_text = font.render("Lives: " + str(lives), True, (255, 255, 255))
    screen.blit(lives_text, (x, y))

def show_level(x, y):
    level_text = font.render("Level: " + str(level), True, (255, 255, 255))
    screen.blit(level_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (screen_width // 2 - over_text.get_width() // 2, screen_height // 2 - over_text.get_height() // 2))
    levels_reached_text = font.render("Levels Reached: " + str(level), True, (255, 255, 255))
    screen.blit(levels_reached_text, (screen_width // 2 - levels_reached_text.get_width() // 2, screen_height // 2 + 50))
    score_text = font.render("Your Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 100))
    high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
    screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 2 + 150))
    continue_text = font.render("Press ENTER to restart", True, (255, 255, 255))
    screen.blit(continue_text, (screen_width // 2 - continue_text.get_width() // 2, screen_height // 2 + 200))

def start_screen():
    screen.blit(splash_screen_img, (0, 0))

def reset_game():
    global player_x, player_y, player_x_change, player_y_change, enemies, bullets, score_value, lives, last_shot, level, last_enemy_spawn_time, is_powered_up, power_up, power_up_start_time, high_score, trail_particles, coins, invincible, invincible_start_time
    player_x = player_x_start
    player_y = player_y_start
    player_x_change = 0
    player_y_change = 0
    enemies = []
    bullets = []
    score_value = 0
    lives = 5
    level = 1
    last_shot = time.time()
    last_enemy_spawn_time = time.time()
    is_powered_up = False
    power_up = {"x": random.randint(0, screen_width - 64), "y": -100, "y_change": 3, "alive": False}
    power_up_start_time = 0
    trail_particles = []
    coins = []
    invincible = False
    invincible_start_time = 0
    if score_value > high_score:
        high_score = score_value

def create_enemy():
    enemy_speed = base_enemy_speed + level * 0.2  # Speed increases with levels
    enemy = {
        "img": pygame.image.load(random.choice(enemy_imgs)),
        "x": random.randint(0, screen_width - 64),
        "y": random.randint(-500, -50),  # Make enemies appear closer to the top
        "x_change": 0,
        "y_change": enemy_speed,
        "alive": True
    }
    enemies.append(enemy)

def player(x, y):
    screen.blit(player_img, (x, y))

def draw_enemy(enemy):
    screen.blit(enemy["img"], (enemy["x"], enemy["y"]))

def fire_bullet(x, y):
    if not sounds_muted:
        shoot_sound.play()
    if is_powered_up:
        bullets.append({"img": bullet_img, "x": x + 16, "y": y})
        bullets.append({"img": bullet_img, "x": x - 16, "y": y})
    else:
        bullets.append({"img": bullet_img, "x": x + 16, "y": y})

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27

def is_player_collision(player_x, player_y, enemy_x, enemy_y):
    distance = math.sqrt(math.pow(player_x - enemy_x, 2) + math.pow(player_y - enemy_y, 2))
    return distance < 40  # Adjust collision distance as needed

def is_power_up_collision(player_x, player_y, power_up_x, power_up_y):
    distance = math.sqrt(math.pow(player_x - power_up_x, 2) + math.pow(player_y - power_up_y, 2))
    return distance < 40

def is_coin_collision(player_x, player_y, coin_x, coin_y):
    distance = math.sqrt(math.pow(player_x - coin_x, 2) + math.pow(player_y - coin_y, 2))
    return distance < 40

def toggle_mute():
    global mute_state, music_playing, sounds_muted
    mute_state = (mute_state + 1) % 3
    if mute_state == 0:
        pygame.mixer.music.unpause()
        music_playing = True
        sounds_muted = False
    elif mute_state == 1:
        pygame.mixer.music.pause()
        music_playing = False
        sounds_muted = False
    elif mute_state == 2:
        sounds_muted = True

def toggle_pause():
    global game_state, music_playing
    if game_state == state_playing:
        game_state = state_paused
        pygame.mixer.music.pause()
        music_playing = False
    elif game_state == state_paused:
        game_state = state_playing
        pygame.mixer.music.unpause()
        music_playing = True

# Add a trail particle effect behind the player
def add_trail_particle(x, y):
    color = (255, random.randint(100, 200), 0)  # Vary the green component for variety
    trail_particles.append({
        "x": x + 32 + random.randint(-2, 2),  # Add slight horizontal randomness
        "y": y + 45 + random.randint(-2, 2),  # Adjusted vertical position closer to the ship
        "alpha": 255,
        "size": random.uniform(2, 4),  # Randomize particle size
        "color": color
    })

# Draw the trail particles with fading effect
def draw_trail_particles():
    for particle in trail_particles:
        particle["y"] += random.uniform(1, 3)  # Randomize downward movement speed
        particle["alpha"] -= 5  # Reduce the alpha value to create fading effect
        particle["size"] -= 0.1  # Reduce the size of the particle
        if particle["alpha"] <= 0 or particle["size"] <= 0:
            trail_particles.remove(particle)
        else:
            particle_surface = pygame.Surface((int(particle["size"]), int(particle["size"])), pygame.SRCALPHA)
            particle_surface.fill((*particle["color"], particle["alpha"]))  # Use the particle's color
            screen.blit(particle_surface, (particle["x"], particle["y"]))

# Create a new coin
def create_coin():
    coin = {
        "img": coin_img.copy(),
        "x": random.randint(0, screen_width - 64),
        "y": random.randint(-500, -50),  # Make coins appear closer to the top
        "y_change": 3,
        "alive": True,
        "alpha": 255,
        "pulse_direction": 1
    }
    coins.append(coin)

# Draw coins with a pulsing effect
def draw_coins():
    for coin in coins:
        if coin["alive"]:
            coin["y"] += coin["y_change"]

            # Pulsing effect for coin
            coin["alpha"] += coin["pulse_direction"] * 5
            if coin["alpha"] >= 255:
                coin["alpha"] = 255
                coin["pulse_direction"] = -1
            elif coin["alpha"] <= 100:
                coin["alpha"] = 100
                coin["pulse_direction"] = 1
            coin["img"].set_alpha(coin["alpha"])

            screen.blit(coin["img"], (coin["x"], coin["y"]))

# Game Loop
running = True
reset_game()

# Play background music
pygame.mixer.music.play(-1)

while running:
    # Cap the frame rate
    clock.tick(60)

    screen.fill((0, 0, 0))  # RGB - Black background
    screen.blit(background, (0, 0))  # Draw background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                toggle_mute()
            if event.key == pygame.K_p:
                toggle_pause()

        if game_state == state_start:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = state_playing
                    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the window
                    screen = pygame.display.set_mode((screen_width, screen_height))
                    background = create_space_background(screen_width, screen_height)
                    reset_game()

        elif game_state == state_playing:
            # Keystroke check for player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -player_speed
                if event.key == pygame.K_RIGHT:
                    player_x_change = player_speed
                if event.key == pygame.K_UP:
                    player_y_change = -player_speed
                if event.key == pygame.K_DOWN:
                    player_y_change = player_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_y_change = 0

        elif game_state == state_paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = state_playing

    if game_state == state_start:
        start_screen()

    elif game_state == state_playing:
        # Continuous shooting while holding the spacebar
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and time.time() - last_shot > bullet_cooldown:
            fire_bullet(player_x, player_y)
            last_shot = time.time()

        # Player movement
        player_x += player_x_change
        player_y += player_y_change

        if player_x <= 0:
            player_x = 0
        elif player_x >= screen_width - 64:
            player_x = screen_width - 64
        if player_y <= 0:
            player_y = 0
        elif player_y >= screen_height - 64:
            player_y = screen_height - 64

        add_trail_particle(player_x, player_y)

        # Enemy movement and spawning
        current_time = time.time()
        if current_time - last_enemy_spawn_time > enemy_spawn_rate:
            create_enemy()
            last_enemy_spawn_time = current_time

        for enemy in enemies:
            if enemy["alive"]:
                enemy["y"] += enemy["y_change"]

                # Player collision
                if not invincible and is_player_collision(player_x, player_y, enemy["x"], enemy["y"]):
                    lives -= 1
                    enemy["alive"] = False
                    player_x = player_x_start  # Respawn player at start position
                    player_y = player_y_start
                    is_powered_up = False  # Reset power-up effect when player dies
                    invincible = True  # Enable invincibility
                    invincible_start_time = time.time()  # Start invincibility timer
                    if lives == 0:
                        game_state = state_game_over

                # Collision with bullet
                for bullet in bullets:
                    if is_collision(enemy["x"], enemy["y"], bullet["x"], bullet["y"]):
                        score_value += 1
                        enemy["alive"] = False
                        bullets.remove(bullet)

                draw_enemy(enemy)

        # Remove dead enemies
        enemies = [enemy for enemy in enemies if enemy["alive"]]

        # Power-up logic
        if power_up["alive"]:
            power_up["y"] += power_up["y_change"]

            # Pulsing effect for power-up
            power_up_alpha += power_up_pulse_direction * 5
            if power_up_alpha >= 255:
                power_up_alpha = 255
                power_up_pulse_direction = -1
            elif power_up_alpha <= 100:
                power_up_alpha = 100
                power_up_pulse_direction = 1
            power_up_img.set_alpha(power_up_alpha)

            screen.blit(power_up_img, (power_up["x"], power_up["y"]))

            # Power-up collision
            if is_power_up_collision(player_x, player_y, power_up["x"], power_up["y"]):
                is_powered_up = True
                power_up["alive"] = False

            if power_up["y"] > screen_height:
                power_up["alive"] = False

        # Spawn power-up
        if not power_up["alive"] and time.time() - last_power_up_spawn_time > power_up_spawn_rate:
            power_up["x"] = random.randint(0, screen_width - 64)
            power_up["y"] = -100
            power_up["alive"] = True
            last_power_up_spawn_time = time.time()

        # Coin logic
        if time.time() - last_coin_spawn_time > coin_spawn_rate:
            create_coin()
            last_coin_spawn_time = time.time()

        draw_coins()

        for coin in coins:
            if coin["alive"]:
                # Coin collision
                if is_coin_collision(player_x, player_y, coin["x"], coin["y"]):
                    score_value += 7
                    coin["alive"] = False

                if coin["y"] > screen_height:
                    coin["alive"] = False

        # Bullet movement
        for bullet in bullets:
            bullet["y"] -= bullet_y_change
            if bullet["y"] <= 0:
                bullets.remove(bullet)
            screen.blit(bullet["img"], (bullet["x"], bullet["y"]))

        # Check if invincibility has expired
        if invincible and time.time() - invincible_start_time > invincible_duration:
            invincible = False

        player(player_x, player_y)
        draw_trail_particles()
        show_score(text_x, text_y)
        show_high_score(text_x, text_y + 40)
        show_lives(lives_x, lives_y)
        show_level(screen_width // 2 - 50, 10)

        # Level up when enough enemies have been defeated
        if score_value >= level * 10:
            level += 1
            max_enemies_on_screen += 2  # Increase max enemies on screen with each level
            for _ in range(5):  # Add more enemies at the start of each new level
                create_enemy()

    elif game_state == state_paused:
        pause_text = over_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2 - pause_text.get_height() // 2))

    elif game_state == state_game_over:
        if score_value > high_score:
            high_score = score_value
        game_over_text()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_state = state_start
            os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the window
            screen = pygame.display.set_mode((splash_screen_width, splash_screen_height))
            start_screen()  # Restart the splash screen

    pygame.display.update()

# Quit the game
pygame.quit()
