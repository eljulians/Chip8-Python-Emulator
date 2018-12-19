import unittest
from unittest import mock
from chip8_emulator.chip8 import Chip8
from chip8_emulator.memory import Memory


class Chip8Test(unittest.TestCase):

    def _init_chip8(self, program_counter=0x200, stack_pointer=0xEA0, stack=[],
                    v_registers=[0x00] * 16, i_register=None,
                    program_memory=[None] * 4096, delay_timer=None, sound_timer=None):
        screen_mock = mock.Mock()
        keyboard_mock = mock.Mock()
        memory = Memory()
        memory.program_counter = program_counter
        memory.stack = stack
        memory.v_registers = v_registers
        memory.i_register = i_register
        memory.program_memory = program_memory
        memory._delay_timer = delay_timer
        memory.sound_timer = sound_timer

        chip8 = Chip8(screen_mock, keyboard_mock)
        chip8.memory = memory

        return chip8

    @mock.patch('chip8_emulator.screen_proxy.ScreenProxy.clear_screen')
    def test_00e0(self, mocked_clear_screen):
        chip8 = self._init_chip8()

        chip8._00e0()

        self.assertTrue(mocked_clear_screen.called)

    def test_00ee(self):
        program_counter = 0x317
        stack_pointer = 0xEA2
        stack = [0x201, 0x204, 0x25F]

        chip8 = self._init_chip8(program_counter, stack_pointer, stack)
        chip8._00ee()

        expected_program_counter = 0x261
        actual_program_counter = chip8.memory.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_1nnn(self):
        jump_to = 0x47F

        chip8 = self._init_chip8()
        chip8._1nnn(jump_to)

        expected_program_counter = jump_to
        actual_program_counter = chip8.memory.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_2nnn(self):
        program_counter = 0x617
        stack_pointer = 0xEA3
        stack = [0x351, 0x215, 0x812, 0x4FA]
        call_subroutine_at = 0xBA4

        chip8 = self._init_chip8(program_counter, stack_pointer, stack)
        chip8._2nnn(call_subroutine_at)

        expected_program_counter = call_subroutine_at
        actual_program_counter = chip8.memory.program_counter
        expected_stack = [0x351, 0x215, 0x812, 0x4FA, 0x617]
        actual_stack = chip8.memory.stack

        self.assertEqual(expected_program_counter, actual_program_counter)
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
        actual_program_counter = chip8.memory.program_counter

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
        actual_program_counter = chip8.memory.program_counter

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
        actual_program_counter = chip8.memory.program_counter

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
        actual_program_counter = chip8.memory.program_counter

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
        actual_program_counter = chip8.memory.program_counter

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
        actual_program_counter = chip8.memory.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_6xkk(self):
        v_registers = [None] * 16
        vx_index = 0xA
        value = 0xEA
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._6xkk(vx_index, value)

        expected_vx = value
        actual_vx = chip8.memory.v_registers[vx_index]

        self.assertEqual(expected_vx, actual_vx)

    def test_7xkk(self):
        vx_index = 0x5
        v_registers = [None] * 16
        v_registers[vx_index] = 0x38
        value_to_add = 0xAF
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._7xkk(vx_index, value_to_add)

        expected_vx_value = 0xE7
        actual_vx_value = chip8.memory.v_registers[vx_index]

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
        actual_vx_value = chip8.memory.v_registers[vx_index]

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
        actual_vx_value = chip8.memory.v_registers[vx_index]

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
        actual_vx_value = chip8.memory.v_registers[vx_index]

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
        actual_vx_value = chip8.memory.v_registers[vx_index]

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
        actual_vx_value = chip8.memory.v_registers[vx_index]

        expected_vf_value = 0x00
        actual_vf_value = chip8.memory.v_registers[0xF]

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
        actual_vx_value = chip8.memory.v_registers[vx_index]

        expected_vf_value = 0x01
        actual_vf_value = chip8.memory.v_registers[0xF]

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
        actual_vx_value = chip8.memory.v_registers[vx_index]

        expected_vf_value = 0x01
        actual_vf_value = chip8.memory.v_registers[0xF]

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
        actual_vx_value = chip8.memory.v_registers[vx_index]

        expected_vf_value = 0x00
        actual_vf_value = chip8.memory.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xy6__least_significant_bit_0(self):
        vx_index = 0x1
        v_registers = [None] * 16
        v_registers[vx_index] = 0x5A
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy6(vx_index)

        expected_vx_value = 0x2D
        actual_vx_value = chip8.memory.v_registers[vx_index]

        expected_vf_value = 0x00
        actual_vf_value = chip8.memory.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xy6__least_significant_bit_1(self):
        vx_index = 0x1
        v_registers = [None] * 16
        v_registers[vx_index] = 0xAF
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xy6(vx_index)

        expected_vx_value = 0x57
        actual_vx_value = chip8.memory.v_registers[vx_index]

        expected_vf_value = 0x01
        actual_vf_value = chip8.memory.v_registers[0xF]

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
        actual_vx_value = chip8.memory.v_registers[vx_index]

        expected_vf_value = 0x01
        actual_vf_value = chip8.memory.v_registers[0xF]

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
        actual_vx_value = chip8.memory.v_registers[vx_index]

        expected_vf_value = 0x00
        actual_vf_value = chip8.memory.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xye__least_significant_bit_0(self):
        vx_index = 0x1
        v_registers = [None] * 16
        v_registers[vx_index] = 0x52
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xye(vx_index)

        expected_vx_value = 0xA4
        actual_vx_value = chip8.memory.v_registers[vx_index]

        expected_vf_value = 0x00
        actual_vf_value = chip8.memory.v_registers[0xF]

        self.assertEqual(expected_vx_value, actual_vx_value)
        self.assertEqual(expected_vf_value, actual_vf_value)

    def test_8xye__least_significant_bit_1(self):
        vx_index = 0x1
        v_registers = [None] * 16
        v_registers[vx_index] = 0x71
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._8xye(vx_index)

        expected_vx_value = 0xE2
        actual_vx_value = chip8.memory.v_registers[vx_index]

        expected_vf_value = 0x01
        actual_vf_value = chip8.memory.v_registers[0xF]

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
        actual_program_counter = chip8.memory.program_counter

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
        actual_program_counter = chip8.memory.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_annn(self):
        chip8 = self._init_chip8()

        new_i_value = 0xA52

        chip8._annn(new_i_value)

        expected_i_register = 0xA52
        actual_i_register = chip8.memory.i_register

        self.assertEqual(expected_i_register, actual_i_register)

    def test_bnnn(self):
        program_counter = 0x7A1
        v_registers = [None] * 16
        v_registers[0] = 0x14
        chip8 = self._init_chip8(program_counter, v_registers=v_registers)

        new_address = 0x47F
        chip8._bnnn(new_address)

        expected_program_counter = 0x493
        actual_program_counter = chip8.memory.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    @mock.patch('random.getrandbits')
    def test_cxkk(self, mocked_getrandbits):
        v_registers = [None] * 16
        vx_index = 0x4
        mocked_getrandbits.return_value = 0xAE
        input_value = 0x45
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._cxkk(vx_index, input_value)

        expected_vx_value = 0x04
        actual_vx_value = chip8.memory.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_dxyn(self):
        screen_proxy_mock = mock.Mock()
        v_registers = [None] * 16
        vx_index = 0x4
        vy_index = 0x6
        vx_value = 0x15
        vy_value = 0x20
        v_registers[vx_index] = vx_value
        v_registers[vy_index] = vy_value
        sprite = [0xFA, 0xC0, 0xAE, 0x15]
        sprite_memory_address = 0x317
        program_memory = [0x00] * 0xE9F
        program_memory[sprite_memory_address:sprite_memory_address+len(sprite)]=sprite
        i_register = sprite_memory_address
        chip8 = self._init_chip8(v_registers=v_registers,
                                 i_register=i_register,
                                 program_memory=program_memory)
        chip8.screen_proxy = screen_proxy_mock

        chip8._dxyn(vx_index, vy_index, len(sprite))

        screen_proxy_mock.draw_sprite.assert_called_with(sprite, vx_value, vy_value)

    def test_ex9e__equals(self):
        keyboard_mock = mock.Mock()
        keyboard_return_value = 0x77
        keyboard_mock.get_pressed_key.return_value = keyboard_return_value
        v_registers = [0x00] * 16
        vx_index = 0x3
        vx_value = keyboard_return_value
        v_registers[vx_index] = vx_value
        program_counter = 0x300
        chip8 = self._init_chip8(v_registers=v_registers,
                                 program_counter=program_counter)
        chip8.keyboard = keyboard_mock

        chip8._ex9e(vx_index)

        expected_program_counter = 0x304
        actual_program_counter = chip8.memory.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_ex9e__not_equals(self):
        keyboard_mock = mock.Mock()
        keyboard_return_value = 0x65
        keyboard_mock.get_pressed_key.return_value = keyboard_return_value
        v_registers = [0x00] * 16
        vx_index = 0x3
        vx_value = 0x77
        v_registers[vx_index] = vx_value
        program_counter = 0x300
        chip8 = self._init_chip8(v_registers=v_registers,
                                 program_counter=program_counter)
        chip8.keyboard = keyboard_mock

        chip8._ex9e(vx_index)

        expected_program_counter = 0x302
        actual_program_counter = chip8.memory.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_exa1__equals(self):
        keyboard_mock = mock.Mock()
        keyboard_return_value = 0x61
        keyboard_mock.get_pressed_key.return_value = keyboard_return_value
        v_registers = [0x00] * 16
        vx_index = 0x3
        vx_value = keyboard_return_value
        v_registers[vx_index] = vx_value
        program_counter = 0x715
        chip8 = self._init_chip8(v_registers=v_registers,
                                 program_counter=program_counter)
        chip8.keyboard = keyboard_mock

        chip8._exa1(vx_index)

        expected_program_counter = 0x717
        actual_program_counter = chip8.memory.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_exa1__not_equals(self):
        keyboard_mock = mock.Mock()
        keyboard_return_value = 0x61
        keyboard_mock.get_pressed_key.return_value = keyboard_return_value
        v_registers = [0x00] * 16
        vx_index = 0x3
        v_registers[vx_index] = 0x73
        program_counter = 0x715
        chip8 = self._init_chip8(v_registers=v_registers,
                                 program_counter=program_counter)
        chip8.keyboard = keyboard_mock

        chip8._exa1(vx_index)

        expected_program_counter = 0x719
        actual_program_counter = chip8.memory.program_counter

        self.assertEqual(expected_program_counter, actual_program_counter)

    def test_fx07(self):
        delay_timer = 0x05
        vx_index = 0x7
        chip8 = self._init_chip8(delay_timer=delay_timer)

        chip8._fx07(vx_index)

        expected_vx_value = 0x05
        actual_vx_value = chip8.memory.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_fx0a(self):
        keyboard_mock = mock.Mock()
        keyboard_return_value = 0x71
        keyboard_mock.wait_for_key.return_value = keyboard_return_value
        vx_index = 0x7
        chip8 = self._init_chip8()
        chip8.keyboard = keyboard_mock

        chip8._fx0a(vx_index)

        expected_vx_value = keyboard_return_value
        actual_vx_value = chip8.memory.v_registers[vx_index]

        self.assertEqual(expected_vx_value, actual_vx_value)

    def test_fx15(self):
        v_registers = [None] * 16
        vx_index = 0x7
        v_registers[vx_index] = 0xAE
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._fx15(vx_index)

        expected_delay_timer = 0xAE
        actual_delay_timer = chip8.memory._delay_timer

        self.assertEqual(expected_delay_timer, actual_delay_timer)

    def test_fx18(self):
        v_registers = [None] * 16
        vx_index = 0x3
        v_registers[vx_index] = 0x45
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._fx18(vx_index)

        expected_sound_timer = 0x45
        actual_sound_timer = chip8.memory.sound_timer

        self.assertEqual(expected_sound_timer, actual_sound_timer)

    def test_fx1e(self):
        v_registers = [None] * 16
        vx_index = 0x5
        v_registers[vx_index] = 0xAE
        i_register = 0xC15
        chip8 = self._init_chip8(v_registers=v_registers,
                                 i_register=i_register)

        chip8._fx1e(vx_index)

        expected_i_register = 0xCC3
        actual_i_register = chip8.memory.i_register

        self.assertEqual(expected_i_register, actual_i_register)

    def test_fx29(self):
        v_registers = [0x00] * 16
        vx_index = 0x7
        sprite_character = 0xA
        v_registers[vx_index] = sprite_character
        chip8 = self._init_chip8(v_registers=v_registers)

        chip8._fx29(vx_index)

        preloaded_sprites_addresses = list(chip8.memory.PRELOADED_SPRITES)
        expected_i_register = preloaded_sprites_addresses[sprite_character]
        actual_i_register = chip8.memory.i_register

        self.assertEqual(expected_i_register, actual_i_register)

    def test_fx33(self):
        v_registers = [None] * 16
        memory = [None] * 4096
        vx_index = 0x5
        v_registers[vx_index] = 0xAE
        i_register = 0xCE5
        chip8 = self._init_chip8(v_registers=v_registers,
                                 i_register=i_register, program_memory=memory)

        chip8._fx33(vx_index)

        expected_i0_memory_location_value = 1
        actual_i0_memory_location_value = chip8.memory.program_memory[0xCE5]
        expected_i1_memory_location_value = 7
        actual_i1_memory_location_value = chip8.memory.program_memory[0xCE6]
        expected_i2_memory_location_value = 4
        actual_i2_memory_location_value = chip8.memory.program_memory[0xCE7]

        self.assertEqual(expected_i0_memory_location_value,
                         actual_i0_memory_location_value)
        self.assertEqual(expected_i1_memory_location_value,
                         actual_i1_memory_location_value)
        self.assertEqual(expected_i2_memory_location_value,
                         actual_i2_memory_location_value)

    def test_fx55(self):
        v_registers = [0x14, 0xF4, 0x61, 0xDE, 0xAE]
        memory = [None] * 4096
        vx_index = 0x4
        i_register = 0x7A4
        chip8 = self._init_chip8(v_registers=v_registers,
                                 i_register=i_register, program_memory=memory)

        chip8._fx55(vx_index)

        expected_i0_memory_location_value = 0x14
        actual_i0_memory_location_value = chip8.memory.program_memory[0x7A4]
        expected_i1_memory_location_value = 0xF4
        actual_i1_memory_location_value = chip8.memory.program_memory[0x7A5]
        expected_i2_memory_location_value = 0x61
        actual_i2_memory_location_value = chip8.memory.program_memory[0x7A6]
        expected_i3_memory_location_value = 0xDE
        actual_i3_memory_location_value = chip8.memory.program_memory[0x7A7]
        expected_i4_memory_location_value = 0xAE
        actual_i4_memory_location_value = chip8.memory.program_memory[0x7A8]

        self.assertEqual(expected_i0_memory_location_value,
                         actual_i0_memory_location_value)
        self.assertEqual(expected_i1_memory_location_value,
                         actual_i1_memory_location_value)
        self.assertEqual(expected_i2_memory_location_value,
                         actual_i2_memory_location_value)
        self.assertEqual(expected_i3_memory_location_value,
                         actual_i3_memory_location_value)
        self.assertEqual(expected_i4_memory_location_value,
                         actual_i4_memory_location_value)

    def test_fx65(self):
        v_registers = [None] * 16
        vx_index = 0x4
        i_register = 0x5DA
        memory = [None] * 4096
        memory[0x5DA] = 0x48
        memory[0x5DB] = 0xAE
        memory[0x5DC] = 0x81
        memory[0x5DD] = 0xDA
        memory[0x5DE] = 0x15
        chip8 = self._init_chip8(v_registers=v_registers,
                                 i_register=i_register, program_memory=memory)

        chip8._fx65(vx_index)

        expected_v0_value = 0x48
        actual_v0_value = chip8.memory.v_registers[0x0]
        expected_v1_value = 0xAE
        actual_v1_value = chip8.memory.v_registers[0x1]
        expected_v2_value = 0x81
        actual_v2_value = chip8.memory.v_registers[0x2]
        expected_v3_value = 0xDA
        actual_v3_value = chip8.memory.v_registers[0x3]
        expected_v4_value = 0x15
        actual_v4_value = chip8.memory.v_registers[0x4]

        self.assertEqual(expected_v0_value, actual_v0_value)
        self.assertEqual(expected_v1_value, actual_v1_value)
        self.assertEqual(expected_v2_value, actual_v2_value)
        self.assertEqual(expected_v3_value, actual_v3_value)
        self.assertEqual(expected_v4_value, actual_v4_value)

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
