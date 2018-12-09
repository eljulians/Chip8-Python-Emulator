import unittest
from chip8_emulator import opcode_parser


class OpcodeParserTest(unittest.TestCase):

    def test_parse_operation_and_parameters__00e0(self):
        opcode = bytes([0x00, 0xE0])

        expected = ('00e0', ())
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__00ee(self):
        opcode = bytes([0x00, 0xEE])

        expected = ('00ee', ())
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__1nnn(self):
        opcode = bytes([0x1C, 0xE4])

        expected = ('1nnn', [0xCE4])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__2nnn(self):
        opcode = bytes([0x25, 0x36])

        expected = ('2nnn', [0x536])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__3xkk(self):
        opcode = bytes([0x3D, 0x78])

        expected = ('3xkk', [0xD, 0x78])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__4xkk(self):
        opcode = bytes([0x41, 0xAE])

        expected = ('4xkk', [0x1, 0xAE])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__5xy0(self):
        opcode = bytes([0x5D, 0x00])

        expected = ('5xy0', [0xD, 0x0])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__6xkk(self):
        opcode = bytes([0x6A, 0x15])

        expected = ('6xkk', [0xA, 0x15])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__7xkk(self):
        opcode = bytes([0x71, 0xF5])

        expected = ('7xkk', [0x1, 0xF5])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__8xy0(self):
        opcode = bytes([0x82, 0xC0])

        expected = ('8xy0', [0x2, 0xC])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__8xy1(self):
        opcode = bytes([0x8A, 0x51])

        expected = ('8xy1', [0xA, 0x5])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__8xy2(self):
        opcode = bytes([0x81, 0x02])

        expected = ('8xy2', [0x1, 0x0])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__8xy3(self):
        opcode = bytes([0x8B, 0xB3])

        expected = ('8xy3', [0xB, 0xB])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__8xy4(self):
        opcode = bytes([0x80, 0xC4])

        expected = ('8xy4', [0x0, 0xC])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__8xy5(self):
        opcode = bytes([0x8F, 0xB5])

        expected = ('8xy5', [0xF, 0xB])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__8xy6(self):
        opcode = bytes([0x82, 0x76])

        expected = ('8xy6', [0x2, 0x7])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__8xy7(self):
        opcode = bytes([0x8E, 0x37])

        expected = ('8xy7', [0xE, 0x3])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__8xye(self):
        opcode = bytes([0x8D, 0xCE])

        expected = ('8xye', [0xD, 0xC])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__9xy0(self):
        opcode = bytes([0x92, 0x30])

        expected = ('9xy0', [0x2, 0x3])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__annn(self):
        opcode = bytes([0xA7, 0xFE])

        expected = ('annn', [0x7FE])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__bnnn(self):
        opcode = bytes([0xB5, 0xB1])

        expected = ('bnnn', [0x5B1])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__cxkk(self):
        opcode = bytes([0xC1, 0x07])

        expected = ('cxkk', [0x1, 0x07])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__dxyn(self):
        opcode = bytes([0xDF, 0x08])

        expected = ('dxyn', [0xF, 0x0, 0x8])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__ex9e(self):
        opcode = bytes([0xE5, 0x9E])

        expected = ('ex9e', [0x5])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__exa1(self):
        opcode = bytes([0xE9, 0xA1])

        expected = ('exa1', [0x9])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__fx07(self):
        opcode = bytes([0xF4, 0x07])

        expected = ('fx07', [0x4])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__fx0a(self):
        opcode = bytes([0xFA, 0x0A])

        expected = ('fx0a', [0xA])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__fx15(self):
        opcode = bytes([0xF8, 0x15])

        expected = ('fx15', [0x8])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__fx18(self):
        opcode = bytes([0xFB, 0x18])

        expected = ('fx18', [0xB])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__fx1e(self):
        opcode = bytes([0xF3, 0x1E])

        expected = ('fx1e', [0x3])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__fx29(self):
        opcode = bytes([0xF0, 0x29])

        expected = ('fx29', [0x0])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__fx33(self):
        opcode = bytes([0xFA, 0x33])

        expected = ('fx33', [0xA])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__fx55(self):
        opcode = bytes([0xF7, 0x55])

        expected = ('fx55', [0x7])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_parse_operation_and_parameters__fx65(self):
        opcode = bytes([0xF0, 0x65])

        expected = ('fx65', [0x0])
        actual = opcode_parser.parse_operation_and_parameters(opcode)

        self.assertEqual(expected, actual)

    def test_construct_operation__00e0(self):
        opcode = bytes([0x00, 0xE0])
        constant_part = '0e'

        expected = '00e0'
        actual = opcode_parser._construct_operation(opcode, constant_part)

        self.assertEqual(expected, actual)

    def test_construct_operation__00ee(self):
        opcode = bytes([0x00, 0xEE])
        constant_part = '0e'

        expected = '00ee'
        actual = opcode_parser._construct_operation(opcode, constant_part)

        self.assertEqual(expected, actual)

    def test_construct_operation__1nnn(self):
        opcode = bytes([0x1C, 0xE4])
        constant_part = 'nn'
        last_nibble = 'n'

        expected = '1nnn'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                    last_nibble)

        self.assertEqual(expected, actual)

    def test_construct_operation__2nnn(self):
        opcode = bytes([0x25, 0x36])
        constant_part = 'nn'
        last_nibble = 'n'

        expected = '2nnn'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                    last_nibble)

        self.assertEqual(expected, actual)

    def test_construct_operation__3xkk(self):
        opcode = bytes([0x3D, 0x78])
        constant_part = 'xk'
        last_nibble = 'k'

        expected = '3xkk'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                    last_nibble)

        self.assertEqual(expected, actual)

    def test_construct_operation__4xkk(self):
        opcode = bytes([0x41, 0xAE])

        constant_part = 'xk'
        last_nibble = 'k'

        expected = '4xkk'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                    last_nibble)

        self.assertEqual(expected, actual)

    def test_construct_operation__5xy0(self):
        opcode = bytes([0x5D, 0x00])
        constant_part = 'xy'
        last_nibble = '0'

        expected = '5xy0'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                    last_nibble)

        self.assertEqual(expected, actual)

    def test_construct_operation__6xkk(self):
        opcode = bytes([0x6A, 0x15])
        constant_part = 'xk'
        last_nibble = 'k'

        expected = '6xkk'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                    last_nibble)

        self.assertEqual(expected, actual)

    def test_construct_operation__7xkk(self):
        opcode = bytes([0x71, 0xF5])
        constant_part = 'xk'
        last_nibble = 'k'

        expected = '7xkk'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                    last_nibble)

        self.assertEqual(expected, actual)

    def test_construct_operation__8xy0(self):
        opcode = bytes([0x82, 0xC0])
        constant_part = 'xy'
        last_nibble = '0'

        expected = '8xy0'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                    last_nibble)

        self.assertEqual(expected, actual)

    def test_construct_operation__8xy1(self):
        opcode = bytes([0x8A, 0x51])
        constant_part = 'xy'

        expected = '8xy1'
        actual = opcode_parser._construct_operation(opcode, constant_part)

        self.assertEqual(expected, actual)

    def test_construct_operation__8xy2(self):
        opcode = bytes([0x81, 0x02])
        constant_part = 'xy'

        expected = '8xy2'
        actual = opcode_parser._construct_operation(opcode, constant_part)

        self.assertEqual(expected, actual)

    def test_construct_operation__8xy3(self):
        opcode = bytes([0x8B, 0xB3])
        constant_part = 'xy'

        expected = '8xy3'
        actual = opcode_parser._construct_operation(opcode, constant_part)

        self.assertEqual(expected, actual)

    def test_construct_operation__8xy4(self):
        opcode = bytes([0x80, 0xC4])
        constant_part = 'xy'

        expected = '8xy4'
        actual = opcode_parser._construct_operation(opcode, constant_part)

        self.assertEqual(expected, actual)

    def test_construct_operation__8xy5(self):
        opcode = bytes([0x8F, 0xB5])
        constant_part = 'xy'

        expected = '8xy5'
        actual = opcode_parser._construct_operation(opcode, constant_part)

        self.assertEqual(expected, actual)

    def test_construct_operation__8xy6(self):
        opcode = bytes([0x82, 0x76])
        constant_part = 'xy'

        expected = '8xy6'
        actual = opcode_parser._construct_operation(opcode, constant_part)

        self.assertEqual(expected, actual)

    def test_construct_operation__8xy7(self):
        opcode = bytes([0x8E, 0x37])
        constant_part = 'xy'

        expected = '8xy7'
        actual = opcode_parser._construct_operation(opcode, constant_part)

        self.assertEqual(expected, actual)

    def test_construct_operation__8xye(self):
        opcode = bytes([0x8D, 0xCE])
        constant_part = 'xy'

        expected = '8xye'
        actual = opcode_parser._construct_operation(opcode, constant_part)

        self.assertEqual(expected, actual)

    def test_construct_operation__9xy0(self):
        opcode = bytes([0x92, 0x30])
        constant_part = 'xy'

        expected = '9xy0'
        actual = opcode_parser._construct_operation(opcode, constant_part)

        self.assertEqual(expected, actual)

    def test_construct_operation__annn(self):
        opcode = bytes([0xA7, 0xFE])
        constant_part = 'nn'
        last_nibble = 'n'

        expected = 'annn'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                   last_nibble)

        self.assertEqual(expected, actual)

    def test_construct_operation__bnnn(self):
        opcode = bytes([0xB5, 0xB1])
        constant_part = 'nn'
        last_nibble = 'n'

        expected = 'bnnn'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                   last_nibble)

        self.assertEqual(expected, actual)

    def test_construct_operation__cxkk(self):
        opcode = bytes([0xC1, 0x07])
        constant_part = 'xk'
        last_nibble = 'k'

        expected = 'cxkk'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                    last_nibble)

        self.assertEqual(expected, actual)

    def test_construct_operation__dxyn(self):
        opcode = bytes([0xDF, 0x08])
        constant_part = 'xy'
        last_nibble = 'n'

        expected = 'dxyn'
        actual = opcode_parser._construct_operation(opcode, constant_part,
                                                    last_nibble)

        self.assertEqual(expected, actual)

    def test_get_byte_first_nibble_int(self):
        byte = 0xFD

        expected = 0xF
        actual = opcode_parser._get_byte_first_nibble_int(byte)

        self.assertEqual(expected, actual)

    def test_get_byte_last_nibble_int(self):
        byte = 0xFD

        expected = 0xD
        actual = opcode_parser._get_byte_last_nibble_int(byte)

        self.assertEqual(expected, actual)

    def test_get_byte_first_nibble_hex(self):
        byte = 0xFD

        expected = 'f'
        actual = opcode_parser._get_byte_first_nibble_hex(byte)

        self.assertEqual(expected, actual)

    def test_get_byte_last_nibble_hex(self):
        byte = 0xFD

        expected = 'd'
        actual = opcode_parser._get_byte_last_nibble_hex(byte)

        self.assertEqual(expected, actual)
