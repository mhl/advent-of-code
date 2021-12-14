#!/usr/bin/env python3

from collections import Counter

with open("input-jenny.txt") as f:
    template = f.readline().rstrip()
    f.readline()
    rules_string = f.read()

rules = {}
for line in rules_string.rstrip().split("\n"):
    pair, insert_char = line.split(" -> ")
    new_pair_1 = pair[0] + insert_char
    new_pair_2 = insert_char + pair[1]
    rules[pair] = (new_pair_1, new_pair_2)

initial_pairs = ["".join(p) for p in zip(template[:-1], template[1:])]

pair_counter = Counter(initial_pairs)


def step(pair_counter):
    new_counter = Counter()
    for pair, count in pair_counter.items():
        new_pair_1, new_pair_2 = rules[pair]
        new_counter[new_pair_1] += count
        new_counter[new_pair_2] += count
    return new_counter


for i in range(40):
    pair_counter = step(pair_counter)

letter_counter = Counter()
for pair, count in pair_counter.items():
    letter_counter[pair[0]] += count
    letter_counter[pair[1]] += count

letter_counter[template[0]] += 1
letter_counter[template[-1]] += 1

ordered_counts = letter_counter.most_common()
print(ordered_counts[0][1] // 2 - ordered_counts[-1][1] // 2)
