
class ScreenProxy:

    _SPRITE_WIDTH_BITS = 8
    _SCALATION_FACTOR = 8
    _WIDTH = 64 * _SCALATION_FACTOR
    _HEIGHT = 32 * _SCALATION_FACTOR

    def __init__(self, screen):
        self.screen = screen
        self.screen.width = self._WIDTH
        self.screen.height = self._HEIGHT
        self._init_screen_buffer_to_0()

    def init_screen(self):
        self.screen.init()

    def clear_screen(self):
        self._init_screen_buffer_to_0()
        self.screen.clear()

    def _init_screen_buffer_to_0(self):
        self._screen_buffer = [[0] * self._WIDTH for _ in range(self._HEIGHT)]

    def _refresh_segment(self, segment, initial_x, initial_y):
        segment_row_index = 0
        current_y = initial_y

        for segment_row in segment:
            current_x = initial_x
            segment_column_index = 0
            for _ in segment_row:
                if segment[segment_row_index][segment_column_index]:
                    self.screen.draw_pixel(current_x, current_y)
                else:
                    self.screen.clear_pixel(current_x, current_y)
                current_x += 1
                segment_column_index += 1
            segment_row_index += 1
            current_y += 1

        self.screen.refresh()

    def _get_segment_bit_matrix_to_draw(self, row_index_begin,
                                        column_index_begin, sprite_width,
                                        sprite_height):
        segment = []

        row_index_end = row_index_begin + sprite_height
        column_index_end = column_index_begin + sprite_width

        for buffer_row in self._screen_buffer[row_index_begin:row_index_end]:
            segment.append(buffer_row[column_index_begin:column_index_end])

        return segment

    def _wrap_row_if_overflow(self, row):
        if row >= self._HEIGHT:
            row = row - self._HEIGHT

        return row

    def _wrap_column_if_overflow(self, column):
        if column >= self._WIDTH:
            column = column - self._WIDTH

        return column

    def _set_bit_row_to_screen_buffer(self, sprite_row_bitstring, buffer_row,
                                      buffer_column):
        for sprite_column_bitchar in sprite_row_bitstring:
            sprite_column_bit_int = int(sprite_column_bitchar)
            buffer_row = self._wrap_row_if_overflow(buffer_row)
            buffer_column = self._wrap_column_if_overflow(buffer_column)
            self._screen_buffer[buffer_row][buffer_column] ^= sprite_column_bit_int
            buffer_column += 1

    def _update_screen_buffer(self, sprite, buffer_row, buffer_column):
        for sprite_row_int in sprite:
            row_length_bits = self._SPRITE_WIDTH_BITS * self._SCALATION_FACTOR
            bit_row_formatter = '{:0' + str(row_length_bits) + 'b}'
            sprite_row_bitstring = bit_row_formatter.format(sprite_row_int)
            self._set_bit_row_to_screen_buffer(sprite_row_bitstring,
                                               buffer_row, buffer_column)
            buffer_row += 1

    def _scale_sprite_row(self, sprite_row):
        scaled_sprite_row_bitstring = ''
        original_sprite_row_bitstring = '{:08b}'.format(sprite_row)

        for sprite_bit in original_sprite_row_bitstring:
            for _ in range(self._SCALATION_FACTOR):
                scaled_sprite_row_bitstring += sprite_bit

        return scaled_sprite_row_bitstring

    def _scale_sprite(self, sprite):
        scaled_sprite = []

        for sprite_row in sprite:
            scaled_sprite_row_bitstring = self._scale_sprite_row(sprite_row)
            scaled_sprite_row_int = int(scaled_sprite_row_bitstring, 2)

            for _ in range(self._SCALATION_FACTOR):
                scaled_sprite.append(scaled_sprite_row_int)

        return scaled_sprite

    def draw_sprite(self, sprite, buffer_column, buffer_row):
        scaled_sprite = self._scale_sprite(sprite)
        buffer_column *= self._SCALATION_FACTOR
        buffer_row *= self._SCALATION_FACTOR
        self._update_screen_buffer(scaled_sprite, buffer_row, buffer_column)

        sprite_width = 8 * self._SCALATION_FACTOR
        sprite_height = len(scaled_sprite)

        segment_to_draw = self._get_segment_bit_matrix_to_draw(
            buffer_row, buffer_column, sprite_width, sprite_height
        )

        self._refresh_segment(segment_to_draw, buffer_column, buffer_row)
