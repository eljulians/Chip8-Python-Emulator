class Screen:

    _WIDTH = 128
    _HEIGHT = 64

    def __init__(self):
        self._init_frame_buffer_to_0()

    def _init_frame_buffer_to_0(self):
        self._frame_buffer = [[0] * self._WIDTH for i in range(self._HEIGHT)]

    def _set_bit_row_to_frame_buffer(self, bit_row_string, x, y):
        for bit_column_string in bit_row_string:
            bit_column_int = int(bit_column_string)
            self._frame_buffer[x][y] ^= bit_column_int
            y += 1

    def _update_frame_buffer(self, sprite, x, y):
        for pixel_int_row in sprite:
            bit_row_string = '{:08b}'.format(pixel_int_row)
            self._set_bit_row_to_frame_buffer(bit_row_string, x, y)
            x += 1
