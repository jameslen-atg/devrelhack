import pygame
import sys

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

# Load player sprite
player_image = pygame.image.load(r'Assets\PNG\Default size\Ships\ship (1).png')
player_rect = player_image.get_rect()
player_rect.center = (screen_width // 2, screen_height // 2)
player_speed = 5

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    # Fill the screen with ocean blue
    screen.fill(ocean_blue)

    # Draw the player
    screen.blit(player_image, player_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()