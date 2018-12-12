import unittest
from unittest import mock
from chip8_emulator.memory import Memory


class MemoryTest(unittest.TestCase):

    def _init_memory(self, program_memory=[None] * 4096, program_counter=0x200):
        memory = Memory()
        memory.program_memory = program_memory
        memory.program_counter = program_counter

        return memory

    def test_get_current_opcode(self):
        program_memory = [None] * 4096
        program_counter = 0x30F
        loaded_memory_from_0x300 = [
            0x6A, 0x2, 0x6B, 0xC, 0x6C, 0x3F, 0x6D, 0xC, 0xA2, 0xEA,
            0xDA, 0xB6, 0xDC, 0xD6, 0x6E, 0xAE, 0x22, 0xD4, 0x66, 0x3,
            0x68, 0x2, 0x60, 0x60, 0xF0, 0x15, 0xF0, 0x7, 0x30, 0x0,
            0x12, 0x1A, 0xC7, 0x17, 0x77, 0x8, 0x69, 0xFF, 0xA2, 0xF0,
        ]
        program_memory[0x300:0x300] = loaded_memory_from_0x300
        memory = self._init_memory(program_memory, program_counter)

        expected_opcode = bytes([0xAE, 0x22])
        actual_opcode = memory.get_current_opcode()

        self.assertEqual(expected_opcode, actual_opcode)
