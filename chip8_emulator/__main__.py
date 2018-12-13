import sys
import os

sys.path.insert(0, os.getcwd())

from chip8_emulator.chip8 import Chip8
from chip8_emulator.pygame_screen import PygameScreen
from chip8_emulator.pygame_keyboard import PygameKeyboard


def main():
    screen = PygameScreen()
    keyboard = PygameKeyboard()
    chip8 = Chip8(screen, keyboard)
    chip8.main(sys.argv[1])


if __name__ == '__main__':
    main()
