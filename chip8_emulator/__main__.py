from chip8 import Chip8
from screen import Screen

if __name__ == '__main__':
    screen = Screen()
    chip8 = Chip8(screen)
    chip8.main()
