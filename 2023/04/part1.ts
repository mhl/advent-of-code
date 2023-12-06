import { getInputLines } from "../aoc";

function calculate_points(number_of_matches: number) {
    if (number_of_matches === 0) {
        return 0;
    }
    return 2 ** (number_of_matches - 1);
}

async function main() {
    const lines = await getInputLines(2023, 4);
    let total_points = 0;
    for (const line of lines) {
        if (!line.length) {
            continue;
        }
        const numbers = line.split(/:\s+/)[1].split(/\s+\|\s+/);
        const winning_numbers = numbers[0].split(/\s+/).map(Number);
        const numbers_we_have = numbers[1].split(/\s+/).map(Number);
        const matches = numbers_we_have.filter(
            (n) => winning_numbers.indexOf(n) >= 0,
        );
        const number_of_matches = matches.length;
        total_points += calculate_points(number_of_matches);
    }
    console.log(total_points);
}

main();
