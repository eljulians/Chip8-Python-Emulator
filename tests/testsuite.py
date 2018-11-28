import sys
import unittest

from .chip8_test import Chip8Test


def suite():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(Chip8Test))

    return suite


if __name__ == '__main__':
    suite = suite()
    runner = unittest.TextTestRunner()
    success = not runner.run(suite).wasSuccessful()

    sys.exit(success)
