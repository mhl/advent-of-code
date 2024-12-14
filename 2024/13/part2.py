#!/usr/bin/env python3

from collections import defaultdict
from dataclasses import dataclass
import math
import os
import re
import sys

import numpy as np
np.set_printoptions(suppress=True, precision=20)

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")

import aoc
from dijkstra import dijkstra

lines = aoc.get_input_lines(2024, 13)
# lines = aoc.get_example_lines()

machines = []

@dataclass
class Machine:
    a_x: int = None
    a_y: int = None
    b_x: int = None
    b_y: int = None
    goal_x: int = None
    goal_y: int = None
    def goal_tuple(self):
        return (self.goal_x, self.goal_y)

current_machine = Machine()
for line in lines:
    if not len(line):
        machines.append(current_machine)
        current_machine = Machine()
        continue
    m = re.search(r"Button ([AB]): X\+(\d+), Y\+(\d+)", line)
    if m:
        button, x, y = m.groups()
        if button == "A":
            current_machine.a_x = int(x)
            current_machine.a_y = int(y)
        elif button == "B":
            current_machine.b_x = int(x)
            current_machine.b_y = int(y)
        continue
    m = re.search(r"Prize: X=(\d+), Y=(\d+)", line)
    if m:
        current_machine.goal_x = 10000000000000 + int(m.group(1))
        current_machine.goal_y = 10000000000000 + int(m.group(2))
        continue
    raise Exception(f"Unparseable line: {line}")
# In case there's no final empty line:
if current_machine.a_x is not None:
    machines.append(current_machine)

sum = 0

for machine in machines:
    print("machine is:", machine)

    matrix = np.array([
        [machine.a_x, machine.b_x],
        [machine.a_y, machine.b_y],
    ])
    vector = np.array([machine.goal_x, machine.goal_y]).reshape(2, 1)
    inverted = np.linalg.inv(matrix)
    result = np.dot(inverted, vector)
    flattened = result.flatten()

    recalculated_x = round(flattened[0]) * machine.a_x + round(flattened[1]) * machine.b_x
    recalculated_y = round(flattened[0]) * machine.a_y + round(flattened[1]) * machine.b_y

    if not(machine.goal_x == recalculated_x and machine.goal_y == recalculated_y):
        continue

    sum += flattened[0] * 3 + flattened[1]

print(sum)
