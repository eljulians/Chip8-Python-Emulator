import sys
import unittest

from .chip8_test import Chip8Test
from .opcode_parser_test import OpcodeParserTest
from .screen_proxy_test import ScreenProxyTest
from .memory_test import MemoryTest
from .pygame_keyboard_test import PygameKeyboardTest


def suite():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(Chip8Test))
    suite.addTest(unittest.makeSuite(OpcodeParserTest))
    suite.addTest(unittest.makeSuite(ScreenProxyTest))
    suite.addTest(unittest.makeSuite(MemoryTest))
    suite.addTest(unittest.makeSuite(PygameKeyboardTest))

    return suite


if __name__ == '__main__':
    suite = suite()
    runner = unittest.TextTestRunner()
    success = not runner.run(suite).wasSuccessful()

    sys.exit(success)
