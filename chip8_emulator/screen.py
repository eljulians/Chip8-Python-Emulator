from threading import Thread
import pygame


class Screen(Thread):

    _SCALATION_FACTOR = 1
    _WIDTH = 64 * _SCALATION_FACTOR
    _HEIGHT = 32 * _SCALATION_FACTOR
    _SCREEN_COLOR_RGB = (0, 0, 0)
    _PIXEL_COLOR_RGB = (255, 255, 255)

    def __init__(self):
        Thread.__init__(self)
        self._init_screen_buffer_to_0()
        self.screen = None

    def init_screen(self):
        self.screen = pygame.display.set_mode((self._WIDTH, self._HEIGHT))

    def _clear_screen(self):
        self.screen.fill(self._SCREEN_COLOR_RGB)
        pygame.display.flip()

    def _init_screen_buffer_to_0(self):
        self._screen_buffer = [[0] * self._WIDTH for i in range(self._HEIGHT)]

    def _draw_pixel(self, x, y):
        pygame.draw.line(self.screen, self._PIXEL_COLOR_RGB, (x, y), (x, y))

    def _refresh_segment(self, segment, initial_x, initial_y):
        segment_row_y_axis = 0
        current_y = initial_y

        for segment_row in segment:
            current_x = initial_x
            segment_column_x_axis = 0
            for segment_column in segment_row:
                if segment[segment_row_y_axis][segment_column_x_axis]:
                    self._draw_pixel(current_x, current_y)
                current_x += 1
                segment_column_x_axis += 1
            segment_row_y_axis += 1
            current_y += 1

        pygame.display.flip()

    def _get_segment_bit_matrix_to_draw(self, row_index_begin,
                                        column_index_begin, sprite_width,
                                        sprite_height):
        segment = []

        row_index_end = row_index_begin + sprite_height
        column_index_end = column_index_begin + sprite_width

        for buffer_row in self._screen_buffer[row_index_begin:row_index_end]:
            segment.append(buffer_row[column_index_begin:column_index_end])

        return segment

    def _set_bit_row_to_screen_buffer(self, bit_row_string, buffer_row_y_axis,
                                     buffer_column_x_axis):
        for bit_column_string in bit_row_string:
            bit_column_int = int(bit_column_string)
            if buffer_row_y_axis >= self._HEIGHT:
                buffer_row_y_axis = buffer_row_y_axis - self._HEIGHT
            if buffer_column_x_axis >= self._WIDTH:
                buffer_column_x_axis = buffer_column_x_axis - self._WIDTH
            self._screen_buffer[buffer_row_y_axis][buffer_column_x_axis] ^= bit_column_int
            buffer_column_x_axis += 1

    def _update_screen_buffer(self, sprite, buffer_row_y_axis,
                             buffer_column_x_axis):
        for pixel_int_row in sprite:
            row_size_bits = 8 * self._SCALATION_FACTOR
            bit_row_formatter = '{:0' + str(row_size_bits) + 'b}'
            bit_row_string = bit_row_formatter.format(pixel_int_row)
            self._set_bit_row_to_screen_buffer(bit_row_string,
                                              buffer_row_y_axis,
                                              buffer_column_x_axis)
            buffer_row_y_axis += 1

    def _scale_sprite(self, sprite):
        scaled_sprite = []

        for sprite_row in sprite:
            scaled_sprite_row_bit_string = ''
            original_sprite_bit_string = '{:08b}'.format(sprite_row)
            for sprite_bit in original_sprite_bit_string:
                for _ in range(self._SCALATION_FACTOR):
                    scaled_sprite_row_bit_string += sprite_bit

            scaled_sprite_row_int = int(scaled_sprite_row_bit_string, 2)
            for _ in range(self._SCALATION_FACTOR):
                scaled_sprite.append(scaled_sprite_row_int)

        return scaled_sprite

    def draw_sprite(self, sprite, buffer_column_x_axis, buffer_row_y_axis):
        scalated_sprite = self._scale_sprite(sprite)
        buffer_column_x_axis *= self._SCALATION_FACTOR
        buffer_row_y_axis *= self._SCALATION_FACTOR
        self._update_screen_buffer(scalated_sprite, buffer_row_y_axis,
                                   buffer_column_x_axis)

        sprite_width = 8 * self._SCALATION_FACTOR
        sprite_height = len(scalated_sprite)

        segment_to_draw = self._get_segment_bit_matrix_to_draw(
            buffer_row_y_axis, buffer_column_x_axis, sprite_width,
            sprite_height
        )

        self._refresh_segment(segment_to_draw, buffer_column_x_axis,
                              buffer_row_y_axis)

    def run(self):
        print('Thread started')
