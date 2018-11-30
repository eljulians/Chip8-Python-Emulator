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

    def ret(self):
        pass

    def jump(self, address):
        pass

    def call(self, address):
        pass

    def skip_next_instruction_if_equals(self, v_index, instruction):
        pass

    def skip_next_instruction_if_not_equals(self, v_index, instruction):
        pass

    def set_v_fixed_value(self, v_index, value):
        pass

    def add_to_v(self, v_index, value):
        pass

    def set_vx_to_vy(self, vx_index, vy_index):
        pass

    def vx_or_vy(self, vx_index, vy_index):
        pass

    def vx_and_vy(self, vx_index, vy_index):
        pass

    def vx_xor_vy(self, vx_index, vy_index):
        pass
