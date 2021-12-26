#!/usr/bin/env python3

from collections import defaultdict, Counter
import re

start_positions = {}

with open("input.txt") as f:
    for line in f:
        m = re.search(r"^Player (\d+) starting position: (\d+)", line)
        if not m:
            continue
        player, start_position = [int(g) for g in m.groups()]
        start_positions[player] = start_position

sum_to_ways_of_getting_it = defaultdict(int)
for first_roll in [1, 2, 3]:
    for second_roll in [1, 2, 3]:
        for third_roll in [1, 2, 3]:
            sum_of_rolls = first_roll + second_roll + third_roll
            sum_to_ways_of_getting_it[sum_of_rolls] += 1

TARGET_SCORE = 21

# Return a structure like:
# {
#    1: 1235
#    2: 2345
# }
# ... representing the ways of player 1 and player 2 winning


def ways_of_winning(
    player_positions, player_scores, turns_completed, ways_of_getting_here
):
    current_player = (turns_completed) % 2 + 1

    new_ways_of_winning = Counter()

    for sum_rolled in range(3, 10):
        ways_of_getting_that_sum = sum_to_ways_of_getting_it[sum_rolled]
        new_position = (player_positions[current_player] - 1 + sum_rolled) % 10 + 1
        if new_position + player_scores[current_player] >= TARGET_SCORE:
            new_ways_of_winning[current_player] += (
                ways_of_getting_that_sum * ways_of_getting_here
            )
        else:
            new_player_positions = player_positions.copy()
            new_player_scores = player_scores.copy()

            new_player_positions[current_player] = new_position
            new_player_scores[current_player] += new_position

            new_ways_of_winning += ways_of_winning(
                new_player_positions,
                new_player_scores,
                turns_completed + 1,
                ways_of_getting_here * ways_of_getting_that_sum,
            )
    return new_ways_of_winning


print(ways_of_winning(start_positions, {1: 0, 2: 0}, 0, 1))
