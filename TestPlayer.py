import pygame
import sys
from Player import Player

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
ocean_blue = (0, 105, 148)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simple Testbed for Player Class')

# Create player instance
player = Player(screen_width, screen_height)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player
    player.update(screen_width, screen_height)

    # Fill the screen with ocean blue
    screen.fill(ocean_blue)

    # Draw player
    player.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()