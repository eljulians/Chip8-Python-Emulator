import pygame

class PygameKeyboard:

    def __init__(self):
        self.waiting_for_key = False
        self.pressed_key = None

    def listen(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.pressed_key = event.unicode
                self.waiting_for_key = False
            elif event.type == pygame.KEYUP:
                self.pressed_key = None

    def wait_for_key(self):
        waiting = True

        while waiting:
            event = pygame.event.wait()

            if event.type == pygame.KEYDOWN:
                waiting = False
                key = event.unicode

        return key
