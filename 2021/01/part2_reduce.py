#!/usr/bin/env python3

from functools import reduce

with open("input.txt") as f:
    numbers = [int(line) for line in f]

increases = reduce(
    lambda acc, i: acc + int(numbers[i] > numbers[i-3]),
    range(3, len(numbers)),
    0
)

print(increases)
