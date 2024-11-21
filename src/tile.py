from enum import IntEnum

from colorama import Fore

class Color(IntEnum):
    BLACK = 0
    ORANGE = 1
    BLUE = 2
    RED = 3


tile_color = {
    Color.BLACK: Fore.WHITE,
    Color.ORANGE: Fore.YELLOW,
    Color.BLUE: Fore.LIGHTBLUE_EX,
    Color.RED: Fore.LIGHTRED_EX,
}
class Tile:

    number: int
    color: Color
    must: bool = True
    used: bool = False

    def __init__(self, color: Color, number: int):
        self.number = number
        self.color = color

    def to_print(self, debug=False)->str:
        if not debug:
            return '{}{:>3}{}'.format(tile_color[self.color], self.number, Fore.RESET)


