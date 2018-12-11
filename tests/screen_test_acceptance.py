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

    def test_draw_chip8(self):
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

    def test_draw_horizontal_overflowing_line(self):
        sprite = [0xFF] * 15
        screen = self._init_screen()

        screen.draw_sprite(sprite, 30, screen._HEIGHT - 5)

        input()

    def test_draw_vertical_overflowing_line(self):
        sprites = [[0xFF] for _ in range(10)]
        screen = self._init_screen()

        x = screen._WIDTH - 10

        for sprite in sprites:
            screen.draw_sprite(sprite, x, 30)
            x += 8

        input()

    def test_draw_diagonal_overflowing_line(self):
        sprites = [
            # [0x01], [0x02], [0x04], [0x08], [0x10], [0x20], [0x40], [0x80]
            [0x80], [0x40], [0x20], [0x10], [0x08], [0x04], [0x02], [0x01],
        ]
        screen = self._init_screen()

        y = screen._HEIGHT - 5

        for sprite in sprites:
            screen.draw_sprite(sprite, screen._WIDTH - 4, y)
            y += 1

        input()

