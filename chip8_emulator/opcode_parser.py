def parse_0_prefix_operation_and_parameters(opcode):
    pass


def parse_1_prefix_operation_and_parameters(opcode):
    pass


def parse_2_prefix_operation_and_parameters(opcode):
    pass


def parse_3_prefix_operation_and_parameters(opcode):
    pass


def parse_4_prefix_operation_and_parameters(opcode):
    pass


def parse_5_prefix_operation_and_parameters(opcode):
    pass


def parse_6_prefix_operation_and_parameters(opcode):
    pass


def parse_7_prefix_operation_and_parameters(opcode):
    pass


def parse_8_prefix_operation_and_parameters(opcode):
    pass


def parse_9_prefix_operation_and_parameters(opcode):
    pass


def parse_A_prefix_operation_and_parameters(opcode):
    pass


def parse_B_prefix_operation_and_parameters(opcode):
    pass


def parse_C_prefix_operation_and_parameters(opcode):
    pass


def parse_D_prefix_operation_and_parameters(opcode):
    pass


def parse_E_prefix_operation_and_parameters(opcode):
    pass


def parse_F_prefix_operation_and_parameters(opcode):
    pass

parse_functions = [
    parse_0_prefix_operation_and_parameters,
    parse_1_prefix_operation_and_parameters,
    parse_2_prefix_operation_and_parameters,
    parse_3_prefix_operation_and_parameters,
    parse_4_prefix_operation_and_parameters,
    parse_5_prefix_operation_and_parameters,
    parse_6_prefix_operation_and_parameters,
    parse_7_prefix_operation_and_parameters,
    parse_8_prefix_operation_and_parameters,
    parse_9_prefix_operation_and_parameters,
    parse_A_prefix_operation_and_parameters,
    parse_B_prefix_operation_and_parameters,
    parse_C_prefix_operation_and_parameters,
    parse_D_prefix_operation_and_parameters,
    parse_E_prefix_operation_and_parameters,
    parse_F_prefix_operation_and_parameters,
]


def parse_operation_and_parameters(opcode):
    opcode_prefix_nibble = opcode[0] & 0xA0

    parse_function = parse_functions[opcode_prefix_nibble]

    return None, None

