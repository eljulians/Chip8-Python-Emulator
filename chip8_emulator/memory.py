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

    def add_to_stack(self, memory_address):
        self.stack.append(memory_address)

    def pop_from_stack(self):
        return self.stack.pop()

    def increment_program_counter(self):
        self.program_counter += 2

    def decrement_program_counter(self):
        self.program_counter -= 2
