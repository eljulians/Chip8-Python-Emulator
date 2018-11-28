import unittest
from chip8_emulator.chip8 import Chip8


class Chip8Test(unittest.TestCase):

    def _init_chip8(self, program_counter=0x200, stack_pointer=0xEA0, stack=[]):
        chip8 = Chip8()
        chip8.program_counter = program_counter
        chip8.stack_pointer = stack_pointer
        chip8.stack = stack

        return chip8

    def test_ret(self):
        program_counter = 0x317
        stack_pointer = 0xEA2
        stack = [0x201, 0x204, 0x25F]

        chip8 = self._init_chip8(program_counter, stack_pointer, stack)
        chip8.ret()

        expected_program_counter = 0x25F
        actual_program_counter = chip8.program_counter
        expected_stack_pointer = 0xEA1
        actual_stack_pointer = chip8.stack_pointer

        self.assertEqual(expected_program_counter, actual_program_counter)
        self.assertEqual(expected_stack_pointer, actual_stack_pointer)

    def test_jump(self):
        self.fail('Not yet implemented')

    def test_call(self):
        self.fail('Not yet implemented')

    def test_skip_next_instruction_if_equals(self):
        self.fail('Not yet implemented')

    def test_skip_next_instructions_if_not_equals(self):
        self.fail('Not yet implemented')

    def test_set_v_fixed_value(self):
        self.fail('Not yet implemented')

    def test_add_to_v(self):
        self.fail('Not yet implemented')

    def test_set_vx_to_vy(self):
        self.fail('Not yet implemented')

    def test_vx_or_vy(self):
        self.fail('Not yet implemented')

    def test_vx_and_vy(self):
        self.fail('Not yet implemented')

    def test_vx_xor_vy(self):
        self.fail('Not yet implemented')
