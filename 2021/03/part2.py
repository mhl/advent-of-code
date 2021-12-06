#!/usr/bin/env python3

from collections import Counter

# Obviously this is throwaway code for fun or we'd avoid relying on
# these actual values (see comments below)
FIND_RAREST = 0
FIND_COMMONEST = 1

with open("input.txt") as f:
    input_strings = [line.strip() for line in f]


def summarize_column(letters, strategy):
    counter = Counter(letters)
    assert len(counter) == 2
    if counter["0"] == counter["1"]:
        # We've made the strategy constants match the tie-breaker value
        # for each strategy
        return str(strategy)
    # This also relies on the value of the strategy constants and that
    # there are only two digits in the counter
    return counter.most_common()[1 - strategy][0]


def process_rows(rows, digits_so_far, strategy):
    if len(rows) == 1:
        return digits_so_far + rows[0]
    first_column = "".join(row[0] for row in rows)
    digit_to_keep = summarize_column(first_column, strategy)
    new_rows = [r[1:] for r in rows if r[0] == digit_to_keep]
    return process_rows(new_rows, digits_so_far + digit_to_keep, strategy)


oxygen_generator_reading, co2_scrubber_rating = (
    int(process_rows(input_strings, "", strategy), 2)
    for strategy in (FIND_COMMONEST, FIND_RAREST)
)

print(oxygen_generator_reading * co2_scrubber_rating)
