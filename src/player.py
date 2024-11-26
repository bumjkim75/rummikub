from src.tile import Tile


class Player:
    tiles: list[Tile] = []

    def clear(self):
        self.tiles = []

    def addTile(self, tile: Tile):
        self.tiles.append(tile)
        tile.must = False
