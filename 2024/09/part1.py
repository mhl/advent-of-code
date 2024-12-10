#!/usr/bin/env python3

from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
import os
import re
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")

import aoc

lines = aoc.get_input_lines(2024, 9)
# lines = aoc.get_example_lines()

line = lines[0]

line_as_list = list(line)


@dataclass(frozen=True)
class Span:
    is_file: bool
    id_number: int
    length: int

    def __str__(self):
        if self.is_file:
            return "-".join(([str(self.id_number)] * self.length))
        else:
            return "." * self.length

    def empty(self):
        return self.length == 0


spans = []

id_number = 0
is_file = True
for input_charater in line_as_list:
    if is_file:
        spans.append(Span(is_file, 1 * id_number, int(input_charater)))
        id_number += 1
    else:
        spans.append(Span(is_file, None, int(input_charater)))
    is_file = not is_file


def print_blocks():
    for block in spans:
        print(block, end="")
    print()


print_blocks()


def split_span(i, length_of_outer_part, start_from_left):
    rightmost_index_adjustment = 0
    if i >= len(spans):
        raise Exception(f"BUG: i {i} of the end of spans (of length {len(spans)}")
    original_span = spans[i]
    if length_of_outer_part > original_span.length:
        raise Exception(f"BUG: {original_span} was shorter than {length_of_outer_part}")
    if length_of_outer_part == original_span.length:
        return rightmost_index_adjustment
    if start_from_left:
        new_first_span = Span(
            original_span.is_file, original_span.id_number, length_of_outer_part
        )
        new_second_span = Span(
            original_span.is_file,
            original_span.id_number,
            original_span.length - length_of_outer_part,
        )
        rightmost_index_adjustment += 1
    else:
        new_first_span = Span(
            original_span.is_file,
            original_span.id_number,
            original_span.length - length_of_outer_part,
        )
        new_second_span = Span(
            original_span.is_file, original_span.id_number, length_of_outer_part
        )
        rightmost_index_adjustment += 1
    spans[i : i + 1] = (new_first_span, new_second_span)
    return rightmost_index_adjustment


def swap(i, j):
    tmp = spans[i]
    spans[i] = spans[j]
    spans[j] = tmp


leftmost_space_index = 1
rightmost_file_index = len(spans) - 1


def get_leftmost_space_index():
    for leftmost_space_index in range(len(spans)):
        if (not spans[leftmost_space_index].is_file) and (
            spans[leftmost_space_index].length > 0
        ):
            return leftmost_space_index


def get_rightmost_file_index():
    for rightmost_file_index in range(len(spans) - 1, 0, -1):
        if spans[rightmost_file_index].is_file and (
            spans[rightmost_file_index].length > 0
        ):
            return rightmost_file_index


def checksum():
    sum = 0
    i = 0
    for span in spans:
        if span.is_file:
            for span_i in range(span.length):
                sum += i * span.id_number
                i += 1
        else:
            i += span.length
    return sum


while True:
    leftmost_space_index = get_leftmost_space_index()
    rightmost_file_index = get_rightmost_file_index()
    if leftmost_space_index > rightmost_file_index:
        break
    length_to_swap = min(
        spans[leftmost_space_index].length, spans[rightmost_file_index].length
    )
    rightmost_file_index += split_span(leftmost_space_index, length_to_swap, True)
    rightmost_file_index += split_span(rightmost_file_index, length_to_swap, False)
    swap(leftmost_space_index, rightmost_file_index)


checksum_result = checksum()
print(checksum_result)
