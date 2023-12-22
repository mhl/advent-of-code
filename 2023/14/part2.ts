import { getExampleLines, getInputLines, getInputString } from "../aoc";

function printRows(rows: string[], indent = "") {
    for (const row of rows) {
        process.stdout.write(`${indent}${row}\n`);
    }
}

function calculateLoadColumn(column: string) {
    // console.log("Considering column", column);
    let load = 0;
    for (let i = 0; i < column.length; ++i) {
        const c = column[i];
        if (c === "." || c === "#") {
            continue;
        }
        const load_increase = column.length - i;
        // console.log("load_increate is:", load_increase);
        load += load_increase;
    }
    return load;
}

function calculateLoad(rows: string[]) {
    let total_load = 0;
    const transposed = transpose(rows);
    for (const column of transposed) {
        const load = calculateLoadColumn(column);
        // console.log(`load of ${column} is ${load}`);
        total_load += load;
    }
    return total_load;
}

export function tiltString(s: string) {
    const array_result: string[] = [];
    let last_before_next_space = -1;
    for (let i = 0; i < s.length; ++i) {
        const c = s[i];
        if (c === "#") {
            array_result[i] = "#";
            last_before_next_space = i;
            continue;
        }
        if (c === ".") {
            continue;
        }
        // c === "O"
        array_result[last_before_next_space + 1] = "O";
        last_before_next_space++;
    }
    for (let i = 0; i < s.length; ++i) {
        if (!array_result[i]) {
            array_result[i] = ".";
        }
    }
    return array_result.join("");
}

function tiltWest(rows: string[]) {
    return rows.map((r) => tiltString(r));
}

function rotate90Clockwise(rows: string[]) {
    const transposed = transpose(rows);
    return transposed.map((r) => [...r].reverse().join(""));
}

function rotate90Anticlockwise(rows: string[]) {
    const transposed = transpose(rows);
    return transposed.reverse();
}

function rotate180(rows: string[]) {
    return rotate90Anticlockwise(rotate90Anticlockwise(rows));
}

function tiltNorth(rows: string[]) {
    return rotate90Anticlockwise(tiltEast(rotate90Clockwise(rows)));
}

function tiltEast(rows: string[]) {
    return rotate180(tiltWest(rotate180(rows)));
}

function tiltSouth(rows: string[]) {
    return rotate90Clockwise(tiltEast(rotate90Anticlockwise(rows)));
}

function cycle(rows: string[]) {
    return tiltEast(tiltSouth(tiltWest(tiltNorth(rows))));
}

function getKey(rows: string[]) {
    return JSON.stringify(rows);
}

function getEarliestState(
    n: number,
    start_of_loop: number,
    cycle_length: number,
) {
    return ((n - start_of_loop) % cycle_length) + start_of_loop;
}

async function main() {
    // let lines = await getExampleLines();
    let lines = await getInputLines(2023, 14);
    lines.filter((l) => l.length > 0);
    const first_saw_state: Map<string, number> = new Map();
    const cycles_to_state: Map<number, string[]> = new Map();
    let cycles_done = 0;
    let current_platform = lines;
    printRows(lines);
    while (!first_saw_state.has(getKey(current_platform))) {
        first_saw_state.set(getKey(current_platform), cycles_done);
        cycles_to_state.set(cycles_done, current_platform);
        current_platform = cycle(current_platform);
        cycles_done++;
        console.log("========================================");
        console.log(
            `After ${cycles_done} cycle ${calculateLoad(current_platform)}`,
        );
        printRows(current_platform);
    }
    const start_of_loop = first_saw_state.get(getKey(current_platform));
    if (start_of_loop == null) {
        throw new Error("Couldn't find start of loop");
    }
    console.log(
        "After",
        cycles_done,
        "state was the same as after",
        start_of_loop,
    );
    const equivalent_cycles_done = getEarliestState(
        1000000000,
        start_of_loop,
        cycles_done - start_of_loop,
    );
    console.log({ equivalent_cycles_done });
    const final_state = cycles_to_state.get(equivalent_cycles_done);
    if (final_state == null) {
        throw new Error("Failed to find final state in cycles_to_state");
    }
    const total_load = calculateLoad(final_state);
    console.log({ total_load });
}

export function transpose(rows: string[]): string[] {
    const rows_as_arrays = rows.map((row) => [...row]);
    return rows_as_arrays[0].map((_, i) =>
        rows_as_arrays.map((row) => row[i]).join(""),
    );
}

if (require.main === module) {
    main();
}
