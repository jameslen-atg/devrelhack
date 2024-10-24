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

# Load ball sprite
ball_image = pygame.image.load(r'Assets\PNG\Default size\Ship parts\cannonBall.png')

# Ball class
class Ball:
    def __init__(self, x, y, direction):
        self.image = ball_image
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10

    def move(self):
        radians = math.radians(self.direction)
        self.rect.x += self.speed * math.cos(radians)
        self.rect.y += self.speed * math.sin(radians)

    def is_off_screen(self):
        return (self.rect.right < 0 or self.rect.left > screen_width or
                self.rect.bottom < 0 or self.rect.top > screen_height)

# List to hold balls
balls = []

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        rotation_angle += 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        rotation_angle -= 5
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        # Calculate movement in the direction the ship is facing
        radians = math.radians(rotation_angle)
        player_rect.x -= player_speed * math.sin(radians)
        player_rect.y -= player_speed * math.cos(radians)
    # if keys[pygame.K_DOWN]:
    #     player_rect.y += player_speed

    if keys[pygame.K_e]:
        # Propel ball to the right of the ship
        radians = math.radians(rotation_angle)
        ball_x = player_rect.centerx + player_rect.width // 2 * math.cos(radians)
        ball_y = player_rect.centery + player_rect.height // 2 * math.sin(radians)
        balls.append(Ball(ball_x, ball_y, rotation_angle - 90))

    if keys[pygame.K_q]:
        # Propel ball to the left of the ship
        radians = math.radians(rotation_angle)
        ball_x = player_rect.centerx - player_rect.width // 2 * math.cos(radians)
        ball_y = player_rect.centery - player_rect.height // 2 * math.sin(radians)
        balls.append(Ball(ball_x, ball_y, rotation_angle + 90))

    # Rotate the player image
    rotated_image = pygame.transform.rotate(player_image, rotation_angle)
    rotated_rect = rotated_image.get_rect(center=player_rect.center)

    # Fill the screen with ocean blue
    screen.fill(ocean_blue)

    # Draw the player
    screen.blit(rotated_image, rotated_rect)

    # Move and draw balls
    for ball in balls[:]:
        ball.move()
        if ball.is_off_screen():
            balls.remove(ball)
        else:
            screen.blit(ball.image, ball.rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()