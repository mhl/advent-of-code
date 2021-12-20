#!/usr/bin/env python3

from dataclasses import dataclass
from functools import reduce

DARK = 0
LIGHT = 1

letter_to_value = {
    ".": DARK,
    "#": LIGHT,
}
value_to_letter = {v: k for k, v in letter_to_value.items()}


def int_from_list(l):
    return reduce(lambda acc, digit: acc * 2 + digit, l, 0)


@dataclass
class InfiniteImage:
    background_value: int
    grid: list[list[int]]

    def __str__(self):
        return f"background: {value_to_letter[self.background_value]}\n" + "\n".join(
            "".join(value_to_letter[v] for v in row) for row in self.grid
        )

    def get_kernel_values(self, centre_x, centre_y):
        w = len(self.grid[0])
        h = len(self.grid)
        kernel_values = []
        for y in range(centre_y - 1, centre_y + 2):
            for x in range(centre_x - 1, centre_x + 2):
                if 0 <= x < w and 0 <= y < h:
                    kernel_values.append(self.grid[y][x])
                else:
                    kernel_values.append(self.background_value)
        return kernel_values

    def enhance(self, algorithm):
        original_width = len(self.grid[0])
        original_height = len(self.grid)
        new_grid = [[None] * (original_width + 2) for _ in range(original_height + 2)]
        for y_new_grid in range(len(new_grid)):
            for x_new_grid in range(len(new_grid[0])):
                kernel_values = self.get_kernel_values(x_new_grid - 1, y_new_grid - 1)
                lookup_value = int_from_list(kernel_values)
                new_grid[y_new_grid][x_new_grid] = algorithm[lookup_value]
        return InfiniteImage(algorithm[self.background_value * -1], new_grid)

    def count_light(self):
        if self.background_value == LIGHT:
            raise Exception("Infinite number of light pixels")
        return sum(v for row in self.grid for v in row)


with open("input.txt") as f:
    algorithm = [letter_to_value[l] for l in f.readline().rstrip()]
    assert len(algorithm) == 512
    f.readline()
    grid = [[int(letter_to_value[l]) for l in row.rstrip()] for row in f.readlines()]

# Part 1:
image = InfiniteImage(DARK, grid)
for i in range(2):
    image = image.enhance(algorithm)
print(image.count_light())

# Part 2:
image = InfiniteImage(DARK, grid)
for i in range(50):
    image = image.enhance(algorithm)
print(str(image))
print(image.count_light())
