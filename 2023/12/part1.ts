import { getExampleLines, getInputLines } from "../aoc";

export function countSprings(s: string) {
    const matches = Array.from("#.#.###".matchAll(/#+/g));
    return matches.map((m) => m[0].length);
}

async function main() {
    let lines = await getInputLines(2023, 11);
    // let lines = await getExampleLines();
    lines = lines.filter((l) => l.length > 0);
}

main();
