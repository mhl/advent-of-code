#!/usr/bin/env python3

from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Optional
import numpy as np


with open("input.txt") as f:
    all_scans = [
        [
            np.array([int(c) for c in line.split(",")])
            for line in scan_section.split("\n")
            if line and not line.startswith("---")
        ]
        for scan_section in f.read().split("\n\n")
    ]

# Generate all 24 rotation matrices
all_rotation_matrices = []
for i, i_sign in product((0, 1, 2), (1, -1)):
    for j, j_sign in product((0, 1, 2), (1, -1)):
        if j == i:
            continue
        for k, k_sign in product((0, 1, 2), (1, -1)):
            if k == i or k == j:
                continue
            rotation_matrix = np.zeros((3, 3))
            rotation_matrix[i][0] = i_sign
            rotation_matrix[j][1] = j_sign
            rotation_matrix[k][2] = k_sign
            # Make sure the determinant is 1, so that this is a pure
            # rotation, with no reflection
            if np.linalg.det(rotation_matrix) == 1:
                all_rotation_matrices.append(rotation_matrix)


def hash_for_point(beacon_index, scan_result):
    beacon_point = scan_result[beacon_index]
    # Order the other points in the scan by their distance to this point
    dsquared_with_index = sorted(
        (np.dot((other_point - beacon_point), (other_point - beacon_point)), i)
        for i, other_point in enumerate(scan_result)
        if i != beacon_index
    )
    # Our hash value is a tuple of:
    #  - The angle between this point and the two nearest points
    #  - The distance squared to the nearest of those two points
    #  - The distance squared to the further of those two points
    # Obviously this isn't well defined if there are more than two points
    # that are equally near to this point, so return None in that case -
    # we only add points to the lookup for which this hash key is well-defined.
    if (
        dsquared_with_index[0][0]
        == dsquared_with_index[1][0]
        == dsquared_with_index[2][0]
    ):
        return None
    vector_to_nearest = scan_result[dsquared_with_index[0][1]]
    vector_to_further = scan_result[dsquared_with_index[1][1]]
    # print(vector_to_nearest, vector_to_further)
    cos_angle = np.dot(vector_to_nearest, vector_to_further) / (
        np.linalg.norm(vector_to_nearest) * np.linalg.norm(vector_to_further)
    )
    angle_radians = round(np.arccos(cos_angle))
    # So that the angle hashes predictably, covert this to an integer number
    # of degrees, rather than hashing a floating point radians value
    angle_degrees = round(np.degrees(angle_radians))
    # print(angle_radians, "->", angle_degrees)
    return (
        angle_degrees,
        dsquared_with_index[0][0],
        dsquared_with_index[1][0],
    )


lookup = defaultdict(list)

for scan_index, scan_result in enumerate(all_scans):
    for beacon_index in range(len(scan_result)):
        h = hash_for_point(beacon_index, scan_result)
        if h is not None:
            lookup[h].append({"scan_index": scan_index, "beacon_index": beacon_index})


class ScanCorrespondence(object):
    def __init__(self, scan_index, other_scan_index, rotation_index, translation):
        self.scan_index = scan_index
        self.other_scan_index = other_scan_index
        self.rotation_index = rotation_index
        self.translation = translation

    def __repr__(self):
        return f"ScanResultCorrespondence(scan_index={self.scan_index}, other_scan_scan_index={self.other_scan_index}, rotation_index={self.rotation_index}, translation={self.translation})"


def transform_scan_result(scan_result, rotation_matrix):
    return [
        np.rint(np.dot(rotation_matrix, beacon_point)).astype(int)
        for beacon_point in scan_result
    ]


# This is used when we know that two scans overlap, and the points
# that we thing correspond between them, but we still need to find
# the rotation and translation to map them between the scans'
# coordinate systems.


def get_scan_correspondence(
    all_scans, scan_index, other_scan_index, point_correspondences
):
    scan_result = all_scans[scan_index]
    other_scan_result = all_scans[other_scan_index]
    # Find all rotations of the other scan
    all_rotations_of_other_scan_result = [
        transform_scan_result(other_scan_result, rotation_matrix)
        for rotation_matrix in all_rotation_matrices
    ]
    # Look at the translation between the corresponding points with each
    # rotation of the other scan; when it's the right rotation then all
    # (or almost all) the translations should be the same.
    best_scan_correspondence = None
    highest_identical_translation_count = None
    for rotation_index, rotated_scan_result in enumerate(
        all_rotations_of_other_scan_result
    ):
        translations_of_correspondences = Counter()
        for beacon_index, other_beacon_index in point_correspondences:
            translation_to_other = tuple(
                scan_result[beacon_index] - rotated_scan_result[other_beacon_index]
            )
            translations_of_correspondences[translation_to_other] += 1
        commonest_translation, count = translations_of_correspondences.most_common(1)[0]
        if (
            highest_identical_translation_count is None
            or count > highest_identical_translation_count
        ):
            best_scan_correspondence = ScanCorrespondence(
                scan_index, other_scan_index, rotation_index, commonest_translation
            )
            highest_identical_translation_count = count
    return best_scan_correspondence


