import pygame
import math

# Initialize Pygame mixer for sound
pygame.mixer.init()

# Load player sprite and rotate it by 180 degrees
player_image = pygame.image.load(r'Assets\PNG\Default size\Ships\ship (1).png')
player_image = pygame.transform.rotate(player_image, 180)

# Load ball sprite
ball_image = pygame.image.load(r'Assets\PNG\Default size\Ship parts\cannonBall.png')

# Load shoot sound
shoot_sound = pygame.mixer.Sound(r'Assets\audio\shoot.wav')

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

    def is_off_screen(self, screen_width, screen_height):
        return (self.rect.right < 0 or self.rect.left > screen_width or
                self.rect.bottom < 0 or self.rect.top > screen_height)

class Player:
    def __init__(self, screen_width, screen_height):
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5
        self.rotation_angle = 0
        self.balls = []

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotation_angle += 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotation_angle -= 5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # Calculate movement in the direction the ship is facing
            radians = math.radians(self.rotation_angle)
            self.rect.x -= self.speed * math.sin(radians)
            self.rect.y -= self.speed * math.cos(radians)
        # if keys[pygame.K_DOWN]:
        #     self.rect.y += self.speed

        if keys[pygame.K_e]:
            # Propel ball to the right of the ship (starboard)
            ball_direction = self.rotation_angle - 90
            ball_position = pygame.math.Vector2(self.rect.center)
            self.balls.append(Ball(ball_position.x, ball_position.y, ball_direction))
            shoot_sound.play()

        if keys[pygame.K_q]:
            # Propel ball to the left of the ship (port)
            ball_direction = self.rotation_angle + 90
            ball_position = pygame.math.Vector2(self.rect.center)
            self.balls.append(Ball(ball_position.x, ball_position.y, ball_direction))
            shoot_sound.play()

    def update(self, screen_width, screen_height):
        self.handle_input()
        self.balls = [ball for ball in self.balls if not ball.is_off_screen(screen_width, screen_height)]
        for ball in self.balls:
            ball.move()

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect)
        for ball in self.balls:
            screen.blit(ball.image, ball.rect)