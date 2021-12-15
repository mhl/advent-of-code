#!/usr/bin/env python3

from heapq import heappush, heappop

with open("input-jenny.txt") as f:
    original_grid = [[int(digit) for digit in line.rstrip()] for line in f]

def generate_giant_grid(original_grid):
    width = len(original_grid[0])
    height = len(original_grid)
    giant_grid = [[None]*width*5 for _ in range(height*5)]
    for i in range(5):
        for j in range(5):
            increase = i + j
            for y in range(height):
                for x in range(width):
                    original_value = original_grid[y][x]
                    new_value = original_value + increase
                    if new_value > 9:
                        new_value -= 9
                    giant_grid[y + j * height][x + i * width] = new_value
    return giant_grid

giant_grid = generate_giant_grid(original_grid)

def find_cost_of_shortest_path(grid):
    # This is an implementation of Dijkstra's algorithm based on
    # the pseudcode here: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    width = len(grid[0])
    height = len(grid)

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

    start = (0,0)
    target = (width - 1, height - 1)

    large_sentinel = 1000000

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
            heappush(queue, (tentative_distance, coord))

    while queue:
        u_tentative_distance, u = heappop(queue)

        if u == target:
            break

        if u_tentative_distance > dist[u]:
            continue

        for adjacent_coord in get_adjacent_coords(*u):
            x, y = adjacent_coord
            alternative_distance = u_tentative_distance + grid[y][x]
            if alternative_distance < dist[adjacent_coord]:
                dist[adjacent_coord] = alternative_distance
                prev[adjacent_coord] = u
                heappush(queue, (alternative_distance, adjacent_coord))

    path_coord = target
    path_reversed = [path_coord]

    while path_coord != start:
        path_coord = prev[path_coord]
        if path_coord != start:
            path_reversed.append(path_coord)

    return sum(grid[y][x] for x, y in reversed(path_reversed))

print(find_cost_of_shortest_path(original_grid))
print(find_cost_of_shortest_path(giant_grid))
