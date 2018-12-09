import unittest
from chip8_emulator.screen import Screen


class ScreenTest(unittest.TestCase):

    def _init_screen(self, frame_buffer):
        screen = Screen()
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

    def test_update_frame_buffer(self):
        init_sprite = [0x18, 0x3C, 0x7E, 0x7E, 0x3C, 0x18, 0x18, 0x18, 0x18]
        x0 = 10
        y0 = 20
        frame_buffer = self._init_frame_buffer_with_sprite(init_sprite, x0, y0)
        screen = self._init_screen(frame_buffer)

        input_sprite = [0x66, 0x42, 0x00, 0x00, 0x42, 0x66, 0x66, 0x66, 0x66]
        screen._update_frame_buffer(input_sprite, x0, y0)

        expected_sprite = [0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E]
        expected_frame_buffer = self._init_frame_buffer_with_sprite(
            expected_sprite, x0, y0
        )
        actual_frame_buffer = screen._frame_buffer

        self.assertEqual(expected_frame_buffer, actual_frame_buffer)
