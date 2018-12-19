import sys
import os

sys.path.insert(0, os.getcwd())

from chip8_emulator.chip8 import Chip8
from chip8_emulator.pygame_screen import PygameScreen
from chip8_emulator.pygame_keyboard import PygameKeyboard
from chip8_emulator.delay_timer_thread import DelayTimerThread


def main():
    screen = PygameScreen()
    keyboard = PygameKeyboard()
    chip8 = Chip8(screen, keyboard)
    delay_timer_thread = DelayTimerThread(chip8.memory)
    delay_timer_thread.start()
    chip8.main(sys.argv[1])


if __name__ == '__main__':
    main()
