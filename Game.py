import pygame
from Colors import *
from Camera import Camera
from MapLoader import MapLoader

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load and set the icon image
icon_image = pygame.image.load('Assets\PNG\Default size\Ships\ship (1).png')
pygame.display.set_icon(icon_image)
pygame.display.set_caption("Ocean of Pirates")

# Time limit (in milliseconds)
TIME_LIMIT = 5 * 60 * 1000  # 5 minutes

def handle_game_over() -> None:
    pygame.quit()
    exit()

# Load the map using MapLoader
map_loader = MapLoader('World.tmx', WIDTH, HEIGHT)
collidable_tiles = map_loader.get_collidable_tiles()

# Initialize the camera
starting_camera_pos = pygame.Vector2(3510, 5200)
camera = Camera(WIDTH, HEIGHT, map_loader.get_map_data())
camera.center_on(starting_camera_pos)

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

    keys = pygame.key.get_pressed()
    camera.update(keys, events)  # AMARTZ TODO: eventually remove this and just use the camera's center_on method

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the map
    camera.draw(screen)

    camera.update_group()

    # Check time limit
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time > TIME_LIMIT:
        game_over = True

    if not game_over:
        # Display remaining time
        remaining_time = max(0, TIME_LIMIT - elapsed_time)
        minutes = remaining_time // 60000
        seconds = (remaining_time % 60000) // 1000
        time_text = f"Time: {minutes:02}:{seconds:02}"
        time_surface = font.render(time_text, True, WHITE)
        screen.blit(time_surface, (WIDTH - 150, 10))

        # Display framerate
        framerate = int(clock.get_fps())
        framerate_text = f"FPS: {framerate}"
        framerate_surface = font.render(framerate_text, True, WHITE)
        screen.blit(framerate_surface, (WIDTH - 100, HEIGHT - 40))
    else:
        # Display "Game Over" message
        game_over_text = "Game Over"
        game_over_surface = font.render(game_over_text, True, WHITE)
        screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - game_over_surface.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)