#!/usr/bin/env python3

from collections import defaultdict
from functools import lru_cache
import os
import re
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('..')

import aoc

lines = aoc.get_input_lines(2024, 7)
# lines = aoc.get_example_lines()

@lru_cache
def operator_combinations(n):
    result = []
    if n == 1:
        return [["+"], ["*"], ["|"]]
    for new_operator in ('+', '*', '|'):
        combinations_for_one_less = operator_combinations(n - 1)
        for c in combinations_for_one_less:
            result.append([new_operator] + c)
    return result

def can_it_work(result, numbers):
    n_operators = len(numbers) - 1
    cs = operator_combinations(n_operators)
    for c in cs:
        acc = numbers[0]
        for i in range(1, len(numbers)):
            operator = c[i - 1]
            if operator == '*':
                acc = acc * numbers[i]
            elif operator == '+':
                acc = acc + numbers[i]
            elif operator == '|':
                acc = int(str(acc) + str(numbers[i]))
        if acc == result:
            return True
    return False

sum = 0

for line in lines:
    if not len(line):
        continue
    m = re.search(r"^(\d+): (.*)", line)
    result = int(m.group(1))
    numbers = [int(s) for s in m.group(2).split()]
    print(result, "<-?", numbers)
    if can_it_work(result, numbers):
        sum += result

print(sum)
