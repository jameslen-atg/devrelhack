import pyscroll
import pytmx

class MapLoader:
    def __init__(self, tmx_file, width, height, zoom_level=0.5):
        self.tmx_data = pytmx.util_pygame.load_pygame(tmx_file)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, (width, height))
        self.map_layer.zoom = zoom_level

    def get_map_layer(self):
        return self.map_layer