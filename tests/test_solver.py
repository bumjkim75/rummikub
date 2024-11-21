import pytest

from src.board import Board
from src.player import Player
from src.solver import Solver
from src.tile import Color, Tile


@pytest.mark.parametrize("board_data, player_data, result", ([
        ([
            Tile(Color.RED, 1), Tile(Color.RED, 2), Tile(Color.RED, 3),
            Tile(Color.RED, 4), Tile(Color.BLUE, 4), Tile(Color.BLACK, 4)
         ],[
            Tile(Color.RED, 2)
        ], [
            Tile(Color.RED, 1)
        ]),
    ]))
def test_solver_basic(board_data, player_data, result):
    board = Board()
    player = Player()
    for tile in board_data:
        board.addTile(tile)
    for tile in player_data:
        player.addTile(tile)

    solver = Solver(board, player)
    solver.find_optimal_solution()
    solver.print_solution()