import { getExampleLines, getInputLines, getInputString } from "../aoc";

function printRows(rows: string[], indent = "") {
    for (const row of rows) {
        process.stdout.write(`${indent}${row}\n`);
    }
}

function calculateLoad(column: string) {
    // console.log("Considering column", column);
    let load = 0;
    let last_stop = -1;
    let number_in_run_so_far = 0;
    for (let i = 0; i < column.length; ++i) {
        const c = column[i];
        if (c === ".") {
            continue;
        }
        if (c === "#") {
            last_stop = i;
            number_in_run_so_far = 0;
            continue;
        }
        // c === "O"
        number_in_run_so_far++;
        const load_increase =
            column.length - (number_in_run_so_far + last_stop);
        // console.log("load_increate is:", load_increase);
        load += load_increase;
    }
    return load;
}

async function main() {
    // let lines = await getExampleLines();
    let lines = await getInputLines(2023, 14);
    lines.filter((l) => l.length > 0);
    const transposed = transpose(lines);
    printRows(transposed);
    let total_load = 0;
    for (const column of transposed) {
        const load = calculateLoad(column);
        total_load += load;
    }
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
