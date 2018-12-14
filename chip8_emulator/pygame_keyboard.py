import pygame

class PygameKeyboard:

    def __init__(self):
        self.pressed_key = None

    def listen(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.pressed_key = event.unicode
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
                key = event.unicode

        return key
