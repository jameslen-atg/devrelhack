class UniformGrid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = width // cell_size
        self.rows = height // cell_size
        self.grid = [[[] for _ in range(self.cols)] for _ in range(self.rows)]

    def _get_cell_indices(self, x, y):
        col = int(x // self.cell_size)
        row = int(y // self.cell_size)
        return col, row

    def add_tile(self, tile):
        col, row = self._get_cell_indices(tile.get_x(), tile.get_y())
        self.grid[row][col].append(tile)

    def get_nearby_tiles(self, x, y):
        col, row = self._get_cell_indices(x, y)
        nearby_tiles = []
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                nearby_tiles.extend(self.grid[i][j])
        return nearby_tiles