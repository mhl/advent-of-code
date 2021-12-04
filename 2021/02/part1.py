#!/usr/bin/env python3

from collections import namedtuple

with open("input.txt") as f:
    instructions = [line.strip() for line in f]

Position = namedtuple('Position', ['horizontal', 'depth'])

def get_next_position(current, direction, distance):
    match direction:
        case "forward":
            return Position(current.horizontal + distance, current.depth)
        case "down":
            return Position(current.horizontal, current.depth + distance)
        case "up":
            return Position(current.horizontal, current.depth - distance)
        case _:
            raise Exception(f"Unknown direction '{direction}'")    

current_position = Position(horizontal=0, depth=0)
for instruction in instructions:
    direction, distance = instruction.split()
    current_position = get_next_position(current_position, direction, int(distance))

print("Product is:", current_position.horizontal * current_position.depth)
