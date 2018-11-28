class Chip8:

    def __init__(self):
        self.memory = []
        self.stack = []
        self.stack_pointer = 0
        self.program_counter = 0
        self.v_registers = []
        self.i_register = None
