#!/usr/bin/env python3

from dataclasses import dataclass
import operator
from random import randint
from typing import NamedTuple

with open("input.txt") as f:
    instructions = []
    for line in f:
        if not line.strip():
            continue
        instruction_parts = line.strip().split()
        instructions.append(instruction_parts)

instruction_to_operator = {
    "mul": operator.mul,
    "add": operator.add,
    "mod": operator.mod,
    "div": operator.floordiv,
    "eql": operator.eq,
}

# This is a straightforward interpretation of the assembly language
# style instructions. We don't need this for the solution, but it was
# handy for checking that
def run_program(instructions, variables, input_digits):
    input_digits = input_digits.copy()
    for instr in instructions:
        match instr[0]:
            case "inp":
                variables[instr[1]] = input_digits.pop(0)
            case "mul" | "add" | "div" | "mod" | "eql":
                op = instruction_to_operator[instr[0]]
                second_argument = variables.get(instr[2])
                if second_argument is None:
                    second_argument = int(instr[2])
                variables[instr[1]] = int(op(variables[instr[1]], second_argument))
            case _:
                raise Exception("Unsupported instruction", instr[0])


# Now we generate a simplified version of the actual program from our
# input to help in understanding the problem. Again, lots of this isn't
# actually needed for calculating the solution

# A "Section" represent a block of instructions starting with an "inp w"
# These blocks only differ in three integer values in each block.
@dataclass
class Section:
    pop_z: bool
    x_inc: int
    y_inc: int


# Extract these sections from the program instructions:
sections = []
current_section = None
for instr in instructions:
    if instr[0] == "inp":
        if current_section is not None:
            sections.append(current_section)
        current_section = Section(None, None, None)
        section_line = 0
    section_line += 1
    if section_line == 5:
        assert instr[0] == "div"
        assert instr[1] == "z"
        current_section.pop_z = instr[2] == "26"
    elif section_line == 6:
        assert instr[0] == "add"
        assert instr[1] == "x"
        current_section.x_inc = int(instr[2])
    elif section_line == 16:
        assert instr[0] == "add"
        assert instr[1] == "y"
        current_section.y_inc = int(instr[2])
sections.append(current_section)

# Print the section objects for later reference
for i, section in enumerate(sections):
    print(i + 1, section)

# `run_section` is the core of our simplified version of the program
# The z value is essentially a stack of base 26 digits, so z_stack
# is a list being used as a stack.
def run_section(z_stack, w, section):
    if section.pop_z:
        x = z_stack.pop()
    else:
        # Peek at the top of the stack
        x = z_stack[-1] if z_stack else 0

    if (x + section.x_inc) != w:
        z_stack.append(w + section.y_inc)


def z_to_z_stack(z):
    z_stack = []
    while z > 0:
        z_stack.append(z % 26)
        z = z // 26
    z_stack.reverse()
    return z_stack


def z_stack_to_z(z_stack):
    z = 0
    for entry in z_stack:
        z = z * 26
        z += entry
    return z


# run_all_sections is similar to running the whole program; it maintains
# a z_stack and runs all the sections on it.
def run_all_sections(sections, input_digits):
    input_digits = input_digits.copy()
    z_stack = []
    for section in sections:
        run_section(z_stack, input_digits.pop(0), section)
    return z_stack_to_z(z_stack)


# We used this to check that our simplified version of the program
# produced the same results
def compare_two_methods(input_digits):
    variables = {"w": 0, "x": 0, "y": 0, "z": 0}
    run_program(instructions, variables, input_digits)
    original_z = variables["z"]
    simplified_z = run_all_sections(sections, input_digits)
    if original_z != simplified_z:
        print("Mismatch for input digits", input_digits)
    if original_z == 0:
        print("Found a zero input!", input_digits)


# This finds the pairs of indices of the sections that push and pop
# from the stack. (We're going to try to find input digits such that
# there is only one push or pop done by each section.)
def get_push_pop_pairs():
    pairs = []
    stack = []
    for i, section in enumerate(sections):
        if section.pop_z:
            pairs.append((stack.pop(), i))
        else:
            stack.append(i)
    return reversed(pairs)


# To explain this a little, we want input digits such that each
# section that does a pop doesn't push as well, which we do by making
# the (x + section.x_inc) != w condition false. A key point is that
# the value which is pushed onto the stack at each point only depends
# on y_inc for that section and w (the input digit). This means that
# at the point where you pop, you know that the value you got off the
# stack was the value added by the corresponding push earlier.

# So now we can say when pushing:
#    value_put_on_stack = i_push + push_section.y_inc
# ... and we want to arrange the input digits i_push and i_pop
# such that:
#    value_put_on_stack + pop_section.x_inc = i_pop
# Eliminating value_put_on_stack between them we get this relationship:
#    i_pop = i_push + push_section.y_inc + pop_section.x_inc
#
# So now we can find the maximum digits for each pair of digits quite
# simply.

# Part 1 - find the maximum value that produces 0

largest_input_digits = [None] * 14

for push_section_index, pop_section_index in get_push_pop_pairs():
    push_section = sections[push_section_index]
    pop_section = sections[pop_section_index]

    adjustment = push_section.y_inc + pop_section.x_inc
    if adjustment >= 0:
        largest_input_digits[pop_section_index] = 9
        largest_input_digits[push_section_index] = 9 - adjustment
    else:
        largest_input_digits[push_section_index] = 9
        largest_input_digits[pop_section_index] = 9 + adjustment

print("".join(str(d) for d in largest_input_digits))
compare_two_methods(largest_input_digits)

# Part 2 - find the minimum value that produces 0

smallest_input_digits = [None] * 14

for push_section_index, pop_section_index in get_push_pop_pairs():
    push_section = sections[push_section_index]
    pop_section = sections[pop_section_index]

    adjustment = push_section.y_inc + pop_section.x_inc
    if adjustment >= 0:
        smallest_input_digits[push_section_index] = 1
        smallest_input_digits[pop_section_index] = 1 + adjustment
    else:
        smallest_input_digits[pop_section_index] = 1
        smallest_input_digits[push_section_index] = 1 - adjustment

print("".join(str(d) for d in smallest_input_digits))
compare_two_methods(smallest_input_digits)
