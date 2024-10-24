import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
ocean_blue = (0, 105, 148)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simple Pygame Example')

# Load player sprite and rotate it by 180 degrees
player_image = pygame.image.load(r'Assets\PNG\Default size\Ships\ship (1).png')
player_image = pygame.transform.rotate(player_image, 180)
player_rect = player_image.get_rect()
player_rect.center = (screen_width // 2, screen_height // 2)
player_speed = 5
rotation_angle = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rotation_angle += 5
    if keys[pygame.K_RIGHT]:
        rotation_angle -= 5
    if keys[pygame.K_UP]:
        # Calculate movement in the direction the ship is facing
        radians = math.radians(rotation_angle)
        player_rect.x -= player_speed * math.sin(radians)
        player_rect.y -= player_speed * math.cos(radians)
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    # Rotate the player image
    rotated_image = pygame.transform.rotate(player_image, rotation_angle)
    rotated_rect = rotated_image.get_rect(center=player_rect.center)

    # Fill the screen with ocean blue
    screen.fill(ocean_blue)

    # Draw the player
    screen.blit(rotated_image, rotated_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()