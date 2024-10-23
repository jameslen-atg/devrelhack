import pygame
import random
from Entity import Entity
from Coin import Coin
from Obstacle import *
from Colors import *

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flocking Behavior Simulation")

NUM_ENTITIES = 50
NUM_OBSTACLES = 10

# Team scores
scores = {'red': 0, 'blue': 0, 'green': 0}

# Time limit (in milliseconds)
TIME_LIMIT = 5 * 60 * 1000  # 5 minute

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            handle_game_over()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            coin = Coin(x, y)

    screen.fill(BLACK)

    # Check time limit
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time > TIME_LIMIT:
        game_over = True

    if not game_over:
        if pygame.time.get_ticks() - coin_spawn_time > COIN_SPAWN_INTERVAL:
            coin = spawn_coin(entities, obstacles)
            coin_spawn_time = pygame.time.get_ticks()

        for obstacle in obstacles:
            obstacle.draw(screen)

        for entity in entities:
            entity.flock(entities, obstacles, coin)
            entity.update(entities, coin)
            edges(entity)
            entity.draw(screen)

        if coin and not coin.collected:
            coin.draw(screen)
        else:
            coin = None

        # Display scores
        score_text = f"Red: {scores['red']}  Blue: {scores['blue']}  Green: {scores['green']}"
        score_surface = font.render(score_text, True, WHITE)
        screen.blit(score_surface, (10, 10))

        # Display remaining time
        remaining_time = max(0, TIME_LIMIT - elapsed_time)
        minutes = remaining_time // 60000
        seconds = (remaining_time % 60000) // 1000
        time_text = f"Time: {minutes:02}:{seconds:02}"
        time_surface = font.render(time_text, True, WHITE)
        screen.blit(time_surface, (WIDTH - 150, 10))
    else:
        # Display "Game Over" message
        game_over_text = "Game Over"
        game_over_surface = font.render(game_over_text, True, WHITE)
        screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - game_over_surface.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)