import pygame


class PygameKeyboard:

    KEY_MAPPINGS = {
        '1': 0x1, '2': 0x2, '3': 0x3, '4': 0xC,
        'q': 0x4, 'w': 0x5, 'e': 0x6, 'r': 0xD,
        'a': 0x7, 's': 0x8, 'd': 0x9, 'f': 0xE,
        'z': 0xA, 'x': 0x0, 'c': 0xB, 'v': 0xF,
    }

    def __init__(self):
        self.pressed_key = None

    def listen(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.pressed_key = self.KEY_MAPPINGS.get(event.unicode)
            elif event.type == pygame.KEYUP:
                self.pressed_key = None

    def get_pressed_key(self):
        return self.pressed_key

    def wait_for_key(self):
        waiting = True

        while waiting:
            event = pygame.event.wait()

            if event.type == pygame.KEYDOWN:
                waiting = False

        return self.KEY_MAPPINGS.get(event.unicode)
