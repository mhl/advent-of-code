import { countSprings, getConstraints } from "./part1";

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