#!/usr/bin/env python3

from collections import namedtuple

State = namedtuple('State', ['horizontal', 'depth', 'aim'])

def get_next_position(current, direction, distance):
    match direction:
        case "forward":
            return State(
                horizontal=(current.horizontal + distance),
                depth=(current.depth + current.aim * distance),
                aim=current.aim
            )
        case "down" | "up":
            multiplier = 1 if direction == "down" else -1
            return State(
                horizontal=current.horizontal,
                depth=current.depth,
                aim=(current.aim + distance * multiplier)
            )
        case _:
            raise Exception(f"Unknown direction '{direction}'")    

with open("input.txt") as f:
    current_state = State(horizontal=0, depth=0, aim=0)
    for line in f:
        direction, distance = line.strip().split()
        current_state = get_next_position(current_state, direction, int(distance))

print("Product is:", current_state.horizontal * current_state.depth)
