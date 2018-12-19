import unittest
import pygame
from unittest import mock
from chip8_emulator.pygame_keyboard import PygameKeyboard


class EventMock:

    def __init__(self, event_type, key_unicode):
        self.type = event_type
        self.unicode = key_unicode


class PygameKeyboardTest(unittest.TestCase):

    def setUp(self):
        self.keyboard = PygameKeyboard()

    @mock.patch('pygame.event.get')
    def test_listen__event_keydown(self, mocked_pygame_event_get):
        mocked_pressed_key = 'q'
        mocked_event = EventMock(pygame.KEYDOWN, mocked_pressed_key)
        mocked_return = [mocked_event]
        mocked_pygame_event_get.return_value = mocked_return

        self.keyboard.listen()

        expected_pressed_key = self.keyboard.KEY_MAPPINGS[mocked_pressed_key]
        actual_pressed_key = self.keyboard.get_pressed_key()

        self.assertEqual(expected_pressed_key, actual_pressed_key)

    @mock.patch('pygame.event.get')
    def test_listen__event_keyup(self, mocked_pygame_event_get):
        mocked_pressed_key = 'q'
        mocked_event = EventMock(pygame.KEYUP, mocked_pressed_key)
        mocked_return = [mocked_event]
        mocked_pygame_event_get.return_value = mocked_return

        self.keyboard.listen()

        expected_pressed_key = None
        actual_pressed_key = self.keyboard.get_pressed_key()

        self.assertEqual(expected_pressed_key, actual_pressed_key)

    @mock.patch('pygame.event.get')
    def test_listen__other(self, mocked_pygame_event_get):
        mocked_pressed_key = '3'
        mocked_event = EventMock(pygame.MOUSEBUTTONUP, mocked_pressed_key)
        mocked_return = [mocked_event]
        mocked_pygame_event_get.return_value = mocked_return

        self.keyboard.listen()

        expected_pressed_key = None
        actual_pressed_key = self.keyboard.get_pressed_key()

        self.assertEqual(expected_pressed_key, actual_pressed_key)

    @mock.patch('pygame.event.wait')
    def test_wait_for_key(self, mocked_pygame_event_wait):
        mocked_pressed_key = 'a'
        mocked_return = EventMock(pygame.KEYDOWN, mocked_pressed_key)
        mocked_pygame_event_wait.return_value = mocked_return

        expected_pressed_key = self.keyboard.KEY_MAPPINGS[mocked_pressed_key]
        actual_pressed_key = self.keyboard.wait_for_key()

        self.assertEqual(expected_pressed_key, actual_pressed_key)
