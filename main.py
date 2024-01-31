from Game2048 import Game2048
import numpy as np
from pynput import keyboard

game = Game2048()

game.set_board(np.array([[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [4, 4, 8, 2]]))


def on_press(key):
    if key == keyboard.Key.up:
        game.move_up()
    if key == keyboard.Key.down:
        game.move_down()
    if key == keyboard.Key.left:
        game.move_left()
    if key == keyboard.Key.right:
        game.move_right()
    print(game)


def on_release(key):
    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
print(game)
