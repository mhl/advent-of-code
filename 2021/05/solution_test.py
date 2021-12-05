import pytest

from part1 import get_line_points, inclusive_range


def test_get_line_points_increasing_x():
    line_ends = ((0, 9), (5, 9))
    assert get_line_points(line_ends) == (
        (0, 9),
        (1, 9),
        (2, 9),
        (3, 9),
        (4, 9),
        (5, 9),
    )


def test_get_line_points_decreasing_x():
    line_ends = ((5, 9), (0, 9))
    assert get_line_points(line_ends) == (
        (5, 9),
        (4, 9),
        (3, 9),
        (2, 9),
        (1, 9),
        (0, 9),
    )


def test_get_line_points_increasing_y():
    line_ends = ((5, 9), (5, 11))
    assert get_line_points(line_ends) == ((5, 9), (5, 10), (5, 11))


def test_get_line_points_decreasing_y():
    line_ends = ((5, 11), (5, 9))
    assert get_line_points(line_ends) == ((5, 11), (5, 10), (5, 9))


def test_get_line_points_diagonal_easy():
    line_ends = ((1, 1), (3, 3))
    assert get_line_points(line_ends) == ((1, 1), (2, 2), (3, 3))


def test_get_line_points_diagonal_less_easy():
    line_ends = ((9, 7), (7, 9))
    assert get_line_points(line_ends) == ((9, 7), (8, 8), (7, 9))


def test_inclusive_range_increasing():
    assert list(inclusive_range(0, 2)) == [0, 1, 2]


def test_inclusive_range_decreasing():
    assert list(inclusive_range(2, 0)) == [2, 1, 0]
