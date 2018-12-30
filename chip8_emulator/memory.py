from threading import Lock


class Memory:

    PROGRAM_COUNTER_START = 0x200
    PROGRAM_MEMORY_LENGTH = 0xE9F
    STACK_LENGTH_BYTES = 48
    V_REGISTERS_LENGTH_BYTES = 16
    PRELOADED_SPRITES = {
        0x000: (0xF0, 0x90, 0x90, 0x90, 0xF0),  # 0
        0x005: (0x20, 0x60, 0x20, 0x20, 0x70),  # 1
        0x00A: (0xF0, 0x10, 0xF0, 0x80, 0xF0),  # 2
        0x00F: (0xF0, 0x10, 0xF0, 0x10, 0xF0),  # 3
        0x014: (0x90, 0x90, 0xF0, 0x10, 0x10),  # 4
        0x019: (0xF0, 0x80, 0xF0, 0x10, 0xF0),  # 5
        0x01E: (0xF0, 0x80, 0xF0, 0x90, 0xF0),  # 6
        0x023: (0xF0, 0x10, 0x20, 0x40, 0x40),  # 7
        0x028: (0xF0, 0x90, 0xF0, 0x90, 0xF0),  # 8
        0x02D: (0xF0, 0x90, 0xF0, 0x10, 0xF0),  # 9
        0x032: (0xF0, 0x90, 0xF0, 0x90, 0x90),  # A
        0x037: (0xE0, 0x90, 0xE0, 0x90, 0xE0),  # B
        0x03C: (0xF0, 0x80, 0x80, 0x80, 0xF0),  # C
        0x041: (0xE0, 0x90, 0x90, 0x90, 0xE0),  # D
        0x046: (0xF0, 0x80, 0xF0, 0x80, 0xF0),  # E
        0x04B: (0xF0, 0x80, 0xF0, 0x80, 0x80),  # F
    }

    def __init__(self):
        self.program_memory = [0x00] * self.PROGRAM_MEMORY_LENGTH
        self.stack = []
        self.v_registers = [0x00] * self.V_REGISTERS_LENGTH_BYTES
        self.i_register = None
        self.program_counter = self.PROGRAM_COUNTER_START
        self._delay_timer = 0
        self._delay_timer_mutex = Lock()
        self._sound_timer = 0
        self._sound_timer_mutex = Lock()
        self._load_digit_sprites()

    def _load_digit_sprites(self):
        for memory_address_start, sprite in self.PRELOADED_SPRITES.items():
            sprite_size = len(sprite)
            memory_address_end = memory_address_start + sprite_size
            self.program_memory[memory_address_start:memory_address_end] = sprite

    def get_address_of_preloaded_sprite(self, sprite_value):
        sprites_addresses = list(self.PRELOADED_SPRITES)
        return sprites_addresses[sprite_value]

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

    def load_rom(self, rom_bytes):
        memory_index = self.PROGRAM_COUNTER_START

        for rom_byte in rom_bytes:
            self.program_memory[memory_index] = rom_byte
            memory_index += 1

    def decrement_delay_timer(self):
        self._delay_timer_mutex.acquire()

        if self._delay_timer > 0:
            self._delay_timer -= 1

        self._delay_timer_mutex.release()

    def decrement_sound_timer(self):
        self._sound_timer_mutex.acquire()

        if self._sound_timer > 0:
            self._sound_timer -= 1

        self._sound_timer_mutex.release()

    def set_delay_timer_to_v_value(self, v_index):
        self._delay_timer_mutex.acquire()
        self._delay_timer = self.v_registers[v_index]
        self._delay_timer_mutex.release()

    def set_v_value_to_delay_timer(self, v_index):
        self._delay_timer_mutex.acquire()
        self.v_registers[v_index] = self._delay_timer
        self._delay_timer_mutex.release()

    def set_sound_timer_to_v_value(self, v_index):
        self._sound_timer_mutex.acquire()
        self._sound_timer = self.v_registers[v_index]
        self._sound_timer_mutex.release()
