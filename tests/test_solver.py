import json
import pytest

from src.board import Board
from src.player import Player
from src.solver import Solver
from src.tile import Color, Tile


def custom_encoder(obj):
    if isinstance(obj, Tile):
        # Return a dictionary representation of the object
        return {"color": obj.color.value, "number": obj.number}
    # Let json handle other types
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

@pytest.mark.parametrize("board_data, player_data, result", ([
        ([
            Tile(Color.RED, 1), Tile(Color.RED, 2), Tile(Color.RED, 3),
            Tile(Color.RED, 4), Tile(Color.BLUE, 4), Tile(Color.BLACK, 4)
         ],[
            Tile(Color.RED, 2)
        ], '[[[{"color": 0, "number": 4}, null, {"color": 2, "number": 4}, {"color": 3, "number": 4}], [{"color": 3, '
           '"number": 1}, {"color": 3, "number": 2}, {"color": 3, "number": 3}]]]'
        ),
        ([
            Tile(Color.RED, 1), Tile(Color.RED, 2), Tile(Color.RED, 3),
            Tile(Color.RED, 4), Tile(Color.BLUE, 4), Tile(Color.BLACK, 4),
            Tile(Color.ORANGE, 5), Tile(Color.BLUE, 5), Tile(Color.BLACK, 5)

         ],[
            Tile(Color.RED, 2),Tile(Color.RED, 5),
        ],
            '[[[{"color": 0, "number": 4}, null, {"color": 2, "number": 4}, {"color": 3, "number": 4}], '
            '[{"color": 0, "number": 5}, {"color": 1, "number": 5}, {"color": 2, "number": 5}, null], '
            '[{"color": 3, "number": 1}, {"color": 3, "number": 2}, {"color": 3, "number": 3}]], '
            '[[{"color": 0, "number": 4}, null, {"color": 2, "number": 4}, {"color": 3, "number": 4}], '
            '[{"color": 0, "number": 5}, {"color": 1, "number": 5}, {"color": 2, "number": 5}, '
            '{"color": 3, "number": 5}], [{"color": 3, "number": 1}, {"color": 3, "number": 2}, '
            '{"color": 3, "number": 3}]]]'
        ),([
            Tile(Color.RED, 1), Tile(Color.RED, 2), Tile(Color.RED, 3),
            Tile(Color.RED, 4),
            Tile(Color.RED, 4), Tile(Color.BLACK, 4), Tile(Color.BLUE, 4),
            Tile(Color.ORANGE, 13), Tile(Color.BLACK, 13), Tile(Color.BLUE, 13),
            Tile(Color.BLACK, 10), Tile(Color.BLACK, 11), Tile(Color.BLACK, 12),
         ],[
            Tile(Color.RED, 2)
        ], '[[[{"color": 0, "number": 4}, null, {"color": 2, "number": 4}, {"color": 3, "number": 4}], '
            '[{"color": 0, "number": 10}, {"color": 0, "number": 11}, {"color": 0, "number": 12}], '
            '[{"color": 0, "number": 13}, {"color": 1, "number": 13}, {"color": 2, "number": 13}, null], '
            '[{"color": 3, "number": 1}, {"color": 3, "number": 2}, {"color": 3, "number": 3}, '
            '{"color": 3, "number": 4}]]]'
        ),
    ]))
def test_solver_basic(board_data, player_data, result):
    board = Board()
    board.clear()
    player = Player()
    player.clear()
    for tile in board_data:
        board.addTile(tile)
    for tile in player_data:
        player.addTile(tile)

    solver = Solver(board, player)
    solver.find_optimal_solution()
    solver.print_solution()
    res = json.dumps(solver._solution, default=custom_encoder)
    print (res)
    assert res == result



@pytest.mark.parametrize("board_data, player_data, result", ([
        ([
            Tile(Color.RED, 3), Tile(Color.ORANGE, 3), Tile(Color.BLUE, 3),
            Tile(Color.BLACK, 3), Tile(Color.RED, 3), Tile(Color.ORANGE, 3),
            Tile(Color.BLUE, 3), Tile(Color.BLACK, 3)
         ],[
        ], ''
        ),
    ]))
def  test_solver_verticals(board_data, player_data, result):
    board = Board()
    board.clear()
    player = Player()
    player.clear()
    for tile in board_data:
        board.addTile(tile)
    for tile in player_data:
        player.addTile(tile)

    solver = Solver(board, player)
    solver.find_optimal_solution()
    solver.print_solution()
    res = json.dumps(solver._solution, default=custom_encoder)
    print (res)
    if result != '':
        assert res == result

@pytest.mark.parametrize("board_data, player_data, result", ([
        ([
            Tile(Color.RED, 4), Tile(Color.RED, 5), Tile(Color.RED, 6),
            Tile(Color.RED, 4), Tile(Color.RED, 5), Tile(Color.RED, 6),
            Tile(Color.RED, 1), Tile(Color.BLUE, 1), Tile(Color.BLACK, 1),
            Tile(Color.ORANGE, 10), Tile(Color.ORANGE, 11), Tile(Color.ORANGE, 12),
            Tile(Color.ORANGE, 13),
            Tile(Color.BLUE, 9), Tile(Color.BLACK, 9), Tile(Color.ORANGE, 9),
            Tile(Color.RED, 9),
            Tile(Color.BLUE, 3), Tile(Color.BLUE, 4), Tile(Color.BLUE, 5),
            Tile(Color.BLUE, 6), Tile(Color.BLUE, 7), Tile(Color.BLUE, 8),

        ], [
            Tile(Color.RED, 1), Tile(Color.BLACK, 2), Tile(Color.BLACK, 3),
            Tile(Color.BLACK, 4), Tile(Color.BLACK, 13), Tile(Color.ORANGE, 8),
            Tile(Color.BLACK, 3), Tile(Color.RED, 7), Tile(Color.ORANGE, 7),
            Tile(Color.BLUE, 8)
        ],''
        )
    ]))
