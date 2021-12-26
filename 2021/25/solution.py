#!/usr/bin/env python3

EAST = ">"
SOUTH = "v"
EMPTY = "."

with open("input.txt") as f:
    grid = [
        [letter for letter in line.rstrip()]
        for line in f
    ]

width = len(grid[0])
height = len(grid)

def print_grid(grid_to_print):
    for row in grid_to_print:
        print("".join(row))

def copy_grid(old_grid):
    return [row.copy() for row in old_grid]

def step():
    global grid
    any_moved = False
    grid_after_east_movement = copy_grid(grid)
    # First handle the East-moving sea cucumbers
    for y in range(height):
        for x in range(width):
            next_x = (x + 1) % width
            in_old_grid = grid[y][x]
            in_old_grid_next = grid[y][next_x]
            if in_old_grid == EAST and in_old_grid_next == EMPTY:
                grid_after_east_movement[y][x] = EMPTY
                grid_after_east_movement[y][next_x] = EAST
                any_moved = True
    grid_after_south_movement = copy_grid(grid_after_east_movement)
    # Next handle the south-moving sea cucumbers
    for y in range(height):
        for x in range(width):
            next_y = (y + 1) % height
            in_old_grid = grid_after_east_movement[y][x]
            in_old_grid_next = grid_after_east_movement[next_y][x]
            if in_old_grid == SOUTH and in_old_grid_next == EMPTY:
                grid_after_south_movement[y][x] = EMPTY
                grid_after_south_movement[next_y][x] = SOUTH
                any_moved = True
    grid = grid_after_south_movement
    return any_moved

steps_done = 0
while step():
    steps_done += 1
    # print("=======", steps_done)
    # print_grid(grid)
steps_done += 1 # because the last call of step() breaks the loop without incrementing
print(steps_done)
