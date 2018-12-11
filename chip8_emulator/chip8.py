import random
from .opcode_parser import parse_operation_and_parameters


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
        self.memory = [0x00] * 0xE9F
        self.stack = []
        self.stack_pointer = 0
        self.program_counter = 0x200
        self.v_registers = [None] * self.V_REGISTERS_LENGTH_BYTES
        self.i_register = None
        self.delay_timer = None
        self.sound_timer = None

    def _00e0(self):
        # TODO: implement
        self._increment_program_counter(1)

    def _00ee(self):
        self.program_counter = self.stack.pop()
        self.stack_pointer -= 1

    def _1nnn(self, address):
        self.program_counter = address

    def _2nnn(self, address):
        self.stack.append(self.program_counter)
        self.stack_pointer += 1
        self.program_counter = address

    def _3xkk(self, v_index, instruction):
        if self.v_registers[v_index] == instruction:
            self._increment_program_counter(2)
        else:
            self._increment_program_counter(1)

    def _4xkk(self, v_index, instruction):
        if self.v_registers[v_index] != instruction:
            self._increment_program_counter(2)
        else:
            self._increment_program_counter(1)

    def _5xy0(self, vx_index, vy_index):
        if self.v_registers[vx_index] == self.v_registers[vy_index]:
            self._increment_program_counter(2)
        else:
            self._increment_program_counter(1)

    def _6xkk(self, v_index, value):
        self.v_registers[v_index] = value
        self._increment_program_counter(1)

    def _7xkk(self, v_index, value):
        self.v_registers[v_index] += value
        self._increment_program_counter(1)

    def _8xy0(self, vx_index, vy_index):
        self.v_registers[vx_index] = self.v_registers[vy_index]
        self._increment_program_counter(1)

    def _8xy1(self, vx_index, vy_index):
        self.v_registers[vx_index] |= self.v_registers[vy_index]
        self._increment_program_counter(1)

    def _8xy2(self, vx_index, vy_index):
        self.v_registers[vx_index] &= self.v_registers[vy_index]
        self._increment_program_counter(1)

    def _8xy3(self, vx_index, vy_index):
        self.v_registers[vx_index] ^= self.v_registers[vy_index]
        self._increment_program_counter(1)

    def _8xy4(self, vx_index, vy_index):
        addition_result = self.v_registers[vx_index] \
            + self.v_registers[vy_index]
        addition_result_last_8_bits = addition_result & 0x0FF
        self.v_registers[vx_index] = addition_result_last_8_bits
        self.v_registers[0xF] = 0x00 if addition_result <= 0xFF else 0x01

        self._increment_program_counter(1)

    def _8xy5(self, vx_index, vy_index):
        vx_value = self.v_registers[vx_index]
        vy_value = self.v_registers[vy_index]

        self.v_registers[0xF] = 0x01 if vx_value > vy_value else 0x00

        subtraction_result_abs = abs(vx_value - vy_value)
        self.v_registers[vx_index] = subtraction_result_abs

        self._increment_program_counter(1)

    def _8xy6(self, vx_index):
        vx_value = self.v_registers[vx_index]
        vx_last_bit = vx_value & 0x01
        right_shifted_vx_value = vx_value >> 1
        self.v_registers[vx_index] = right_shifted_vx_value
        self.v_registers[0xF] = vx_last_bit

        self._increment_program_counter(1)

    def _8xy7(self, vx_index, vy_index):
        vx_value = self.v_registers[vx_index]
        vy_value = self.v_registers[vy_index]

        self.v_registers[0xF] = 0x01 if vy_value > vx_value else 0x00

        subtraction_result_abs = abs(vy_value - vx_value)
        self.v_registers[vx_index] = subtraction_result_abs

        self._increment_program_counter(1)

    def _8xye(self, vx_index):
        vx_value = self.v_registers[vx_index]
        vx_last_bit = vx_value & 0x01
        left_shifted_vx_value = vx_value << 1
        self.v_registers[vx_index] = left_shifted_vx_value
        self.v_registers[0xF] = vx_last_bit

        self._increment_program_counter(1)

    def _9xy0(self, vx_index, vy_index):
        if self.v_registers[vx_index] != self.v_registers[vy_index]:
            self._increment_program_counter(2)
        else:
            self._increment_program_counter(1)

    def _annn(self, value):
        self.i_register = value
        self._increment_program_counter(1)

    def _bnnn(self, address):
        self.program_counter = address + self.v_registers[0x0]

    def _cxkk(self, vx_index, value):
        self.v_registers[vx_index] = random.getrandbits(8) & value
        self._increment_program_counter(1)

    def _dxyn(self, vx_index, vy_index, sprite_height):
        x_coordinate = self.v_registers[vx_index]
        y_coordinate = self.v_registers[vy_index]
        sprite_address_start = self.i_register
        sprite_address_end = sprite_address_start + sprite_height
        sprite = self.memory[sprite_address_start:sprite_address_end]
        self.screen.draw_sprite(sprite, x_coordinate, y_coordinate)
        self._increment_program_counter(1)

    def _ex9e(self):
        # TODO: implement
        self._increment_program_counter(1)

    def _exa1(self):
        # TODO: implement
        self._increment_program_counter(1)

    def _fx07(self, vx_index):
        self.v_registers[vx_index] = self.delay_timer
        self._increment_program_counter(1)

    def _fx0a(self, vx_index):
        # TODO: implement
        self._increment_program_counter(1)

    def _fx15(self, vx_index):
        self.delay_timer = self.v_registers[vx_index]
        self._increment_program_counter(1)

    def _fx18(self, vx_index):
        self.sound_timer = self.v_registers[vx_index]
        self._increment_program_counter(1)

    def _fx1e(self, vx_index):
        self.i_register += self.v_registers[vx_index]
        self._increment_program_counter(1)

    def _fx29(self, vx_index):
        # TODO: implement
        self._increment_program_counter(1)

    def _fx33(self, vx_index):
        vx_value = '{:03}'.format(self.v_registers[vx_index])
        vx_value_digits = [int(digit) for digit in str(vx_value)]
        addresses = self._get_addresses_from_i_register_to_offset(3)

        for address in addresses:
            self.memory[address] = vx_value_digits.pop(0)

        self._increment_program_counter(1)

    def _fx55(self, vx_index):
        addresses = self._get_addresses_from_i_register_to_offset(vx_index)
        v_register_values = self.v_registers[:vx_index]

        for address in addresses:
            self.memory[address] = v_register_values.pop(0)

        self._increment_program_counter(1)

    def _fx65(self, vx_index):
        addresses = self._get_addresses_from_i_register_to_offset(vx_index)

        for v_index in range(0, vx_index):
            address = addresses.pop(0)
            self.v_registers[v_index] = self.memory[address]

        self._increment_program_counter(1)

    # No opcode methods #

    def _get_addresses_from_i_register_to_offset(self, offset):
        return [self.i_register + index for index in range(0, offset)]

    def _load_rom_to_memory(self, rom_path):
        memory_index = 0x200

        with open(rom_path, 'rb') as rom_handle:
            for rom_byte in rom_handle.read():
                self.memory[memory_index] = rom_byte
                memory_index += 1

    def _get_current_opcode(self):
        opcode_first_byte = self.memory[self.program_counter]
        opcode_last_byte = self.memory[self.program_counter + 1]

        return bytes([opcode_first_byte, opcode_last_byte])

    def _increment_program_counter(self, byte_units):
        self.program_counter += byte_units * 2

    def _execute_operation(self, operation, parameters):
        """
        TODO: refactor operation calling
        """
        operation_name_in_class = '_' + operation
        operation_function = getattr(self, operation_name_in_class)
        if operation_name_in_class.startswith('_00'):
            operation_function()
        elif operation_name_in_class.startswith('_0') \
                or operation_name_in_class.startswith('_1') \
                or operation_name_in_class.startswith('_2') \
                or operation_name_in_class.startswith('_a') \
                or operation_name_in_class.startswith('_b') \
                or operation_name_in_class.startswith('_e') \
                or operation_name_in_class.startswith('_f'):
            operation_function(parameters[0])
        elif operation_name_in_class.startswith('_3') \
                or operation_name_in_class.startswith('_4') \
                or operation_name_in_class.startswith('_5') \
                or operation_name_in_class.startswith('_6') \
                or operation_name_in_class.startswith('_7') \
                or operation_name_in_class.startswith('_8') \
                or operation_name_in_class.startswith('_9') \
                or operation_name_in_class.startswith('_c'):
            operation_function(parameters[0], parameters[1])
        elif operation_name_in_class.startswith('_d'):
            operation_function(parameters[0], parameters[1], parameters[2])

    def _debug(self, opcode):
        print('>>> after {0}'.format(hex(int.from_bytes(opcode, 'big'))[2:]))
        print('> Program counter: ' + hex(self.program_counter))
        v_registers = []
        for v in self.v_registers:
            try:
                v_registers.append(hex(v))
            except TypeError:
                v_registers.append('0x00')
        print('> V registers: ' + ','.join(v for v in v_registers))

        try:
            i_register = hex(self.i_register)
        except TypeError:
            i_register = 'None'
        print('> I register: ' + i_register)

    def main(self):
        while True:
            opcode = self._get_current_opcode()
            operation, parameters = parse_operation_and_parameters(opcode)
            self._execute_operation(operation, parameters)
            self._debug(opcode)
