import pygame


class PygameScreen:

    _SCREEN_COLOR_RGB = (0, 0, 0)
    _PIXEL_COLOR_RGB = (255, 255, 255)

    def __init__(self):
        self.width = None
        self.height = None
        self.screen = None

    def init(self):
        self.screen = pygame.display.set_mode((self.width, self.height))

    def clear(self):
        self.screen.fill(self._SCREEN_COLOR_RGB)
        pygame.display.flip()

    def _draw_pixel_pygame(self, x, y, color):
        pygame.draw.line(self.screen, color, (x, y), (x, y))

    def draw_pixel(self, x, y):
        self._draw_pixel_pygame(x, y, self._PIXEL_COLOR_RGB)

    def clear_pixel(self, x, y):
        self._draw_pixel_pygame(x, y, self._SCREEN_COLOR_RGB)

    def refresh(self):
        pygame.display.flip()
