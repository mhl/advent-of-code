#!/usr/bin/env python3

from collections import Counter

with open("input-jenny.txt") as f:
    initial_population = tuple(int(n) for n in f.read().split(","))


def get_next_day_counter(today_counter):
    next_day_counter = Counter()
    # Deal with the new generation
    next_day_counter[6] = today_counter[0] + today_counter[7]
    next_day_counter[8] = today_counter[0]
    # and then all the fish just getting older
    for timer in (1, 2, 3, 4, 5, 6, 8):
        next_day_counter[timer - 1] = today_counter[timer]

    return next_day_counter


today_counter = Counter(initial_population)
for day in range(80):
    today_counter = get_next_day_counter(today_counter)
print(sum(today_counter.values()))

today_counter = Counter(initial_population)
for day in range(256):
    today_counter = get_next_day_counter(today_counter)
print(sum(today_counter.values()))
