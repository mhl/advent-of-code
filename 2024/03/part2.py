#!/usr/bin/env python3

import os
import re
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('..')

import aoc

lines = aoc.get_input_lines(2024, 3)
# lines = aoc.get_example_lines()

sum = 0

enabled = True
for line in lines:
    if not len(line):
        continue
    for match in re.findall(r'(do)\(\)|(don\'t)\(\)|(mul)\((\d{1,3}),(\d{1,3})\)', line):
        if match[0] == "do":
            print("Enabling")
            enabled = True
        elif match[1] == "don't":
            print("Disabling")
            enabled = False
        elif enabled:
            print(f"Will add {match[3]} * {match[4]}")
            sum += int(match[3]) * int(match[4])

print(sum)
