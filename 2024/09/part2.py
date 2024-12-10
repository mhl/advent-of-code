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

highest_id_number = id_number - 1

# def print_blocks():
#     for block in spans:
#         print(block, end="")
#     print()

# print_blocks()


def split_span(i, length_of_outer_part, start_from_left):
    if i >= len(spans):
        raise Exception(f"BUG: i {i} of the end of spans (of length {len(spans)}")
    original_span = spans[i]
    if length_of_outer_part > original_span.length:
        raise Exception(f"BUG: {original_span} was shorter than {length_of_outer_part}")
    if length_of_outer_part == original_span.length:
        return
    if start_from_left:
        new_first_span = Span(
            original_span.is_file, original_span.id_number, length_of_outer_part
        )
        new_second_span = Span(
            original_span.is_file,
            original_span.id_number,
            original_span.length - length_of_outer_part,
        )
    else:
        new_first_span = Span(
            original_span.is_file,
            original_span.id_number,
            original_span.length - length_of_outer_part,
        )
        new_second_span = Span(
            original_span.is_file, original_span.id_number, length_of_outer_part
        )
    spans[i : i + 1] = (new_first_span, new_second_span)


def swap(i, j):
    tmp = spans[i]
    spans[i] = spans[j]
    spans[j] = tmp


leftmost_space_index = 1
rightmost_file_index = len(spans) - 1


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


id_number_to_move = highest_id_number

while True:
    for rightmost_file_index in range(len(spans) - 1, 0, -1):
        if spans[rightmost_file_index].id_number == id_number_to_move:
            break
    length_required = spans[rightmost_file_index].length
    for first_space_big_enough_index in range(len(spans)):
        span = spans[first_space_big_enough_index]
        if (not span.is_file) and span.length >= length_required:
            break
    if first_space_big_enough_index > rightmost_file_index:
        id_number_to_move -= 1
        if id_number_to_move < 0:
            break
        continue
    split_span(first_space_big_enough_index, length_required, True)
    for rightmost_file_index in range(len(spans) - 1, 0, -1):
        if spans[rightmost_file_index].id_number == id_number_to_move:
            break
    swap(first_space_big_enough_index, rightmost_file_index)
    id_number_to_move -= 1
    if id_number_to_move < 0:
        break

print(checksum())
