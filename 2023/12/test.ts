import { choose, countSprings, getConstraints } from "./part1";

describe("countSprings", () => {
    test("a simple example from the problem statement", () => {
        expect(countSprings("#.#.###")).toEqual([1, 1, 3]);
    });
});

describe("getConstraints", () => {
    test("a simple example from the problem statement", () => {
        expect(getConstraints("???.### 1,1,3")).toEqual({
            total_springs: 5,
            unknowns: 3,
            springs_in_unknowns: 2,
            unknown_indices: [0, 1, 2]
        });
    });
});

describe("choose", () => {
    test("all combinations of 2 choose 2", () => {
        const result = choose([7, 8], 2);
        const result_set = new Set<number[]>(result);
        const expected_set = new Set<number []>([
            [7, 8],
        ]);
        expect(result_set).toEqual(expected_set);
    });

    test("all combinations of 2 choose 1", () => {
        const result = choose([7, 8], 1);
        const result_set = new Set<number[]>(result);
        const expected_set = new Set<number []>([
            [7], [8]
        ]);
        expect(result_set).toEqual(expected_set);
    });

    test("all combinations of 4 choose 2", () => {
        const result = choose([0, 5, 6, 10], 2);
        const result_set = new Set<number[]>(result);
        const expected_set = new Set<number []>([
            [0, 5],
            [0, 6],
            [0, 10],
            [5, 6],
            [5, 10],
            [6, 10],
        ]);
        expect(result_set).toEqual(expected_set);
    });
});
