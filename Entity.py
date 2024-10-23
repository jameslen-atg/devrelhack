import pygame
import random
from GameObject import GameObject
from Colors import *

MAX_SPEED = 2
MAX_FORCE = 0.03
NEIGHBOR_RADIUS = 50
SEPARATION_RADIUS = 25
AVOID_RADIUS = 75
ENTITY_RADIUS = 5

class Entity(GameObject):
    def __init__(self, x, y, team):
        super().__init__(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED
        self.acceleration = pygame.Vector2(0, 0)
        self.team = team
        self.radius = ENTITY_RADIUS
        self.coin_collected_callback = None

    def register_coin_collected_callback(self, callback):
        self.coin_collected_callback = callback

    def update(self, entities, coin):
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.position += self.velocity
        self.acceleration *= 0
        self.handle_collisions(entities)
        self.collect_coin(coin)

    def apply_force(self, force):
        self.acceleration += force

    def seek(self, target):
        desired = (target - self.position).normalize() * MAX_SPEED
        steer = desired - self.velocity
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def separate(self, entities):
        steer = pygame.Vector2(0, 0)
        count = 0
        for other in entities:
            if other.team == self.team:
                distance = self.position.distance_to(other.position)
                if 0 < distance < SEPARATION_RADIUS:
                    diff = self.position - other.position
                    diff /= distance
                    steer += diff
                    count += 1
        if count > 0:
            steer /= count
        if steer.length() > 0:
            steer = steer.normalize() * MAX_SPEED - self.velocity
            if steer.length() > MAX_FORCE:
                steer.scale_to_length(MAX_FORCE)
        return steer

    def align(self, entities):
        steer = pygame.Vector2(0, 0)
        count = 0
        for other in entities:
            if other.team == self.team:
                distance = self.position.distance_to(other.position)
                if 0 < distance < NEIGHBOR_RADIUS:
                    steer += other.velocity
                    count += 1
        if count > 0:
            steer /= count
            steer = steer.normalize() * MAX_SPEED - self.velocity
            if steer.length() > MAX_FORCE:
                steer.scale_to_length(MAX_FORCE)
        return steer

    def cohesion(self, entities):
        target = pygame.Vector2(0, 0)
        count = 0
        for other in entities:
            if other.team == self.team:
                distance = self.position.distance_to(other.position)
                if 0 < distance < NEIGHBOR_RADIUS:
                    target += other.position
                    count += 1
        if count > 0:
            target /= count
            return self.seek(target)
        return pygame.Vector2(0, 0)

    def avoid_obstacles(self, obstacles):
        steer = pygame.Vector2(0, 0)
        for obstacle in obstacles:
            distance = self.position.distance_to(obstacle.position)
            if distance < AVOID_RADIUS:
                diff = self.position - obstacle.position
                diff /= distance
                steer += diff
        if steer.length() > 0:
            steer = steer.normalize() * MAX_SPEED - self.velocity
            if steer.length() > MAX_FORCE:
                steer.scale_to_length(MAX_FORCE)
        return steer

    def flock(self, entities, obstacles, coin):
        separation = self.separate(entities)
        alignment = self.align(entities)
        cohesion = self.cohesion(entities)
        avoidance = self.avoid_obstacles(obstacles)
        self.apply_force(separation * 1.5)
        self.apply_force(alignment)
        self.apply_force(cohesion)
        self.apply_force(avoidance * 3)
        if coin:
            self.apply_force(self.seek(coin.position))

    def handle_collisions(self, entities):
        for other in entities:
            if other != self:
                distance = self.position.distance_to(other.position)
                if distance < self.radius + other.radius:
                    overlap = self.radius + other.radius - distance
                    direction = (self.position - other.position).normalize()
                    self.position += direction * (overlap / 2)
                    other.position -= direction * (overlap / 2)

    def collect_coin(self, coin):
        if coin and self.position.distance_to(coin.position) < self.radius + coin.radius:
            coin.collected = True
            if self.coin_collected_callback:
                self.coin_collected_callback(self)

    def draw(self, screen):
        color = WHITE
        if self.team == 'red':
            color = RED
        elif self.team == 'blue':
            color = BLUE
        elif self.team == 'green':
            color = GREEN
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), self.radius)