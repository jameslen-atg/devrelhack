import pygame

class GameObject:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)

    def draw(self, screen):
        pass