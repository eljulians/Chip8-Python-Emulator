import unittest
from chip8_emulator.screen import Screen


class ScreenTest(unittest.TestCase):

    def _init_screen(self, frame_buffer=None):
        screen = Screen()
        if frame_buffer is not None:
            screen._frame_buffer = frame_buffer

        return screen

    def _init_frame_buffer_with_sprite(self, sprite, x, y):
        frame_buffer = [[0] * 128 for i in range(64)]
        x_index = x

        for pixel_int_row in sprite:
            y_index = y
            pixel_row_bits_string = '{:08b}'.format(pixel_int_row)

            for row_bit_string in pixel_row_bits_string:
                row_bit_int = int(row_bit_string)
                frame_buffer[x_index][y_index] = row_bit_int
                y_index += 1

            x_index += 1

        return frame_buffer

    def test_draw(self):
        """
        Draw "CHIP8" in screen (each sprite 8x6, space between chars 2 pixels)
        """
        sprites = [
            [0xFF, 0xC0, 0xC0, 0xC0, 0xC0, 0xFF],  # C
            [0xC3, 0xC3, 0xFF, 0xFF, 0xC3, 0xC3],  # H
            [0x18, 0x18, 0x18, 0x18, 0x18, 0x18],  # I
            [0xFF, 0xC3, 0xC3, 0xFF, 0xC0, 0xC0],  # P
            [0xFF, 0xC3, 0xFF, 0xFF, 0xC3, 0xFF],  # 8
        ]
        x = 10
        y = 5

        screen = self._init_screen()

        for sprite in sprites:
            screen.draw_sprite(sprite, x, y)
            x += 10

        input()
