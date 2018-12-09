import sys
import unittest

from .chip8_test import Chip8Test
from .opcode_parser_test import OpcodeParserTest
from .screen_test import ScreenTest


def suite():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(Chip8Test))
    suite.addTest(unittest.makeSuite(OpcodeParserTest))
    suite.addTest(unittest.makeSuite(ScreenTest))

    return suite


if __name__ == '__main__':
    suite = suite()
    runner = unittest.TextTestRunner()
    success = not runner.run(suite).wasSuccessful()

    sys.exit(success)
