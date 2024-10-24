import pygame
import random
from Entity import Entity
from Coin import Coin
from Obstacle import *
from Colors import *
from Camera import Camera
from MapLoader import MapLoader  # Import MapLoader

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load and set the icon image
icon_image = pygame.image.load('Assets\PNG\Default size\Ships\ship (1).png')
pygame.display.set_icon(icon_image)
pygame.display.set_caption("Ocean of Pirates")

NUM_ENTITIES = 50
NUM_OBSTACLES = 10

# Team scores
scores = {'red': 0, 'blue': 0, 'green': 0}

# Time limit (in milliseconds)
TIME_LIMIT = 5 * 60 * 1000  # 5 minutes

# Define a callback function
def on_coin_collected(entity):
    print(f"Coin collected by {entity.team} team!")
    scores[entity.team] += 1

def is_valid_coin_position(x, y, entities, obstacles):
    for entity in entities:
        if pygame.Vector2(x, y).distance_to(entity.position) < entity.radius + 10:
            return False
    for obstacle in obstacles:
        if pygame.Vector2(x, y).distance_to(obstacle.position) < OBSTACLE_RADIUS + 10:
            return False
    return True

def spawn_coin(entities, obstacles):
    while True:
        x = random.uniform(0, WIDTH)
        y = random.uniform(0, HEIGHT)
        if is_valid_coin_position(x, y, entities, obstacles):
            return Coin(x, y)

def handle_game_over() -> None:
    pygame.quit()
    exit()

def edges(entity):
    if entity.position.x > WIDTH:
        entity.position.x = 0
    elif entity.position.x < 0:
        entity.position.x = WIDTH
    if entity.position.y > HEIGHT:
        entity.position.y = 0
    elif entity.position.y < 0:
        entity.position.y = HEIGHT

# Load the map using MapLoader
map_loader = MapLoader('World.tmx', WIDTH, HEIGHT)

# Initialize the camera
starting_camera_pos = pygame.Vector2(3510, 5200)
camera = Camera(WIDTH, HEIGHT, map_loader.get_map_data())
camera.center_on(starting_camera_pos)

# Create entities with teams
teams = ['red', 'blue', 'green']
entities = []
for _ in range(NUM_ENTITIES):
    entity = Entity(random.uniform(0, WIDTH), random.uniform(0, HEIGHT), random.choice(teams))
    entity.register_coin_collected_callback(on_coin_collected)
    entities.append(entity)

# Create obstacles
obstacles = []
for _ in range(NUM_OBSTACLES):
    x = random.uniform(OBSTACLE_RADIUS, WIDTH - OBSTACLE_RADIUS)
    y = random.uniform(OBSTACLE_RADIUS, HEIGHT - OBSTACLE_RADIUS)
    obstacles.append(Obstacle(x, y))

# Coin variables
coin = None
coin_spawn_time = 0
COIN_SPAWN_INTERVAL = 5000

# Main loop
running = True
game_over = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Track start time
start_time = pygame.time.get_ticks()

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            handle_game_over()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            x, y = event.pos
            coin = Coin(x, y)

    keys = pygame.key.get_pressed()
    camera.update(keys, events)  # AMARTZ TODO: eventually remove this and just use the camera's center_on method

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the map
    camera.draw(screen)

    pygame.display.flip()
    clock.tick(60)