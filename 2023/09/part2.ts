import { getInputLines } from "../aoc";

function getDifferencesBetweenNumbers(numbers: number[]) {
    const result: number[] = [];
    for (let i = 1; i < numbers.length; ++i) {
        result.push(numbers[i] - numbers[i - 1]);
    }
    return result;
}

function allZero(numbers: number[]) {
    return numbers.every(n => n === 0);
}

function getNextElementInSequence(line: string) {
    const numbers = line.split(" ").map(Number);
    const rows = [numbers];
    while (!allZero(rows[rows.length - 1])) {
        rows.push(getDifferencesBetweenNumbers(rows[rows.length - 1]));
    }
    let total = 0;
    for (let i = rows.length - 1; i >= 0; --i) {
        const row = rows[i];
        total = row[0] - total;
    }
    return total;
}

async function main() {
    let lines = await getInputLines(2023, 9);

    let total_of_predicted_numbers = 0;
    for (const line of lines) {
        if (!line.length) {
            continue;
        }
        total_of_predicted_numbers += getNextElementInSequence(line);
    }
    console.log(total_of_predicted_numbers);
}

main();
