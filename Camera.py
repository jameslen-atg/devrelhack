import pygame
import pyscroll
import pytmx
from MapLoader import MapLoader

max_zoom = 1.5
min_zoom = 0.175

class Camera:
    def __init__(self, width, height, map_data):
        self.width = width
        self.height = height
        self.move_speed = 10
        self.zoom_level = 0.30
        self.zoom_speed = 0.10

        # Load the map using MapLoader
        # map_loader = MapLoader(tmx_file, width, height, self.zoom_level)
        self.map_layer = pyscroll.BufferedRenderer(map_data, (width, height))
        self.map_layer.zoom = self.zoom_level

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
                current_center = self.group.view.center
                if event.y > 0:  # Scroll up
                    self.zoom_level += self.zoom_speed
                elif event.y < 0:  # Scroll down
                    self.zoom_level -= self.zoom_speed
                
                # Clamp the zoom level to never be less than min_zoom
                self.zoom_level = max(self.zoom_level, min_zoom)
                # Clamp the zoom level to never be more than max_zoom
                self.zoom_level = min(self.zoom_level, max_zoom)
                
                self.map_layer.zoom = self.zoom_level
                self.group.center(current_center)

    def center_on(self, position):
        self.group.center(position)

    def draw(self, screen):
        self.group.draw(screen)

    def update_group(self):
        self.group.update()