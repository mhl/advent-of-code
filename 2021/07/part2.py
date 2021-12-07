#!/usr/bin/env python3

with open("input-jenny.txt") as f:
    positions = [int(p) for p in f.read().split(",")]


def triangular_number(n):
    return (n * (n + 1)) // 2


def fuel_to_move_to_position(aligning_position, starting_positions):
    return sum(
        triangular_number(abs(p - aligning_position)) for p in starting_positions
    )


best_fuel_cost = min(
    fuel_to_move_to_position(p, positions)
    for p in range(min(positions), max(positions) + 1)
)

print(best_fuel_cost)
