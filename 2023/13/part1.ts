import { getExampleLines, getInputString } from "../aoc";

function printRows(rows: string[], indent = "") {
    for (const row of rows) {
        process.stdout.write(`${indent}${row}\n`);
    }
}

async function main() {
    let s = await getInputString(2023, 13);
    console.log("s is:", s);
    const grids = s.split(/\n\n/);
    let total = 0;
    for (const grid_string of grids) {
        const rows = grid_string.split("\n").filter((r) => r.length > 0);
        // printRows(rows, "not tranposed: ");
        let line = findHorizontalSymmetryLine(rows);
        if (line == null) {
            const transposed = transpose(rows);
            // printRows(transposed, "tranposed: ");
            line = findHorizontalSymmetryLine(transposed);
            if (line == null) {
                throw new Error(
                    `No horizontal or vertical line found for ${rows}`,
                );
            }
            total += line;
        } else {
            total += 100 * line;
        }
    }
    console.log(total);
}

export function transpose(rows: string[]): string[] {
    const rows_as_arrays = rows.map((row) => [...row]);
    return rows_as_arrays[0].map((_, i) =>
        rows_as_arrays.map((row) => row[i]).join(""),
    );
}

export function findHorizontalSymmetryLine(rows: string[]): number | null {
    for (let i = 1; i < rows.length; ++i) {
        // console.log("Considering i", i);
        let all_the_same = true;
        for (
            let offset = 0;
            i + offset < rows.length && i - offset - 1 >= 0;
            ++offset
        ) {
            const row1 = rows[i - offset - 1];
            const row2 = rows[i + offset];
            // console.log(`  at offset ${offset} comparing rows ${row1} and ${row2}`);
            if (row1 !== row2) {
                // console.log('   They were not the same, continuing');
                all_the_same = false;
            }
        }
        if (all_the_same) {
            return i;
        }
    }
    return null;
}

if (require.main === module) {
    main();
}
