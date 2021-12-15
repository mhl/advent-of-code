#!/usr/bin/env python3

with open("input-jenny.txt") as f:
    grid = [[int(digit) for digit in line.rstrip()] for line in f]

width = len(grid[0])
height = len(grid)
start = (0,0)
target = (width - 1, height - 1)

large_sentinel = 1000000

def get_adjacent_coords(x, y):
    return tuple(
        (i, j)
        for i, j in (
            (x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1),
        )
        if 0 <= i < width and 0 <= j < height
    )

dist = {}
prev = {}
queue = []

for y in range(height):
    for x in range(width):
        coord = (x, y)
        if coord == start:
            tentative_distance = 0
        else:
            tentative_distance = large_sentinel
        dist[coord] = tentative_distance
        prev[coord] = None
        queue.append((tentative_distance, coord))

while queue:
    queue.sort(reverse=True)
    u_tentative_distance, u = queue.pop()

    if u == target:
        break

    for adjacent_coord in get_adjacent_coords(*u):
        x, y = adjacent_coord
        alternative_distance = u_tentative_distance + grid[y][x]
        if alternative_distance < dist[adjacent_coord]:
            dist[adjacent_coord] = alternative_distance
            prev[adjacent_coord] = u
            for i in range(len(queue)):
                if queue[i][1] == adjacent_coord:
                    queue[i] = (alternative_distance, adjacent_coord)

path_coord = target
path_reversed = [path_coord]

while path_coord != start:
    path_coord = prev[path_coord]
    if path_coord != start:
        path_reversed.append(path_coord)

print(sum(grid[y][x] for x, y in reversed(path_reversed)))
