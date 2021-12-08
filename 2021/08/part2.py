#!/usr/bin/env python3

from itertools import permutations
import re
from collections import namedtuple

with open("input.txt") as f:
    entries = [re.findall("[a-g]+", line) for line in f]

SEGMENTS_CORRECT = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9",
}

# Order the segment strings by length from shortest to longest, since
# checking the two letter string represting "1" on the display first
# is the fastest way to cut down the search space.
SEGMENTS_CORRECT_ORDERED = sorted(SEGMENTS_CORRECT.keys(), key=lambda s: len(s))

# This is a generator function so that we don't have to map any more
# letters once we've established this can't be the right mapping
def displays_from_mapping(mapping_correct_to_wrong):
    for correct_display in SEGMENTS_CORRECT_ORDERED:
        wrong_letters = [mapping_correct_to_wrong[l] for l in correct_display]
        yield "".join(sorted(wrong_letters))

def brute_force_entry(entry):
    # Sort each of the strings alphabetically to normalize them for lookup
    displays_set = set("".join(sorted(d)) for d in entry[:10])
    for letters_permutation in permutations('abcdefg'):
        mapping_correct_to_wrong = {
            correct: wrong for correct, wrong in zip('abcdefg', letters_permutation)
        }
        correct_mapping = True
        for wrong_display in displays_from_mapping(mapping_correct_to_wrong):
            if wrong_display not in displays_set:
                correct_mapping = False
                break
        if correct_mapping:
            break
    # Now we've got the mapping, reverse it and use it to translate the
    # 4 output displays into the correct 4 digit number
    mapping_wrong_to_correct = {v: k for k, v in mapping_correct_to_wrong.items()}
    correct_output_numbers = [
        SEGMENTS_CORRECT["".join(sorted([mapping_wrong_to_correct[l] for l in output_wrong]))]
        for output_wrong in entry[10:]
    ]
    return int("".join(correct_output_numbers))

print(sum(brute_force_entry(entry) for entry in entries))
