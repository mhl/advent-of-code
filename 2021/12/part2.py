#!/usr/bin/env python3

from collections import defaultdict
import re

cave_to_neighbours = defaultdict(set)

with open("input.txt") as f:
    for line in f:
        m = re.search(r"^(\w+)-(\w+)$", line)
        cave_a, cave_b = m.groups()
        cave_to_neighbours[cave_a].add(cave_b)
        cave_to_neighbours[cave_b].add(cave_a)


def find_all_paths_to_end(current_cave, path_so_far, visited_small_cave_twice):
    depth_so_far = len(path_so_far)
    if current_cave == "end":
        return [path_so_far + [current_cave]]
    if current_cave.islower() and (current_cave in path_so_far):
        if current_cave == "start" or visited_small_cave_twice:
            return []
        visited_small_cave_twice = True
    all_paths_to_end = []
    for next_cave in cave_to_neighbours[current_cave]:
        new_path_so_far = path_so_far + [current_cave]
        paths_to_end = find_all_paths_to_end(
            next_cave, new_path_so_far, visited_small_cave_twice
        )
        all_paths_to_end.extend(paths_to_end)
    return all_paths_to_end


all_paths = find_all_paths_to_end("start", [], False)

for path in all_paths:
    print(" -> ".join(path))

print(len(all_paths))
