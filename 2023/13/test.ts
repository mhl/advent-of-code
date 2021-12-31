import { findHorizontalSymmetryLine, transpose } from "./part1";

describe("findLineBetweenRows", () => {
    test("a simple example from the problem statement", () => {
        const result = findHorizontalSymmetryLine([
            "#...##..#",
            "#....#..#",
            "..##..###",
            "#####.##.",
            "#####.##.",
            "..##..###",
            "#....#..#",
        ]);
        expect(result).toEqual(4);
    });
});

describe("transpose", () => {
    test("a simple example", () => {
        const result = transpose(["123", "456", "789"]);
        const expected = ["147", "258", "369"];
        expect(result).toEqual(expected);
    });
});
