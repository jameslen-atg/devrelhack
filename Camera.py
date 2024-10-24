import pygame
import pyscroll
import pytmx

class Camera:
    def __init__(self, width, height, tmx_file):
        self.width = width
        self.height = height
        self.move_speed = 10
        self.zoom_level = 0.5
        self.zoom_speed = 0.1

        # Load the map
        self.tmx_data = pytmx.util_pygame.load_pygame(tmx_file)

        # Create a new data source for pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)

        # Create a new renderer
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, (width, height))
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
                if event.y > 0:  # Zoom in
                    self.zoom_level += self.zoom_speed
                elif event.y < 0:  # Zoom out
                    self.zoom_level -= self.zoom_speed
                self.zoom_level = max(0.1, self.zoom_level)  # Prevent zooming out too far
                self.map_layer.zoom = self.zoom_level

    def handle_zoom(self, event):
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # Zoom in
                self.zoom_level += self.zoom_speed
            elif event.y < 0:  # Zoom out
                self.zoom_level -= self.zoom_speed
            self.zoom_level = max(0.1, self.zoom_level)  # Prevent zooming out too far
            self.map_layer.zoom = self.zoom_level

    def center_on(self, position):
        self.group.center(position)

    def draw(self, screen):
        self.group.draw(screen)

    def update_group(self):
        self.group.update()