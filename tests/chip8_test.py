import unittest
from unittest import mock
from chip8_emulator.chip8 import Chip8


class Chip8Test(unittest.TestCase):

    def _init_chip8(self, program_counter=0x200, stack_pointer=0xEA0, stack=[],
                    v_registers=[], i_register=None, memory=[None] * 4096):
        chip8 = Chip8()
        chip8.program_counter = program_counter
        chip8.stack_pointer = stack_pointer
        chip8.stack = stack
        chip8.v_registers = v_registers
        chip8.i_register = i_register
        chip8.memory = memory

        return chip8

    def test_00e0(self):
        self.fail('Not yet tested')

    def test_00ee(self):
        program_counter = 0x317
        stack_pointer = 0xEA2
        stack = [0x201, 0x204, 0x25F]

        chip8 = self._init_chip8(program_counter, stack_pointer, stack)
        chip8._00ee()

        expected_program_counter = 0x25F
        actual_program_counter = chip8.program_counter
        expected_stack_pointer = 0xEA1
        actual_stack_pointer = chip8.stack_pointer

        self.assertEqual(expected_program_counter, actual_program_counter)
        self.assertEqual(expected_stack_pointer, actual_stack_pointer)

    def test_1nnn(self):
        jump_to = 0x47F

        chip8 = self._init_chip8()
        chip8._1nnn(jump_to)

        expected = jump_to
        actual = chip8.program_counter

        self.assertEqual(expected, actual)

    def test_2nnn(self):
        program_counter = 0x617
        stack_pointer = 0xEA3
        stack = [0x351, 0x215, 0x812, 0x4FA]
        call_subroutine_at = 0xBA4

        chip8 = self._init_chip8(program_counter, stack_pointer, stack)
        chip8._2nnn(call_subroutine_at)

        expected_program_counter = call_subroutine_at
        actual_program_counter = chip8.program_counter
        expected_stack_pointer = 0xEA4
        actual_stack_pointer = chip8.stack_pointer
        expected_stack = [0x351, 0x215, 0x812, 0x4FA, 0x617]
        actual_stack = chip8.stack

        self.assertEqual(expected_program_counter, actual_program_counter)
        self.assertEqual(expected_stack_pointer, actual_stack_pointer)
        self.assertEqual(expected_stack, actual_stack)

    def test_3xkk__equals(self):
        program_counter = 0x31A
        v_registers = [None] * 16
        vx_index = 0x5
        v_registers[vx_index] = 0xAE
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        value_to_compare = 0xAE
        chip8._3xkk(vx_index, value_to_compare)

        expected_program_counter = 0x31E
        actual_program_counter = chip8.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_3xkk__not_equals(self):
        program_counter = 0x31A
        v_registers = [None] * 16
        vx_index = 0x5
        v_registers[vx_index] = 0xAE
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        value_to_compare = 0xAF
        chip8._3xkk(vx_index, value_to_compare)

        expected_program_counter = 0x31C
        actual_program_counter = chip8.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_4xkk__not_equals(self):
        program_counter = 0xBAE
        v_registers = [None] * 16
        vx_index = 0x2
        v_registers[vx_index] = 0x14
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        value_to_compare = 0xAE
        chip8._4xkk(vx_index, value_to_compare)

        expected_program_counter = 0xBB2
        actual_program_counter = chip8.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_4xkk__equals(self):
        program_counter = 0xBAE
        v_registers = [None] * 16
        vx_index = 0x2
        v_registers[vx_index] = 0x14
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        value_to_compare = 0x14
        chip8._4xkk(vx_index, value_to_compare)

        expected_program_counter = 0xBB0
        actual_program_counter = chip8.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_5xy0__equals(self):
        program_counter = 0x4FE
        v_registers = [None] * 16
        vx_index = 0x5
        vy_index = 0x6
        v_registers[vx_index] = 0x14
        v_registers[vy_index] = 0x14
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        chip8._5xy0(vx_index, vy_index)

        expected_program_counter = 0x502
        actual_program_counter = chip8.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_5xy0__not_equals(self):
        program_counter = 0x4FE
        v_registers = [None] * 16
        vx_index = 0x5
        vy_index = 0x6
        v_registers[vx_index] = 0x14
        v_registers[vy_index] = 0x10
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        chip8._5xy0(vx_index, vy_index)

        expected_program_counter = 0x500
        actual_program_counter = chip8.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_6xkk(self):
        v_registers = [None] * 16
        vx_index = 0xA
        value = 0xEA
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._6xkk(vx_index, value)

        expected_vx = value
        actual_vx = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx, actual_vx)

    def test_7xkk(self):
        vx_index = 0x5
        v_registers = [None] * 16
        v_registers[vx_index] = 0x38
        value_to_add = 0xAF
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._7xkk(vx_index, value_to_add)

        expected_vx_value = 0xE7
        actual_vx_value = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_8xy0(self):
        vx_index = 0x2
        vy_index = 0x4
        v_registers = [None] * 16
        v_registers[vx_index] = 0xAE
        v_registers[vy_index] = 0x13
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy0(vx_index, vy_index)

        expected_vx_value = 0x13
        actual_vx_value = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_8xy1(self):
        vx_index = 0x2
        vy_index = 0x4
        v_registers = [None] * 16
        v_registers[vx_index] = 0xDE
        v_registers[vy_index] = 0x81
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy1(vx_index, vy_index)

        expected_vx_value = 0xDF
        actual_vx_value = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_8xy2(self):
        vx_index = 0x3
        vy_index = 0xF
        v_registers = [None] * 16
        v_registers[vx_index] = 0xA8
        v_registers[vy_index] = 0x37
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy2(vx_index, vy_index)

        expected_vx_value = 0x20
        actual_vx_value = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_8xy3(self):
        vx_index = 0x4
        vy_index = 0x5
        v_registers = [None] * 16
        v_registers[vx_index] = 0x23
        v_registers[vy_index] = 0x61
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy3(vx_index, vy_index)

        expected_vx_value = 0x42
        actual_vx_value = chip8.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_8xy4__lower_than_255(self):
        vx_index = 0x1
        vy_index = 0x6
        v_registers = [None] * 16
        v_registers[vx_index] = 0x32
        v_registers[vy_index] = 0xAE
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy4(vx_index, vy_index)

        expected_vx_value = 0xE0
        actual_vx_value = chip8.v_registers[vx_index]

        expected_vf_value = 0x00
        actual_vf_value = chip8.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xy4__greater_than_255(self):
        vx_index = 0x1
        vy_index = 0x6
        v_registers = [None] * 16
        v_registers[vx_index] = 0xFB
        v_registers[vy_index] = 0xC4
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy4(vx_index, vy_index)

        expected_vx_value = 0xBF  # Only the lowest 8 bits of the result are kept
        actual_vx_value = chip8.v_registers[vx_index]

        expected_vf_value = 0x01
        actual_vf_value = chip8.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xy5__vx_greater_than_vy(self):
        vx_index = 0x1
        vy_index = 0x2
        v_registers = [None] * 16
        v_registers[vx_index] = 0x15
        v_registers[vy_index] = 0x04
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy5(vx_index, vy_index)

        expected_vx_value = 0x11
        actual_vx_value = chip8.v_registers[vx_index]

        expected_vf_value = 0x01
        actual_vf_value = chip8.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xy5__vx_lower_than_vy(self):
        vx_index = 0x1
        vy_index = 0x2
        v_registers = [None] * 16
        v_registers[vx_index] = 0x04
        v_registers[vy_index] = 0x15
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy5(vx_index, vy_index)

        expected_vx_value = 0x11
        actual_vx_value = chip8.v_registers[vx_index]

        expected_vf_value = 0x00
        actual_vf_value = chip8.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xy6__least_significant_bit_0(self):
        vx_index = 0x1
        v_registers = [None] * 16
        v_registers[vx_index] = 0x5A
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy6(vx_index)

        expected_vx_value = 0x2D
        actual_vx_value = chip8.v_registers[vx_index]

        expected_vf_value = 0x00
        actual_vf_value = chip8.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xy6__least_significant_bit_1(self):
        vx_index = 0x1
        v_registers = [None] * 16
        v_registers[vx_index] = 0xAF
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy6(vx_index)

        expected_vx_value = 0x57
        actual_vx_value = chip8.v_registers[vx_index]

        expected_vf_value = 0x01
        actual_vf_value = chip8.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xy7__vy_greater_than_vx(self):
        vx_index = 0x1
        vy_index = 0x2
        v_registers = [None] * 16
        v_registers[vx_index] = 0xE0
        v_registers[vy_index] = 0xF0
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy7(vx_index, vy_index)

        expected_vx_value = 0x10
        actual_vx_value = chip8.v_registers[vx_index]

        expected_vf_value = 0x01
        actual_vf_value = chip8.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xy7__vy_lower_than_vx(self):
        vx_index = 0x1
        vy_index = 0x2
        v_registers = [None] * 16
        v_registers[vx_index] = 0xE0
        v_registers[vy_index] = 0xC0
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy7(vx_index, vy_index)

        expected_vx_value = 0x20
        actual_vx_value = chip8.v_registers[vx_index]

        expected_vf_value = 0x00
        actual_vf_value = chip8.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xye__least_significant_bit_0(self):
        vx_index = 0x1
        v_registers = [None] * 16
        v_registers[vx_index] = 0x52
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xye(vx_index)

        expected_vx_value = 0xA4
        actual_vx_value = chip8.v_registers[vx_index]

        expected_vf_value = 0x00
        actual_vf_value = chip8.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xye__least_significant_bit_1(self):
        vx_index = 0x1
        v_registers = [None] * 16
        v_registers[vx_index] = 0x71
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xye(vx_index)

        expected_vx_value = 0xE2
        actual_vx_value = chip8.v_registers[vx_index]

        expected_vf_value = 0x01
        actual_vf_value = chip8.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_9xy0__not_equals(self):
        program_counter = 0x35F
        v_registers = [None] * 16
        vx_index = 0x5
        vy_index = 0x6
        v_registers[vx_index] = 0x14
        v_registers[vy_index] = 0x15
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        chip8._9xy0(vx_index, vy_index)

        expected_program_counter = 0x363
        actual_program_counter = chip8.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_9xy0__equals(self):
        program_counter = 0x35F
        v_registers = [None] * 16
        vx_index = 0x5
        vy_index = 0x6
        v_registers[vx_index] = 0x14
        v_registers[vy_index] = 0x14
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        chip8._9xy0(vx_index, vy_index)

        expected_program_counter = 0x361
        actual_program_counter = chip8.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_annn(self):
        chip8 = self._init_chip8()

        new_i_value = 0xA52

        chip8._annn(new_i_value)

        expected_i_register = 0xA52
        actual_i_register = chip8.i_register

        self.assertEqual(expected_i_register, actual_i_register)

    def test_bnnn(self):
        program_counter = 0x7A1
        v_registers = [None] * 16
        v_registers[0] = 0x14
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        new_address = 0x47F
        chip8._bnnn(new_address)

        expected_program_counter = 0x493
        actual_program_counter = chip8.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_cxkk(self):
        self.fail('Not yet tested')

    def test_dxyn(self):
        self.fail('Not yet tested')

    def test_ex9e(self):
        self.fail('Not yet tested')

    def test_exa1(self):
        self.fail('Not yet tested')

    def test_fx07(self):
        self.fail('Not yet tested')

    def test_fx0a(self):
        self.fail('Not yet tested')

    def test_fx15(self):
        self.fail('Not yet tested')

    def test_fx18(self):
        self.fail('Not yet tested')

    def test_fx1e(self):
        v_registers = [None] * 16
        vx_index = 0x5
        v_registers[vx_index] = 0xAE
        i_register = 0xC15
        chip8 = self._init_chip8(v_registers=v_registers,
                                 i_register=i_register)

        chip8._fx1e(vx_index)

        expected_i_register = 0xCC3
        actual_i_register = chip8.i_register

        self.assertEqual(expected_i_register, actual_i_register)

    def test_fx29(self):
        self.fail('Not yet tested')

    def test_fx33(self):
        v_registers = [None] * 16
        memory = [None] * 4096
        vx_index = 0x5
        v_registers[vx_index] = 0xAE
        i_register = 0xCE5
        chip8 = self._init_chip8(v_registers=v_registers,
                                 i_register=i_register, memory=memory)

        chip8._fx33(vx_index)

        expected_i0_memory_location_value = 1
        actual_i0_memory_location_value = chip8.memory[0xCE5]
        expected_i1_memory_location_value = 7
        actual_i1_memory_location_value = chip8.memory[0xCE6]
        expected_i2_memory_location_value = 4
        actual_i2_memory_location_value = chip8.memory[0xCE7]

        self.assertEqual(expected_i0_memory_location_value,
                         actual_i0_memory_location_value)
        self.assertEqual(expected_i1_memory_location_value,
                         actual_i1_memory_location_value)
        self.assertEqual(expected_i2_memory_location_value,
                         actual_i2_memory_location_value)

    def test_fx55(self):
        v_registers = [0x14, 0xF4, 0x61, 0xDE]
        memory = [None] * 4096
        vx_index = 0x4
        i_register = 0x7A4
        chip8 = self._init_chip8(v_registers=v_registers,
                                 i_register=i_register, memory=memory)

        chip8._fx55(vx_index)

        expected_i0_memory_location_value = 0x14
        actual_i0_memory_location_value = chip8.memory[0x7A4]
        expected_i1_memory_location_value = 0xF4
        actual_i1_memory_location_value = chip8.memory[0x7A5]
        expected_i2_memory_location_value = 0x61
        actual_i2_memory_location_value = chip8.memory[0x7A6]
        expected_i3_memory_location_value = 0xDE
        actual_i3_memory_location_value = chip8.memory[0x7A7]

        self.assertEqual(expected_i0_memory_location_value,
                         actual_i0_memory_location_value)
        self.assertEqual(expected_i1_memory_location_value,
                         actual_i1_memory_location_value)
        self.assertEqual(expected_i2_memory_location_value,
                         actual_i2_memory_location_value)
        self.assertEqual(expected_i3_memory_location_value,
                         actual_i3_memory_location_value)

    def test_fx65(self):
        v_registers = [None] * 16
        vx_index = 0x4
        i_register = 0x5DA
        memory = [None] * 4096
        memory[0x5DA] = 0x48
        memory[0x5DB] = 0xAE
        memory[0x5DC] = 0x81
        memory[0x5DD] = 0xDA
        chip8 = self._init_chip8(v_registers=v_registers,
                                 i_register=i_register, memory=memory)

        chip8._fx65(vx_index)

        expected_v0_value = 0x48
        actual_v0_value = chip8.v_registers[0x0]
        expected_v1_value = 0xAE
        actual_v1_value = chip8.v_registers[0x1]
        expected_v2_value = 0x81
        actual_v2_value = chip8.v_registers[0x2]
        expected_v3_value = 0xDA
        actual_v3_value = chip8.v_registers[0x3]

        self.assertEqual(expected_v0_value, actual_v0_value)
        self.assertEqual(expected_v1_value, actual_v1_value)
        self.assertEqual(expected_v2_value, actual_v2_value)
        self.assertEqual(expected_v3_value, actual_v3_value)

    def test_load_rom_to_memory(self):
        chip8 = self._init_chip8()
        rom_path = 'roms/pong.rom'

        chip8._load_rom_to_memory(rom_path)

        expected_memory = [None] * 4096
        expected_memory[0x200:0x200] = [
            0x6A, 0x2, 0x6B, 0xC, 0x6C, 0x3F, 0x6D, 0xC, 0xA2, 0xEA,
            0xDA, 0xB6, 0xDC, 0xD6, 0x6E, 0x0, 0x22, 0xD4, 0x66, 0x3,
            0x68, 0x2, 0x60, 0x60, 0xF0, 0x15, 0xF0, 0x7, 0x30, 0x0,
            0x12, 0x1A, 0xC7, 0x17, 0x77, 0x8, 0x69, 0xFF, 0xA2, 0xF0,
            0xD6, 0x71, 0xA2, 0xEA, 0xDA, 0xB6, 0xDC, 0xD6, 0x60, 0x1,
            0xE0, 0xA1, 0x7B, 0xFE, 0x60, 0x4, 0xE0, 0xA1, 0x7B, 0x2,
            0x60, 0x1F, 0x8B, 0x2, 0xDA, 0xB6, 0x60, 0xC, 0xE0, 0xA1,
            0x7D, 0xFE, 0x60, 0xD, 0xE0, 0xA1, 0x7D, 0x2, 0x60, 0x1F,
            0x8D, 0x2, 0xDC, 0xD6, 0xA2, 0xF0, 0xD6, 0x71, 0x86, 0x84,
            0x87, 0x94, 0x60, 0x3F, 0x86, 0x2, 0x61, 0x1F, 0x87, 0x12,
            0x46, 0x2, 0x12, 0x78, 0x46, 0x3F, 0x12, 0x82, 0x47, 0x1F,
            0x69, 0xFF, 0x47, 0x0, 0x69, 0x1, 0xD6, 0x71, 0x12, 0x2A,
            0x68, 0x2, 0x63, 0x1, 0x80, 0x70, 0x80, 0xB5, 0x12, 0x8A,
            0x68, 0xFE, 0x63, 0xA, 0x80, 0x70, 0x80, 0xD5, 0x3F, 0x1,
            0x12, 0xA2, 0x61, 0x2, 0x80, 0x15, 0x3F, 0x1, 0x12, 0xBA,
            0x80, 0x15, 0x3F, 0x1, 0x12, 0xC8, 0x80, 0x15, 0x3F, 0x1,
            0x12, 0xC2, 0x60, 0x20, 0xF0, 0x18, 0x22, 0xD4, 0x8E, 0x34,
            0x22, 0xD4, 0x66, 0x3E, 0x33, 0x1, 0x66, 0x3, 0x68, 0xFE,
            0x33, 0x1, 0x68, 0x2, 0x12, 0x16, 0x79, 0xFF, 0x49, 0xFE,
            0x69, 0xFF, 0x12, 0xC8, 0x79, 0x1, 0x49, 0x2, 0x69, 0x1,
            0x60, 0x4, 0xF0, 0x18, 0x76, 0x1, 0x46, 0x40, 0x76, 0xFE,
            0x12, 0x6C, 0xA2, 0xF2, 0xFE, 0x33, 0xF2, 0x65, 0xF1, 0x29,
            0x64, 0x14, 0x65, 0x0, 0xD4, 0x55, 0x74, 0x15, 0xF2, 0x29,
            0xD4, 0x55, 0x0, 0xEE, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
            0x80, 0x0, 0x0, 0x0, 0x0, 0x0
        ]
        del expected_memory[4096:]
        actual_memory = chip8.memory

        self.assertEqual(expected_memory, actual_memory)

    def test_get_current_opcode(self):
        memory = [None] * 4096
        program_counter = 0x30F
        loaded_memory_from_0x300 = [
            0x6A, 0x2, 0x6B, 0xC, 0x6C, 0x3F, 0x6D, 0xC, 0xA2, 0xEA,
            0xDA, 0xB6, 0xDC, 0xD6, 0x6E, 0xAE, 0x22, 0xD4, 0x66, 0x3,
            0x68, 0x2, 0x60, 0x60, 0xF0, 0x15, 0xF0, 0x7, 0x30, 0x0,
            0x12, 0x1A, 0xC7, 0x17, 0x77, 0x8, 0x69, 0xFF, 0xA2, 0xF0,
        ]
        memory[0x300:0x300] = loaded_memory_from_0x300
        chip8 = self._init_chip8(program_counter=program_counter,
                                 memory=memory)

        expected_opcode = bytes([0xAE, 0x22])
        actual_opcode = chip8._get_current_opcode()

        self.assertEqual(expected_opcode, actual_opcode)

    @mock.patch('chip8_emulator.chip8.Chip8._1nnn')
    def test_execute_operation__1nnn(self, mocked_1nnn):
        operation = '1nnn'
        parameters = [0x4AE]
        chip8 = self._init_chip8()

        chip8._execute_operation(operation, parameters)

        self.assertTrue(mocked_1nnn.called)

    @mock.patch('chip8_emulator.chip8.Chip8._3xkk')
    def test_execute_operation__3xkk(self, mocked_3xkk):
        operation = '3xkk'
        parameters = (0x4, 0xEA)
        chip8 = self._init_chip8()

        chip8._execute_operation(operation, parameters)

        self.assertTrue(mocked_3xkk.called)

    @mock.patch('chip8_emulator.chip8.Chip8._8xy3')
    def test_execute_operation__8xy3(self, mocked_8xy3):
        operation = '8xy3'
        parameters = (0x1, 0x2)
        chip8 = self._init_chip8()

        chip8._execute_operation(operation, parameters)

        self.assertTrue(mocked_8xy3.called)
