from src.tile import Tile


class Board:
    opened: list[Tile] = []

    def clear(self):
        self.opened = []

    def addTile(self, tile: Tile):
        self.opened.append(tile)
        tile.must = True
