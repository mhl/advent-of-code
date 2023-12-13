import { countSprings } from "./part1";

describe("countSprings", () => {
    test("a simple example from the problem statement", () => {
        expect(countSprings("#.#.###")).toEqual([1, 1, 3]);
    });
});