# Find all the scans that might overlap with the one at scan_index based
# on hashing each point in the other scans.


def find_matching_scans(all_scans, scan_index, other_scan_indices):
    correspondences_by_other_scan = defaultdict(list)
    for other_scan_index in other_scan_indices:
        for other_beacon_index in range(len(all_scans[other_scan_index])):
            h_other = hash_for_point(other_beacon_index, all_scans[other_scan_index])
            if h_other is None:
                continue
            for match in lookup[h_other]:
                if match["scan_index"] == scan_index:
                    correspondences_by_other_scan[other_scan_index].append(
                        (match["beacon_index"], other_beacon_index)
                    )
    best_correspondences = sorted(
        (correspondences_by_other_scan.items()), key=lambda t: len(t[1]), reverse=True
    )
    # Only consider the cases where at least 6 points match between the two
    # scans; our hash function might not have a well defined value for some.
    best_correspondences = [t for t in best_correspondences if len(t[1]) > 6]
    return [
        get_scan_correspondence(
            all_scans, scan_index, good_correspondence[0], good_correspondence[1]
        )
        for good_correspondence in best_correspondences
    ]


scan_correspondences = []

# Start from scan 0 and find the other scans that overlap with that.
# Then explore from each of the scans that overlap until we've found
# all of the scans.

connected = set([0])
already_started_from = set()
while len(connected) < len(all_scans):
    start_from = next(iter(connected - already_started_from))
    for scan_correspondence in find_matching_scans(
        all_scans, start_from, range(1, len(all_scans))
    ):
        # Ignore ones that we've already connected
        if scan_correspondence.other_scan_index in connected:
            continue
        scan_correspondences.append(scan_correspondence)
        connected.add(scan_correspondence.other_scan_index)
    already_started_from.add(start_from)

# Now we know the correpondences between different scan results and that
# they are all connected, create a graph so that we can find the route
# to map them all back into the coordinates of scan_result 0 through the
# overlapping scans.


@dataclass
class Node:
    scan_index: int
    parent: Optional["Node"]
    scan_correspondence: Optional[ScanCorrespondence]


scan_index_to_node = {0: Node(0, None, None)}
for scan_correspondence in scan_correspondences:
    scan_index_to_node[scan_correspondence.other_scan_index] = Node(
        scan_correspondence.other_scan_index,
        scan_index_to_node[scan_correspondence.scan_index],
        scan_correspondence,
    )

all_beacons = set(tuple(point) for point in all_scans[0])


def map_point_back(beacon, scan_index):
    current_scan_index = scan_index
    current_position = np.copy(beacon)
    if scan_index == 0:
        return current_position
    # FIXME: It's inefficient to do these separate operations for each
    # point rather than building a matrix to do it (you'd need to use
    # homogenous coordinates to represent the translations), but we've
    # sunk quite enough time into this already, so this FIXME will probably
    # never be fixed.
    while current_scan_index != 0:
        node = scan_index_to_node[current_scan_index]
        rotation_matrix = all_rotation_matrices[
            node.scan_correspondence.rotation_index
        ]
        current_position = np.rint(np.dot(rotation_matrix, current_position)).astype(int)
        translation = node.scan_correspondence.translation
        current_position += translation
        current_scan_index = node.scan_correspondence.scan_index
    return current_position


# Now map every beacon in every other scan back to the coordinate system
# of scan 0

for scan_index in range(1, len(all_scans)):
    for beacon in all_scans[scan_index]:
        mapped_position = map_point_back(beacon, scan_index)
        all_beacons.add(tuple(mapped_position))

# Answer to part 1
print(len(all_beacons))


def manhanttan_distance(p, q):
    return abs(q[0] - p[0]) + abs(q[1] - p[1]) + abs(q[2] - p[2])


# The scanners are always at the origin of each scan
scanner_positions = [
    map_point_back((0, 0, 0), scan_index) for scan_index in range(len(all_scans))
]

# Find the maximum Manhattan distance between any two scanners
print(
    max(
        manhanttan_distance(p, q)
        for p, q in product(scanner_positions, scanner_positions)
    )
)
