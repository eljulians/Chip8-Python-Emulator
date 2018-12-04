def parse_00_opcode(opcode):
    operation = _construct_operation(opcode, '0e')

    return operation, ()


def parse_znnn_opcode(opcode):
    opcode_int = int.from_bytes(opcode, byteorder='big')
    operation = _construct_operation(opcode, 'nn', 'n')
    parameters = opcode_int & 0x0FFF

    return operation, parameters


def parse_zxkk_opcode(opcode):
    operation = _construct_operation(opcode, 'xk', 'k')
    first_parameter = opcode[0] & 0x0F
    second_parameter = opcode[1]

    return operation, (first_parameter, second_parameter)


def parse_zxyz_opcode(opcode):
    operation = _construct_operation(opcode, 'xy')
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
    opcode_prefix = _get_byte_first_nibble_hex(opcode[0])
    opcode_suffix = '{:02x}'.format(opcode[1])
    opcode_suffix = _get_byte_first_nibble_hex(opcode[1]) \
        + _get_byte_last_nibble_hex(opcode[1])
    operation = '{0}x{1}'.format(opcode_prefix, opcode_suffix)

    parameter = opcode[0] & 0x0F

    return operation, parameter


OPCODE_PARSER_FUNCTIONS_PER_PREFIX = {
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


def _construct_operation(opcode, constant_part, last_nibble=None):
    suffix = last_nibble if last_nibble is not None \
        else _get_byte_last_nibble_hex(opcode[1])

    return '{0}{1}{2}'.format(
        _get_byte_first_nibble_hex(opcode[0]),
        constant_part,
        suffix,
    )


def _get_byte_first_nibble_hex(byte):
    return hex(byte >> 4)[2:]


def _get_byte_last_nibble_hex(byte):
    return hex(byte & 0x0F)[2:]


def parse_operation_and_parameters(opcode):
    opcode_prefix_nibble = opcode[0] >> 4

    parse_function = OPCODE_PARSER_FUNCTIONS_PER_PREFIX[opcode_prefix_nibble]
    operation, parameters = parse_function(opcode)

    return operation, parameters
