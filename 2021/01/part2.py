#!/usr/bin/env python3

with open("input.txt") as f:
    numbers = [int(line) for line in f]

increases = 0
for i in range(3, len(numbers)):
    if numbers[i] > numbers[i - 3]:
        increases += 1

print(increases)
