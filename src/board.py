from src.tile import Tile


class Board:
    opened : dict[int, Tile] = {}

    def hasTile(self, tile: Tile) -> bool:
        key = self._get_key(tile)
        return key in self.opened

    def _get_key(self, tile: Tile) -> int:
        return tile.color.value * 100 + tile.number

    def addTile(self, tile: Tile):
        self.opened[self._get_key(tile)] = tile