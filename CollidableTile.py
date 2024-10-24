import pyscroll
import pytmx

class CollidableTile:
    def __init__(self, x, y, tile):
        self.x = x
        self.y = y
        self.is_collidable_projectile = 'CollideShip' in tile
        self.is_collidable_ship = 'CollideProjectile' in tile
        self.tile = tile

    def is_collidable_ship(self):
        return self.is_collidable_ship

    def is_collidable_projectile(self):
        return self.is_collidable_projectile

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_tile(self):
        return self.tile