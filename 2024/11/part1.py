#!/usr/bin/env python3

from collections import defaultdict
from dataclasses import dataclass
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")

import aoc

lines = aoc.get_input_lines(2024, 11)
# lines = aoc.get_example_lines()

line = lines[0]

pebbles = [int(s) for s in line.strip().split()]

def change_pebble(initial_value):
    if not initial_value:
        return [1]
    s = str(initial_value)
    l = len(s)
    l_div_2 = l // 2
    l_mod_2 = l % 2
    if not(l_mod_2):
        return [int(s[:l_div_2]), int(s[l_div_2:])]
    return [initial_value * 2024]

def change_all_pebbles():
    global pebbles
    result = []
    for pebble in pebbles:
        result.extend(change_pebble(pebble))
    pebbles = result

for i in range(25):
    change_all_pebbles()

print(len(pebbles))

