from Agents.Agent import Agent
from typing import Union
from Game.Game2048 import Game2048
from Game.Windowed2048 import Windowed2048
import random


class RandomAgent(Agent):
    """
    An agent that chooses its moves randomly until it loses
    """

    def __init__(self, game: Union[Game2048, Windowed2048]):
        super().__init__(game)

    def __choose_action(self):
        choice = random.choice([0, 1, 2, 3])
        if choice == 0:
            self._move_left()
        elif choice == 1:
            self._move_right()
        elif choice == 2:
            self._move_down()
        elif choice == 3:
            self._move_up()
