#!/usr/bin/env python3

from dataclasses import dataclass
from math import prod
from types import SimpleNamespace

with open("input.txt") as f:
    hex_string = f.readline().rstrip()

input_string = [
    binary_character
    for digit in hex_string
    for binary_character in "{0:04b}".format(int(digit, 16))
]


def to_int(binary_digits):
    return int("".join(binary_digits), 2)


types = SimpleNamespace()
types.SUM = 0
types.PRODUCT = 1
types.MIN = 2
types.MAX = 3
types.LITERAL = 4
types.GREATER_THAN = 5
types.LESS_THAN = 6
types.EQUAL_TO = 7


@dataclass
class LiteralPacket:
    version: int
    type_id: int
    value: int

    def evaluate(self):
        return self.value


@dataclass
class OperatorPacket:
    version: int
    type_id: int
    subpackets: list

    def evaluate(self):
        subpacket_values = [p.evaluate() for p in self.subpackets]
        match self.type_id:
            case types.SUM:
                return sum(subpacket_values)
            case types.PRODUCT:
                return prod(subpacket_values)
            case types.MIN:
                return min(subpacket_values)
            case types.MAX:
                return max(subpacket_values)
            case types.GREATER_THAN:
                return int(subpacket_values[0] > subpacket_values[1])
            case types.LESS_THAN:
                return int(subpacket_values[0] < subpacket_values[1])
            case types.EQUAL_TO:
                return int(subpacket_values[0] == subpacket_values[1])
            case _:
                raise Exception(f"Unknown operator type ID {self.type_id}")


def parse_literal_packet_payload(input_string, start_index, version, type_id):
    payload_index = start_index
    binary_digits = []
    while True:
        new_binary_digits = input_string[payload_index + 1 : payload_index + 5]
        binary_digits += new_binary_digits
        if input_string[payload_index] == "0":
            break
        payload_index += 5
    value = to_int(binary_digits)
    return LiteralPacket(version, type_id, value), payload_index + 5


def parse_operator_packet_payload(input_string, start_index, version, type_id):
    length_type_id = to_int(input_string[start_index : start_index + 1])
    subpackets_bit_length = None
    number_of_subpackets = None
    if length_type_id == 0:
        subpackets_bit_length = to_int(input_string[start_index + 1 : start_index + 16])
        subpackets_start_index = start_index + 16
    else:
        number_of_subpackets = to_int(input_string[start_index + 1 : start_index + 12])
        subpackets_start_index = start_index + 12
    all_subpackets = []
    current_subpacket_start_index = subpackets_start_index
    while True:
        subpacket, index_after_subpacket = parse_packet(
            input_string, current_subpacket_start_index
        )
        all_subpackets.append(subpacket)
        current_subpacket_start_index = index_after_subpacket
        subpacket_bits_parsed = index_after_subpacket - subpackets_start_index
        if subpackets_bit_length and (subpacket_bits_parsed >= subpackets_bit_length):
            break
        if number_of_subpackets and (len(all_subpackets) == number_of_subpackets):
            break
    return OperatorPacket(version, type_id, all_subpackets), index_after_subpacket


def parse_packet(input_string, start_index):
    version = to_int(input_string[start_index : start_index + 3])
    type_id = to_int(input_string[start_index + 3 : start_index + 6])
    if type_id == types.LITERAL:
        return parse_literal_packet_payload(
            input_string, start_index + 6, version, type_id
        )
    else:
        return parse_operator_packet_payload(
            input_string, start_index + 6, version, type_id
        )


parsed_tree, after_end_index = parse_packet(input_string, 0)


def find_sum_of_version_numbers(packet):
    if packet.type_id == types.LITERAL:
        return packet.version
    else:
        return packet.version + sum(
            find_sum_of_version_numbers(p) for p in packet.subpackets
        )


print(find_sum_of_version_numbers(parsed_tree))
print(parsed_tree.evaluate())
