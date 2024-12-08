#!/usr/bin/env python3

from collections import defaultdict
import os
import re
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('..')

import aoc

lines = aoc.get_input_lines(2024, 5)
# lines = aoc.get_example_lines()

rules_lines = []
update_lines = []

adding_rules = True
for line in lines:
    if not len(line):
        adding_rules = False
        continue
    if adding_rules:
        rules_lines.append(line)
    else:
        update_lines.append(line)

must_precede = defaultdict(set)

for rule_line in rules_lines:
    split_rule = rule_line.split("|")
    before = int(split_rule[0])
    after = int(split_rule[1])
    must_precede[before].add(after)

sum = 0

for update_line in update_lines:
    split_update = update_line.split(",")
    update_page_numbers = [int(s) for s in split_update]
    if (len(update_page_numbers) % 2) == 0:
        raise Exception(f"Even number items in list! {update_page_numbers}")
    correct_order = True
    print("////", update_page_numbers)
    for i, n in enumerate(update_page_numbers):
        only_after = must_precede.get(n)
        if only_after is not None:
            print(f"Got rule {n} must precede {only_after}")
            for earlier_n in update_page_numbers[:i]:
                print("   considering earlier number:", earlier_n)
                if earlier_n in only_after:
                    correct_order = False
                    break
    if correct_order:
        middle_number = update_page_numbers[len(update_page_numbers) // 2]
        sum += middle_number

print(sum)
