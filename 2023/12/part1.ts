import { getExampleLines, getInputLines } from "../aoc";

export function countSprings(s: string) {
    const matches = Array.from(s.matchAll(/#+/g));
    return matches.map((m) => m[0].length);
}

export function choose(all_indices: number[], r: number, depth: number = 0): number[][] {
    if (r > all_indices.length) {
        return []; // That means it's impossible
    }
    if (!r) {
        return [[]];
    }
    const results: number[][] = [];
    for (const choice of choose(all_indices.slice(1), r - 1, depth + 1)) {
        choice.unshift(all_indices[0]);
        results.push(choice);
    }
    for (const choice of choose(all_indices.slice(1), r, depth + 1)) {
        results.push(choice);
    }
    return results;
}

type Constraints = {
    total_springs: number;
    unknowns: number;
    springs_in_unknowns: number;
    unknown_indices: number[];
}

function parseCounts(s: string): number[] {
    return s.split(",").map(Number);
}

function arraysEqual(a1: number[], a2: number[]): boolean {
    return JSON.stringify(a1) === JSON.stringify(a2);
}

export function getConstraints(s: string): Constraints {
    const matches = Array.from(s.matchAll(/\?/g));
    const unknowns = matches.length;
    const unknown_indices = matches.map(m => {
        if (m.index == null) throw new Error(`No index found on match ${m}`);
        return m.index;
    });

    const known_springs = Array.from(s.matchAll(/#/g)).length;

    const counts = parseCounts(s.split(" ")[1]);
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
    let total_possible_solutions = 0;
    for (const line of lines) {
        const [springs, counts_string] = line.split(" ");
        console.log({springs});
        const constraints = getConstraints(line);
        let possible_solutions = 0;
        for (const choice_indices of choose(constraints.unknown_indices, constraints.springs_in_unknowns)) {
            const new_characters = springs.split("");
            for (const index of choice_indices) {
                new_characters[index] = "#";
            }
            for (let i = 0; i < new_characters.length; ++i) {
                if (new_characters[i] === "?") {
                    new_characters[i] = ".";
                }
            }
            const new_string = new_characters.join("");
            const sprint_counts_from_new_sprint = countSprings(new_string);
            if (arraysEqual(sprint_counts_from_new_sprint, parseCounts(counts_string))) {
                possible_solutions++;
            }
        }
        console.log({possible_solutions});
        total_possible_solutions += possible_solutions;
    }
    console.log({total_possible_solutions});
}

main();
