#!/usr/bin/env python3

from collections import defaultdict
from dataclasses import dataclass
from functools import cache
import os
import re
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")

import aoc

lines = aoc.get_input_lines(2024, 11)
# lines = aoc.get_example_lines()

line = lines[0]

pebbles = [int(s) for s in line.strip().split()]

@cache
def eventual_length_of_pebbles(initial_value, blinks_left):
    if not blinks_left:
        return 1
    if not initial_value:
        return eventual_length_of_pebbles(1, blinks_left - 1)
    s = str(initial_value)
    l = len(s)
    l_div_2 = l // 2
    l_mod_2 = l % 2
    if not(l_mod_2):
        return eventual_length_of_pebbles(int(s[:l_div_2]), blinks_left - 1) + \
            eventual_length_of_pebbles(int(s[l_div_2:]), blinks_left - 1)
    return eventual_length_of_pebbles(initial_value * 2024, blinks_left - 1)

sum = 0

for i, initial_pebble in enumerate(pebbles):
    sum += eventual_length_of_pebbles(initial_pebble, 75)

print(sum)
