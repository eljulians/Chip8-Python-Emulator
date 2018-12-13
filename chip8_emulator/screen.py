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
        self._init_frame_buffer_to_0()
        self.screen = None

    def init_screen(self):
        self.screen = pygame.display.set_mode((self._WIDTH, self._HEIGHT))

    def _clear_screen(self):
        self.screen.fill(self._SCREEN_COLOR_RGB)
        pygame.display.flip()

    def _init_frame_buffer_to_0(self):
        self._frame_buffer = [[0] * self._WIDTH for i in range(self._HEIGHT)]

    def _set_bit_row_to_frame_buffer(self, bit_row_string, buffer_row_y_axis,
                                     buffer_column_x_axis):
        xored_sprite_row = []
        for bit_column_string in bit_row_string:
            bit_column_int = int(bit_column_string)
            if buffer_row_y_axis >= self._HEIGHT:
                buffer_row_y_axis = buffer_row_y_axis - self._HEIGHT
            if buffer_column_x_axis >= self._WIDTH:
                buffer_column_x_axis = buffer_column_x_axis - self._WIDTH
            self._frame_buffer[buffer_row_y_axis][buffer_column_x_axis] ^= bit_column_int
            xored_sprite_row.append(self._frame_buffer[buffer_row_y_axis][buffer_column_x_axis])
            buffer_column_x_axis += 1

        return xored_sprite_row

    def _update_frame_buffer(self, sprite, buffer_row_y_axis,
                             buffer_column_x_axis):
        xored_sprite = []
        for pixel_int_row in sprite:
            row_size_bits = 8 * self._SCALATION_FACTOR
            bit_row_formatter = '{:0' + str(row_size_bits) + 'b}'
            bit_row_string = bit_row_formatter.format(pixel_int_row)
            xored_sprite_row =self._set_bit_row_to_frame_buffer(bit_row_string,
                                                 buffer_row_y_axis,
                                                 buffer_column_x_axis)
            xored_sprite.append(xored_sprite_row)
            buffer_row_y_axis += 1

        return xored_sprite

    def _draw_pixel(self, x, y):
        pygame.draw.line(self.screen, self._PIXEL_COLOR_RGB, (x, y), (x, y))

    def _refresh(self):
        buffer_row_y_axis = 0
        for row in self._frame_buffer:
            buffer_column_x_axis = 0
            for column in row:
                if self._frame_buffer[buffer_row_y_axis][buffer_column_x_axis]:
                    self._draw_pixel(buffer_column_x_axis, buffer_row_y_axis)
                buffer_column_x_axis += 1
            buffer_row_y_axis += 1

        pygame.display.flip()

    def _refresh_with_sprite(self, xored_sprite, initial_x, initial_y):
        sprite_row_y_axis = 0
        current_y = initial_y
        for sprite_row in xored_sprite:
            current_x = initial_x
            sprite_column_x_axis = 0
            for sprite_column in sprite_row:
                if xored_sprite[sprite_row_y_axis][sprite_column_x_axis]:
                    self._draw_pixel(current_x, current_y)
                current_x += 1
                sprite_column_x_axis += 1
            sprite_row_y_axis += 1
            current_y += 1

        pygame.display.flip()

    def draw_sprite(self, sprite, buffer_column_x_axis, buffer_row_y_axis):
        # self._clear_screen()
        scalated_sprite = self._scale_sprite(sprite)
        buffer_column_x_axis *= self._SCALATION_FACTOR
        buffer_row_y_axis *= self._SCALATION_FACTOR
        refresh_with = self._update_frame_buffer(scalated_sprite, buffer_row_y_axis,
                                  buffer_column_x_axis)
        # self._refresh()
        self._refresh_with_sprite(refresh_with, buffer_column_x_axis,
                                  buffer_row_y_axis)

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

    def run(self):
        print('Thread started')
