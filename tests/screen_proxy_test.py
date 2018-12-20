import unittest
from unittest.mock import Mock, call, patch
from chip8_emulator.screen_proxy import ScreenProxy


class ScreenProxyTest(unittest.TestCase):

    def _init_screen_proxy(self, screen_buffer=None, scalation_factor=1):
        screen_implementation_mock = Mock()
        screen_proxy = ScreenProxy(screen_implementation_mock)
        screen_proxy._SCALATION_FACTOR = scalation_factor

        if screen_buffer is not None:
            screen_proxy._screen_buffer = screen_buffer

        screen_proxy.init_screen()

        return screen_proxy

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
        screen_buffer = self._init_screen_buffer_with_sprite(
            init_sprite, x0, y0)
        screen_proxy = self._init_screen_proxy(screen_buffer)

        input_sprite = [0x66, 0x42, 0x00, 0x00, 0x42, 0x66, 0x66, 0x66, 0x66]
        screen_proxy._update_screen_buffer(input_sprite, x0, y0)

        expected_sprite = [0x7E, 0x7E, 0x7E,
                           0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E]
        expected_screen_buffer = self._init_screen_buffer_with_sprite(
            expected_sprite, x0, y0
        )
        actual_screen_buffer = screen_proxy._screen_buffer

        self.assertEqual(expected_screen_buffer, actual_screen_buffer)

    def test_scale_sprite_x2(self):
        screen_proxy = self._init_screen_proxy()
        screen_proxy._SCALATION_FACTOR = 2
        original_sprite = [0xFF, 0xC0, 0xC0, 0xC0, 0xC0, 0xFF]  # C

        expected_sprite = [
            0xFFFF, 0xFFFF,
            0xF000, 0xF000,
            0xF000, 0xF000,
            0xF000, 0xF000,
            0xF000, 0xF000,
            0xFFFF, 0xFFFF,
        ]
        actual_sprite = screen_proxy._scale_sprite(original_sprite)

        self.assertEqual(expected_sprite, actual_sprite)

    def test_scale_sprite_x3(self):
        screen_proxy = self._init_screen_proxy()
        screen_proxy._SCALATION_FACTOR = 3
        original_sprite = [0xFF, 0xC0, 0xC0, 0xC0, 0xC0, 0xFF]  # C

        expected_sprite = [
            0xFFFFFF, 0xFFFFFF, 0xFFFFFF,
            0xFC0000, 0xFC0000, 0xFC0000,
            0xFC0000, 0xFC0000, 0xFC0000,
            0xFC0000, 0xFC0000, 0xFC0000,
            0xFC0000, 0xFC0000, 0xFC0000,
            0xFFFFFF, 0xFFFFFF, 0xFFFFFF,
        ]
        actual_sprite = screen_proxy._scale_sprite(original_sprite)

        self.assertEqual(expected_sprite, actual_sprite)

    def test_get_sprite_bit_matrix_to_draw(self):
        original_sprite = [0xFF, 0xC0, 0xC0, 0xC0, 0xC0, 0xFF]  # C
        sprite_x = 20
        sprite_y = 10
        screen_buffer = self._init_screen_buffer_with_sprite(original_sprite,
                                                             sprite_x, sprite_y)
        screen_proxy = self._init_screen_proxy(screen_buffer)

        expected_sprite = [[0] * 8 for _ in range(6)]
        expected_sprite[0] = [1] * 8
        expected_sprite[1] = [1, 1, 0, 0, 0, 0, 0, 0]
        expected_sprite[2] = [1, 1, 0, 0, 0, 0, 0, 0]
        expected_sprite[3] = [1, 1, 0, 0, 0, 0, 0, 0]
        expected_sprite[4] = [1, 1, 0, 0, 0, 0, 0, 0]
        expected_sprite[5] = [1] * 8

        actual_sprite = screen_proxy._get_segment_bit_matrix_to_draw(
            sprite_x, sprite_y, 8, 6)

        self.assertEqual(expected_sprite, actual_sprite)

    def test_wrap_row_if_overflow__overflow(self):
        screen_proxy = self._init_screen_proxy()
        row_overflow = 23
        row = screen_proxy._HEIGHT + row_overflow

        expected_row = row - screen_proxy._HEIGHT
        actual_row = screen_proxy._wrap_row_if_overflow(row)

        self.assertEqual(expected_row, actual_row)

    def test_wrap_column_if_overflow__overflow(self):
        screen_proxy = self._init_screen_proxy()
        column_overflow = 17
        column = screen_proxy._WIDTH + column_overflow

        expected_column = column - screen_proxy._WIDTH
        actual_column = screen_proxy._wrap_column_if_overflow(column)

        self.assertEqual(expected_column, actual_column)

    def test_set_collision__collision(self):
        screen_proxy = self._init_screen_proxy()
        pixel_before = 1
        pixel_after = 0

        screen_proxy._set_collision(pixel_before, pixel_after)

        actual_collision = screen_proxy.collision

        self.assertTrue(actual_collision)

    def test_set_collision__no_collision(self):
        screen_proxy = self._init_screen_proxy()
        pixel_before = 0
        pixel_after = 0

        screen_proxy._set_collision(pixel_before, pixel_after)

        actual_collision = screen_proxy.collision

        self.assertFalse(actual_collision)

    def test_refresh_segment(self):
        initial_x = 10
        initial_y = 5
        screen_segment = [[0] * 8 for _ in range(5)]
        screen_segment[1] = [1, 0, 1, 0, 1, 0, 1, 0]
        screen_segment[4] = [1, 1, 1, 1, 0, 0, 0, 0]
        screen_proxy = self._init_screen_proxy()

        screen_proxy._refresh_segment(screen_segment, initial_x, initial_y)

        expected_draw_pixel_calls = [
            call(10, 6), call(12, 6), call(14, 6), call(16, 6),
            call(10, 9), call(11, 9), call(12, 9), call(13, 9),
        ]
        expected_clear_pixel_calls = [
            call(10, 5), call(11, 5), call(12, 5), call(13, 5), call(
                14, 5), call(15, 5), call(16, 5), call(17, 5),
            call(11, 6), call(13, 6), call(15, 6), call(17, 6),
            call(10, 7), call(11, 7), call(12, 7), call(13, 7), call(
                14, 7), call(15, 7), call(16, 7), call(17, 7),
            call(10, 8), call(11, 8), call(12, 8), call(13, 8), call(
                14, 8), call(15, 8), call(16, 8), call(17, 8),
            call(14, 9), call(15, 9), call(16, 9), call(17, 9),
        ]
        screen_proxy.screen.draw_pixel.assert_has_calls(
            expected_draw_pixel_calls
        )
        screen_proxy.screen.clear_pixel.assert_has_calls(
            expected_clear_pixel_calls
        )
        screen_proxy.screen.refresh.assert_called()

    @patch('chip8_emulator.screen_proxy.ScreenProxy._update_screen_buffer')
    @patch('chip8_emulator.screen_proxy.ScreenProxy._get_segment_bit_matrix_to_draw')
    @patch('chip8_emulator.screen_proxy.ScreenProxy._refresh_segment')
    def test_draw_sprite(self, mocked_refresh_segment,
                         mocked_get_segment_bit_matrix_to_draw,
                         mocked_update_screen_buffer):
        scalation_factor = 2
        sprite = [0xFF, 0x00, 0xFF]
        scaled_sprite = [0xFFFF, 0xFFFF, 0x0000, 0x0000, 0xFFFF, 0xFFFF]
        x = 10
        y = 5
        scaled_x = x * scalation_factor
        scaled_y = y * scalation_factor
        screen_proxy = self._init_screen_proxy(
            scalation_factor=scalation_factor
        )

        mocked_get_segment_bit_matrix_to_draw.return_value = 'mocked_matrix'

        screen_proxy.draw_sprite(sprite, x, y)

        mocked_update_screen_buffer.assert_called_with(
            scaled_sprite, scaled_y, scaled_x
        )
        mocked_get_segment_bit_matrix_to_draw.assert_called_with(
            scaled_y, scaled_x, 16, len(scaled_sprite)
        )
        mocked_refresh_segment.assert_called_with(
            'mocked_matrix', scaled_x, scaled_y
        )

    def test_clear_screen(self):
        screen_proxy = self._init_screen_proxy()

        screen_proxy.clear_screen()

        screen_proxy.screen.clear.assert_called()
