#!/usr/bin/env python3

import re

start_positions = {}

with open("input.txt") as f:
    for line in f:
        m = re.search(r"^Player (\d+) starting position: (\d+)", line)
        if not m:
            continue
        player, start_position = [int(g) for g in m.groups()]
        start_positions[player] = start_position


class DeterministicDie(object):
    def __init__(self):
        self.next_number = 1
        self.times_rolled = 0

    def get_die_roll(self):
        value_to_return = self.next_number
        self.next_number += 1
        if self.next_number > 100:
            self.next_number = 1
        self.times_rolled += 1
        return value_to_return


player_scores = {}
for player in start_positions.keys():
    player_scores[player] = 0

die = DeterministicDie()

players = list(start_positions.keys())
player_index = 0
current_positions = start_positions.copy()
while all(v < 1000 for v in player_scores.values()):
    current_player = players[player_index]
    sum_of_rolls = sum(die.get_die_roll() for _ in range(3))
    current_positions[current_player] = (
        (current_positions[current_player] - 1 + sum_of_rolls) % 10
    ) + 1
    player_scores[current_player] += current_positions[current_player]
    print(
        "Player",
        current_player,
        "is on space",
        current_positions[current_player],
        "with score",
        player_scores[current_player],
    )
    player_index = (player_index + 1) % len(players)

loser_score = min(player_scores.values())
print(loser_score * die.times_rolled)
