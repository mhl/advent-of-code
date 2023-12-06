import { getInputLines } from "../aoc";

async function main() {
    const lines = await getInputLines(2023, 1);
    let total = 0;
    for (let line of lines) {
        const matches = Array.from(line.matchAll(/\d/g));
        if (!matches.length) continue;
        const first_digit = matches[0][0];
        const last_digit = matches[matches.length - 1][0];
        const combined = first_digit + last_digit;
        const combined_as_number = Number(combined);
        total += combined_as_number;
    }
    console.log("total is:", total);
}
main();
