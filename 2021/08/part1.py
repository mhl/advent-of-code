#!/usr/bin/env python3

import re
from collections import namedtuple

with open("input.txt") as f:
    entries = [re.findall("[a-g]+", line) for line in f]

unique_number_lengths = (2, 3, 4, 7)
unique_number_lengths_count = sum(
    [1 for e in entries for v in e[-4:] if len(v) in unique_number_lengths]
)

print(unique_number_lengths_count)
