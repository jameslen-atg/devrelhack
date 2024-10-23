import pygame
from GameObject import GameObject
from Colors import *

OBSTACLE_RADIUS = 30

class Obstacle(GameObject):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)
        self.radius = OBSTACLE_RADIUS

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.position.x), int(self.position.y)), OBSTACLE_RADIUS)