import unittest
from chip8_emulator.screen import Screen


class ScreenTest(unittest.TestCase):

    def _init_screen(self, screen_buffer=None, scalation_factor=1):
        screen = Screen()
        screen._SCALATION_FACTOR = scalation_factor

        if screen_buffer is not None:
            screen._screen_buffer = screen_buffer

        return screen

    def _init_screen_buffer_with_sprite(self, sprite, x, y):
        screen_buffer = [[0] * 128 for i in range(64)]
        x_index = x

        for pixel_int_row in sprite:
            y_index = y
            pixel_row_bits_string = '{:08b}'.format(pixel_int_row)

            for row_bit_string in pixel_row_bits_string:
                row_bit_int = int(row_bit_string)
                screen_buffer[x_index][y_index] = row_bit_int
                y_index += 1

            x_index += 1

        return screen_buffer

    def test_update_screen_buffer(self):
        init_sprite = [0x18, 0x3C, 0x7E, 0x7E, 0x3C, 0x18, 0x18, 0x18, 0x18]
        x0 = 10
        y0 = 20
        screen_buffer = self._init_screen_buffer_with_sprite(init_sprite, x0, y0)
        screen = self._init_screen(screen_buffer)

        input_sprite = [0x66, 0x42, 0x00, 0x00, 0x42, 0x66, 0x66, 0x66, 0x66]
        screen._update_screen_buffer(input_sprite, x0, y0)

        expected_sprite = [0x7E, 0x7E, 0x7E,
                           0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E]
        expected_screen_buffer = self._init_screen_buffer_with_sprite(
            expected_sprite, x0, y0
        )
        actual_screen_buffer = screen._screen_buffer

        self.assertEqual(expected_screen_buffer, actual_screen_buffer)

    def test_scale_sprite_x2(self):
        screen = self._init_screen()
        screen._SCALATION_FACTOR = 2
        original_sprite = [0xFF, 0xC0, 0xC0, 0xC0, 0xC0, 0xFF]  # C

        expected_sprite = [
            0xFFFF, 0xFFFF,
            0xF000, 0xF000,
            0xF000, 0xF000,
            0xF000, 0xF000,
            0xF000, 0xF000,
            0xFFFF, 0xFFFF,
        ]
        actual_sprite = screen._scale_sprite(original_sprite)

        self.assertEqual(expected_sprite, actual_sprite)

    def test_scale_sprite_x3(self):
        screen = self._init_screen()
        screen._SCALATION_FACTOR = 3
        original_sprite = [0xFF, 0xC0, 0xC0, 0xC0, 0xC0, 0xFF]  # C

        expected_sprite = [
            0xFFFFFF, 0xFFFFFF, 0xFFFFFF,
            0xFC0000, 0xFC0000, 0xFC0000,
            0xFC0000, 0xFC0000, 0xFC0000,
            0xFC0000, 0xFC0000, 0xFC0000,
            0xFC0000, 0xFC0000, 0xFC0000,
            0xFFFFFF, 0xFFFFFF, 0xFFFFFF,
        ]
        actual_sprite = screen._scale_sprite(original_sprite)

        self.assertEqual(expected_sprite, actual_sprite)

    def test_get_sprite_bit_matrix_to_draw(self):
        original_sprite = [0xFF, 0xC0, 0xC0, 0xC0, 0xC0, 0xFF]  # C
        sprite_x = 20
        sprite_y = 10
        screen_buffer = self._init_screen_buffer_with_sprite(original_sprite,
                                                             sprite_x, sprite_y)
        screen = self._init_screen(screen_buffer)

        expected_sprite = [[0] * 8 for _ in range(6)]
        expected_sprite[0] = [1] * 8
        expected_sprite[1] = [1, 1, 0, 0, 0, 0, 0, 0]
        expected_sprite[2] = [1, 1, 0, 0, 0, 0, 0, 0]
        expected_sprite[3] = [1, 1, 0, 0, 0, 0, 0, 0]
        expected_sprite[4] = [1, 1, 0, 0, 0, 0, 0, 0]
        expected_sprite[5] = [1] * 8

        actual_sprite = screen._get_segment_bit_matrix_to_draw(sprite_x, sprite_y, 8, 6)

        self.assertEqual(expected_sprite, actual_sprite)
