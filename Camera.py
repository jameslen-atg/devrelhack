import pygame
import pyscroll
import pytmx
from MapLoader import MapLoader

class Camera:
    def __init__(self, width, height, map_data):
        self.width = width
        self.height = height
        self.move_speed = 10
        self.zoom_level = 0.5
        self.zoom_speed = 0.1

        # Load the map using MapLoader
        # map_loader = MapLoader(tmx_file, width, height, self.zoom_level)
        self.map_layer = pyscroll.BufferedRenderer(map_data, (width, height))

        # Create a new group for all sprites
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

    def update(self, keys, events):
        move_x, move_y = 0, 0
        if keys[pygame.K_LEFT]:
            move_x -= self.move_speed
        if keys[pygame.K_RIGHT]:
            move_x += self.move_speed
        if keys[pygame.K_UP]:
            move_y -= self.move_speed
        if keys[pygame.K_DOWN]:
            move_y += self.move_speed

        # Center the map on the new position
        self.group.center((self.group.view.centerx + move_x, self.group.view.centery + move_y))

        # Handle zooming with mouse scroll wheel
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                # Add zoom handling logic here
                pass
    def draw(self, surface):
        self.group.draw(surface)

    def center_on(self, position):
        # Center the camera on a specific position
        self.group.center(position)

    def get_bounds(self):
        left = self.group.view.left
        top = self.group.view.top
        right = self.group.view.right
        bottom = self.group.view.bottom
        return (left, top, right, bottom)