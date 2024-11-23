import copy

from src.board import Board
from src.player import Player
from src.tile import Tile

TILE_NUM_MAX = 13
TILE_COLOR_MAX = 4
TILE_BULK_MAX = 2


class Solver:
    _board: Board
    _player: Player

    _tiles: [[Tile | None]] = [[None for x in range(TILE_NUM_MAX)] for y in range(TILE_COLOR_MAX * TILE_BULK_MAX)]
    _solution = []

    def __init__(self, board: Board, player: Player):
        self._board = board
        self._player = player

    def _clear_tiles(self):
        for col in range(TILE_COLOR_MAX * TILE_BULK_MAX):
            for num in range(TILE_NUM_MAX):
                self._tiles[col][num] = None
        self._solution = []

    def _is_usuable(self, tile: (Tile | None)):
        return tile is not None and not tile.used

    def _find_next_avail_tile(self, color: int, number: int) -> [int, int]:
        for num in range(number, TILE_NUM_MAX + 1):
            tile = self._get_a_tile(color, num)
            if self._is_usuable(tile):
                return [color, num]
        for col in range(color + 1, TILE_COLOR_MAX * TILE_BULK_MAX):
            for num in range(1, TILE_NUM_MAX + 1):
                tile = self._get_a_tile(col, num)
                if self._is_usuable(tile):
                    return [col, num]
        return [-1, -1]

    def _fill_tiles(self, tiles: list[Tile], must: bool):
        offset = 0
        for tile in tiles:
            if self._get_a_tile(tile.color.value, tile.number) is not None:
                offset = TILE_COLOR_MAX
            tile.used = False
            tile.must = must
            self._set_a_tile(tile.color.value + offset, tile.number, tile)

    def _mark_unused(self, tiles: list[Tile]):
        for tile in tiles:
            tile.used = False

    def _register_solution(self, solution: list):
        if len(solution) > 0:
            self._solution.append(copy.deepcopy(solution))

    def _remove_solution_to_end(self, sets: list[Tile], solution: list):
        try:
            idx = solution.index(sets)
            del solution[idx - 1:]
        except ValueError:
            print("Logical error.. it is not possible")

    def _get_a_tile(self, color: int, number: int) -> Tile | None:
        return self._tiles[color][number - 1]

    def _set_a_tile(self, color: int, number: int, tile: Tile | None):
        self._tiles[color][number - 1] = tile

    def find_optimal_solution(self):
        self._clear_tiles()
        self._fill_tiles([t for t in self._board.opened.values()], True)
        self._fill_tiles([t for t in self._player.tiles.values()], False)
        self._search_optimal(0, 1, [])

    def print_solution(self):
        if len(self._solution) == 0:
            print("\nSolution is not found!")
            return
        print('')
        for solution in self._solution:
            for group in solution:
                print('[', end='')
                for tile in group:
                    if tile is not None:
                        print(tile.to_print(), end='')
                print(' ] ', end='')
            print ('')

    def _search_optimal(self, color: int, number: int, solution: list):
        n_col, n_num = self._find_next_avail_tile(color, number)
        if n_col == -1 or n_num == -1:
            self._register_solution(solution)
            return
        self._try_numbers(n_col, n_num, solution)
        self._try_colors(n_col, n_num, solution)
        tile: Tile = self._get_a_tile(n_col, n_num)
        if tile is not None and not tile.must:
            self._search_optimal(n_col, n_num + 1, solution)

    def _add_dict(self, sets: list[Tile], tile: Tile | None) -> bool:
        if not self._is_usuable(tile) or sets[tile.color.value] is not None:
            return False
        sets[tile.color.value] = tile
        tile.used = True
        return True

    def unset_tile(self, sets: list[Tile | None], tile: Tile | None):
        if tile is None:
            return
        sets[tile.color.value] = None
        tile.used = False

    def _try_colors(self, color: int, number: int, solution: list):
        tile = self._get_a_tile(color, number)
        sets: list[Tile | None] = [None] * 4
        self._add_dict(sets, tile)
        for col2 in range(color + 1, TILE_COLOR_MAX * TILE_BULK_MAX):
            tile2 = self._get_a_tile(col2, number)
            if not self._add_dict(sets, tile2):
                continue

            for col3 in range(col2 + 1, TILE_COLOR_MAX * TILE_BULK_MAX):
                tile3 = self._get_a_tile(col3, number)
                if not self._add_dict(sets, tile3):
                    continue
                solution.append(sets)
                self._search_optimal(color, number + 1, solution)
                solution.remove(sets)

                for col4 in range(col3 + 1, TILE_COLOR_MAX * TILE_BULK_MAX):
                    tile4 = self._get_a_tile(col4, number)
                    if not self._add_dict(sets, tile4):
                        continue
                    solution.append(sets)
                    self._search_optimal(color, number + 1, solution)
                    solution.remove(sets)
                    self.unset_tile(sets, tile4)
                    break
                self.unset_tile(sets, tile3)
            self.unset_tile(sets, tile2)
        self.unset_tile(sets, tile)

    def _try_numbers(self, color: int, number: int, solution: list):
        sets: list[Tile | None] = []
        for num in range(number, TILE_NUM_MAX + 1):
            tile = self._get_a_tile(color, num)
            if not self._is_usuable(tile):
                break
            sets.append(tile)
            tile.used = True
            if len(sets) >= 3:
                solution.append(sets)
                self._search_optimal(color, number + 1, solution)
                solution.remove(sets)
        self._mark_unused(sets)
