class Memory:
    """
    Memory map
    0x000 - 0x1FF: CHIP8 interpreter itself; don't touch these addresses
    0x200 - 0xE9F: program memory (3.231 bytes)
    0xEA0 - 0xECF: stack (48 bytes)
    0xED0 - 0xEFF: work area (48 bytes)
        0xEFO - 0xEFF: v registers (16 bytes)
    0xF00 - 0xFFF: display refresh
    """

    MEMORY_LENGTH_BYTES = 4096
    STACK_LENGTH_BYTES = 48
    V_REGISTERS_LENGTH_BYTES = 16

    def __init__(self):
        self.program_memory = [0x00] * 0xE9F
        self.stack = []
        self.program_counter = 0x200
        self.v_registers = [0x00] * self.V_REGISTERS_LENGTH_BYTES
        self.i_register = None
        self.delay_timer = None
        self.sound_timer = None
        self._init_digit_sprites()

    def _init_digit_sprites(self):
        sprites_bytes = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
        ]

        memory_index = 0

        for sprite_byte in sprites_bytes:
            self.program_memory[memory_index] = sprite_byte
            memory_index += 1

    def add_to_stack(self, memory_address):
        self.stack.append(memory_address)

    def pop_from_stack(self):
        return self.stack.pop()

    def increment_program_counter(self):
        self.program_counter += 2

    def get_current_opcode(self):
        opcode_first_byte = self.program_memory[self.program_counter]
        opcode_last_byte = self.program_memory[self.program_counter + 1]

        return bytes([opcode_first_byte, opcode_last_byte])

    def get_addresses_from_i_register_to_offset(self, offset):
        return [self.i_register + index for index in range(0, offset)]

    def load_rom(self, rom_handle):
        memory_index = 0x200

        for rom_byte in rom_handle.read():
            self.program_memory[memory_index] = rom_byte
            memory_index += 1
