import pygame
from GameObject import GameObject
from Colors import *

class Coin(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = 10
        self.collected = False

    def draw(self, screen):
        pygame.draw.circle(screen, GOLD, (int(self.position.x), int(self.position.y)), self.radius)