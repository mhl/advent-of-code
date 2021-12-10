#!/usr/bin/env python

from statistics import median

with open("input.txt") as f:
    input_strings = [line.strip() for line in f]

matching_brackets = (
    ("(", ")"),
    ("[", "]"),
    ("{", "}"),
    ("<", ">"),
)

close_to_open = {v: k for k, v in matching_brackets}
open_to_close = {k: v for k, v in matching_brackets}

illegal_character_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

autocompletion_character_scores = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

total_illegal_character_score = 0
autocomplete_scores = []
for input_string in input_strings:
    stack = list()
    corrupted = False
    for c in input_string:
        if c in open_to_close:
            stack.append(c)
        elif c in close_to_open:
            try:
                top_of_stack = stack.pop()
            except IndexError:
                top_of_stack = None
            if top_of_stack is None or c != open_to_close[top_of_stack]:
                total_illegal_character_score += illegal_character_scores[c]
                corrupted = True
                break
    if stack and not corrupted:
        # Then the string was incomplete, so calculate the autocomplete score
        total_score = 0
        while stack:
            closing_bracket = open_to_close[stack.pop()]
            total_score = (
                5 * total_score + autocompletion_character_scores[closing_bracket]
            )
        autocomplete_scores.append(total_score)

print("total_illegal_character_score", total_illegal_character_score)
print("median autocomplete score", median(autocomplete_scores))
