#!/usr/bin/env python3

with open("input-jenny.txt") as f:
    positions = [int(p) for p in f.read().split(",")]

min_position = min(positions)
max_position = max(positions)


def triangular_number(n):
    return (n * (n + 1)) // 2


def fuel_to_move_to_position(aligning_position, starting_positions):
    return sum(
        triangular_number(abs(p - aligning_position)) for p in starting_positions
    )


best_fuel_cost_so_far = None
for p in range(min_position, max_position + 1):
    fuel_cost = fuel_to_move_to_position(p, positions)
    if best_fuel_cost_so_far is None or fuel_cost < best_fuel_cost_so_far:
        best_fuel_cost_so_far = fuel_cost

print(best_fuel_cost_so_far)
