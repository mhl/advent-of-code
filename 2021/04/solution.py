#!/usr/bin/env python3

with open("input.txt") as f:
    calls_string = f.readline()
    f.readline()
    all_boards_string = f.read()

calls = tuple(int(n) for n in calls_string.split(","))

whole_board_strings = all_boards_string.rstrip().split("\n\n")


class Board(object):
    def __init__(self, board_string):
        self.board_string = board_string
        self.rows = tuple(
            tuple(int(number_string) for number_string in row.split())
            for row in board_string.rstrip().split("\n")
        )
        self.columns = tuple(zip(*self.rows))

    def __str__(self):
        return self.board_string

    def check_if_won(self, calls_so_far_set):
        row_complete = any(all(n in calls_so_far_set for n in row) for row in self.rows)
        col_complete = any(
            all(n in calls_so_far_set for n in col) for col in self.columns
        )
        return row_complete or col_complete

    def score(self, calls_so_far):
        calls_set = set(calls_so_far)
        unmarked_numbers = [n for row in self.rows for n in row if n not in calls_set]
        return sum(unmarked_numbers) * calls_so_far[-1]


boards = [Board(b) for b in whole_board_strings]


def find_first_winning_board():
    for i in range(0, len(calls)):
        calls_so_far = calls[: i + 1]
        calls_so_far_set = set(calls_so_far)
        winning_boards = [b for b in boards if b.check_if_won(calls_so_far_set)]
        if not winning_boards:
            continue
        assert len(winning_boards) == 1
        winning_board = winning_boards[0]
        return winning_board.score(calls_so_far)


def find_last_winning_board():
    remaining_boards = set(boards)
    board_to_calls_at_win = {}
    for i in range(0, len(calls)):
        calls_so_far = calls[: i + 1]
        calls_so_far_set = set(calls_so_far)
        for b in remaining_boards.copy():
            if b.check_if_won(calls_so_far_set):
                remaining_boards.remove(b)
                board_to_calls_at_win[b] = calls_so_far
    last_winner = list(board_to_calls_at_win.keys())[-1]
    return last_winner.score(board_to_calls_at_win[last_winner])


print(find_first_winning_board())
print(find_last_winning_board())
