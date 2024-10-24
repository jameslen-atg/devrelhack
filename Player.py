import pygame
import math

# Load player sprite and rotate it by 180 degrees
player_image = pygame.image.load(r'Assets\PNG\Default size\Ships\ship (1).png')
player_image = pygame.transform.rotate(player_image, 180)

# Load ball sprite
ball_image = pygame.image.load(r'Assets\PNG\Default size\Ship parts\cannonBall.png')

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
            # Propel ball to the right of the ship
            radians = math.radians(self.rotation_angle)
            ball_x = self.rect.centerx + self.rect.width // 2 * math.cos(radians)
            ball_y = self.rect.centery + self.rect.height // 2 * math.sin(radians)
            self.balls.append(Ball(ball_x, ball_y, self.rotation_angle - 90))

        if keys[pygame.K_q]:
            # Propel ball to the left of the ship
            radians = math.radians(self.rotation_angle)
            ball_x = self.rect.centerx - self.rect.width // 2 * math.cos(radians)
            ball_y = self.rect.centery - self.rect.height // 2 * math.sin(radians)
            self.balls.append(Ball(ball_x, ball_y, self.rotation_angle + 90))

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