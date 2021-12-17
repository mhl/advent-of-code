#!/usr/bin/env python3

import re

with open("input.txt") as f:
    first_line = f.readline().rstrip()
    m = re.search(r"^target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)$", first_line)
    target_x_min, target_x_max, target_y_min, target_y_max = (
        int(n) for n in m.groups()
    )

best_initial_dy = target_y_min * -1 - 1

best_solution_found = False
for initial_dy in range(best_initial_dy, 0, -1):
    steps = 2 * initial_dy + 2
    for candidate_dx_initial in range(1, target_x_max + 1):
        eventual_x_position = 0
        dx = candidate_dx_initial
        for n in range(steps):
            eventual_x_position += dx
            dx = max(dx - 1, 0)
        if target_x_min <= eventual_x_position <= target_x_max:
            best_solution_found = True
            break
        if eventual_x_position > target_x_max:
            break
    if best_solution_found:
        break

print("Best initial_dy is:", initial_dy)
print("Works with an initial_dx of", candidate_dx_initial)
print("Reaches height of", (initial_dy * (initial_dy + 1)) // 2)
