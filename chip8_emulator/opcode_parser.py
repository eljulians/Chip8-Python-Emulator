def parse_0_prefix_operation_and_parameters(opcode):
    if opcode[1] == 0xE0:
        operation = '00e0'
    elif opcode[1] == 0xEE:
        operation = '00ee'

    return operation, ()


def parse_1_prefix_operation_and_parameters(opcode):
    opcode_int = int.from_bytes(opcode, byteorder='big')
    operation = '1nnn'
    parameters = opcode_int & 0x0FFF

    return operation, parameters


def parse_2_prefix_operation_and_parameters(opcode):
    opcode_int = int.from_bytes(opcode, byteorder='big')
    operation = '2nnn'
    parameters = opcode_int & 0x0FFF

    return operation, parameters


def parse_3_prefix_operation_and_parameters(opcode):
    operation = '3xkk'
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1]

    return operation, (first_parameter, second_parameter)


def parse_4_prefix_operation_and_parameters(opcode):
    operation = '4xkk'
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1]

    return operation, (first_parameter, second_parameter)


def parse_5_prefix_operation_and_parameters(opcode):
    operation = '5xy0'
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1] >> 4

    return operation, (first_parameter, second_parameter)


def parse_6_prefix_operation_and_parameters(opcode):
    operation = '6xkk'
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1]

    return operation, (first_parameter, second_parameter)


def parse_7_prefix_operation_and_parameters(opcode):
    operation = '7xkk'
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1]

    return operation, (first_parameter, second_parameter)


def parse_8_prefix_operation_and_parameters(opcode):
    opcode_suffix = hex(opcode[1] & 0x0F)[2:]
    operation = '8xy{0}'.format(opcode_suffix)

    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1] >> 4

    return operation, (first_parameter, second_parameter)


def parse_9_prefix_operation_and_parameters(opcode):
    operation = '9xy0'
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1] >> 4

    return operation, (first_parameter, second_parameter)


def parse_A_prefix_operation_and_parameters(opcode):
    opcode_int = int.from_bytes(opcode, byteorder='big')
    operation = 'annn'
    parameter = opcode_int & 0x0FFF

    return operation, parameter


def parse_B_prefix_operation_and_parameters(opcode):
    opcode_int = int.from_bytes(opcode, byteorder='big')
    operation = 'bnnn'
    parameter = opcode_int & 0x0FFF

    return operation, parameter


def parse_C_prefix_operation_and_parameters(opcode):
    operation = 'cxkk'
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1]

    return operation, (first_parameter, second_parameter)


def parse_D_prefix_operation_and_parameters(opcode):
    operation = 'dxyn'
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1] >> 4
    third_parameter = opcode[1] & 0x0F

    return operation, (first_parameter, second_parameter, third_parameter)


def parse_E_prefix_operation_and_parameters(opcode):
    if opcode[1] == 0x9E:
        operation = 'ex9e'
    elif opcode[1] == 0xA1:
        operation = 'exa1'

    parameter = opcode[0] & 0x0F

    return operation, parameter


def parse_F_prefix_operation_and_parameters(opcode):
    opcode_suffix = hex(opcode[1])[2:]
    opcode_suffix = '{:02x}'.format(opcode[1])
    operation = 'fx{0}'.format(opcode_suffix)

    parameter = opcode[0] & 0x0F

    return operation, parameter

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
    opcode_prefix_nibble = opcode[0] >> 4

    parse_function = parse_functions[opcode_prefix_nibble]
    operation, parameters = parse_function(opcode)

    return operation, parameters
