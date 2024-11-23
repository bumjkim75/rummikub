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
        ),
        ([
            Tile(Color.ORANGE, 5), Tile(Color.ORANGE, 6), Tile(Color.ORANGE, 7),
            Tile(Color.ORANGE, 8), Tile(Color.ORANGE, 9), Tile(Color.ORANGE, 10),
            Tile(Color.ORANGE, 11), Tile(Color.ORANGE, 12), Tile(Color.ORANGE, 13),
            Tile(Color.RED, 4), Tile(Color.BLUE, 4), Tile(Color.BLACK, 4),
            Tile(Color.RED, 5), Tile(Color.BLUE, 5), Tile(Color.BLACK, 5)

         ],[
            Tile(Color.RED, 2),Tile(Color.RED, 5),Tile(Color.BLACK, 12)
        ], '[[[{"color": 0, "number": 4}, null, {"color": 2, "number": 4}, {"color": 3, "number": 4}], '
            '[{"color": 0, "number": 5}, {"color": 1, "number": 5}, {"color": 2, "number": 5}, '
            '{"color": 3, "number": 5}], [{"color": 1, "number": 6}, {"color": 1, "number": 7}, '
            '{"color": 1, "number": 8}], [{"color": 1, "number": 9}, {"color": 1, "number": 10}, {"color": 1, '
           '"number": 11}, {"color": 1, "number": 12}, {"color": 1, "number": 13}]], [[{"color": 0, "number": 4}, '
           'null, {"color": 2, "number": 4}, {"color": 3, "number": 4}], [{"color": 0, "number": 5}, {"color": 1, '
           '"number": 5}, {"color": 2, "number": 5}, {"color": 3, "number": 5}], [{"color": 1, "number": 6}, '
           '{"color": 1, "number": 7}, {"color": 1, "number": 8}, {"color": 1, "number": 9}], [{"color": 1, '
           '"number": 10}, {"color": 1, "number": 11}, {"color": 1, "number": 12}, {"color": 1, "number": 13}]], '
           '[[{"color": 0, "number": 4}, null, {"color": 2, "number": 4}, {"color": 3, "number": 4}], [{"color": 0, '
           '"number": 5}, {"color": 1, "number": 5}, {"color": 2, "number": 5}, {"color": 3, "number": 5}], '
           '[{"color": 1, "number": 6}, {"color": 1, "number": 7}, {"color": 1, "number": 8}, {"color": 1, '
           '"number": 9}, {"color": 1, "number": 10}], [{"color": 1, "number": 11}, {"color": 1, "number": 12}, '
           '{"color": 1, "number": 13}]], [[{"color": 0, "number": 4}, null, {"color": 2, "number": 4}, {"color": 3, '
           '"number": 4}], [{"color": 0, "number": 5}, {"color": 1, "number": 5}, {"color": 2, "number": 5}, '
           '{"color": 3, "number": 5}], [{"color": 1, "number": 6}, {"color": 1, "number": 7}, {"color": 1, '
           '"number": 8}, {"color": 1, "number": 9}, {"color": 1, "number": 10}, {"color": 1, "number": 11}, '
           '{"color": 1, "number": 12}, {"color": 1, "number": 13}]], [[{"color": 0, "number": 4}, null, {"color": 2, '
           '"number": 4}, {"color": 3, "number": 4}], [{"color": 0, "number": 5}, null, {"color": 2, "number": 5}, '
           '{"color": 3, "number": 5}], [{"color": 1, "number": 5}, {"color": 1, "number": 6}, {"color": 1, '
           '"number": 7}], [{"color": 1, "number": 8}, {"color": 1, "number": 9}, {"color": 1, "number": 10}], '
           '[{"color": 1, "number": 11}, {"color": 1, "number": 12}, {"color": 1, "number": 13}]], [[{"color": 0, '
           '"number": 4}, null, {"color": 2, "number": 4}, {"color": 3, "number": 4}], [{"color": 0, "number": 5}, '
           'null, {"color": 2, "number": 5}, {"color": 3, "number": 5}], [{"color": 1, "number": 5}, {"color": 1, '
           '"number": 6}, {"color": 1, "number": 7}], [{"color": 1, "number": 8}, {"color": 1, "number": 9}, '
           '{"color": 1, "number": 10}, {"color": 1, "number": 11}, {"color": 1, "number": 12}, {"color": 1, '
           '"number": 13}]], [[{"color": 0, "number": 4}, null, {"color": 2, "number": 4}, {"color": 3, '
           '"number": 4}], [{"color": 0, "number": 5}, null, {"color": 2, "number": 5}, {"color": 3, "number": 5}], '
           '[{"color": 1, "number": 5}, {"color": 1, "number": 6}, {"color": 1, "number": 7}, {"color": 1, '
           '"number": 8}], [{"color": 1, "number": 9}, {"color": 1, "number": 10}, {"color": 1, "number": 11}, '
           '{"color": 1, "number": 12}, {"color": 1, "number": 13}]], [[{"color": 0, "number": 4}, null, {"color": 2, '
           '"number": 4}, {"color": 3, "number": 4}], [{"color": 0, "number": 5}, null, {"color": 2, "number": 5}, '
           '{"color": 3, "number": 5}], [{"color": 1, "number": 5}, {"color": 1, "number": 6}, {"color": 1, '
           '"number": 7}, {"color": 1, "number": 8}, {"color": 1, "number": 9}], [{"color": 1, "number": 10}, '
           '{"color": 1, "number": 11}, {"color": 1, "number": 12}, {"color": 1, "number": 13}]], [[{"color": 0, '
           '"number": 4}, null, {"color": 2, "number": 4}, {"color": 3, "number": 4}], [{"color": 0, "number": 5}, '
           'null, {"color": 2, "number": 5}, {"color": 3, "number": 5}], [{"color": 1, "number": 5}, {"color": 1, '
           '"number": 6}, {"color": 1, "number": 7}, {"color": 1, "number": 8}, {"color": 1, "number": 9}, '
           '{"color": 1, "number": 10}], [{"color": 1, "number": 11}, {"color": 1, "number": 12}, {"color": 1, '
           '"number": 13}]], [[{"color": 0, "number": 4}, null, {"color": 2, "number": 4}, {"color": 3, '
           '"number": 4}], [{"color": 0, "number": 5}, null, {"color": 2, "number": 5}, {"color": 3, "number": 5}], '
           '[{"color": 1, "number": 5}, {"color": 1, "number": 6}, {"color": 1, "number": 7}, {"color": 1, '
           '"number": 8}, {"color": 1, "number": 9}, {"color": 1, "number": 10}, {"color": 1, "number": 11}, '
           '{"color": 1, "number": 12}, {"color": 1, "number": 13}]]]'
        ),
    ]))
def test_solver_basic(board_data, player_data, result):
    board = Board()
    board.opened = {}
    player = Player()
    player.tiles = {}
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
