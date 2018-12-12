import sys
import os

sys.path.insert(0, os.getcwd())

from chip8_emulator.chip8 import Chip8
from chip8_emulator.screen import Screen


def main():
    screen = Screen()
    chip8 = Chip8(screen)
    chip8.main(sys.argv[1])


if __name__ == '__main__':
    main()
