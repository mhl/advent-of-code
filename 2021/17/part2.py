#!/usr/bin/env python3

import re

with open("input.txt") as f:
    first_line = f.readline().rstrip()
    m = re.search(r"^target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)$", first_line)
    target_x_min, target_x_max, target_y_min, target_y_max = (
        int(n) for n in m.groups()
    )


max_initial_dy = target_y_min * -1 - 1
min_initial_dy = target_y_min

min_initial_dx = 1
while True:
    max_possible_x_with_this_initial_dx = (min_initial_dx * (min_initial_dx + 1)) // 2
    if max_possible_x_with_this_initial_dx > target_x_min:
        break
    min_initial_dx += 1
max_initial_dx = target_x_max


def hits_target_zone(initial_dx, initial_dy):
    dx = initial_dx
    dy = initial_dy
    x = 0
    y = 0
    while True:
        x += dx
        y += dy
        if (target_x_min <= x <= target_x_max) and (target_y_min <= y <= target_y_max):
            return True
        if x > target_x_max or y < target_y_min:
            return False
        dx = max(dx - 1, 0)
        dy -= 1


all_possible_initial_velocities = []
for initial_dy in range(min_initial_dy, max_initial_dy + 1):
    for initial_dx in range(min_initial_dx, max_initial_dx + 1):
        if hits_target_zone(initial_dx, initial_dy):
            all_possible_initial_velocities.append((initial_dx, initial_dy))

print(len(all_possible_initial_velocities))