def test_solver_complex(board_data, player_data, result):
    board = Board()
    board.clear()
    player = Player()
    player.clear()
    for tile in board_data:
        board.addTile(tile)
    for tile in player_data:
        player.addTile(tile)

    solver = Solver(board, player)
    solver.find_optimal_solution()
    solver.print_solution()
    res = json.dumps(solver._solution, default=custom_encoder)
    print (res)
    if result != '':
        assert res == result


@pytest.mark.parametrize("board_data, player_data, result", ([
        ([
            Tile(Color.BLUE, 1), Tile(Color.BLUE, 2), Tile(Color.BLUE, 3),
            Tile(Color.RED, 1), Tile(Color.BLUE, 1), Tile(Color.ORANGE,1),
            Tile(Color.BLACK, 1),
            Tile(Color.RED, 9), Tile(Color.BLACK, 9), Tile(Color.ORANGE, 9),
            Tile(Color.ORANGE, 10), Tile(Color.ORANGE, 11), Tile(Color.ORANGE, 12),
            Tile(Color.RED, 9), Tile(Color.RED, 10), Tile(Color.RED, 11),
            Tile(Color.RED, 12), Tile(Color.RED, 13),
            Tile(Color.RED, 12), Tile(Color.BLUE, 12), Tile(Color.BLACK, 12),
            Tile(Color.BLUE, 4), Tile(Color.BLUE, 5), Tile(Color.BLUE, 6),
            Tile(Color.ORANGE, 7), Tile(Color.ORANGE, 8), Tile(Color.ORANGE, 9),
            Tile(Color.RED, 5), Tile(Color.BLUE, 5), Tile(Color.ORANGE, 5),
            Tile(Color.BLACK, 5),
            Tile(Color.BLUE, 11), Tile(Color.ORANGE, 11), Tile(Color.BLACK, 11),
            Tile(Color.BLUE, 8), Tile(Color.BLUE, 9), Tile(Color.BLUE, 10),
            Tile(Color.BLUE, 11), Tile(Color.BLUE, 12), Tile(Color.BLUE, 13),
            Tile(Color.RED, 13), Tile(Color.BLUE, 13), Tile(Color.ORANGE, 13),
            Tile(Color.BLACK, 13),
            Tile(Color.ORANGE, 4), Tile(Color.BLUE, 4), Tile(Color.BLACK, 4),
            Tile(Color.RED, 7), Tile(Color.BLACK, 7), Tile(Color.ORANGE, 7),
         ],[
            Tile(Color.ORANGE, 2), Tile(Color.ORANGE, 3), Tile(Color.ORANGE, 8),
            Tile(Color.ORANGE, 10), Tile(Color.BLACK, 3), Tile(Color.BLACK, 6),
            Tile(Color.BLACK, 10), Tile(Color.BLACK, 13), Tile(Color.RED, 1),
            Tile(Color.RED, 2), Tile(Color.RED, 3), Tile(Color.RED, 6),
            Tile(Color.BLUE, 9),
        ]
        , ''
        ),
    ]))
def test_solver_complex_real_cases(board_data, player_data, result):
    board = Board()
    board.clear()
    player = Player()
    player.clear()
    for tile in board_data:
        board.addTile(tile)
    for tile in player_data:
        player.addTile(tile)

    solver = Solver(board, player)
    solver.find_optimal_solution()
    solver.print_solution()
    res = json.dumps(solver._solution, default=custom_encoder)
    print (res)
    if result != '':
        assert res == result

@pytest.mark.parametrize("board_data, player_data, result", ([
        ([
            Tile(Color.BLUE, 1), Tile(Color.BLUE, 2), Tile(Color.BLUE, 3),
            Tile(Color.BLUE, 1), Tile(Color.BLUE, 2), Tile(Color.BLUE, 3),
            Tile(Color.BLACK, 3), Tile(Color.RED, 3), Tile(Color.ORANGE, 3),
            Tile(Color.BLACK, 3), Tile(Color.RED, 3), Tile(Color.ORANGE, 3),
            Tile(Color.BLACK, 13), Tile(Color.RED, 13), Tile(Color.ORANGE, 13),
            Tile(Color.BLUE, 13),
            Tile(Color.BLACK, 13), Tile(Color.RED, 13), Tile(Color.ORANGE, 13),
            Tile(Color.BLUE, 13)
         ],[

        ]
        , ''
        ),
    ]))
def test_solver_exceptional(board_data, player_data, result):
    board = Board()
    board.clear()
    player = Player()
    player.clear()
    for tile in board_data:
        board.addTile(tile)
    for tile in player_data:
        player.addTile(tile)

    solver = Solver(board, player)
    solver.find_optimal_solution()
    solver.print_solution()
    res = json.dumps(solver._solution, default=custom_encoder)
    print (res)
    if result != '':
        assert res == result



