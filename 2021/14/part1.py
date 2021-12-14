#!/usr/bin/env python3

from collections import Counter

with open("input.txt") as f:
    template = f.readline().rstrip()
    f.readline()
    rules_string = f.read()

rules = {}
for line in rules_string.rstrip().split("\n"):
    pair, insert_char = line.split(" -> ")
    rules[pair] = insert_char

def step(polymer_elements):
    new_polymer_elements = []
    for i in range(len(polymer_elements) - 1):
        current_element, next_element = polymer_elements[i:i+2]
        new_polymer_elements.append(current_element)
        pair = current_element + next_element
        if pair in rules:
            new_polymer_elements.append(rules[pair])
    new_polymer_elements.append(polymer_elements[-1])
    return new_polymer_elements

polymer_elements = list(template)
for i in range(10):
    polymer_elements = step(polymer_elements)

counter = Counter(polymer_elements)
print(counter.most_common()[0][1] - counter.most_common()[-1][1])
