import { tiltString } from "./part2";

console.log("tiltString is:", tiltString);

describe("tiltString", () => {
    test("a simple example from the problem statement", () => {
        expect(tiltString("..O.O##...O.#.O")).toEqual("OO...##O....#O.");
    });
});
