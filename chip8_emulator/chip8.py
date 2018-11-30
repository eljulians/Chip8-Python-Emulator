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
        pass

    def jump(self, address):
        """ 1NNN """
        pass

    def call(self, address):
        """ 2NNN """
        pass

    def skip_next_instruction_if_equals(self, v_index, instruction):
        """ 3XNN """
        pass

    def skip_next_instruction_if_not_equals(self, v_index, instruction):
        """ 4XNN """
        pass

    def skip_next_instruction_if_vx_equals_vy(self, vx_index, vy_index):
        """ 5XY0 """
        pass

    def set_v_fixed_value(self, v_index, value):
        """ 6XNN """
        pass

    def add_to_v(self, v_index, value):
        """ 7XNN """
        pass

    def set_vx_to_vy(self, vx_index, vy_index):
        """ 8XY0 """
        pass

    def vx_or_vy(self, vx_index, vy_index):
        """ 8XY1 """
        pass

    def vx_and_vy(self, vx_index, vy_index):
        """ 8XY2 """
        pass

    def vx_xor_vy(self, vx_index, vy_index):
        """ 8XY3 """
        pass

    def add_vy_to_vx(self, vx_index, vy_index):
        """ 8XY4 """
        pass

    def subtract_vy_from_vx(self, vx_index, vy_index):
        """ 8XY5 """
        pass

    def shift_right_vx(self):
        """ 8XY6 """
        pass

    def subtract_vy_from_vx_negative(self, vx_index, vy_index):
        """ 8XY7 """
        pass

    def shift_left_vx(self):
        """ 8XYE """
        pass

    def skip_next_instruction_if_vx_not_equals_vy(self, vx_index, vy_index):
        """ 9XY0 """
        pass

    def set_i_register(self, value):
        """ ANNN """
        pass

    def jump_to_address_plus_v0(self, address):
        """ BNNN """
        pass

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
        pass

    def set_i_register_to_location_of_sprite_for_vx(self, vx_index):
        """ FX29 """
        pass

    def store_bcd_of_vx_in_i_register(self, vx_index):
        """ FX33 """
        pass

    def store_from_v0_to_vx_in_i_register(self, vx_index):
        """ FX55 """
        pass

    def read_from_v0_to_vx_in_i_register(self, vx_index):
        """ Fx65"""
        pass
