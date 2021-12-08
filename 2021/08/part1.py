#!/usr/bin/env python3

import re
from collections import namedtuple

with open("input-jenny.txt") as f:
    raw_entries = f.read()

matches = re.findall("^([a-g]+) ([a-g]+) ([a-g]+) ([a-g]+) ([a-g]+) ([a-g]+) ([a-g]+) ([a-g]+) ([a-g]+) ([a-g]+) \| ([a-g]+) ([a-g]+) ([a-g]+) ([a-g]+$)", raw_entries, flags=re.MULTILINE)

Entry = namedtuple("Entry", ["signal_patterns", "output_value"])

entries = tuple(Entry(signal_patterns=match[:10], output_value=match[10:]) for match in matches)

unique_number_lengths = (2, 3, 4, 7)

unique_number_lengths_count = sum([1 for e in entries for v in e.output_value if len(v) in unique_number_lengths])

print(unique_number_lengths_count)
