#!/usr/bin/env python3

from collections import Counter

with open("input.txt") as f:
    input_strings = [line.strip() for line in f]

columns = list(zip(*input_strings))

def commonest_binary_digit(letters):
    return Counter(letters).most_common(1)[0][0]

gamma_rate_str = "".join(commonest_binary_digit(c) for c in columns)
gamma_rate = int(gamma_rate_str, 2)
# This is a binary NOT on 'columns' digits
mask = 2**len(columns) - 1
epsilon_rate = mask - gamma_rate

print(gamma_rate * epsilon_rate)
