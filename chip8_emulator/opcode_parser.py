def parse_00_opcode(opcode):
    if opcode[1] == 0xE0:
        operation = '00e0'
    elif opcode[1] == 0xEE:
        operation = '00ee'

    return operation, ()


def parse_znnn_opcode(opcode):
    opcode_int = int.from_bytes(opcode, byteorder='big')
    opcode_prefix = hex(opcode[0] >> 4)[2:]
    operation = '{0}nnn'.format(opcode_prefix)
    parameters = opcode_int & 0x0FFF

    return operation, parameters


def parse_zxkk_opcode(opcode):
    opcode_prefix = hex(opcode[0] >> 4)[2:]
    operation = '{0}xkk'.format(opcode_prefix)
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1]

    return operation, (first_parameter, second_parameter)


def parse_zxyz_opcode(opcode):
    opcode_prefix = hex(opcode[0] >> 4)[2:]
    opcode_suffix = hex(opcode[1] & 0x0F)[2:]
    operation = '{0}xy{1}'.format(opcode_prefix, opcode_suffix)
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1] >> 4

    return operation, (first_parameter, second_parameter)


def parse_zxyn_opcode(opcode):
    operation = 'dxyn'
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1] >> 4
    third_parameter = opcode[1] & 0x0F

    return operation, (first_parameter, second_parameter, third_parameter)


def parse_zxzz_opcode(opcode):
    opcode_prefix = hex(opcode[0] >> 4)[2:]
    opcode_suffix = '{:02x}'.format(opcode[1])
    operation = '{0}x{1}'.format(opcode_prefix, opcode_suffix)

    parameter = opcode[0] & 0x0F

    return operation, parameter


opcode_parser_functions_per_prefix = {
    0x0: parse_00_opcode,
    0x1: parse_znnn_opcode,
    0x2: parse_znnn_opcode,
    0x3: parse_zxkk_opcode,
    0x4: parse_zxkk_opcode,
    0x5: parse_zxyz_opcode,
    0x6: parse_zxkk_opcode,
    0x7: parse_zxkk_opcode,
    0x8: parse_zxyz_opcode,
    0x9: parse_zxyz_opcode,
    0xA: parse_znnn_opcode,
    0xB: parse_znnn_opcode,
    0xC: parse_zxkk_opcode,
    0xD: parse_zxyn_opcode,
    0xE: parse_zxzz_opcode,
    0xF: parse_zxzz_opcode,
}


def parse_operation_and_parameters(opcode):
    opcode_prefix_nibble = opcode[0] >> 4

    parse_function = opcode_parser_functions_per_prefix[opcode_prefix_nibble]
    operation, parameters = parse_function(opcode)

    return operation, parameters
