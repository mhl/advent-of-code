#!/usr/bin/env python3

with open("input-jenny.txt") as f:
    grid = [[int(digit) for digit in line.rstrip()] for line in f]

width = len(grid[0])
height = len(grid)

all_coords = tuple((x, y) for y in range(height) for x in range(width))


def get_adjacent_coords(x, y):
    return tuple(
        (i, j)
        for i, j in (
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
        )
        if 0 <= i < width and 0 <= j < height
    )


def increase_energy_levels(coords_list):
    for x, y in coords_list:
        grid[y][x] += 1


def get_energy_level(coords):
    x, y = coords
    return grid[y][x]


def find_octopuses_ready_to_flash(flashed_this_step):
    return tuple(
        coords
        for coords in all_coords
        if get_energy_level(coords) > 9 and coords not in flashed_this_step
    )


def flash_octopuses(ready_to_flash):
    for x, y in ready_to_flash:
        increase_energy_levels(get_adjacent_coords(x, y))


def reset_energy_levels(flashed_this_step):
    for x, y in flashed_this_step:
        grid[y][x] = 0


def step():
    increase_energy_levels(all_coords)
    flashed_this_step = set()
    while ready_to_flash := find_octopuses_ready_to_flash(flashed_this_step):
        flash_octopuses(ready_to_flash)
        flashed_this_step.update(ready_to_flash)
    reset_energy_levels(flashed_this_step)
    return len(flashed_this_step)


print(sum(step() for _ in range(100)))

with open("input-jenny.txt") as f:
    grid = [[int(digit) for digit in line.rstrip()] for line in f]

step_count = 0
while True:
    step_count += 1
    if step() == width * height:
        print("All octopuses flashed in step", step_count)
        break
