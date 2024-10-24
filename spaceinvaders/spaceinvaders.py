# simple_game.py
import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simple Game")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

# Set up the player
player_size = 50
player_pos = [375, 550]  # Position the player at the bottom of the screen
player_speed = 5
quit_prompt_active = False
player_hit = False
player_hit_time = 0

# Set up arrows
arrow_size = [5, 10]
arrows = []
arrow_speed = 7

# Set up opponent arrows
opponent_arrow_size = [5, 10]
opponent_arrows = []
opponent_arrow_speed = 5
last_opponent_arrow_time = 0

# Load sounds
laser_sound = pygame.mixer.Sound("laser.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Set up opponents
opponent_size = 30
opponents = []
opponent_speed = 2
opponent_direction = 1  # 1 for right, -1 for left
rows = 3
cols = 8
for row in range(rows):
    for col in range(cols):
        x = col * (opponent_size + 10) + 50
        y = row * (opponent_size + 10) + 50
        opponents.append([x, y])

# Initialize score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_prompt_active = True
            elif quit_prompt_active:
                if event.key == pygame.K_y:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_n:
                    quit_prompt_active = False
            elif event.key == pygame.K_SPACE and not quit_prompt_active:
                # Create a new arrow
                arrow_pos = [player_pos[0] + player_size // 2 - arrow_size[0] // 2, player_pos[1]]
                arrows.append(arrow_pos)
                # Play laser sound
                laser_sound.play()

    if not quit_prompt_active:
        # Get keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed

        # Ensure the player stays within the screen bounds
        player_pos[0] = max(0, min(player_pos[0], 800 - player_size))

        # Move arrows
        for arrow in arrows:
            arrow[1] -= arrow_speed

        # Remove arrows that have moved off the screen
        arrows = [arrow for arrow in arrows if arrow[1] > 0]

        # Move opponents
        move_down = False
        for opponent in opponents:
            opponent[0] += opponent_speed * opponent_direction
            if opponent[0] <= 0 or opponent[0] >= 800 - opponent_size:
                move_down = True

        if move_down:
            opponent_direction *= -1
            for opponent in opponents:
                opponent[1] += opponent_size // 2

        # Check for collisions
        for arrow in arrows:
            for opponent in opponents:
                if (opponent[0] < arrow[0] < opponent[0] + opponent_size and
                        opponent[1] < arrow[1] < opponent[1] + opponent_size):
                    arrows.remove(arrow)
                    opponents.remove(opponent)
                    explosion_sound.play()
                    score += 10  # Increment score
                    break

        # Opponents shoot arrows
        current_time = pygame.time.get_ticks()
        if current_time - last_opponent_arrow_time > 1000:
            last_opponent_arrow_time = current_time
            if opponents:  # Check if the opponents list is not empty
                shooting_opponent = random.choice(opponents)
                opponent_arrow_pos = [shooting_opponent[0] + opponent_size // 2 - opponent_arrow_size[0] // 2, shooting_opponent[1] + opponent_size]
                opponent_arrows.append(opponent_arrow_pos)

        # Move opponent arrows
        for opponent_arrow in opponent_arrows:
            opponent_arrow[1] += opponent_arrow_speed

        # Remove opponent arrows that have moved off the screen
        opponent_arrows = [arrow for arrow in opponent_arrows if arrow[1] < 600]

        # Check for collisions with player
        for opponent_arrow in opponent_arrows:
            if (player_pos[0] < opponent_arrow[0] < player_pos[0] + player_size and
                    player_pos[1] < opponent_arrow[1] < player_pos[1] + player_size):
                opponent_arrows.remove(opponent_arrow)
                explosion_sound.play()
                player_hit = True
                player_hit_time = pygame.time.get_ticks()
                break

        # Fill the screen with white
        screen.fill(WHITE)

        # Draw the player
        if player_hit:
            if (pygame.time.get_ticks() - player_hit_time) // 250 % 2 == 0:
                pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
            if pygame.time.get_ticks() - player_hit_time > 2000:
                player_hit = False
        else:
            pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

        # Draw the arrows
        for arrow in arrows:
            pygame.draw.rect(screen, RED, (arrow[0], arrow[1], arrow_size[0], arrow_size[1]))

        # Draw the opponent arrows
        for opponent_arrow in opponent_arrows:
            pygame.draw.rect(screen, PURPLE, (opponent_arrow[0], opponent_arrow[1], opponent_arrow_size[0], opponent_arrow_size[1]))

        # Draw the opponents
        for opponent in opponents:
            points = [
                (opponent[0] + opponent_size // 2, opponent[1]),
                (opponent[0], opponent[1] + opponent_size),
                (opponent[0] + opponent_size, opponent[1] + opponent_size)
            ]
            pygame.draw.polygon(screen, GREEN, points)

        # Render the score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
    else:
        # Display quit prompt
        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        text = font.render("Quit? Y/N", True, (0, 0, 0))
        screen.blit(text, (250, 250))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)