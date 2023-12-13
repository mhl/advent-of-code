import { getExampleLines, getInputLines } from "../aoc";

export function countSprings(s: string) {
    const matches = Array.from("#.#.###".matchAll(/#+/g));
    return matches.map((m) => m[0].length);
}

export function getConstraints(s: string) {
    const matches = Array.from(s.matchAll(/\?/g));
    const unknowns = matches.length;
    const unknown_indices = matches.map(m => m.index);

    const known_springs = Array.from(s.matchAll(/#/g)).length;

    const counts = s.split(" ")[1].split(",").map(Number);
    const total_springs = counts.reduce(
        (total_so_far, c) => total_so_far + c,
        0,
    );
    const springs_in_unknowns = total_springs - known_springs;
    return {total_springs, unknowns, springs_in_unknowns, unknown_indices};
}

async function main() {
    let lines = await getInputLines(2023, 12);
    // let lines = await getExampleLines();
    lines = lines.filter((l) => l.length > 0);
}

main();
