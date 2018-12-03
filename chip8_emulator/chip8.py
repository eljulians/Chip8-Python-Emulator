class Chip8:
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
    I_REGISTER_LENGTH_BYTES = 2

    def __init__(self):
        self.memory = []
        self.stack = []
        self.stack_pointer = 0
        self.program_counter = 0
        self.v_registers = []
        self.i_register = None

    def clear_screen(self):
        """ 00E0"""
        pass

    def ret(self):
        """ 00EE """
        self.program_counter = self.stack.pop()
        self.stack_pointer -= 1

    def jump(self, address):
        """ 1NNN """
        self.program_counter = address

    def call(self, address):
        """ 2NNN """
        self.stack.append(self.program_counter)
        self.stack_pointer += 1
        self.program_counter = address

    def skip_next_instruction_if_equals(self, v_index, instruction):
        """ 3XNN """
        if self.v_registers[v_index] == instruction:
            self.program_counter += 2

    def skip_next_instruction_if_not_equals(self, v_index, instruction):
        """ 4XNN """
        if self.v_registers[v_index] != instruction:
            self.program_counter += 2

    def skip_next_instruction_if_vx_equals_vy(self, vx_index, vy_index):
        """ 5XY0 """
        if self.v_registers[vx_index] == self.v_registers[vy_index]:
            self.program_counter += 2

    def set_v_fixed_value(self, v_index, value):
        """ 6XNN """
        self.v_registers[v_index] = value

    def add_to_v(self, v_index, value):
        """ 7XNN """
        self.v_registers[v_index] += value

    def set_vx_to_vy(self, vx_index, vy_index):
        """ 8XY0 """
        self.v_registers[vx_index] = self.v_registers[vy_index]

    def set_vx_to_vx_or_vy(self, vx_index, vy_index):
        """ 8XY1 """
        self.v_registers[vx_index] |= self.v_registers[vy_index]

    def set_vx_to_vx_and_vy(self, vx_index, vy_index):
        """ 8XY2 """
        self.v_registers[vx_index] &= self.v_registers[vy_index]

    def set_vx_to_vx_xor_vy(self, vx_index, vy_index):
        """ 8XY3 """
        self.v_registers[vx_index] ^= self.v_registers[vy_index]

    def add_vy_to_vx(self, vx_index, vy_index):
        """ 8XY4 """
        addition_result = self.v_registers[vx_index] \
            + self.v_registers[vy_index]
        addition_result_last_8_bits = addition_result & 0x0FF
        self.v_registers[vx_index] = addition_result_last_8_bits
        self.v_registers[0xF] = 0x00 if addition_result <= 0xFF else 0x01

    def subtract_vy_from_vx(self, vx_index, vy_index):
        """ 8XY5 """
        vx_value = self.v_registers[vx_index]
        vy_value = self.v_registers[vy_index]

        self.v_registers[0xF] = 0x01 if vx_value > vy_value else 0x00

        subtraction_result_abs = abs(vx_value - vy_value)
        self.v_registers[vx_index] = subtraction_result_abs

    def shift_right_vx(self, vx_index):
        """ 8XY6 """
        vx_value = self.v_registers[vx_index]
        vx_last_bit = vx_value & 0x01
        right_shifted_vx_value = vx_value >> 1
        self.v_registers[vx_index] = right_shifted_vx_value
        self.v_registers[0xF] = vx_last_bit

    def subtract_vx_from_vy_store_in_vx(self, vx_index, vy_index):
        """ 8XY7 """
        vx_value = self.v_registers[vx_index]
        vy_value = self.v_registers[vy_index]

        self.v_registers[0xF] = 0x01 if vy_value > vx_value else 0x00

        subtraction_result_abs = abs(vy_value - vx_value)
        self.v_registers[vx_index] = subtraction_result_abs

    def shift_left_vx(self, vx_index):
        """ 8XYE """
        vx_value = self.v_registers[vx_index]
        vx_last_bit = vx_value & 0x01
        left_shifted_vx_value = vx_value << 1
        self.v_registers[vx_index] = left_shifted_vx_value
        self.v_registers[0xF] = vx_last_bit

    def skip_next_instruction_if_vx_not_equals_vy(self, vx_index, vy_index):
        """ 9XY0 """
        if self.v_registers[vx_index] != self.v_registers[vy_index]:
            self.program_counter += 2

    def set_i_register(self, value):
        """ ANNN """
        self.i_register = value

    def jump_to_address_plus_v0(self, address):
        """ BNNN """
        self.program_counter = address + self.v_registers[0x0]

    def set_vx_to_random_anded_value(self, value):
        """ CXNN """
        pass

    def draw_sprite_at_coordinate(self, vx_coord, vy_coord, sprite_height):
        """ DXYN """
        pass

    def skip_next_instruction_if_pressed_key_equals_vx(self):
        """ EX9E """
        pass

    def skip_next_instruction_if_pressed_key_not_equals_vx(self):
        """ EXA1 """
        pass

    def set_vx_to_delay_timer(self, vx_index):
        """ FX07"""
        pass

    def wait_for_key_store_value_in_vx(self, vx_index):
        """ FX0A """
        pass

    def set_delay_timer_to_vx(self, vx_index):
        """ FX15 """
        pass

    def set_sound_timer_to_vx(self, vx_index):
        """ FX18 """
        pass

    def add_vx_to_i_register(self, vx_index):
        """ FX1E """
        self.i_register += self.v_registers[vx_index]

    def set_i_register_to_location_of_sprite_for_vx(self, vx_index):
        """ FX29 """
        pass

    def _get_addresses_from_i_register_to_offset(self, offset):
        return [self.i_register + index for index in range(0, offset)]

    def store_binary_coded_decimal_of_vx_in_i_register(self, vx_index):
        """ FX33 """
        vx_value = self.v_registers[vx_index]
        vx_value_digits = [int(digit) for digit in str(vx_value)]
        addresses = self._get_addresses_from_i_register_to_offset(3)

        for address in addresses:
            self.memory[address] = vx_value_digits.pop(0)

    def store_from_v0_to_vx_in_i_register(self, vx_index):
        """ FX55 """
        addresses = self._get_addresses_from_i_register_to_offset(vx_index)
        v_register_values = self.v_registers[:vx_index]

        for address in addresses:
            self.memory[address] = v_register_values.pop(0)

    def read_v0_to_vx_from_i_register(self, vx_index):
        """ Fx65"""
        addresses = self._get_addresses_from_i_register_to_offset(vx_index)

        for v_index in range(0, vx_index):
            address = addresses.pop(0)
            self.v_registers[v_index] = self.memory[address]

    def _load_rom_to_memory(self, rom_path):
        with open(rom_path, 'rb') as rom_handle:
            for rom_byte in rom_handle.read():
                self.memory.append(rom_byte)

    def main(self):
        pass
