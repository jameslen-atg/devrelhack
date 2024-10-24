import pyscroll
import pytmx
from CollidableTile import CollidableTile

class MapLoader:
    def __init__(self, tmx_file, width, height, zoom_level=0.5):
        self.tmx_data = pytmx.util_pygame.load_pygame(tmx_file)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, (width, height))
        self.map_layer.zoom = zoom_level

    def get_map_layer(self):
        return self.map_layer

    def get_collidable_tiles(self):
        collidable_tiles = []
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_properties_by_gid(gid)
                    if tile and ('CollideShip' in tile or 'CollideProjectile' in tile):
                        collidable_tile = CollidableTile(x, y, tile)
                        collidable_tiles.append(collidable_tile)
        for tile in collidable_tiles:
            print(f"Collidable Tile - X: {tile.get_x()}, Y: {tile.get_y()}, Properties: {tile.get_tile()}")
        return collidable_tiles