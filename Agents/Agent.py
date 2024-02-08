from Game.Game2048 import Game2048
from Game.Windowed2048 import Windowed2048
from typing import Union


class Agent():

    def __init__(self, game: Union[Game2048, Windowed2048]):
        self._game = game
        if isinstance(game, Game2048):
            self._windowed: bool = False
        elif isinstance(game, Windowed2048):
            self._windowed = True
        else:
            raise TypeError(f"Unsupported game type: {type(game)}")

    def _move_up(self):
        self._game.move_up()

    def _move_down(self):
        self._game.move_down()

    def _move_left(self):
        self._game.move_left()

    def _move_right(self):
        self._game.move_right()

    def play(self):
        while not self._game.has_lost():
            self.__choose_action()

    def __choose_action(self):
        pass
