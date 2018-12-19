import unittest
from unittest import mock
from chip8_emulator.screen_proxy import ScreenProxy


class ScreenProxyTest(unittest.TestCase):

    def _init_screen(self, screen_buffer=None, scalation_factor=1):
        screen_implementation_mock = mock.Mock()
        screen = ScreenProxy(screen_implementation_mock)
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

    def test_wrap_row_if_overflow__overflow(self):
        screen = self._init_screen()
        row_overflow = 23
        row = screen._HEIGHT + row_overflow

        expected_row = row - screen._HEIGHT
        actual_row = screen._wrap_row_if_overflow(row)

        self.assertEqual(expected_row, actual_row)

    def test_wrap_column_if_overflow__overflow(self):
        screen = self._init_screen()
        column_overflow = 17
        column = screen._WIDTH + column_overflow

        expected_column = column - screen._WIDTH
        actual_column = screen._wrap_column_if_overflow(column)

        self.assertEqual(expected_column, actual_column)

    def test_set_collision__collision(self):
        screen = self._init_screen()
        pixel_before = 1
        pixel_after = 0

        screen._set_collision(pixel_before, pixel_after)

        actual_collision = screen.collision

        self.assertTrue(actual_collision)

    def test_set_collision__no_collision(self):
        screen = self._init_screen()
        pixel_before = 0
        pixel_after = 0

        screen._set_collision(pixel_before, pixel_after)

        actual_collision = screen.collision

        self.assertFalse(actual_collision)
