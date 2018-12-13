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

    def draw_pixel(self, x, y):
        pygame.draw.line(self.screen, self._PIXEL_COLOR_RGB, (x, y), (x, y))

    def clear_pixel(self, x, y):
        pygame.draw.line(self.screen, self._SCREEN_COLOR_RGB, (x, y), (x, y))

    def refresh(self):
        pygame.display.flip()
