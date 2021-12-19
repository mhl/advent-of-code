#!/usr/bin/env python3

import ast
from functools import reduce
import itertools
import math
from dataclasses import dataclass
from typing import Union, Optional


def other_side(side):
    return "left" if side == "right" else "right"


@dataclass
class Pair:
    left: Union[int, "Pair"]
    right: Union[int, "Pair"]
    parent: Optional["Pair"]

    def __repr__(self):
        return f"Pair(left={repr(self.left)}, right={repr(self.right)})"

    def __str__(self):
        return f"[{str(self.left)},{str(self.right)}]"

    def __eq__(self, other):
        return id(self) == id(other)

    def is_int(self, side):
        return isinstance(getattr(self, side), int)

    def is_pair(self, side):
        return not self.is_int(side)

    def set_parents_recursively(self, parent=None):
        self.parent = parent
        if self.is_pair("left"):
            self.left.set_parents_recursively(parent=self)
        if self.is_pair("right"):
            self.right.set_parents_recursively(parent=self)

    @classmethod
    def make_from_split_value(cls, value, new_parent):
        left = int(math.floor(value / 2))
        right = int(math.ceil(value / 2))
        return Pair(left, right, new_parent)

    def try_to_split(self):
        for side in ("left", "right"):
            child = getattr(self, side)
            if self.is_int(side) and child >= 10:
                setattr(self, side, Pair.make_from_split_value(child, self))
                return True
            elif self.is_int(side):
                continue
            else:
                if child.try_to_split():
                    return True
        return False

    def try_to_explode(self):
        assert self.parent is None

        pair_to_explode = self.get_leftmost_pair_too_deep()
        if pair_to_explode is None:
            return False

        for side in ("left", "right"):
            t = pair_to_explode.get_pair_of_neighbouring_leaf_on(side)
            if t:
                pair_of_neighbouring_leaf, side_of_neighbour = t
                new_value = getattr(
                    pair_of_neighbouring_leaf, side_of_neighbour
                ) + getattr(pair_to_explode, side)
                setattr(pair_of_neighbouring_leaf, side_of_neighbour, new_value)

        for child_property in ("left", "right"):
            if pair_to_explode == getattr(pair_to_explode.parent, child_property):
                setattr(pair_to_explode.parent, child_property, 0)
        return True

    def get_leftmost_pair_too_deep(self, depth=0):
        if depth >= 4:
            assert self.is_int("left") and self.is_int("right")
            return self
        if self.is_pair("left"):
            found_pair_too_deep = self.left.get_leftmost_pair_too_deep(depth + 1)
            if found_pair_too_deep:
                return found_pair_too_deep
        if self.is_pair("right"):
            return self.right.get_leftmost_pair_too_deep(depth + 1)

    def get_pair_of_leaf_furthest(self, direction):
        if self.is_int(direction):
            return self
        else:
            return getattr(self, direction).get_pair_of_leaf_furthest(direction)

    def get_pair_of_neighbouring_leaf_on(self, direction):
        if self.parent is None:
            return None
        elif self == getattr(self.parent, direction):
            return self.parent.get_pair_of_neighbouring_leaf_on(direction)
        else:  # we've reached the highest point we need to go to, so descend
            if self.parent.is_int(direction):
                return (self.parent, direction)
            else:
                other_direction = other_side(direction)
                return (
                    getattr(self.parent, direction).get_pair_of_leaf_furthest(
                        other_direction
                    ),
                    other_direction,
                )

    def reduce(self):
        assert self.parent is None
        try_again = True
        while try_again:
            if not (self.try_to_explode() or self.try_to_split()):
                try_again = False

    def add(self, other_pair):
        new_root = Pair(self, other_pair, parent=None)
        new_root.set_parents_recursively()
        new_root.reduce()
        return new_root

    def magnitude(self):
        magnitude_left = self.left if self.is_int("left") else self.left.magnitude()
        magnitude_right = self.right if self.is_int("right") else self.right.magnitude()
        return 3 * magnitude_left + 2 * magnitude_right


def parse_input(input_string):
    def list_to_pair(l):
        if isinstance(l, int):
            return l
        return Pair(list_to_pair(l[0]), list_to_pair(l[1]), None)

    as_list = ast.literal_eval(input_string)
    tree = list_to_pair(as_list)
    tree.set_parents_recursively()
    return tree


with open("input.txt") as f:
    tree = [parse_input(line.rstrip()) for line in f.readlines()]
total = reduce(lambda x, y: x.add(y), tree)
print(total.magnitude())


with open("input.txt") as f:
    lines = [line.rstrip() for line in f.readlines()]
print(
    max(
        parse_input(a).add(parse_input(b)).magnitude()
        for a, b in itertools.permutations(lines, r=2)
    )
)
