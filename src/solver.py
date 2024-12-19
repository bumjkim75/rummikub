import copy

from src.board import Board
from src.player import Player
from src.tile import Tile

TILE_NUM_MAX = 13
TILE_COLOR_MAX = 4
TILE_BULK_MAX = 2


class TileHolder:
    _tiles: [[Tile | None]] = [[None for x in range(TILE_NUM_MAX)] for y in range(TILE_COLOR_MAX * TILE_BULK_MAX)]

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
        for tile in tiles:
            offset = 0
            for depth in range(TILE_BULK_MAX):
                if self._get_a_tile(tile.color.value + offset, tile.number) is not None:
                    offset += TILE_COLOR_MAX
            if offset >= TILE_COLOR_MAX * TILE_BULK_MAX:
                raise ValueError(f"There are {tile.to_print()} tile more than {TILE_BULK_MAX}")
            tile.used = False
            tile.must = must
            self._set_a_tile(tile.color.value + offset, tile.number, tile)

    def _mark_unused(self, tiles: list[Tile]):
        for tile in tiles:
            if tile is not None:
                tile.used = False

    def _register_solution(self, solution: list):
        if len(solution) > 0:
            self._solution.append(copy.deepcopy(solution))

    def _get_a_tile(self, color: int, number: int) -> Tile | None:
        return self._tiles[color][number - 1]

    def _set_a_tile(self, color: int, number: int, tile: Tile | None):
        self._tiles[color][number - 1] = tile


class Solver(TileHolder):
    _board: Board
    _player: Player

    _solution = []

    def __init__(self, board: Board, player: Player):
        self._board = board
        self._player = player

    def find_optimal_solution(self):
        self._clear_tiles()
        self._fill_tiles([t for t in self._board.opened], True)
        self._fill_tiles([t for t in self._player.tiles], False)
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
                        if not tile.must:
                            print('*', end='')
                print(' ] ', end='')
            print('')

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

    def _set_tile(self, sets: list[Tile], tile: Tile | None) -> bool:
        if not self._is_usuable(tile) or sets[tile.color.value] is not None:
            return False
        sets[tile.color.value] = tile
        tile.used = True
        return True

    def _unset_tile(self, sets: list[Tile | None], tile: Tile | None):
        if tile is None:
            return
        sets[tile.color.value] = None
        tile.used = False

    def _try_colors(self, color: int, number: int, solution: list, use_users=False):
        tile = self._get_a_tile(color, number)
        sets: list[Tile | None] = [None] * 4
        self._set_tile(sets, tile)
        count = 1
        try_again_for_user_tile = False
        for col in reversed(range(color + 1, TILE_COLOR_MAX * TILE_BULK_MAX)):
            candidate_tile = self._get_a_tile(col, number)
            if not self._set_tile(sets, candidate_tile):
                continue
            if use_users is False and candidate_tile.must is False:
                self._unset_tile(sets, candidate_tile)
                try_again_for_user_tile = True
                continue
            count = sum(tile is not None for tile in sets)
            if count >= 4:
                break
        if count < 3:
            self._mark_unused(sets)
            return
        if count == 3:
            solution.append(sets)
            self._search_optimal(color, number + 1, solution)
            solution.remove(sets)
            self._mark_unused(sets)
            return
        for try_possible in range(4):
            save_tile = None
            if try_possible != color:
                save_tile = sets[try_possible]
                self._unset_tile(sets, save_tile)
            solution.append(sets)
            self._search_optimal(color, number + 1, solution)
            solution.remove(sets)
            if save_tile is not None:
                self._set_tile(sets, save_tile)
        self._mark_unused(sets)
        if try_again_for_user_tile:
            self._try_colors(color, number, solution, True)

    def _try_numbers(self, color: int, number: int, solution: list, use_users=False):
        sets: list[Tile | None] = []
        try_again_for_user_tile = False
        for num in range(number, TILE_NUM_MAX + 1):
            tile = self._get_a_tile(color, num)
            if not self._is_usuable(tile):
                break
            if tile.must is False and use_users is False:
                try_again_for_user_tile = True
                break
            sets.append(tile)
            tile.used = True
            if len(sets) >= 3:
                if self._check_already_has_split_solution(sets, solution):
                    break
                solution.append(sets)
                self._search_optimal(color, number + 1, solution)
                solution.remove(sets)
        self._mark_unused(sets)
        if try_again_for_user_tile:
            self._try_numbers(color, number, solution, True)

    # [123] [456] are same [123456] and need to remove these
    def _check_already_has_split_solution(self, sets: list[Tile | None], solution: list[list[Tile]]):
        if len(solution) == 0:
            return
        last_tile_from_solution: Tile = (solution[-1])[-1]
        if last_tile_from_solution is None:
            return False
        first_tile_of_new_set = sets[0]
        if last_tile_from_solution.color == first_tile_of_new_set.color and \
                last_tile_from_solution.number+1 == first_tile_of_new_set.number:
            return True
        return False




